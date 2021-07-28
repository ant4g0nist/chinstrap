## Copyright 2019-2020 Smart Chain Arena LLC. ##

# This module is used by smartpyc.ml. No other code shoud rely on it.

import sys, traceback, json, browser, smartpyio

debug_mode = False

def print_compile_error(e):
    for i in traceback.format_exception_only(type(e), e):
        sys.stderr.write(i)

def print_filtered_traceback(fns):
    if debug_mode:
        traceback.print_exc(file=sys.stdout)
    else:
        etype, value, tb = sys.exc_info()
        xs = [i for i in traceback.extract_tb(tb) if i.filename in fns]
        if xs:
            sys.stderr.write("Traceback (most recent call last):\n")
            for i in traceback.format_list(xs):
                sys.stderr.write(i)
            for i in traceback.format_exception_only(etype, value):
                sys.stderr.write(i)
        else:
            traceback.print_exc(file=sys.stdout)

def write_pure_py(out, in_py):
    with open(in_py, "r") as in_py:
        with open(out, "w") as out:
            in_py = in_py.read()
            r = smartpyio.adaptBlocks(in_py)
            out.write(r)
    return r

def run_script(in_py, code, context, script_args):
    smartpyio.script_filename = in_py
    sys.argv = [in_py] + list(script_args)
    try:
        code = compile(code, in_py, "exec")
    except Exception as e:
        print_compile_error(e)
        sys.exit(1)
    try:
        exec(code, context)
    except:
        print_filtered_traceback([in_py])
        sys.exit(1)

def init_contract(fn_py, arg, context):
    try:
        contract = compile(arg, "init", "eval")
    except Exception as e:
        print_compile_error(e)
        sys.exit(1)
    try:
        contract = eval(contract, context)
    except:
        print ("Error while evaluating '%s':" % arg)
        print_filtered_traceback([fn_py, "init"])
        sys.exit(1)
    return contract

def write_smlse(out_smlse, in_py, in_pure_py, init):
    open(out_smlse, "w").write(contract.export())

def run_tests(in_py):
    scenarios = []
    for test in browser.window.pythonTests:
        try:
            test.eval()
        except Exception as exn:
            data = {}
            data["action"] = "error"
            data["message"] = str(exn)
            if browser.scenario is not None:
                browser.scenario += [data]
            else:
                browser.scenario = [data]
                print ("Exception while testing")
            print_filtered_traceback([in_py])
        if isinstance(browser.scenario, list):
            scenario = browser.scenario
        else:
            scenario = browser.scenario.messages
        scenarios.append({'shortname': test.shortname, 'longname': test.name, 'scenario' : scenario, 'kind' : test.kind})
    return json.dumps(scenarios, indent = 1)

def write_tests(out_scenario_sc, fn_py, fn_pure_py, *script_args):
    code = write_pure_py(fn_pure_py, fn_py)
    run_script(fn_py, code, {'__name__' : '__main__'}, script_args)
    scenarios = run_tests(fn_py)
    open(out_scenario_sc, "w").write(scenarios)

def write_with_init_expr(out_smlse, fn_py, fn_pure_py, init, *script_args):
    code = write_pure_py(fn_pure_py, fn_py)
    context = {'__name__' : '__main__'}
    run_script(fn_py, code, context, script_args)
    expr = init_contract(fn_py, init, context)
    try:
        import smartpy as sp
        open(out_smlse, "w").write(sp.spExpr(expr).export())
    except:
        print_filtered_traceback([fn_py])
        sys.exit(1)

def write_with_init(out_smlse, fn_py, fn_pure_py, init, script_args):
    code = write_pure_py(fn_pure_py, fn_py)
    context = {'__name__' : '__main__'}
    run_script(fn_py, code, context, script_args)
    contract = init_contract(fn_py, init, context)
    try:
        open(out_smlse, "w").write(contract.export())
    except:
        print_filtered_traceback([fn_py])
        sys.exit(1)

if sys.argv[1] == "write_with_init":
    write_with_init(*sys.argv[2:])
elif sys.argv[1] == "write_with_init_expr":
    write_with_init_expr(*sys.argv[2:])
elif sys.argv[1] == "write_tests":
    write_tests(*sys.argv[2:])
else:
    assert False
