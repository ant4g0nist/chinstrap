## Copyright 2019-2020 Smart Chain Arena LLC. ##

from browser import alert, window

import traceback
import inspect
import sys
import datetime
from types import FunctionType
import json
import os
import smartpyio

pyRange = range
pyBool = bool
pyInt = int
pySet = set
pyList = list
pyTuple = tuple
pyBytes = bytes
pyMap = map

pyLen = len


class LineNo:
    def __init__(self, filename, line_no):
        self.filename = filename
        self.line_no = line_no

    def export(self):
        return f"(\"{self.filename}\" {self.line_no})"

def get_file_line_no(line_no = None):
    if line_no is not None:
        return line_no
    if window.in_browser:
        for x in reversed(getattr(inspect.currentframe(), "$stack")):
            line_info = getattr(x[1], "$line_info")
            if "exec" in line_info:
                return LineNo(x[3].__name__, pyInt(line_info.split(",")[0]))
        return LineNo("", -1)
    else:
        frame = inspect.currentframe().f_back
        while frame:
            fn = frame.f_code.co_filename
            if ("smartpy.py" not in fn
                and "<frozen " not in fn
                and "smartpyc.py" not in fn
                and "init" != fn):
                fn = fn.strip("<>./,' ")
                if ':' in fn:
                    fn = fn[fn.rindex(":") + 1:]
                return LineNo(fn, frame.f_lineno)
            frame = frame.f_back
        return LineNo("", -1)

def get_id_from_line_no():
    l = get_file_line_no()
    if not l.filename:
        return str(l.line_no)
    return l.filename.replace("/", " ").replace(".py", "").strip("<>./,'").split()[-1] + "_" + str(l.line_no)

def pretty_line_no():
    line_no = get_file_line_no()
    if line_no.filename:
        of_file = f" of {line_no.filename}"
    else:
        of_file = ""
    line_no = line_no.line_no
    if window.in_browser:
        return '<button class="text-button" onclick="showLine(%i)">(line %i%s)</button>' \
            % (line_no, line_no, of_file)
    else:
        return '(line %i%s)' % (line_no, of_file)


class Helpers:
    @staticmethod
    def areBytesValid(x):
        return (
            isinstance(x, str)
            and x.startswith("0x")
            and all(c in _hex_digits for c in x[2:])
            and pyLen(x) % 2 == 0
        )


class Expr:
    def __init__(self, f, l):
        self._f = f
        self._l = l
        self.onUpdateHandlers = []
        self.attributes = {}
        self.opens = {}
        setattr(self, "__initialized", True)

    def __eq__(self, other):
        return Expr("eq", [self, spExpr(other), get_file_line_no()])

    def __ne__(self, other):
        return Expr("neq", [self, spExpr(other), get_file_line_no()])

    def __add__(self, other):
        return Expr("add", [self, spExpr(other), get_file_line_no()])

    def __sub__(self, other):
        return Expr("sub", [self, spExpr(other), get_file_line_no()])

    def __mul__(self, other):
        return Expr("mul", [self, spExpr(other), get_file_line_no()])

    def __mod__(self, other):
        return Expr("mod", [self, spExpr(other), get_file_line_no()])

    def __truediv__(self, other):
        return Expr("truediv", [self, spExpr(other), get_file_line_no()])

    def __floordiv__(self, other):
        return Expr("floordiv", [self, spExpr(other), get_file_line_no()])

    def __rtruediv__(self, other):
        return Expr("truediv", [spExpr(other), self, get_file_line_no()])

    def __rfloordiv__(self, other):
        return Expr("floordiv", [spExpr(other), self, get_file_line_no()])

    def __radd__(self, other):
        return Expr("add", [spExpr(other), self, get_file_line_no()])

    def __rmul__(self, other):
        return Expr("mul", [spExpr(other), self, get_file_line_no()])

    def __rsub__(self, other):
        return Expr("sub", [spExpr(other), self, get_file_line_no()])

    def __lt__(self, other):
        return Expr("lt", [self, spExpr(other), get_file_line_no()])

    def __le__(self, other):
        return Expr("le", [self, spExpr(other), get_file_line_no()])

    def __gt__(self, other):
        return Expr("gt", [self, spExpr(other), get_file_line_no()])

    def __ge__(self, other):
        return Expr("ge", [self, spExpr(other), get_file_line_no()])

    def __or__(self, other):
        return Expr("or", [self, spExpr(other), get_file_line_no()])

    def __ror__(self, other):
        return Expr("or", [spExpr(other), self, get_file_line_no()])

    def __xor__(self, other):
        return Expr("xor", [self, spExpr(other), get_file_line_no()])

    def __rxor__(self, other):
        return Expr("xor", [self, spExpr(other), get_file_line_no()])

    def __and__(self, other):
        return Expr("and", [self, spExpr(other), get_file_line_no()])

    def __rand__(self, other):
        return Expr("and", [spExpr(other), self, get_file_line_no()])

    def __lshift__(self, other):
        return Expr("lsl", [self, spExpr(other), get_file_line_no()])

    def __rlshift__(self, other):
        return Expr("lsl", [spExpr(other), self, get_file_line_no()])

    def __rshift__(self, other):
        return Expr("lsr", [self, spExpr(other), get_file_line_no()])

    def __rrshift__(self, other):
        return Expr("lsr", [spExpr(other), self, get_file_line_no()])

    def __getitem__(self, item):
        return Expr("getItem", [self, spExpr(item), get_file_line_no()])

    def __abs__(self):
        return Expr("abs", [self, get_file_line_no()])

    def __neg__(self):
        return Expr("neg", [self, get_file_line_no()])

    def __invert__(self):
        return Expr("not", [self, get_file_line_no()])

    def __bool__(self):
        self.__nonzero__()

    def __nonzero__(self):
        raise Exception(
            "Cannot convert expression to bool. Conditionals are forbidden on contract expressions. Please use ~ or sp.if instead of not or if."
        )

    def __hash__(self):
        return hash(self.export())

    def on_update(self, f):
        self.onUpdateHandlers.append(f)

    def get(self, item, default_value = None, message = None):
        if default_value is not None:
            return Expr("getItemDefault", [self, spExpr(item), spExpr(default_value), get_file_line_no()])
        if message is not None:
            return Expr("getItemMessage", [self, spExpr(item), spExpr(message), get_file_line_no()])
        return self.__getitem__(item)

    def get_opt(self, key):
        return Expr("getOpt", [self, get_file_line_no(), spExpr(key)])

    def __enter__(self):
        return getattr(self, "__asBlock").__enter__()

    def __exit__(self, type, value, traceback):
        getattr(self, "__asBlock").__exit__(type, value, traceback)

    def __iter__(self):
        raise Exception(
            f"Non iterable object from Python. Please use [sp.for var in expr] or [expr.items()] to iterate over a SmartPy expression. {self.export()}"
        )

    def contains(self, value):
        return Expr("contains", [self, spExpr(value), get_file_line_no()])

    def __contains__(self, value):
        raise Exception(
            "Instead of using expressions such as e1 in e2, please use e2.contains(e1)."
        )

    def __call__(self, arg):
        return Expr("call_lambda", [self, spExpr(arg), get_file_line_no()])

    def apply(self, arg):
        return Expr("apply_lambda", [self, spExpr(arg), get_file_line_no()])

    def __getattr__(self, attr):
        if "__" in attr:
            raise AttributeError("")
        try:
            return self.attributes[attr]
        except KeyError:
            result = Expr("attr", [self, attr, get_file_line_no()])
            self.attributes[attr] = result
            return result

    def __setattr__(self, attr, value):
        if "__" not in attr and hasattr(self, "__initialized"):
            sp.set(getattr(self, attr), value)
            if (
                hasattr(getattr(self, attr), "onUpdateHandlers")
                and getattr(self, attr).onUpdateHandlers
            ):
                for f in getattr(self, attr).onUpdateHandlers:
                    f(getattr(self, attr), value)
        else:
            object.__setattr__(self, attr, value)


    def __delitem__(self, item):
        sp.delItem(self, item)

    def __setitem__(self, item, value):
        sp.set(self[item], value)

    def items(self):
        return Expr("items", [self, get_file_line_no()])

    def keys(self):
        return Expr("keys", [self, get_file_line_no()])

    def values(self):
        return Expr("values", [self, get_file_line_no()])

    def elements(self):
        return Expr("elements", [self, get_file_line_no()])

    def rev(self):
        return Expr("rev", [self, get_file_line_no()])

    def rev_items(self):
        return Expr("rev_items", [self, get_file_line_no()])

    def rev_keys(self):
        return Expr("rev_keys", [self, get_file_line_no()])

    def rev_values(self):
        return Expr("rev_values", [self, get_file_line_no()])

    def rev_elements(self):
        return Expr("rev_elements", [self, get_file_line_no()])

    def set(self, other):
        sp.set(self, spExpr(other))

    def add(self, item):
        sp.updateSet(self, item, True)

    def remove(self, item):
        sp.updateSet(self, item, False)

    def __repr__(self):
        return self.export()

    def match(self, constructor, argName=None):
        if argName is None:
            argName = constructor
        b = CommandBlock(sp)
        sp.newCommand(Expr("match", [self, constructor, argName, b, get_file_line_no()]))
        b.value = Expr("variant_arg", [argName, get_file_line_no()])
        b.value.__asBlock = b
        return b

    def match_cases(self, arg = None):
        b = CommandBlock(sp)
        if arg is None:
            arg = "match_%s" % (get_id_from_line_no())
        sp.newCommand(Expr("match_cases", [self, arg, b, get_file_line_no()]))
        b.value = Expr("cases_arg", [arg, get_file_line_no()])
        b.value.__asBlock = b
        return b

    def is_none(self):
        return self.is_variant("None")

    def is_some(self):
        return self.is_variant("Some")

    def is_left(self):
        return self.is_variant("Left")

    def is_right(self):
        return self.is_variant("Right")

    def is_variant(self, name):
        return Expr("isVariant", [self, name, get_file_line_no()])

    def open_some(self, message = None):
        return self.open_variant("Some", message = message)

    def open_variant(self, name, message = None):
        if message is None:
            try:
                return self.opens[name]
            except KeyError:
                result = Expr("openVariant", [self, name, "None" if message is None else spExpr(message), get_file_line_no()])
                self.opens[name] = result
                return result
        else:
            return Expr("openVariant", [self, name, "None" if message is None else spExpr(message), get_file_line_no()])

    def append(self, other):
        raise Exception(
            "myList.append(..) is deprecated. Please use myList.push(..).\nBeware: push adds the element in front of the list (as in Michelson)."
        )

    def push(self, other):
        return sp.set(self, sp.cons(spExpr(other), self))

    def map(self, f):
        return Expr("map_function", [self, spExpr(f), get_file_line_no()])

    def add_seconds(self, seconds):
        return Expr("add_seconds", [self, spExpr(seconds), get_file_line_no()])

    def add_minutes(self, minutes):
        return Expr("add_seconds", [self, spExpr(minutes * 60), get_file_line_no()])

    def add_hours(self, hours):
        return Expr("add_seconds", [self, spExpr(hours * 60 * 60), get_file_line_no()])

    def add_days(self, days):
        return Expr("add_seconds", [self, spExpr(days * 24 * 60 * 60), get_file_line_no()])

    def export(self):
        def ppe(e):
            if hasattr(e, "export"):
                return e.export()
            if isinstance(e, str):
                return '"%s"' % e
            return str(e)
        if self._f == "invalid":
            raise Exception(" ".join(str(x) for x in self._l))
        if self._l:
            return "(%s %s)" % (self._f, " ".join(ppe(x) for x in self._l))
        return "(%s)" % (self._f)

def name_of_type(t):
    a = str(t).replace("<", "").replace(">", "")
    return a or t.__name__

def literal(t, l, pyType, f_name = None):
    f_name = f_name if f_name else t
    if not name_of_type(type(l)) == name_of_type(pyType):
        raise ValueError(
            "sp.%s(..) awaits a %s and got '%s' of type %s. %s"
            % (f_name, name_of_type(pyType), str(l), name_of_type(type(l)), pretty_line_no())
        )
    if t in ["nat", "int_or_nat", "tez", "mutez"] and l < 0:
        raise ValueError(
            "sp.%s(..) cannot contains negative value and got '%s'. %s"
            % (f_name, str(l), pretty_line_no())
        )

    return Expr("literal", [Expr(t, [l]), get_file_line_no()])

def key_hash(s):
    return literal("key_hash", s, str)

def baker_hash(h):
    return literal("baker_hash", h, str)

def variant(cons, x):
    return Expr("variant", [cons, spExpr(x), get_file_line_no()])


unit = Expr("unit", [])


def bool(x):
    return literal("bool", x, pyBool)

def int(x):
    return literal("int", x, pyInt)

def int_or_nat(x):
    return literal("intOrNat", x, pyInt)

def nat(x):
    return literal("nat", x, pyInt)

def string(x):
    return literal("string", x, str)

def bounded(x):
    return Expr("bounded", [spExpr(x), get_file_line_no()])

def unbounded(x):
    return Expr("unbounded", [spExpr(x), get_file_line_no()])

_hex_digits = pySet("0123456789abcdefABCDEF")

def bytes(x):
    if Helpers.areBytesValid(x):
        return literal("bytes", x, str)
    raise Exception(
        "sp.bytes('0x...') awaits a string in hexadecimal format and got '%s'. %s"
        % (str(x), pretty_line_no())
    )

def chain_id_cst(x):
    if Helpers.areBytesValid(x):
        return literal("chain_id_cst", x, str)
    raise Exception(
        "sp.chain_id_cst('0x...') awaits a string in hexadecimal format and got '%s'. %s"
        % (str(x), pretty_line_no())
    )

def some(x):
    return Expr("variant", ["Some", spExpr(x), get_file_line_no()])

def left(x):
    return Expr("variant", ["Left", spExpr(x), get_file_line_no()])

def right(x):
    return Expr("variant", ["Right", spExpr(x), get_file_line_no()])

def mutez(x):
    if isinstance(x, pyInt):
        return literal("mutez", x, pyInt)
    else:
        raise ValueError("sp.mutez(..) is for literals and awaits a python integers and got '%s' of type %s. %s\n\
Please use sp.utils.nat_to_tez to convert a sp.TNat expression into a sp.TMutez expression."
                          % (str(x), name_of_type(type(x)), pretty_line_no()))

def tez(x):
    if isinstance(x, pyInt):
        return literal("mutez", 1000000 * x, pyInt, "tez")
    else:
        raise ValueError("sp.tez(..) is for literals and awaits a python integers and got '%s' of type %s. %s\n\
Please use sp.utils.nat_to_tez to convert a sp.TNat expression into a sp.TMutez expression."
                          % (str(x), name_of_type(type(x)), pretty_line_no()))

def timestamp(seconds):
    return literal("timestamp", seconds, pyInt)

def timestamp_from_utc(year, month, day, hours, minutes, seconds):
    return timestamp(
        pyInt(
            datetime.datetime(
                year, month, day, hours, minutes, seconds, tzinfo=datetime.timezone.utc
            ).timestamp()
        )
    )

def timestamp_from_utc_now():
    return timestamp(pyInt(datetime.datetime.now(datetime.timezone.utc).timestamp()))

def address(s):
    if s == "":
        raise Exception('"" is not a valid address')
    if not (any(s.startswith(prefix) for prefix in ["KT1", "tz1", "tz2", "tz3"])):
        raise Exception(
            '"%s" is not a valid address, it should start with tz1, tz2, tz3 or KT1.'
            % s
        )
    return literal("address", s, str)

def key(s):
    return literal("key", s, str)

def secret_key(s):
    return literal("secret_key", s, str)

def signature(sig):
    return literal("signature", sig, str)


"""
* bls12_381_g1 and bls12_381_g2 are written as their raw bytes, using a big-endian point encoding, as specified here.
* bls12_381_fr is written in raw bytes, using a little-endian encoding.

bls12-381 Serialization: https://docs.rs/bls12_381/0.3.1/bls12_381/notes/serialization/index.html#bls12-381-serialization
"""
def bls12_381_g1(raw_bytes):
    if Helpers.areBytesValid(raw_bytes):
        return literal("bls12_381_g1", raw_bytes, str);

    raise Exception(
        "sp.bls12_381_g1('0x...') awaits a string in hexadecimal format and got '%s'. %s"
        % (str(raw_bytes), pretty_line_no())
    )

def bls12_381_g2(raw_bytes):
    if Helpers.areBytesValid(raw_bytes):
        return literal("bls12_381_g2", raw_bytes, str);

    raise Exception(
        "sp.bls12_381_g2('0x...') awaits a string in hexadecimal format and got '%s'. %s"
        % (str(raw_bytes), pretty_line_no())
    )

def bls12_381_fr(raw_bytes):
    if Helpers.areBytesValid(raw_bytes):
        return literal("bls12_381_fr", raw_bytes, str);

    raise Exception(
        "sp.bls12_381_fr('0x...') awaits a string in hexadecimal format and got '%s'. %s"
        % (str(raw_bytes), pretty_line_no())
    )

def pairing_check(pairs):
    return Expr("pairing_check", [spExpr(pairs), get_file_line_no()])

def hash_key(x):
    return Expr("hash_key", [spExpr(x), get_file_line_no()])

def spMetaExpr(x, context = "expression"):
    debug = False  # isinstance(x, dict)
    if x is None:
        raise Exception("Unexpected value (None) for %s. %s" % (context, pretty_line_no()))
    if isinstance(x, dict):
        return Expr("meta_map", [get_file_line_no()] + [Expr("elem", [spExpr(k), spMetaExpr(v)]) for (k, v) in x.items()])
    if isinstance(x, pyList):
        if debug:
            alert("list")
        return Expr("meta_list", [get_file_line_no()] + [spMetaExpr(y) for y in x])
    if isinstance(x, OffchainView):
        return x
    return Expr("meta_expr", [spExpr(x)])

def spExpr(x, context = "expression"):
    debug = False  # isinstance(x, dict)
    if x is None:
        raise Exception("Unexpected value (None) for %s. %s" % (context, pretty_line_no()))
    if isinstance(x, Contract):
        raise Exception("Contracts are not convertible into expressions.")
    if isinstance(x, Local):
        raise Exception(
            "Local value of variable %s can be accessed by doing %s.value"
            % (x.name, x.name)
        )
    if isinstance(x, Expr):
        if debug:
            alert("Expr")
        return x
    if x == ():
        if debug:
            alert("unit")
        return unit
    if isinstance(x, float):
        raise ValueError(
            "Expression cannot be a float. Got '%s'. %s"
            % (str(x), pretty_line_no())
        )
    if isinstance(x, pyBool):
        if debug:
            alert("bool")
        return literal("bool", x, pyBool)
    if isinstance(x, pyInt):
        if debug:
            alert("int")
        if x < 0:
            return literal("int", x, pyInt)
        return literal("intOrNat", x, pyInt)
    if hasattr(x, "__int__"):
        return literal("intOrNat", pyInt(x), pyInt)
    if isinstance(x, str):
        if debug:
            alert("str")
        return literal("string", x, str)
    if isinstance(x, pyBytes):
        if debug:
            alert("bytes")
        return literal("bytes", x.decode(), str)
    if isinstance(x, WouldBeValue):
        if debug:
            alert("WouldBeValue")
        return x
    if isinstance(x, ContractTyped):
        if debug:
            alert("ContractTyped")
        return x
    if isinstance(x, dict):
        if debug:
            alert("dict")
        return map(x)
    if isinstance(x, pySet):
        if any(isinstance(y, Expr) for y in x):
            raise Exception(
                "{e1, ..., en} syntax is forbidden for SmartPy Expr. Please use sp.set([e1, .., en])"
            )
        return set([spExpr(y) for y in x])
    if isinstance(x, pyTuple):
        if debug:
            alert("tuple")
        return tuple([spExpr(y) for y in x])
    if isinstance(x, pyList):
        if debug:
            alert("list")
        return list([spExpr(y) for y in x])
    if isinstance(x, pyRange):
        if debug:
            alert(x)
            alert("range")
        return list(pyList(x))
    if isinstance(x, Lambda):
        if debug:
            alert(x)
            alert("Lambda")
        return x.f
    if isinstance(x, GlobalLambda):
        if debug:
            alert(x)
            alert("GlobalLambda")
        return Expr("global", [x.name, get_file_line_no()])
    if isinstance(x, FunctionType):
        if debug:
            alert(x)
            alert("FunctionType")
        return build_lambda(x).f
    if isinstance(x, TestAccount):
        if debug:
            alert(x)
            alert("TestAccount")
        return x.e
    if isinstance(x, TType):
        if debug:
            alert(x)
            alert("TType")
        raise Exception("spExpr: using type expression %s as an expression" % (str(x)))
    if isinstance(x, Verbatim):
        return x
    export_string = ""
    try:
        export_string = " with export = '%s'" % x.export()
    except:
        pass
    raise Exception("No conversion to sp.Expr found for '%s' of type '%s'%s. %s" % (str(x), name_of_type(x), export_string, pretty_line_no()))


class TType:
    def __repr__(self):
        return self.export()


class TRecord(TType):
    def __init__(self, **kargs):
        args = {}
        for (k, v) in kargs.items():
            v = sp.types.conv(v)
            args[k] = v
            setattr(self, k, v)
        self.kargs = args
        self.layout_ = None

    def layout(self, layout):
        result = TRecord(**dict(self.kargs))
        result.layout_ = parse_layout(layout)
        return result

    def right_comb(self):
        result = TRecord(**dict(self.kargs))
        result.layout_ = "Right"
        return result

    def with_fields(self, **kargs):
        result = dict(self.kargs)
        for (k, v) in kargs.items():
            result[k] = v
        return TRecord(**result)

    def without_fields(self, l):
        result = dict(self.kargs)
        for k in l:
            del result[k]
        return TRecord(**result)

    def export(self):
        fields = " ".join(
            "(%s %s)" % (x, y.export()) for (x, y) in sorted(self.kargs.items())
        )
        layout = ("(Some %s)" % self.layout_) if self.layout_ else "None"
        return "(record (%s) %s)" % (fields, layout)


def parse_layout(layout):
    if isinstance(layout, pyTuple):
        if pyLen(layout) != 2:
            raise Exception("Layout computation on non-pair %s" % (str(layout)))
        return '(%s %s)' % (parse_layout(layout[0]), parse_layout(layout[1]))
    if isinstance(layout, str):
        return '("%s")' % layout
    raise Exception("Layout computation on non-pair or str %s" % (str(layout)))


class ExprStr:
    def __init__(self, s):
        self.s = s

    def export(self):
        return self.s


def set_record_layout(expression, layout):
    raise Exception("sp.set_record_layout is deprecated. Please use a command like sp.set_type(.., sp.TRecord(...).loyout(..))")

def set_variant_layout(expression, layout):
    raise Exception("sp.set_variant_layout is deprecated. Please use a command like sp.set_type(.., sp.TVariant(...).loyout(..))")

def set_type_record_layout(expression, layout):
    raise Exception("sp.set_type_record_layout is deprecated. Please use a command like sp.set_type(.., sp.TRecord(...).loyout(..))")


def set_type_variant_layout(expression, layout):
    raise Exception("sp.set_type_variant_layout is deprecated. Please use a command like sp.set_type(.., sp.TVariant(...).loyout(..))")


class TVariant(TType):
    def __init__(self, **kargs):
        args = sorted(kargs.items())
        self.kargs = kargs
        self.layout_ = None
        for (k, v) in args:
            setattr(self, k, sp.types.conv(v))

    def layout(self, layout):
        self.layout_ = parse_layout(layout)
        return self

    def right_comb(self):
        self.layout_ = "Right"
        return self

    def export(self):
        fields = " ".join(
            "(%s %s)" % (x, y.export()) for (x, y) in sorted(self.kargs.items())
        )
        layout = ("(Some %s)" % self.layout_) if self.layout_ else "None"
        return "(variant (%s) %s)" % (fields, layout)


def TOr(tleft, tright):
    return TVariant(Left=tleft, Right=tright)


class TSimple(TType):
    def __init__(self, name):
        self.name = name

    def export(self):
        return '"%s"' % self.name

class TSaplingState(TType):
    def __init__(self, memo_size = None):
        self.name = "sapling_state"
        self.memo_size = memo_size

    def export(self):
        return '(%s %s)' % (self.name, str(self.memo_size))

class TSaplingTransaction(TType):
    def __init__(self, memo_size = None):
        self.name = "sapling_transaction"
        self.memo_size = memo_size

    def export(self):
        return '(%s %s)' % (self.name, str(self.memo_size))

class TBounded(TType):
    def __init__(self, cases, t=None, final=True):
        self.t = sp.types.conv(t)
        self.cases = cases
        self.final = final

    def export(self):
        return '(bounded %s %s %s)' % (self.t.export(), str(self.final), " ".join(spExpr(case).export() for case in self.cases))

TUnit = TSimple("unit")
TBool = TSimple("bool")
TInt = TSimple("int")
TNat = TSimple("nat")
TIntOrNat = TSimple("intOrNat")
TString = TSimple("string")
TBytes = TSimple("bytes")
TMutez = TSimple("mutez")
TTimestamp = TSimple("timestamp")
TAddress = TSimple("address")
TKey = TSimple("key")
TSecretKey = TSimple("secret_key")
TKeyHash = TSimple("key_hash")
TBakerHash = TSimple("baker_hash")
TSignature = TSimple("signature")
TChainId = TSimple("chain_id")
TBls12_381_g1 = TSimple("bls12_381_g1") # Points on the BLS12-381 curve G1
TBls12_381_g2 = TSimple("bls12_381_g2") # Points on the BLS12-381 curve G2
TBls12_381_fr = TSimple("bls12_381_fr") # An element of the scalar field Fr, used for scalar multiplication on the BLS12-381 curves G1 and G2.
TOperation = TSimple("operation")
TNever = TSimple("never")


class TUnknown(TType):
    def __init__(self, id):
        self.id = id

    def export(self):
        return '(unknown %i)' % self.id


class TList(TType):
    def __init__(self, t):
        self.t = sp.types.conv(t)

    def export(self):
        return "(list %s)" % self.t.export()


class TTicket(TType):
    def __init__(self, t):
        self.t = sp.types.conv(t)

    def export(self):
        return "(ticket %s)" % self.t.export()


class TMap(TType):
    def __init__(self, k, v):
        self.k = sp.types.conv(k)
        self.v = sp.types.conv(v)

    def export(self):
        return "(map %s %s)" % (self.k.export(), self.v.export())


class TSet(TType):
    def __init__(self, t):
        self.t = sp.types.conv(t)

    def export(self):
        return "(set %s)" % self.t.export()


class TBigMap(TType):
    def __init__(self, k, v):
        self.k = sp.types.conv(k)
        self.v = sp.types.conv(v)

    def export(self):
        return "(bigmap %s %s)" % (self.k.export(), self.v.export())


class TPair(TType):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def export(self):
        return "(tuple %s %s)" % (
            sp.types.conv(self.t1).export(),
            sp.types.conv(self.t2).export(),
        )

class TTuple(TType):
    def __init__(self, *args):
        self.types = args

    def export(self):
        return "(tuple %s)" % (" ".join([sp.types.conv(i).export() for i in self.types]))

class TAnnots(TType):
    def __init__(self, t, *annots):
        self.t = sp.types.conv(t)
        self.annots = annots

    def export(self):
        return "(annots %s (%s))" % (
            self.t.export(),
            " ".join('"%s"' % a for a in self.annots),
        )


class TOption(TType):
    def __init__(self, t):
        self.t = sp.types.conv(t)

    def export(self):
        return "(option %s)" % self.t.export()


class TContract(TType):
    def __init__(self, t):
        self.t = sp.types.conv(t)

    def export(self):
        return "(contract %s)" % self.t.export()


class TLambda(TType):
    def __init__(self, t1, t2):
        self.t1 = sp.types.conv(t1)
        self.t2 = sp.types.conv(t2)

    def export(self):
        return "(lambda %s %s)" % (self.t1.export(), self.t2.export())


class SpTypes:
    def __init__(self):
        self.unknownIds = 0
        self.seqCounter = 0

    def conv(self, t):
        if isinstance(t, WouldBeValue):
            raise Exception("Bad type expression " + str(t))
        if t is None:
            t = self.unknown()
        # This line needs to come before lines with ==.
        if isinstance(t, TType):
            return t
        if isinstance(t, Expr):
            raise Exception("Expression cannot be used as a type: " + str(t))
        if t == pyInt:
            raise Exception("Type int in this context is referred to as sp.TInt.")
        if t == pyBool:
            raise Exception("Type bool in this context is referred to as sp.TBool.")
        if t == str:
            raise Exception("Type str in this context is referred to as sp.TString.")
        if t == pyBytes:
            raise Exception("Type bytes in this context is referred to as sp.TBytes.")
        if isinstance(t, pyList) and pyLen(t) == 1:
            return TList(self.conv(t[0]))
        raise Exception("Bad type expression " + str(t) + " of type " + str(type(t)))

    def trecord(self, **kargs):
        for x in kargs:
            kargs[x] = self.conv(kargs[x])
        return TRecord(kargs)

    def unknown(self):
        self.unknownIds += 1
        return TUnknown(self.unknownIds)

    def seqNo(self):
        self.seqCounter += 1
        return self.seqCounter

    def taddress(self):
        return TAddress

    def tlist(self, t):
        return TList(t)


class Data:
    def __getattr__(self, attr):
        if "__" in attr:
            raise AttributeError("")
        return Expr("attr", [Expr("data", []), attr])

    def __setattr__(self, attr, value):
        sp.set(getattr(self, attr), value)


class TreeBlock:
    def __init__(self):
        self.commands = []

    def append(self, name, command):
        self.commands.append((name,command))

    def export(self):
        def f(n,c):
            if n is None:
                return c.export()
            else:
                return Expr("bind", [n, c]).export()
        return "(%s)" % (" ".join(f(n,c) for (n,c) in self.commands))


class CommandBlock:
    def __init__(self, sp):
        self.sp = sp
        self.commands = TreeBlock()
        self.value = None

    def __enter__(self):
        self.currentBlock = self.sp.mb.currentBlock
        self.sp.mb.currentBlock = self.commands
        return self.value

    def __exit__(self, type, value, traceback):
        self.sp.mb.currentBlock = self.currentBlock

    def export(self):
        return self.commands.export()


class Sp:
    def __init__(self):
        self.types = SpTypes()
        self.profiling = False
        self.profilingLogs = []
        self.mb = None

    def profile(self, s=""):
        if self.profiling:
            import datetime

            self.profilingLogs.append(str(datetime.datetime.now()) + " " + s)

    def setMB(self, mb):
        self.mb = mb

    def delItem(self, expr, item):
        self.newCommand(Expr("delItem", [expr, spExpr(item), get_file_line_no()]))

    def cons(self, x, xs):
        return Expr("cons", [spExpr(x), spExpr(xs), get_file_line_no()])

    def newCommand(self, command, name=None):
        if hasattr(self, "mb") and self.mb is not None:
            line_no = get_file_line_no()
            self.mb.append(name,command)
            return Expr("variant_arg", [name, line_no])
        else:
            raise Exception("New command outside of contract %s:\n%s" % (pretty_line_no(), str(command)))

    def set(self, var, value):
        if value is None:
            raise Exception("None value for ", var)
        self.newCommand(Expr("set", [var, spExpr(value), get_file_line_no()]))

    def updateSet(self, set, item, add):
        self.newCommand(
            Expr("updateSet", [spExpr(set), spExpr(item), add, get_file_line_no()])
        )

    def defineLocal(self, local, name, value):
        self.newCommand(Expr("defineLocal", [name, value, get_file_line_no()]))

    def getData(self):
        return Expr("data", [])


sp = Sp()


class MessageBuilder:
    def __init__(self, addedMessage):
        if addedMessage is not None:
            self.name = addedMessage.name
            self.addedMessage = addedMessage
        self.commands = TreeBlock()
        self.currentBlock = self.commands

    def append(self, name, command):
        self.currentBlock.append(name, command)

    def export(self):
        return self.commands.export()

    def __repr__(self):
        return "Commands:%s" % (" ".join(str(command) for command in self.commands))

    def pp(self):
        output = ["    " + (command.pp()) for command in self.commands]
        return "\n".join(output)


class ExecutedMessage:
    def __init__(self, title, result, expected):
        self.title = title
        self.result = result
        self.expected = expected

    def html(self):
        return (
            ""
            if self.expected
            else "<br><span class='partialType'>ERROR: Unexpected result</span> please use .run(valid = ..expected validation..)<br>"
        ) + self.result

    def __repr__(self):
        return self.html()


def to_constant(value):
    return Expr("to_constant", [spExpr(value), get_file_line_no()])


class TestAccount:
    def __init__(self, seed):
        self.seed = seed
        self.e = Expr("account_of_seed", [self.seed, get_file_line_no()])
        self.address = to_constant(self.e.address)
        self.public_key_hash = to_constant(self.e.public_key_hash)
        self.public_key = to_constant(self.e.public_key)
        self.secret_key = to_constant(self.e.secret_key)

    def export(self):
        return self.e.export()


def test_account(seed):
    return TestAccount(seed)

# sp.sign is already taken by the sign as in plus or minus
def make_signature(secret_key, message, message_format="Raw"):
    return to_constant(
        Expr(
            "make_signature",
            [spExpr(secret_key), spExpr(message), message_format, get_file_line_no()],
        )
    )

def parse_account_or_address(account):
    if account is None:
        return "none"
    if isinstance(account, TestAccount):
        return "seed:%s" % account.seed
    return spExpr(account).export()

class ExecMessage:
    def __init__(self, _contract, _message, params, kargs, contractId = None):
        self.message = _message
        self.params = None if pyLen(params) == 0 else spExpr(params[0])
        self.kargs = (
            None if kargs is None else {k: spExpr(v) for (k, v) in kargs.items()}
        )
        if pyLen(params) and kargs:
            raise Exception(
                "Message execution uses either one args or **kargs syntax, not both."
            )
        self.title = ""
        self.execMessageClass = ""
        self.smartml = None
        self.contractId = contractId
        self.contract = None

        if _contract is not None:
            self.contract = _contract
            self.smartml = self.contract.smartml
            self.contractId = _contract.smartml.contractId
            self.title = self.contract.title if self.contract.title else ""
            self.execMessageClass = self.contract.execMessageClass

        line_no = get_file_line_no()

        sp.profile(self.message + " begin " + str(line_no.line_no))
        if self.contract is not None:
            self.contract.data = contract_data(self.contractId)
        if self.params is None:
            self.params = record(**self.kargs)
        self.result = {
            "action" : "message",
            "id" : self.contractId.export(),
            "line_no" : line_no.export(),
            "message" : self.message,
            "params" : spExpr(self.params).export(),
        }
        if self.title:
            self.result["title"] = self.title
        if self.execMessageClass:
            self.result["messageClass"] = self.execMessageClass
        self.runned = False

    def scenario_message(self):
        if not self.runned:
            self.run()
        return self.result

    def run(
        self,
        sender=None,
        source=None,
        amount=None,
        now=None,
        level=None,
        valid=True,
        exception=None,
        show=True,
        chain_id=None,
        voting_powers=None,
        export=True
    ):
        self.runned = True
        if amount is not None:
            self.result["amount"] = spExpr(amount).export()
        if chain_id is not None:
            self.result["chain_id"] = spExpr(chain_id).export()
        if exception is not None:
            self.result["exception"] = spExpr(exception).export()
        if not(isinstance(export, pyBool) and export == True):
            self.result["export"] = export
        if level is not None:
            self.result["level"] = spExpr(level).export()
        if sender is not None:
            self.result["sender"] = parse_account_or_address(sender)
        if not(isinstance(show, pyBool) and show == True):
            self.result["show"] = show
        if source is not None:
            self.result["source"] = parse_account_or_address(source)
        if now is not None:
            self.result["time"] = spExpr(now).export()
        if not(isinstance(valid, pyBool) and valid == True):
            self.result["valid"] = spExpr(valid).export()
        if voting_powers is not None:
            self.result["voting_powers"] = spExpr(voting_powers).export()
        sp.profile(self.message + " end")
        return self


class WouldBeValue:
    def __repr__(self):
        try:
            return self.export()
        except:
            return "value of type %s. %s" % (
                self.__class__.__name__,
                pretty_line_no(),
            )
    def __iter__(self):
        raise Exception(
            f"Non iterable object from Python. Please use [sp.for var in expr] or [expr.items()] to iterate over a SmartPy value. {self.export()}"
        )


class record(WouldBeValue):
    def __init__(self, **fields):
        self.fields = {k: spExpr(v) for (k, v) in fields.items()}
        for (k, v) in self.fields.items():
            setattr(self, k, v)
        self.line_no = get_file_line_no().export()

    def export(self):
        return "(record %s %s)" % (
            self.line_no,
            " ".join(
                "(%s %s)" % (k, v.export()) for (k, v) in sorted(self.fields.items())
            ),
        )


class tuple(WouldBeValue):
    def __init__(self, l = None):
        if l is None:
            l = []
        self.l = l
        self.line_no = get_file_line_no().export()

    def export(self):
        return "(tuple %s %s)" % (
            self.line_no,
            " ".join(spExpr(x).export() for x in self.l),
        )


def pair(e1, e2):
    return tuple([e1, e2])

class build_list(WouldBeValue):
    def __init__(self, l = None):
        if l is None:
            l = []
        self.l = l
        self.line_no = get_file_line_no().export()

    def push(self, other):
        return sp.set(self, sp.cons(spExpr(other), self))

    def map(self, f):
        return Expr("map_function", [self, spExpr(f), get_file_line_no()])

    def export(self):
        return "(list %s %s)" % (
            self.line_no,
            " ".join(spExpr(x).export() for x in self.l),
        )

    def concat(self):
        return Expr("concat", [self, get_file_line_no()])

    def rev(self):
        return Expr("rev", [self, get_file_line_no()])


class build_set(WouldBeValue):
    def __init__(self, l = None):
        if l is None:
            l = []
        self.l = l
        self.line_no = get_file_line_no().export()

    def contains(self, value):
        return Expr("contains", [self, spExpr(value), get_file_line_no()])

    def elements(self):
        return Expr("elements", [self, get_file_line_no()])

    def rev_elements(self):
        return Expr("rev_elements", [self, get_file_line_no()])

    def add(self, item):
        self.l.append(item)

    def remove(self, item):
        raise Exception(
            "set.remove not implemented for immediate value, please use a local variable."
        )

    def export(self):
        return "(set %s %s)" % (
            self.line_no,
            " ".join(spExpr(x).export() for x in self.l),
        )


class mapOrBigMap(WouldBeValue):
    def __init__(self, l = None):
        if l is None:
            l = {}
        self.l = l
        self.line_no = get_file_line_no().export()

    def contains(self, value):
        return Expr("contains", [self, spExpr(value), get_file_line_no()])

    def __getitem__(self, item):
        return Expr("getItem", [self, spExpr(item), get_file_line_no()])

    def export(self):
        return "(%s %s %s)" % (
            self.name(),
            self.line_no,
            " ".join(
                "(%s %s)" % (spExpr(k).export(), spExpr(v).export())
                for (k, v) in self.l.items()
            ),
        )


class build_map(mapOrBigMap):
    def name(self):
        return "map"

    def items(self):
        return Expr("items", [self, get_file_line_no()])

    def keys(self):
        return Expr("keys", [self, get_file_line_no()])

    def values(self):
        return Expr("values", [self, get_file_line_no()])

    def rev_items(self):
        return Expr("rev_items", [self, get_file_line_no()])

    def rev_keys(self):
        return Expr("rev_keys", [self, get_file_line_no()])

    def rev_values(self):
        return Expr("rev_values", [self, get_file_line_no()])


class build_big_map(mapOrBigMap):
    def name(self):
        return "big_map"


def list(l = None, t = None):
    l = build_list(l)
    return l if t is None else set_type_expr(l,TList(t))

def set(l = None, t = None):
    l = build_set(l)
    return l if t is None else set_type_expr(l,TSet(t))

def map_or_big_map(big, l, tkey, tvalue):
    l = build_big_map(l) if big else build_map(l)
    if tkey is None and tvalue is None:
        return l
    else:
        t = TBigMap(tkey,tvalue) if big else TMap(tkey,tvalue)
        return set_type_expr(l,t)

def map(l = None, tkey = None, tvalue = None):
    return map_or_big_map(False, l, tkey, tvalue)

def big_map(l = None, tkey = None, tvalue = None):
    return map_or_big_map(True, l, tkey, tvalue)

class Smartml:
    def __init__(self, contract=None):
        self.ctx = window.smartmlCtx
        self.time = timestamp(0)
        if contract is not None:
            sp.profile("smartml linking")
            sp.profile("smartml export")
            self.contractId = static_contract_id(window.smartpyContext.nextId())
            window.contracts[self.contractId] = self
            self.contract = contract
            sp.profile("smartml link")

    def runScenario(self, messages):
        self.ctx.call("runScenarioInBrowser", messages)

class Contract:
    def __init__(self, **kargs):
        self.init_type(t = sp.types.unknown())

    def __setattr__(self, attr, value):
        if attr == "data" and self.messages_collecting:
            sp.set(self.data, spExpr(value))
        else:
            object.__setattr__(self, attr, value)

    def add_flag_lazy_entry_points(self):
        self.add_flag("lazy_entry_points", "single")

    def add_flag_lazy_entry_points_multiple(self):
        self.add_flag("lazy_entry_points", "multiple")

    def add_flag(self, flag, *args):
        if not hasattr(self, "flags"):
            self.flags = []
        self.flags += [[flag] + pyList(args)]

    def global_lambda(self, name, f):
        return self.global_variable(name, build_lambda(f, global_name=name))

    def global_variable(self, name, v):
        self.init_internal()
        self.global_variables.append((name, spExpr(v)))
        return Expr("global", [name, get_file_line_no()])

    def offchain_view(self, ov):
        if not hasattr(self, "offchain_views"):
            self.offchain_views = []
        self.offchain_views.append(ov)
        return Expr("offchain_view", [ov.name, get_file_line_no()])

    def set_initial_balance(self, balance):
        self.init_internal()
        if isinstance(balance, pyInt):
            raise Exception(
                "balance should be in tez or mutez and not int (use sp.tez(..) or sp.mutez(..)). %s" % (pretty_line_no())
            )
        if self._initial_balance is None:
            self._initial_balance = balance
        else:
            raise Exception("Balance already set on contract. %s" % (pretty_line_no()))

    def init_internal(self):
        self.currentBlock = None
        if not hasattr(self, "verbose"):
            self.verbose = False
        if not hasattr(self, "messages"):
            self.messages = {}
        if not hasattr(self, "global_variables"):
            self.global_variables = []
        if not hasattr(self, "offchain_views"):
            self.offchain_views = []
        if not hasattr(self, "flags"):
            self.flags = []
        if not hasattr(self, "execMessageClass"):
            self.execMessageClass = ""
        if not hasattr(self, "title"):
            self.title = ""
        if not hasattr(self, "messages_collected"):
            self.messages_collected = False
        if not hasattr(self, "storage"):
            self.storage = None
        if not hasattr(self, "_initial_balance"):
            self._initial_balance = None
        if not hasattr(self, "storage_type"):
            self.storage_type = None
        if not hasattr(self, "entry_points_layout"):
            self.entry_points_layout = None
        if not hasattr(self, "exception_optimization_level"):
            self.exception_optimization_level = None
        if not hasattr(self, "initial_metadata"):
            self.initial_metadata = {}
        if not hasattr(self, "smartml"):
            self.smartml = Smartml(self)
        self.contractId = self.smartml.contractId

        self.address = contract_address(self.smartml.contractId)
        self.typed = contract_typed(self.smartml.contractId)

    def init_type(self, t):
        self.init_internal()
        self.storage_type = t

    def init_entry_points_layout(self, layout):
        self.init_internal()
        self.entry_points_layout = parse_layout(layout)

    def init(self, arg = None, **kwargs):
        self.init_storage(arg, **kwargs)

    def init_storage(self, arg = None, **kwargs):
        self.init_internal()
        if self.storage is not None:
            raise Exception("self.init, self.init_storage error. Storage already set on contract. Please use self.update_initial_storage. %s" % (pretty_line_no()))
        self.update_initial_storage(arg, **kwargs)

    def update_initial_storage(self, arg = None, **kargs):
        self.init_internal()
        if arg is not None and pyLen(kargs):
            raise Exception("self.init, self.init_storage, and self.update_initial_storage use either one arg or **kwargs syntax, not both.")
        if arg is not None:
            self.storage = spExpr(arg)
        else:
            if self.storage is not None:
                if not isinstance(self.storage, record):
                    raise Exception("self.init, self.init_storage, and self.update_initial_storage cannot update a non record with record fields.")
                d = dict(self.storage.fields)
                d.update(**kargs)
            else:
                d = kargs
            d = {k:v for k, v in d.items() if v is not None}
            self.storage = record(**d)

    def addMessage(self, addedMessage):
        if hasattr(addedMessage, "__addedMessage"):
            addedMessage = getattr(addedMessage, "__addedMessage")
        if addedMessage.name is None:
            return
        sp.profile("addMessage begin " + addedMessage.name)
        addedMessage.contract = self
        mb = MessageBuilder(addedMessage)
        self.mb = mb
        sp.setMB(mb)
        params = Expr("params", [addedMessage.line_no])
        nargs = pyLen(addedMessage.args)
        if nargs == 0:
            raise Exception("Entry point '%s' is missing a self parameter (line %i)." % (addedMessage.name, addedMessage.line_no))
        elif nargs == 1:
            x = addedMessage.f(self)
        elif nargs == 2:
            x = addedMessage.f(self, params)
        else:
            args = [ Expr("attr", [params, a, get_file_line_no()]) for a in addedMessage.args[1:] ]
            x = addedMessage.f(self, *args)
        if x is not None:
            raise Exception(
                "Entry point failure for %s (line %i): entry points cannot have return statements."
                % (addedMessage.name, addedMessage.line_no)
            )
        self.mb = None
        sp.setMB(None)
        self.messages[addedMessage.name] = mb
        mb.originate = addedMessage.originate
        mb.lazify = addedMessage.lazify
        mb.lazy_no_code = addedMessage.lazy_no_code
        mb.line_no = addedMessage.line_no
        setattr(self, addedMessage.name, addedMessage)
        # if not isinstance(self.data, Expr) or self.data._f != "data":
        #     raise Exception(
        #         "It's forbidden to change self.data directly.\n self.data = "
        #         + str(self.data)
        #     )
        sp.profile("addMessage end " + addedMessage.name)

    def buildExtraMessages(self):
        pass

    def collectMessages(self):
        if self.messages_collected:
            return
        self.messages_collecting = False
        self.data = sp.getData()
        self.messages_collecting = True
        self.messages_collected = True
        sp.profile("CollectMessages begin " + self.__class__.__name__)
        for f in dir(self):
            if f == "__setattr__":
                continue
            attr = getattr(self, f)
            if hasattr(attr, "__addedMessage"):
                added_message = getattr(attr, "__addedMessage")
                added_message.contract = self
        for f in dir(self):
            attr = getattr(self, f)
            if isinstance(attr, GlobalLambda):
                attr._l = self.global_lambda(attr.name, attr.f)
            if isinstance(attr, OffchainView):
                attr._l = self.offchain_view(attr)
            if isinstance(attr, SubEntryPoint):
                attr._l = self.global_lambda(attr.name, lambda x: attr._fg(self,x))
                attr.contract = self
        for f in dir(self):
            if f == "__setattr__":
                continue
            attr = getattr(self, f)
            if hasattr(attr, "__addedMessage"):
                attr = getattr(attr, "__addedMessage")
                self.addMessage(
                    AddedMessage(attr.name, attr.f, attr.originate, attr.lazify, attr.lazy_no_code, attr.line_no)
                )
        self.buildExtraMessages()
        # self.smartml = window.buildSmartlmJS(self)
        sp.profile("CollectMessages smartml " + self.__class__.__name__)
        self.messages_collecting = False
        self.balance = contract_balance(self.smartml.contractId)
        sp.profile("CollectMessages end " + self.__class__.__name__)
        self.baker = contract_baker(self.smartml.contractId)
        self.data = contract_data(self.smartml.contractId)

    def init_metadata(self, filename, metadata):
        if not hasattr(self, "initial_metadata"):
            self.initial_metadata = {}
        self.initial_metadata[filename] = spMetaExpr(metadata)

    def export(self):
        self.collectMessages()
        messages = {}
        for message in self.messages.values():
            if message.addedMessage.name is not None:
                name = message.addedMessage.name
                if name in messages:
                    raise Exception("Two entry points are called %s (line %i)" % (name, message.addedMessage.line_no))
                messages[name] = message

        if self.exception_optimization_level is not None:
            self.add_flag("exceptions", self.exception_optimization_level)
        result = "(template_id %s \nstorage %s\nstorage_type (%s)\nmessages (%s)\nflags (%s)\nglobals (%s)\nviews (%s)\nentry_points_layout %s\ninitial_metadata (%s)\nbalance %s)" % (
            self.contractId,
            (self.storage.export() if self.storage is not None else "()"),
            ("%s" % (self.storage_type.export()) if self.storage_type is not None else "()"),
            (
                " ".join(
                    "(%s %s %s %s %s %s %s)" % (k, str(v.originate), str(v.lazify), str(v.lazy_no_code), str(pyLen(v.addedMessage.args) > 1), v.line_no.export(), v.export())
                    for (k, v) in sorted(messages.items())
                )
            ),
            (" ".join("(" + " ".join(str(x) for x in call) + ")" for call in self.flags)),
            (
                " ".join(
                    "(%s %s)" % (name, variable.export())
                    for (name, variable) in self.global_variables
                )
            ),
            ( " ".join(ov.exportDef(self) for ov in self.offchain_views)
            ),
            (self.entry_points_layout if self.entry_points_layout is not None else "()"),
            (" ".join("(%s %s)" % (k, spExpr(v).export()) for (k, v) in self.initial_metadata.items())),
            (spExpr(self._initial_balance).export() if self._initial_balance is not None else "()"),
        )
        if self.verbose:
            alert("Creating\n\n%s" % result)
            window.console.log(result)
        return result

    def __repr__(self):
        if hasattr(self, "smartml"):
            return str(self.smartml)
        return "contract"

    def scenario_message(self, accept_unknown_types, default="SmartPy", onlyDefault=False):
        self.collectMessages()
        data = {}
        data["action"] = "newContract"
        data["accept_unknown_types"] = accept_unknown_types
        data["export"] = self.smartml.contract.export()
        data["id"] = self.smartml.contractId.export()
        data["line_no"] = get_file_line_no().export()
        data["show"] = True
        return data

exception_optimization_levels = ["full-debug", "debug-message", "verify-or-line", "default-line", "line", "default-unit", "unit"]

class AddedMessage:
    def __init__(self, name, f, originate, lazify, lazy_no_code, line_no):
        self.name = name
        self.f = f
        self.args = inspect.getargs(f.__code__).args
        self.originate = originate
        self.lazify = lazify
        self.lazy_no_code = lazy_no_code
        self.line_no = line_no

    def __call__(self, *args, **kargs):
        if self.contract.messages_collecting:
            raise Exception("Cannot call an entry_point '%s' from another entry_point." % (self.name))
        res = ExecMessage(self.contract, self.name, args, kargs)
        self.contract.registered_scenario.add_message(res)
        return res


def _add_entry_point(f, name, line_no, originate, lazify, lazy_no_code):
    if name is None:
        name = f.__name__
    if line_no is None:
        line_no = get_file_line_no()
    f.__addedMessage = AddedMessage(name, f, originate, lazify, lazy_no_code, line_no)
    return f

def entry_point(f = None, name = None, line_no = None, private = False, lazify = None, lazy_no_code = None):
    originate = not private
    if f is None:
        def g(f):
            return _add_entry_point(f, name, line_no, originate, lazify, lazy_no_code)
        return g
    else:
        return _add_entry_point(f, name, line_no, originate, lazify, lazy_no_code)


class GlobalLambda:
    def __init__(self, name, f, lineNo):
        self.name = name
        self.f = f
        self.line_no = lineNo
        self._e = Expr("global", [self.name, self.line_no])

    def __call__(self, x):
        return self._e(x)


class OffchainView:
    def __init__(self, name, f, pure, doc, lineNo):
        self.name = name
        self.f = f
        self.pure = pure if pure is not None else False
        if doc is not None:
            self.doc = doc
        elif f.__doc__ is not None:
            self.doc = f.__doc__
        else:
            self.doc = ""
        self.line_no = lineNo

    def export(self):
        return (Expr("meta_offchain_view", [self.name, self.line_no])).export()

    def exportDef(self, contract):
        prev = sp.mb
        newMB = sp.mb is None
        if newMB:
            sp.setMB(MessageBuilder(None))
        currentBlock = sp.mb.currentBlock
        commands = TreeBlock()
        sp.mb.currentBlock = commands

        contract.data = sp.getData()
        import inspect
        args = inspect.getargs(self.f.__code__).args
        nargs = pyLen(args)
        if nargs == 1:
            r = self.f(contract)
        else:
            r = self.f(contract, Expr("params", [self.line_no]))
        if r is not None:
            raise Exception("Please use 'sp.result' instead of 'return' in views.")
        commands = commands.export()

        sp.mb.currentBlock = currentBlock
        self.mb = prev
        if newMB:
            sp.setMB(None)

        contract.data = contract_data(contract.smartml.contractId)

        return "(%s %s %s %s %s %s)" % (self.name, nargs > 1, self.line_no.export(), self.pure, json.dumps(self.doc), commands)

    def __call__(self, x):
        return self._l(x)


def global_lambda(f, name=None):
    if name is None:
        name = f.__name__
    return GlobalLambda(name, f, get_file_line_no())

def offchain_view(pure = None, doc = None):
    def apply_offchain_view(f, name=None):
        if name is None:
            name = f.__name__
        return OffchainView(name, f, pure, doc, get_file_line_no())
    return apply_offchain_view

class SubEntryPoint:
    def __init__(self, name, f, line_no):
        self.name = name
        self._fg = f
        self.line_no = line_no
        self._e = Expr("global", [self.name, self.line_no])

    def __call__(self, x=unit):
        data = Expr("data", [])
        y = local("y%d" % sp.types.seqNo(), self._e(record(in_param=x, in_storage=data)))
        sp.set(data, y.value.storage)
        add_operations(y.value.operations.rev())
        return y.value.result


def sub_entry_point(f, name=None):
    # Currently we only support 1 argument in lambdas > f(self, some_arg)
    argcount = f.__code__.co_argcount
    if (argcount > 2):
        raise Exception("sub_entrypoint (%s) cannot contain more than one argument > e.g. %s(self, some_arg)." % (f.__name__, f.__name__))

    def f_wrapped(self, x=None):
        ops     = local("__operations__", [], t = TList(TOperation))
        storage = local("__storage__", x.in_storage, t = sp.types.unknown())
        y = bind_block()
        with y:
            # sub_entry_point only has self as argument > f(self)
            if (argcount == 1):
                f(self)
            # sub_entry_point has 2 arguments > f(self, some_arg)
            else:
                f(self, x.in_param)
        result(record(result = y.value, operations = ops.value, storage = storage.value))
    if name is None:
        name = f.__name__
    return SubEntryPoint(name, f_wrapped, get_file_line_no())

self = Expr("self", [])
self_address = Expr("self_address", [])
sender = Expr("sender", [])
source = Expr("source", [])
amount = Expr("amount", [])
balance = Expr("balance", [])
now = Expr("now", [])
level = Expr("level", [])
chain_id = Expr("chain_id", [])
none = Expr("variant", ["None", unit, -1])
total_voting_power = Expr("total_voting_power", [])


def voting_power(address):
   return Expr("voting_power", [spExpr(address), get_file_line_no()])

def self_entry_point(entry_point=""):
    return Expr("self", [entry_point, get_file_line_no()])

def to_address(contract):
    return Expr("to_address", [spExpr(contract), get_file_line_no()])

def self_entry_point_address(entry_point = ""):
    return to_address(self_entry_point(entry_point))

def implicit_account(key_hash):
    return Expr("implicit_account", [spExpr(key_hash), get_file_line_no()])

default_verify_message = None
wrap_verify_messages = None

def verify(cond, message=None):
    if message is None:
        message = default_verify_message
    if wrap_verify_messages is not None and message is not None:
        message = wrap_verify_messages(message)
    if message is None:
        sp.newCommand(Expr("verify", [spExpr(cond), get_file_line_no()]))
    else:
        sp.newCommand(
            Expr("verify", [spExpr(cond), spExpr(message), get_file_line_no()])
        )

def verify_equal(v1, v2, message=None):
    verify(poly_equal_expr(v1, v2), message)

def failwith(message):
    sp.newCommand(Expr("failwith", [spExpr(message), get_file_line_no()]))

def never(parameter):
    sp.newCommand(Expr("never", [spExpr(parameter), get_file_line_no()]))

## Control
def else_():
    b = CommandBlock(sp)
    sp.newCommand(Expr("elseBlock", [b]))
    return b

def while_(condition):
    b = CommandBlock(sp)
    sp.newCommand(Expr("whileBlock", [spExpr(condition), b, get_file_line_no()]))
    return b

def match_cons(expression):
    b = CommandBlock(sp)
    sp.newCommand(Expr("match_cons", [spExpr(expression), b, get_file_line_no()]))
    value = Expr("match_cons", [spExpr(expression), get_file_line_no()])
    value.__asBlock = b
    b.value = value
    return value

def if_some(condition, name):
    b = CommandBlock(sp)
    sp.newCommand(Expr("ifSomeBlock", [spExpr(condition), name, b, get_file_line_no()]))
    value = Expr("openVariant", [spExpr(condition), "Some", get_file_line_no()])
    value.__asBlock = b
    b.value = value
    return value

def if_(condition):
    b = CommandBlock(sp)
    sp.newCommand(Expr("ifBlock", [spExpr(condition), b, get_file_line_no()]))
    return b

def for_(name, value):
    value = spExpr(value)
    b = CommandBlock(sp)
    t = sp.types.unknown()
    sp.newCommand(Expr("forGroup", [name, value, b, get_file_line_no()]))
    value = Expr("iter", [name, get_file_line_no()])
    value.__asBlock = b
    b.value = value
    return value

def update_map(map, key, value):
    return Expr("update_map", [spExpr(map), spExpr(key), spExpr(value), get_file_line_no()])

def get_and_update(map, key, value = none):
    return match_pair(Expr("get_and_update", [spExpr(map), spExpr(key), spExpr(value), get_file_line_no()]))

def ediv(num, den):
    return Expr("ediv", [spExpr(num), spExpr(den), get_file_line_no()])

def pack(value):
    return Expr("pack", [spExpr(value), get_file_line_no()])

def unpack(value, t = None):
    return Expr("unpack", [spExpr(value), sp.types.conv(t), get_file_line_no()])

def blake2b(value):
    return Expr("blake2b", [spExpr(value), get_file_line_no()])

def sha512(value):
    return Expr("sha512", [spExpr(value), get_file_line_no()])

def sha256(value):
    return Expr("sha256", [spExpr(value), get_file_line_no()])

def keccak(value):
    return Expr("keccak", [spExpr(value), get_file_line_no()])

def sha3(value):
    return Expr("sha3", [spExpr(value), get_file_line_no()])

def range(a, b, step=1):
    return Expr("range", [spExpr(a), spExpr(b), spExpr(step), get_file_line_no()])

def sum(value):
    return Expr("sum", [value, get_file_line_no()])

def slice(expression, offset, length):
    return Expr(
        "slice", [spExpr(offset), spExpr(length), spExpr(expression), get_file_line_no()]
    )

def concat(value):
    return Expr("concat", [spExpr(value), get_file_line_no()])

def check_signature(pk, sig, msg):
    return Expr("check_signature", [pk, sig, msg, get_file_line_no()])

def sign(e):
    return Expr("sign", [e, get_file_line_no()])

def spmax(x, y):
    return Expr("max", [spExpr(x), spExpr(y), get_file_line_no()])

def spmin(x, y):
    return Expr("min", [spExpr(x), spExpr(y), get_file_line_no()])

def split_tokens(amount, quantity, totalQuantity):
    return Expr(
        "split_tokens",
        [spExpr(amount), spExpr(quantity), spExpr(totalQuantity), get_file_line_no()],
    )

def expr(v):
    return spExpr(v)

def setInt(v):
    return Expr("int", [spExpr(v), get_file_line_no()])

def to_int(v):
    return Expr("toInt", [spExpr(v), get_file_line_no()])

def mul(e1, e2):
    return Expr("mul_overloaded", [spExpr(e1), spExpr(e2), get_file_line_no()])

def is_nat(v):
    return Expr("isNat", [spExpr(v), get_file_line_no()])

def as_nat(v, message = None):
    return is_nat(v).open_some(message = message)

def cmd_result(r):
    return Expr("result", [spExpr(r), get_file_line_no()])

def result(r):
    sp.newCommand(cmd_result(r))

class Lambda:
    def __init__(self, f, params, tParams, global_name, auto_result):
        self.id = window.lambdaNextId
        self.params = params
        self.tParams = tParams
        self.global_name = global_name
        self.auto_result = auto_result
        window.lambdaNextId += 1
        self.f = self.collectLambda(f)

    def collectLambda(self, f):
        prev = sp.mb
        newMB = sp.mb is None
        if newMB:
            sp.setMB(MessageBuilder(None))
        currentBlock = sp.mb.currentBlock
        commands = TreeBlock()
        sp.mb.currentBlock = commands
        r = f(
            Expr("lambdaParams", [self.id, self.params, get_file_line_no(), self.tParams])
        )
        if self.auto_result:
            if r is not None:
                result(r)
        elif r is not None:
            raise Exception("Please use 'sp.result' instead of 'return' in SmartPy functions.")
        r = Expr("lambda", [self.id, self.params, get_file_line_no(), commands])
        sp.mb.currentBlock = currentBlock
        self.mb = prev
        if newMB:
            sp.setMB(None)
        return r

    def __call__(self, arg):
        return Expr("call_lambda", [self.f, spExpr(arg), get_file_line_no()])

    def apply(self, arg):
        return Expr("apply_lambda", [self.f, spExpr(arg), get_file_line_no()])

    def export(self):
        return self.f.export()


def build_lambda(f, params="", tParams = None, global_name=None):
    tParams = sp.types.conv(tParams)
    auto_result = f.__name__ == "<lambda>"
    return Lambda(f, params, tParams, global_name, auto_result)

class Local:
    def __init__(self, name, value, t = None):
        t = sp.types.conv(t)
        sp.defineLocal(self, name, spExpr(value))
        self.init = False
        self.name = name
        self.val = value
        self.t = t
        self.init = True

    def __getattr__(self, attr):
        if attr == "value":
            return Expr("getLocal", [self.name, get_file_line_no()])
        raise AttributeError(
            "Local variable '%s' doesn't have attribute %s. Use '%s.value' to access its value."
            % (self.name, attr, self.name)
        )

    def __eq__(self, other):
        raise AttributeError(
            "Local variable '%s' doesn't have attribute ==. Use '%s.value' to access its value."
            % (self.name, self.name)
        )

    def __setattr__(self, attr, value):
        if attr == "init":
            object.__setattr__(self, attr, value)
        elif attr == "value" and self.init:
            sp.set(self, spExpr(value))
        else:
            object.__setattr__(self, attr, value)

    def export(self):
        return self.value.export()


def local(name, value, t = None):
    return Local(name, set_type_expr(value,t) if t else value, t)

def compute(expression):
    return local("compute_%s" % (get_id_from_line_no()), expression).value

def sapling_empty_state(memo_size):
    if not isinstance(memo_size, pyInt) or memo_size < 0 or memo_size > 65535:
        raise Exception("sapling_empty_state(%s) expected a uint16 value as parameter (between 0 and 65535)" % memo_size);
    return Expr("sapling_empty_state", [memo_size, get_file_line_no()]);

def sapling_verify_update(state, transition):
    return Expr("sapling_verify_update", [spExpr(state), spExpr(transition), get_file_line_no()])

def ensure_str(name, x):
    if not isinstance(x, str):
        raise Exception("%s should be a str literal" % name)

def ensure_int(name, x):
    if not isinstance(x, pyInt):
        raise Exception("%s should be an int literal" % name)

def sapling_test_transaction(source, target, amount, memo_size):
    if source is None:
        source = ""
    if target is None:
        target = ""
    ensure_str("test_sapling_transaction source", source)
    ensure_str("test_sapling_transaction target", target)
    ensure_int("test_sapling_transaction amount", amount)
    if amount < 0:
        raise Exception("test_sapling_transaction amount should be non-negative")
    return Expr("sapling_test_transaction", [memo_size, source, target, str(amount), get_file_line_no()])

def operations():
    return Expr("operations", [get_file_line_no()])

def add_operations(l):
    with for_('op', l) as op:
        operations().push(op)

def transfer_operation(arg, amount, destination, line_no = None):
    return Expr(
        "transfer",
        [spExpr(arg, "transfer arguments"), spExpr(amount, "transfer amount"), spExpr(destination, "transfer destination"), get_file_line_no(line_no)],
    )

def transfer(arg, amount, destination, line_no = None):
    operations().push(transfer_operation(arg, amount, destination, line_no))

def set_delegate_operation(key_hash):
    return Expr("set_delegate", [spExpr(key_hash), get_file_line_no()])

def set_delegate(key_hash):
    operations().push(set_delegate_operation(key_hash))

def contract(t, address, entry_point="", line_no = None):
    t = sp.types.conv(t)
    return Expr(
        "contract", [entry_point, sp.types.conv(t), spExpr(address), get_file_line_no(line_no)]
    )

def create_contract_operation(contract, storage = None, amount = tez(0), baker = None):
    storage = spExpr(storage) if storage is not None else contract.storage
    if storage is None:
        raise Exception("Missing storage in sp.create_contract operation.")
    x = local('create_contract_%s' % get_id_from_line_no(),
              Expr("create_contract",
                   [Expr("contract", [contract]),
                    Expr("storage", [storage]),
                    Expr("baker", [spExpr(baker) if baker is not None else baker]),
                    Expr("amount", [spExpr(amount)]),
                    get_file_line_no()]))
    return x.value

def create_contract(contract, storage = None, amount = tez(0), baker = None):
    x = create_contract_operation(contract, storage, amount, baker)
    operations().push(x.operation)
    return x.address

def set_type_expr(expression, t):
    result = Expr("type_annotation", [spExpr(expression), sp.types.conv(t), get_file_line_no()])
    return result

def set_type(expression, t):
    result = Expr("set_type", [spExpr(expression), sp.types.conv(t), get_file_line_no()])
    sp.newCommand(result)
    return Expr("invalid", ["Invalid expression, sp.set_type should no longer be used as an expression, please use sp.set_type_expr instead. %i" % (get_file_line_no().line_no)])

def set_entry_point(ep_name, new_ep):
    sp.newCommand(Expr("set_entry_point", [ep_name, spExpr(new_ep), get_file_line_no()]))

def has_entry_point(ep_name):
    return Expr("has_entry_point", [ep_name, get_file_line_no()])

def profile(s):
    sp.profile(s)

def setProfiling(b):
    sp.profiling = b
    sp.profilingLogs = []

def fst(e):
    return Expr("first", [spExpr(e), get_file_line_no()])

def snd(e):
    return Expr("second", [spExpr(e), get_file_line_no()])

def len(e):
    return Expr("size", [spExpr(e), get_file_line_no()])


types = sp.types

normalMax = max
max = spmax
min = spmin

def poly_equal_expr(a, b):
    t = sp.types.unknown()
    return pack(set_type_expr(a, t)) == pack(set_type_expr(b, t))

class Dynamic_contract:
    def __init__(self, scenario, id):
        self.contractId = dynamic_contract_id(id)
        self.data = contract_data(self.contractId)
        self.balance = contract_balance(self.contractId)
        self.address = contract_address(self.contractId)
        self.baker = contract_baker(self.contractId)
        self.typed = contract_typed(self.contractId)
        self.registered_scenario = scenario

    def call(self, entry_point, parameters):
        res = ExecMessage(None, entry_point, [parameters], None, contractId = self.contractId)
        self.registered_scenario.add_message(res)
        return res


class Scenario:
    def __init__(self):
        self.messages = []
        self.smartml = Smartml(None)
        self.exceptions = []
        self.nextId = 0

    def acc(self, message, show):
        if isinstance(message, str):
            if show:
                self.messages.append(message)
        else:
            self.messages += [self.setShow(message, show)]

    def setShow(self, x, show):
        if isinstance(x, ExecMessage):
            x.show = show
        else:
            x["show"] = show
        return x

    def register(self, element, show=False, accept_unknown_types=False):
        if isinstance(element, Contract):
            self.acc(element.scenario_message(accept_unknown_types), show)
            element.registered_scenario = self
        else:
            self.acc(element, show)

    def __iadd__(self, element):
        if isinstance(element, ExecMessage):
            return self
        self.register(element, True)
        return self

    def add_message(self, message):
        self.register(message, True)
        return self

    def dynamic_contract(self, dynamic_id, model):
        data = {}
        data["action"] = "dynamic_contract"
        data["dynamic_id"] = dynamic_contract_id(dynamic_id).export()
        data["line_no"] = get_file_line_no().export()
        data["model_id"] = model.contractId.export()
        self.messages += [data]
        return Dynamic_contract(self, dynamic_id)


    def pp(self):
        def fix(message):
            if isinstance(message, ExecMessage):
                return message.scenario_message()
            else:
                return message
        self.messages = [fix(message) for message in self.messages]
        if window.in_browser:
            import javascript
            sp.profile("scenario - clean ui " + self.__class__.__name__)
            window.smartpyContext.setOutput("")
            sp.profile("scenario - prepare messages " + self.__class__.__name__)
            messages = {
                'scenario': self.messages,
                'shortname': 'aaa',
                'kind': 'test'
                }
            messages = javascript.JSON.stringify(messages)
            sp.profile("scenario - run " + self.__class__.__name__)
            self.smartml.runScenario(messages)
            sp.profile("scenario - done " + self.__class__.__name__)
        else:
            window.smartpyContext.setOutput(self.messages)
        return self

    def verify(self, condition):
        if isinstance(condition, pyBool):
            if not condition:
                raise Exception("Assert Failure")
        else:
            data = {}
            data["action"] = "verify"
            data["condition"] = spExpr(condition).export()
            data["line_no"] = get_file_line_no().export()
            self.messages += [data]
        return self

    def verify_equal(self, v1, v2):
        data = {}
        data["action"] = "verify"
        data["condition"] = poly_equal_expr(v1, v2).export()
        data["line_no"] = get_file_line_no().export()
        self.messages += [data]
        return self

    def compute(self, expression):
        id = self.nextId
        data = {}
        data["action"] = "compute"
        data["expression"] = spExpr(expression).export()
        data["id"] = id
        data["line_no"] = get_file_line_no().export()
        self.messages += [data]
        self.nextId += 1
        return Expr("scenario_var", [id, get_file_line_no()])

    def show(self, expression, html=True, stripStrings=False, compile=False):
        data = {}
        data["action"] = "show"
        data["compile"] = compile
        data["expression"] = spExpr(expression).export()
        data["html"] = html
        data["line_no"] = get_file_line_no().export()
        data["stripStrings"] = stripStrings
        self.messages += [data]
        return self

    def table_of_contents(self):
        return self.tag("p", "[[TABLEOFCONTENTS]]")

    def p(self, s):
        return self.tag("p", s)

    def h1(self, s):
        return self.tag("h1", s)

    def h2(self, s):
        return self.tag("h2", s)

    def h3(self, s):
        return self.tag("h3", s)

    def h4(self, s):
        return self.tag("h4", s)

    def tag(self, tag, s):
        data = {}
        data["action"] = "html"
        data["inner"] = s
        data["line_no"] = get_file_line_no().export()
        data["tag"] = tag
        self.messages += [data]
        return self

    def add_flag(self, flag, *args):
        data = {}
        data["action"] = "flag"
        data["flag"] = [flag] + pyList(args)
        data["line_no"] = get_file_line_no().export()
        self.messages += [data]

    def simulation(self, c):
        if window.in_browser:
            data = {}
            data["action"] = "simulation"
            data["id"] = c.smartml.contractId.export()
            data["line_no"] = get_file_line_no().export()
            self.messages += [data]
        else:
            self.p("No interactive simulation available out of browser.")


def test_scenario():
    scenario = Scenario()
    window.activeScenario = scenario
    return scenario

def send(destination, amount, message = None):
    transfer(unit, amount, contract(TUnit, destination).open_some(message = message))

# For backward "compatibility"
def Record(**args):
    raise Exception("sp.Record is obsolete, please use sp.record.")

def BigMap(**args):
    raise Exception("sp.BigMap is obsolete, please use sp.big_map.")

def Map(**args):
    raise Exception("sp.Map is obsolete, please use sp.map.")

def Set(**args):
    raise Exception("sp.Set is obsolete, please use sp.set.")


# Library

in_browser = window.in_browser

class Target:
    def __init__(self, name, shortname, f, profile, is_default, kind):
        self.name = name
        self.shortname = shortname
        self.profile = profile
        self.f = f
        self.is_default = is_default
        self.kind = kind

    def eval(self):
        setProfiling(self.profile)
        profile("start")
        window.activeScenario = None
        window.smartpyContext.contractNextId = 0
        window.lambdaNextId = 0
        window.contracts = {}
        window.validityErrors = []
        try:
            self.f()
        finally:
            if window.activeScenario is not None:
                window.activeScenario.pp()
                for e in window.activeScenario.exceptions:
                    raise e
            if window.validityErrors:
                badValidityText = (
                    "Bad validity for some transactions %s\nPlease use c.entryPoint.run(valid = ..expected validation..)"
                    % (
                        " ".join(
                            " <button class=\"text-button\" onClick='showLine(%s)'>(line %s)</button>"
                            % (lineId, lineId)
                            for lineId in window.validityErrors
                        )
                    )
                )
                raise Exception(badValidityText)
        profile("end")
        if self.profile:
            window.smartpyContext.addOutput(
                "<hr/><h4>Profiling</h4>" + "<br>".join(sp.profilingLogs)
            )


def add_target(name, kind, shortname=None, profile=False, is_default=True):
    if shortname is None:
        shortname = name.replace(" ", "_")
    if any(x.shortname == shortname for x in window.pythonTests):
        raise Exception("Already defined scenario %s" % shortname)
    for x in shortname:
        if not (x in "_-" or x.isalnum()):
            raise Exception(
                "Bad test name: '%s', '%s' is forbidden\nTo solve the issue, you can add a shortname by doing, e.g.,\n\nsp.add_test(name = '%s', shortname='%s')"
                % (
                    shortname,
                    x,
                    name,
                    "".join(x for x in shortname if x in "_-" or x.isalnum()),
                )
            )

    def r(f):
        window.pythonTests.append(Target(name, shortname, f, profile, is_default, kind))

    return r

def add_test(name, shortname=None, profile=False, is_default=True):
    return add_target(name, shortname=shortname, profile=profile, is_default=is_default, kind="test")

def add_simulation_target(contract, name="Simulation", shortname=None, profile=False, is_default=False, flags=[]):
    def test():
        scenario = test_scenario()
        for flag in flags:
            if isinstance(flag, str):
                scenario.add_flag(flag)
            else:
                scenario.add_flag(*flag)
        scenario += contract
        scenario.simulation(contract)
    return add_test(name = name, shortname = shortname, profile = profile, is_default = is_default)(test)

def add_compilation_target(name, contract, storage=None, parameters=[], shortname=None, is_default=False, flags=[]):
    if storage is not None:
        contract.storage = storage
    def f():
        scenario = test_scenario()
        for flag in flags:
            if isinstance(flag, str):
                scenario.add_flag(flag)
            else:
                scenario.add_flag(*flag)
        scenario += contract
        for (f, params) in parameters:
            scenario += getattr(contract, f)(params).run(export = True)
    add_target(name=name, shortname=shortname, is_default=is_default, kind="compilation")(f)

def add_expression_compilation_target(name, expression, shortname=None, is_default=False, flags=[]):
    def f():
        scenario = test_scenario()
        for flag in flags:
            if isinstance(flag, str):
                scenario.add_flag(flag)
            else:
                scenario.add_flag(*flag)
        scenario.show(expression, compile=True)
    add_target(name=name, shortname=shortname, is_default=is_default, kind="compilation")(f)

def compile_contract(
        contract,
        target_directory,
        name = "contract"
):
    """Exports contract to smlse, code and storage files."""
    import subprocess
    import os
    os.makedirs(target_directory, exist_ok=True)
    targetSmlse = target_directory + "/" + name + ".smlse"
    open(targetSmlse, "w").write(contract.export())
    command = [
        "node",
        os.path.dirname(os.path.realpath(__file__)) + "/smartml-cli.js",
        "compile-smartml-contract",
        targetSmlse,
        target_directory
    ]
    subprocess.run(command)

class Verbatim:
    def __init__(self, s):
        self.s = s
    def export(self):
        return self.s


class Lazy_strings(build_big_map):
    def __init__(self, contract, path):
        super().__init__()
        self.next_id = 0
        self.contract = contract
        self.path = path
        self.app = None
        self.d = {}
    def get(self, x):
        result(self.path(fst(x)).get(snd(x), ""))
    def __call__(self, x):
        if not(isinstance(x, str)):
            return x
        try:
            return self.d[x]
        except KeyError:
            self.l[self.next_id] = x
            if False:
                result = self.path(self.contract.data).get(self.next_id, "")
            else:
                if self.app is None:
                    self.app = self.contract.global_lambda("get_error", self.get)
                result = self.app((self.contract.data, self.next_id))
                self.d[x] = result
            self.next_id += 1
            return result
    def export(self):
        m = Verbatim(super().export())
        return set_type_expr(m, TBigMap(TNat, TString)).export()


class bind_block:
    __slots__ = ['name', 'inner', 'value']

    def __init__(self, name=None):
        self.name = "__s%d" % sp.types.seqNo() if name is None else name

    def __enter__(self):
        self.inner = CommandBlock(sp)
        self.inner.__enter__()

    def __exit__(self, type, value, traceback):
        self.inner.__exit__(type, value, traceback)
        sp.newCommand(self.inner, self.name)

    def __getattribute__(self, name):
        if name == "value":
            return Expr("getLocal", [self.name, get_file_line_no()])
        return object.__getattribute__(self, name)

    def __setattribute__(self, name, value):
        if name == "value":
            raise Exception(f"Cannot assign to variable '{self.name}'")
        self.__dict__[name] = value


def trace(expression):
    sp.newCommand(Expr("trace", [spExpr(expression), get_file_line_no()]))


def eif(c, a, b):
    return Expr("eif", [spExpr(c), spExpr(a), spExpr(b), get_file_line_no()])

class Clause:
    def __init__(self, constructor, rhs):
        self.constructor = constructor
        self.rhs = rhs

    def export(self):
        return "(%s %s)" % (self.constructor, self.rhs.export())


def ematch(scrutinee, clauses):
    def f(x):
        if not (isinstance(x, pyTuple) and pyLen(x) == 2 and isinstance(x[0], str)):
            raise Exception("sp.ematch: clause is not a tuple of string and lambda")
        constructor = x[0]
        rhs = spExpr(x[1])
        return Clause(constructor, rhs)
    clauses = pyList(pyMap(f, clauses))
    return Expr("ematch", [ get_file_line_no(), scrutinee ] + clauses)

def eif_somef(c, a, b):
    return ematch(c, [ ("Some", a), ("None", b) ])

def eif_some(c, a, b):
    return eif_somef(c, a, lambda _: b)

def set_result_type(t):
    b = CommandBlock(sp)
    sp.newCommand(Expr("set_result_type", [b, t, get_file_line_no()]))
    return b

def inline_result(f):
    def inner(*args, **kwargs):
        b = bind_block()
        with b:
            f(*args, **kwargs)
        return b.value
    return inner

def ticket(content, amount):
    line_no = get_file_line_no()
    x = local('ticket_%i' % line_no.line_no, Expr("ticket", [spExpr(content), spExpr(amount), line_no]))
    return x.value

def read_ticket_raw(ticket):
    return Expr("read_ticket", [spExpr(ticket), get_file_line_no()])

def split_ticket_raw(ticket, amounts):
    return Expr("split_ticket", [spExpr(ticket), spExpr(amounts), get_file_line_no()])

def join_tickets_raw(tickets):
    return Expr("join_tickets", [spExpr(tickets), get_file_line_no()])

class Read_ticket:
    def __init__(self, ticketer, content, amount, copy):
        self.ticketer = ticketer
        self.content = content
        self.amount = amount
        self.copy = copy


def read_ticket(ticket):
    line_no = get_id_from_line_no()
    data     = 'ticket_%s_data'     % line_no
    ticketer = 'ticket_%s_ticketer' % line_no
    content  = 'ticket_%s_content'  % line_no
    amount   = 'ticket_%s_amount'   % line_no
    copy     = 'ticket_%s_copy'     % line_no
    r = read_ticket_raw(ticket)
    (data,copy) = match_tuple(r, data, copy)
    (ticketer, content, amount) = match_tuple(data, ticketer, content, amount)
    return Read_ticket(ticketer, content, amount, copy)

def split_ticket(ticket, amount1, amount2):
    line_no = get_id_from_line_no()
    ticket1 = 'ticket1_%s' % line_no
    ticket2 = 'ticket2_%s' % line_no
    r = split_ticket_raw(ticket, (amount1, amount2)).open_some()
    return match_tuple(r, ticket1, ticket2)

def join_tickets(ticket1, ticket2):
    return join_tickets_raw((ticket1, ticket2)).open_some()

def match_record(x, *fields):
    id_line_no = get_id_from_line_no()
    line_no = get_file_line_no()
    bs  = [[f"{fld}_{id_line_no}", fld] for fld in fields]
    bse = [Expr("binding", b) for b in bs]
    sp.newCommand(Expr("match_record", [line_no, x] + bse))
    r = [ Expr("variant_arg", [b[0], line_no]) for b in bs ]
    return pyTuple(r)

def match_tuple(x, *names):
    names = pyList(names)
    line_no = get_file_line_no()
    sp.newCommand(Expr("match_tuple", [line_no, spExpr(x)] + names))
    r = [ Expr("variant_arg", [n, line_no]) for n in names ]
    return pyTuple(r)

def match_pair(x):
    line_no = get_id_from_line_no()
    fst = 'match_pair_%s_fst' % line_no
    snd = 'match_pair_%s_snd' % line_no
    return match_tuple(x, *[fst, snd])

class Modify_record(CommandBlock):
    def __init__(self, x, var, sp, line_no):
        super().__init__(sp)
        self.line_no = line_no
        self.attributes = {}
        self.value = self
        self.fields = []
        self.bindings = []
        self._x = x
        self._var = var
        self._loc = Expr("getMetaLocal", [self._var, self.line_no])
        setattr(self, "__initialized", True)

    def __getattr__(self, attr):
        if "__" in attr:
            raise AttributeError("")
        try:
            return self.attributes[attr]
        except KeyError:
            self.fields.append(attr)
            v = getattr(self._loc, attr)
            object.__setattr__(self, attr, v)
            self.attributes[attr] = v
            self.bindings.append(attr)
            return v

    def __setattr__(self, attr, value):
        if "__" not in attr and hasattr(self, "__initialized") and not attr in ["sp", "currentBlock"]:
            sp.set(getattr(self, attr), value)
        else:
            object.__setattr__(self, attr, value)

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)

    def export(self):
        return (Expr("modify_record", [self.line_no, self._x, self._var, self.commands] + [Expr("binding", b) for b in self.bindings])).export()

def modify_record(x, var = None):
    x = spExpr(x)
    line_no = get_file_line_no()
    if var is None:
        var = f"modify_record_{get_id_from_line_no()}"
    bindings = []
    body = Modify_record(x, var, sp, line_no)
    sp.newCommand(body)
    return body

def modify_tuple(x, *variables):
    variables = pyList(variables)
    x = spExpr(x)
    line_no = get_file_line_no()
    body = CommandBlock(sp)
    sp.newCommand(Expr("modify_tuple", [line_no, x, body] + variables))
    value = pyTuple([ Expr("getLocal", [fld, line_no]) for fld in variables])
    body.value = value
    return body

def modify(x, variable):
    x = spExpr(x)
    line_no = get_file_line_no()
    body = CommandBlock(sp)
    sp.newCommand(Expr("modify", [line_no, x, body, variable]))
    value = Expr("getLocal", [variable, line_no])
    body.value = value
    return body

def test_ticket(ticketer, content, amount):
    line_no = get_file_line_no()
    return Expr("test_ticket", [spExpr(ticketer), spExpr(content), spExpr(amount), line_no])

def check_contract_id(context, contractId):
    if not isinstance(contractId, ContractId):
        raise Exception(f"sp.{context} applied to expression that is not a ContractId. {pretty_line_no()}" )

def contract_data(contractId):
    check_contract_id("contract_data", contractId)
    return Expr("contract_data", [contractId, get_file_line_no()])

def contract_balance(contractId):
    check_contract_id("contract_balance", contractId)
    return Expr("contract_balance", [contractId, get_file_line_no()])

def contract_address(contractId, entry_point = ""):
    check_contract_id("contract_address", contractId)
    return Expr("contract_address", [contractId, entry_point, get_file_line_no()])

def contract_baker(contractId):
    check_contract_id("contract_baker", contractId)
    return to_constant(Expr("contract_baker", [contractId, get_file_line_no()]))

class ContractTyped:
    def __init__(self, contractId, entry_point, line_no):
        self.contractId = contractId
        self.line_no = line_no
        self.entry_point = entry_point

    def export(self):
        return Expr("contract_typed", [self.contractId, self.entry_point, self.line_no]).export()

    def __getattr__(self, attr):
        if "__" in attr:
            raise AttributeError("")
        return Expr("contract_typed", [self.contractId, attr, self.line_no])

def contract_typed(contractId, entry_point = ""):
    check_contract_id("contract_typed", contractId)
    return ContractTyped(contractId, entry_point, get_file_line_no())

class ContractId:
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return str(self.expr)
    def export(self):
        return self.expr.export()

def dynamic_contract_id(id):
    return ContractId(Expr("dynamic_id", [id, get_file_line_no()]))

def static_contract_id(id):
    return ContractId(Expr("static_id", [id, get_file_line_no()]))

class michelson:
    def __init__(self, code, types_in, types_out):
        self.types_in = [sp.types.conv(t) for t in types_in]
        self.types_out = [sp.types.conv(t) for t in types_out]
        self.instr = Expr(
            "op",
            [code]
            + self.types_in
            + ["out"]
            + self.types_out,
        )

    def __call__(self, *args):
        return Expr(
            "call_michelson",
            [spExpr(self.instr), get_file_line_no()] + [spExpr(x) for x in args],
        )

def lambda_michelson(code, source = None, target = None):
    source = sp.types.conv(source)
    target = sp.types.conv(target)
    def f(x):
        result(michelson(code, [source], [target])(x))
    return build_lambda(f, "x")

class utils:
    @staticmethod
    def same_underlying_address(attr1, attr2):
        addr1 = set_type_expr(attr1, TAddress)
        addr2 = set_type_expr(attr2, TAddress)
        b1 = slice(pack(addr1), 6, 22)
        b2 = slice(pack(addr2), 6, 22)
        return b1 == b2

    @staticmethod
    def mutez_to_nat(x):
        return fst(ediv(x, mutez(1)).open_some(unit))

    @staticmethod
    def nat_to_mutez(x):
        return mul(x, mutez(1))

    @staticmethod
    def nat_to_tez(x):
        return mul(x, tez(1))

    @staticmethod
    def vector_raw(xs):
        return map(l={k: v for (k, v) in enumerate(xs)})

    @staticmethod
    def matrix_raw(xs):
        return utils.vector_raw([utils.vector_raw(x) for x in xs])

    @staticmethod
    def cube_raw(xs):
        return utils.vector_raw([utils.matrix_raw(x) for x in xs])

    @staticmethod
    def vector(xs, tkey = TIntOrNat, tvalue = None):
        return set_type_expr(utils.vector_raw(xs), TMap(tkey, tvalue))

    @staticmethod
    def matrix(xs, tkey = TIntOrNat, tvalue = None):
        return set_type_expr(utils.matrix_raw(xs), TMap(tkey, TMap(tkey, tvalue)))

    @staticmethod
    def cube(xs, tkey = TIntOrNat, tvalue = None):
        return set_type_expr(utils.cube_raw(xs), TMap(tkey, TMap(tkey, TMap(tkey, tvalue))))

    @staticmethod
    def view(t, message = None):
        def app(f):
            line_no = get_file_line_no()
            def ep(self, params):
                view_result = bind_block()
                with view_result:
                    f(self, fst(params))
                set_type(snd(params), TContract(t))
                transfer(view_result.value,
                        tez(0),
                        snd(params),
                        line_no = line_no)
            return entry_point(ep, name = f.__name__, line_no = line_no)
        return app

    @staticmethod
    def bytes_of_string(s):
        if not(isinstance(s, str)):
            raise Exception("sp.utils.bytes_of_string must be applied to constant strings and got (%s)" % (str(s)))
        return bytes("0x" + s.encode('utf-8').hex())

    @staticmethod
    def metadata_of_url(url):
        return big_map({"" : utils.bytes_of_string(url)})

    @staticmethod
    def lambda_with_operations(f, params="", tParams = None, global_name=None):
        def f_wrapped(x):
            ops = local("__operations__", [], t = TList(TOperation))
            y = bind_block()
            with y:
                f(x)
            result(pair(ops.value, y.value))
        return build_lambda(f_wrapped, params, tParams, global_name)

    @staticmethod
    def lambda_operations_only(f, params="", tParams = None, global_name=None):
        def f_wrapped(x):
            ops = local("__operations__", [], t = TList(TOperation))
            f(x)
            result(ops.value)
        return build_lambda(f_wrapped, params, tParams, global_name)

    @staticmethod
    def wrap_entry_point(ep, f):
        def w(p):
            params, storage = match_pair(p)
            params = params.open_variant(ep)
            storage = local('storage', storage)
            class G: pass
            self = G()
            self.data = storage.value
            f(self, params)
            result(storage.value)
        return utils.lambda_with_operations(w)

class io:
    @staticmethod
    def import_script_from_script(name, script):
        import smartpyio
        template = smartpyio.adaptBlocks(script)
        class Mod: pass
        module = Mod()
        module.__dict__['__name__'] = name
        template = compile(template, name, 'exec')
        exec (template, module.__dict__)
        return module

    @staticmethod
    def import_template(name):
        if in_browser:
            directory = ".." if window.location.pathname.endswith("/") else ".";
        else:
            import pathlib
            directory = pathlib.Path(__file__).parent.absolute()
        template = open(str(directory) + "/templates/" + name, "r").read()
        return io.import_script_from_script("templates/" + name, template)

    @staticmethod
    def import_script_from_url(url, name = None):
        if name is None:
            name = url
        if in_browser:
            import urllib.request
            template = urllib.request.urlopen(url).read()
        else:
            import urllib.request
            template = urllib.request.urlopen(url).read().decode('utf-8')
        return io.import_script_from_script(name, template)

    @staticmethod
    def import_stored_contract(name):
        code = window.smartpyContext.getContractCode(name)
        if not code:
            raise Exception("Could not import_stored_contract (" + name + "). It doesn't exist.")
        return io.import_script_from_script(name, code)
