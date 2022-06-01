import os
import chinstrap
from rich import pretty
from pytezos import ContractInterface
from pytezos import pytezos
from chinstrap import helpers
from chinstrap import sandbox
from argparse import Namespace
from chinstrap.repl import repl
from ptpython.repl import embed
from chinstrap.core import config
from chinstrap import originations
from chinstrap.compiler import Compilers
from chinstrap.languages import TemplateOptions


@helpers.handleException()
def cExit():
    helpers.hexit()


@helpers.handleException()
def stopSandbox():
    sand = sandbox.Sandbox("")
    sand.halt()


@helpers.handleException()
def getContract(name):
    """
    Get Contract Interface from name.
    arguments:
        name: name of the contract from contracts/ folder to get
    returns  :
        pytezos.ContractInterface
    """
    return originations.getContract(name)


@helpers.handleException()
def getContractFromFile(filename):
    """
    Get contract from michelson source code stored in a file and returns.
    arguments:
        filename: filename of the contract to get
    returns  :
        pytezos.ContractInterface
    """
    if os.path.exists(filename):
        return ContractInterface.from_file(filename)

    helpers.error("Please make sure file exists!")


@helpers.handleException()
def getContractFromAddress(address):
    return _config.wallet.contract(address)


@helpers.handleException()
def getContractFromURL(url):
    return ContractInterface.from_url(url)


@helpers.handleException()
def compile(contract=None, local=False, werror=False, warning=False, entrypoint="main"):
    args = Namespace(
        contract=contract,
        local=local,
        werror=werror,
        warning=warning,
        entrypoint=entrypoint,
    )
    chinstrap.chinstrapCompileContracts(args, "")


@helpers.handleException()
def test(test=None, local=False, entrypoint="main"):
    args = Namespace(test=test, local=local, entrypoint=entrypoint)
    chinstrap.chinstrapRunTests(args, "")


@helpers.handleException()
def template(language=TemplateOptions):
    args = Namespace(language=language)
    chinstrap.chinstrapTemplates(args, "")


@helpers.handleException()
def originate(
    originate=None,
    number=None,
    network="development",
    port=20000,
    reset=False,
    show=False,
    force=False,
    contract=None,
    local=False,
    werror=False,
    warning=False,
    entrypoint="main",
):
    args = Namespace(
        originate=originate,
        number=number,
        network=network,
        port=port,
        reset=reset,
        show=show,
        force=force,
        contract=contract,
        local=local,
        werror=werror,
        warning=warning,
        entrypoint=entrypoint,
    )
    chinstrap.chinstrapRunOriginations(args, "")


@helpers.handleException()
def sandboxAccounts():
    sandbox.Sandbox.listAccounts()


@helpers.handleException()
def install(compiler=Compilers, local=False, force=False):
    args = Namespace(compiler=compiler, local=local, force=force)
    chinstrap.chinstrapInstallCompilers(args, "")


def launchRepl(args):
    global _config
    pretty.install()

    if args.network == "development":
        _sandbox = sandbox.Sandbox(args)
        _sandbox.args.detach = True
        _sandbox.initialize()
        _sandbox.run()

    _config = config.Config(args.network, compileFlag=True)

    helpers.printFormatted(
        f"""Loaded wallet <ansiyellow><b>{_config.wallet.key.public_key_hash()}</b> \
    </ansiyellow>. Balance: <ansired>ꜩ</ansired> <ansigreen>\
<b>{_config.wallet.balance()}</b></ansigreen>\n"""
    )

    functions = {
        "pytezos": pytezos,
        "config": _config,
        "network": _config.network,
        "getContract": getContract,
        "getContractFromFile": getContractFromFile,
        "getContractFromURL": getContractFromURL,
        "getContractFromAddress": getContractFromAddress,
        "compile": compile,
        "test": test,
        "template": template,
        "TemplateOptions": TemplateOptions,
        "JsLigo": TemplateOptions.jsligo,
        "CameLIGO": TemplateOptions.cameligo,
        "ReasonLIGO": TemplateOptions.religo,
        "PascaLIGO": TemplateOptions.pascaligo,
        "accounts": sandboxAccounts,
        "stopSandbox": stopSandbox,
        "originate": originate,
        "install": install,
        "compilers": Compilers,
        "exit": cExit,
    }

    embed({}, functions, configure=repl.configure, history_filename=repl.historyPath)
