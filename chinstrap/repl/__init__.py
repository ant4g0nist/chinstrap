import os
import requests
import chinstrap
from rich import pretty
from pytezos import pytezos
from chinstrap import helpers
from argparse import Namespace
from chinstrap.repl import repl
from ptpython.repl import embed
from chinstrap.core import config
from chinstrap import originations
from pytezos import ContractInterface
from chinstrap import sandbox as Sandbox
from chinstrap.compiler import Compilers
from chinstrap.languages import TemplateOptions


@helpers.handleException()
def cExit():
    helpers.hexit()


@helpers.handleException()
def stopSandbox():
    sand = Sandbox.Sandbox("")
    sand.halt()


@helpers.handleException()
def sandbox(
    initialize=False,
    port=20000,
    detach=True,
    num_of_accounts=10,
    minimum_balance=20_000,
    protocol=Sandbox.SandboxProtocols.hangzhou,
    list_accounts=False,
    stop=False,
):
    args = Namespace(
        initialize=initialize,
        port=port,
        detach=detach,
        num_of_accounts=num_of_accounts,
        minimum_balance=minimum_balance,
        protocol=protocol,
        list_accounts=list_accounts,
        stop=stop,
    )

    _sandbox = Sandbox.Sandbox(args)

    if args.initialize:
        return _sandbox.download()

    if args.stop:
        return _sandbox.halt()

    if not _sandbox.isRunning(args.port):
        _sandbox.initialize()
        _sandbox.run()

    return _sandbox


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
    Sandbox.Sandbox.listAccounts()


@helpers.handleException()
def install(compiler=Compilers, local=False, force=False):
    args = Namespace(compiler=compiler, local=local, force=force)
    chinstrap.chinstrapInstallCompilers(args, "")


@helpers.handleException()
def setUsing(shell="mainnet", key=None, mode=None, ipfs_gateway=None):
    """
    Change current rpc endpoint and account

    :param shell: one of 'mainnet', '***net', or RPC node uri, or \
instance of :class:`pytezos.rpc.shell.ShellQuery`
    :param key: base58 encoded key, path to the faucet file, faucet \
file itself, alias from tezos-client, or `Key`
    :param mode: whether to use `readable` or `optimized` encoding \
for parameters/storage/other
    :returns: A copy of current object with changes applied
    """
    return pytezos.using(shell=shell, key=key, mode=mode, ipfs_gateway=ipfs_gateway)


def launchRepl(args):
    global _config
    pretty.install()

    if args.network == "development":
        _sandbox = Sandbox.Sandbox(args)
        _sandbox.args.detach = True
        _sandbox.initialize()
        _sandbox.run()

    _config = config.Config(args.network, compileFlag=True)

    try:
        balance = _config.wallet.balance()
    except requests.exceptions.ConnectionError:
        helpers.fatal(
            f"Failed to connect to {_config.network.host}. Please configure the network!"
        )

    helpers.printFormatted(
        f"""Loaded wallet <ansiyellow><b>{_config.wallet.key.public_key_hash()}</b> \
    </ansiyellow>. Balance: <ansired>ꜩ</ansired> <ansigreen>\
<b>{balance}</b></ansigreen>\n"""
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
        "using": setUsing,
        "account": _config.wallet,
        "sandbox": sandbox,
        "SandboxProtocols": Sandbox.SandboxProtocols,
        "exit": cExit,
    }

    embed({}, functions, configure=repl.configure, history_filename=repl.historyPath)
