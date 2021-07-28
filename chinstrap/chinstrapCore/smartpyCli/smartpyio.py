## Copyright 2019-2020 Smart Chain Arena LLC. ##

from browser import alert, window
import os

window.activeScenario = None
window.contracts = {}
window.pythonTests = []

import traceback

context = globals().copy()
context["alert"] = alert
context["window"] = window
reverseLines = {}


def formatErrorLine(line):
    i = -1
    while i + 2 < len(line) and line[i + 1] == " ":
        i += 1
    if 0 <= i:
        line = i * "&nbsp;" + line[i + 1 :]
    return line


def showTraceback(title, trace):
    title = "Error: " + str(title)
    lines = []
    skip = False
    print(trace)
    for line in trace.split("\n"):
        if not line:
            continue
        if skip:
            skip = False
            continue
        skip = ("module smartpy line" in line
                or "module smartpyio.py line" in line
                or "module smartpyio line" in line
                or ("module __main__" in line and "in run" in line)
        )
        if "Traceback (most recent call last):" in line:
            line = ""
        if not skip:
            lineStrip = line.strip()
            lineId = None
            line = formatErrorLine(line)
            if lineStrip.startswith("module <module>") or lineStrip.startswith("File <string>"):
                lineId = line.strip().split()[3].strip(",")
                line = line.replace(lineId, reverseLines.get(lineId, lineId))
            line = line.replace("module <module>", "SmartPy code").replace("File <string>", "SmartPy code")
            if "SmartPy code" in line:
                line = "<span class='partialType'>%s</span>" % (line)
            if lineId:
                line = (
                    line
                    + " <button class=\"text-button\" onClick='showLine(%s)'>(line %s)</button>"
                    % (lineId, lineId)
                )
            lines.append(line)
    error = title + "\n\n" + lines[0] + "\n\n" + "\n".join(lines[1:-1])
    window.smartpyContext.showError(
        "<div class='michelson'>%s</div>" % (error.replace("\n", "\n<br>"))
    )


def evalTest(name):
    for test in window.pythonTests:
        if test.name == name:
            test.eval()


def syntaxChanges():
    changes = []

    def fix(s, prev=None, prefix="sp."):
        if prev is None:
            prev = []
            capitalize = False
            for c in s:
                if capitalize:
                    prev.append(c.upper())
                    capitalize = False
                    continue
                if c == "_":
                    capitalize = True
                else:
                    prev.append(c)
            prev = "".join(prev)
        changes.append((prefix + prev, prefix + s))

    fix("add_seconds")
    fix("as_nat")
    fix("big_map")
    fix("build_lambda")
    fix("check_signature")
    fix("entry_point")
    fix("int_or_nat")
    fix("is_left")
    fix("is_nat")
    fix("is_right")
    fix("is_some")
    fix("is_variant")
    fix("local", prev="newLocal")
    fix("open_some")
    fix("open_variant")
    fix("set_delegate")
    fix("set_type")
    fix("split_tokens")
    fix("test_scenario")
    fix("to_int")
    fix("update_map")
    fix("sp.add_test", prev="addTest", prefix="")
    # Utils
    fix("sp.utils.bytes_of_string", "sp.bytes_of_string", prefix="")
    fix("sp.utils.metadata_of_url", "sp.metadata_of_url", prefix="")
    fix("sp.utils.view", "sp.view", prefix="")
    fix("sp.utils.cube", "sp.cube", prefix="")
    fix("sp.utils.matrix", "sp.matrix", prefix="")
    fix("sp.utils.vector", "sp.vector", prefix="")
    fix("sp.utils.cube_raw", "sp.cube_raw", prefix="")
    fix("sp.utils.matrix_raw", "sp.matrix_raw", prefix="")
    fix("sp.utils.vector_raw", "sp.vector_raw", prefix="")
    # IO
    fix("sp.io.import_script_from_script", "sp.import_script_from_script", prefix="")
    fix("sp.io.import_template", "sp.import_template", prefix="")
    fix("sp.io.import_script_from_url", "sp.import_script_from_url", prefix="")
    fix("sp.io.import_stored_contract", "sp.import_stored_contract", prefix="")

    return changes


def adaptBlocks(code):
    lines = code.split("\n") + [""]

    def indent(line):
        result = 0
        for i in line:
            if i == " ":
                result += 1
            else:
                break
        return result

    blocks = []
    lineId = 0
    newLines = []

    class NewLine:
        def __init__(self, pos, line):
            if pos is None:
                pos = -1
            self.pos = pos
            self.line = line

    for line in lines:
        initialLine = line
        lineId += 1
        newIndent = indent(line)
        stripped = line.strip()
        nline = line.strip(" \r")
        if line[newIndent:].startswith("sp.for "):
            p = nline[:-1].split(" ")
            if nline[-1] == ":" and p[0] == "sp.for" and p[2] == "in":
                line = "%swith sp.for_('%s', %s) as %s:" % (
                    newIndent * " ",
                    p[1],
                    " ".join(p[3:]),
                    p[1],
                )
        elif line[newIndent:].startswith("sp.if "):
            p = nline[:-1].split(" ")
            if nline[-1] == ":" and p[0] == "sp.if":
                line = "%swith sp.if_(%s):" % (newIndent * " ", " ".join(p[1:]))
        elif line[newIndent:].startswith("sp.while "):
            p = nline[:-1].split(" ")
            if nline[-1] == ":" and p[0] == "sp.while":
                line = "%swith sp.while_(%s):" % (newIndent * " ", " ".join(p[1:]))
        elif line[newIndent:].startswith("sp.else ") or line[newIndent:].startswith(
            "sp.else:"
        ):
            if nline[-1] == ":":
                line = "%swith sp.else_():" % (newIndent * " ")
        if initialLine.endswith("\r") and not line.endswith("\r"):
            line += "\r"
        newLines.append(NewLine(lineId, line))
    result = "\n".join(line.line for line in newLines)
    result = result.rstrip() + "\n"
    global reverseLines
    reverseLines.clear()
    for i in range(len(newLines)):
        reverseLines[str(i + 1)] = str(newLines[i].pos)
    return result


testTemplate = """
@sp.add_test(name = "%s")
def test():
    # define a contract
    c1 = %s(..)
    scenario  = sp.test_scenario()
    scenario += c1
    # scenario += c1.myEntryPoint(..)
    # scenario += c1.myEntryPoint(..)
    # scenario += c1.myEntryPoint(..)
    # scenario.verify(..)
    # scenario.show(..)
    # scenario.p(..)
    # scenario.h1(..)
"""


def run(withTests):
    window.pythonTests.clear()
    window.smartpyContext.clearOutputs()
    import smartpy

    smartpy.defaultVerifyMessage = None
    smartpy.sp.types.unknownIds = 0
    smartpy.sp.types.seqCounter = 0
    code = window.smartpyContext.getEditorValue();
    changes = syntaxChanges()
    for change in changes:
        if change[0] in code:
            if window.in_browser:
                message = (
                    "Warning: syntax change: %s -> %s" % (change[0], change[1])
                    + "\n\nMigrate Syntax to adapt your script automatically?\n\nOther changes:\n"
                    + "\n".join(
                        "%s -> %s" % (change[0], change[1]) for change in changes
                    )
                )
                from browser import confirm

                if confirm(message):
                    for ch in changes:
                        code = code.replace(ch[0], ch[1])
                    window.editor.setValue(code)
                    break
            else:
                print(
                    "Warning: syntax change: %s -> %s. You can use the editor to adapt it."
                    % (change[0], change[1])
                )
    code = adaptBlocks(code)
    env = context.copy()
    env['__name__'] = '__main__'
    exec(code, env)
    window.smartpyContext.clearOutputs()
    for test in window.pythonTests:
        window.smartpyContext.addButton(test.name, test.kind, test.f)
        if withTests and test.is_default:
            test.eval()
    if withTests and len(window.pythonTests) == 0:
        html = ""
        for c in env:
            if "$" in c:
                continue
            if hasattr(env[c], "collectMessages"):
                html += (
                    "There is a sp.Contract class '%s' but no test is defined.\n\nPlease add a test such as:\n%s"
                    % (str(c), testTemplate % (c, c))
                )
        if html:
            alert(html)

def onContract(address, cont):
    window.onContract(address, cont)


def showCommands(platform):
    l = []
    commands = window.editor.commands.commands
    for c in sorted(commands):
        try:
            l.append("%-40s : %s" % (c, commands[c].bindKey[platform]))
        except:
            pass
    return "<pre>%s</pre>" % "\n".join(l)


def toException(x):
    return Exception(x)


def ppMichelson(code, withComments):
    lines = [x.strip() for x in code.split("\n")]

    def split(s):
        if "#" in s:
            pos = s.index("#")
            return s[:pos].strip(), s[pos:].strip()
        return s.strip(), None

    lines = [split(x) for x in lines if x]
    result = []
    for s, c in lines:
        if not withComments:
            c = None
        s = (
            s.replace("{", " { ")
            .replace("}", " } ")
            .replace("(", " ( ")
            .replace(")", " ) ")
            .replace(" ;", ";")
            .replace(" ;", ";")
            .strip()
        )
        split = s.split()
        cursor = 0
        if s == "" and c:
            result.append((s, c))
        while len(split):
            if split[cursor] in ["parameter", "storage", "code"]:
                result.append((" ".join(split[0 : cursor + 1]), None))
                split = split[cursor + 1 :]
                continue
            if split[cursor] in ["{", "}", "};", ";"]:
                if cursor != 0:
                    result.append((" ".join(split[0:cursor]), None))
                    split = split[cursor:]
                    cursor = 0
                else:
                    result.append((" ".join(split[0 : cursor + 1]), None))
                    split = split[cursor + 1 :]
            elif len(split) == cursor + 1:
                result.append((" ".join(split[0 : cursor + 1]), c))
                split = []
            elif split[cursor].endswith(";"):
                result.append((" ".join(split[0 : cursor + 1]), None))
                split = split[cursor + 1 :]
                cursor = 0
            else:
                cursor += 1
    lines = result
    parameter = []
    storage = []
    code = []
    init = []
    result = {"init": init, "parameter": parameter, "storage": storage, "code": code}
    step = "init"
    indent = ""
    for (s, c) in lines:
        if s == "{":
            indent = indent + "  "
            nextIndent = indent + "  "
        elif "}" in s:
            indent = indent[:-2]
            nextIndent = indent[:-2]
        else:
            nextIndent = indent
        if s in ["parameter", "storage", "code"]:
            step = s
        line = (
            (indent + ("%-10s %s" % (s, c) if c else s))
            if step != "init"
            else (("%s %s" % (s, c)).strip() if c else s)
        )
        if line:
            result[step].append(line)
        indent = nextIndent
    if init:
        init = "\n".join(init) + "\n\n"
    else:
        init = ""
    michelson = "%s%s\n%s\n%s" % (
        init,
        " ".join(parameter).replace(" )", ")").replace("( ", "(").replace(" ;", ";"),
        ("storage   %s" % (" ".join(storage[1:]))).replace(" )", ")").replace("( ", "(").replace(" ;", ";"),
        "\n".join(code),
    )
    return michelson


def ppMichelsonEditor(withComments):
    return ppMichelson(window.editor.getValue(), withComments)


def ppMichelsonEditorCompress():
    return removeCommentsMichelson(ppMichelson(window.editor.getValue(), False))


def compressMichelson(lines):
    result = []
    inSeq = False
    for line in lines:
        row = line.split()
        seqOK = (
            "{" not in line
            and "}" not in line
            and row[-1][-1] == ";"
            and not row[0].startswith("parameter")
            and not row[0].startswith("storage")
        )
        if inSeq and seqOK:
            result[-1] += " " + " ".join(row)
        else:
            result.append(line)
            inSeq = seqOK
    return result


def removeCommentsMichelson(michelson):
    lines = [
        x[: x.index("#")].rstrip() if "#" in x else x for x in michelson.split("\n")
    ]
    lines = [x for x in lines if x.strip()]
    lines = compressMichelson(lines)
    return "\n".join(lines)


window.lambdaNextId = 0
window.evalTest = evalTest
window.evalRun = run
window.showTraceback = showTraceback
window.showCommands = showCommands
window.toException = toException
window.ppMichelsonEditor = ppMichelsonEditor
window.ppMichelsonEditorCompress = ppMichelsonEditorCompress
window.removeCommentsMichelson = removeCommentsMichelson

if hasattr(window, 'dispatchEvent'):
    window.dispatchEvent(window.CustomEvent.new('smartpyio_ready'))
