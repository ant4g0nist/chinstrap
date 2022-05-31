import os
import rich
import logging
import argparse
import requests
from rich import pretty
from pathlib import Path
from chinstrap import helpers
from chinstrap.tests import Tests
from chinstrap.repl import launchRepl
from chinstrap.sandbox import Sandbox
from chinstrap.compiler import Compiler
from chinstrap.compiler import Compilers
from chinstrap.core.config import Config
from chinstrap.core.create import Create
from chinstrap.compiler import installCompiler
from chinstrap.languages import TemplateOptions
from chinstrap.sandbox import SandboxProtocols
from chinstrap.originations import Originations
from chinstrap.core.create import CreateOptions
from chinstrap.languages.smartpy import SmartPy
from chinstrap.core.initialize import InitChinstrap
from chinstrap.languages.ligo import LigoLangTemplates
from chinstrap.originations import ChinstrapOriginationState

logging.getLogger().setLevel(logging.CRITICAL)


def chinstrapInitialize(args, env):
    chinstrapPath = os.path.dirname(os.path.abspath(__file__))

    targetPath = Path(f"{os.getcwd()}")
    InitChinstrap(chinstrapPath, targetPath.name, targetPath, args.force)


def chinstrapConfigVerification(args, _):
    Config(args.network)


def listCurrentlyAvailableTestnets(args, _):
    url = "https://teztnets.xyz/teztnets.json"
    res = requests.request(
        url=url,
        method="GET",
        headers={"content-type": "application/json", "user-agent": "chinstrap"},
    )
    if res.status_code == 200:
        for network, value in res.json().items():
            msg = f"<b>{network:30s}</b> : <u>{value['network_url']}</u>"
            helpers.printFormatted(msg)


def chinstrapCompileContracts(args, _):
    chinstrapPath = os.path.dirname(os.path.abspath(__file__))
    config = Config(compileFlag=True)
    compiler = Compiler(args, config, chinstrapPath)
    if args.contract:
        return compiler.compileOne(args.contract)

    return compiler.compileSources()


def chinstrapRunTests(args, _):
    chinstrapPath = os.path.dirname(os.path.abspath(__file__))
    config = Config(compileFlag=True)
    tester = Tests(args, config, chinstrapPath)
    if args.test:
        return tester.runTest(args.test)

    return tester.runAllTests()


def chinstrapInstallCompilers(args, _):
    installCompiler(args.compiler, args.local, args.force)


def chinstrapCreate(args, _):
    config = Config(compileFlag=True)
    Create(args, config)


def chinstrapTemplates(args, _):
    if args.language == TemplateOptions.smartpy:
        SmartPy.templates()

    else:
        LigoLangTemplates.templates(args.language)


def chinstrapSandboxHandler(args, _):
    if args.list_accounts:
        return Sandbox.listAccounts()

    # if args.running:
    #     Sandbox.isRunning()
    #     return

    sandbox = Sandbox(args)
    if args.initialize:
        return sandbox.download()

    if args.stop:
        return sandbox.halt()

    sandbox.initialize()
    sandbox.run()


def chinstrapRunOriginations(args, env):

    if args.show:
        state = ChinstrapOriginationState(False)
        state.showOriginations(args.network)
        return

    config = Config(network=args.network, compileFlag=False)
    originations = Originations(config, args)

    # load state
    originations.loadOriginationState()

    # get all available originations
    if args.originate and args.contract:
        # compile
        chinstrapCompileContracts(args, env)
        originations.getOrigination(args.originate)
    elif args.originate and not args.contract:
        helpers.fatal(
            "Please provide both --originate(-o) and \
--contract(-c) args to originate a specific contract"
        )
    else:
        chinstrapCompileContracts(args, env)
        originations.getOriginations()

    originations.originateAll()
    originations.showCosts()


def chinstrapDevelopmentRepl(args, env):
    launchRepl(args)


def chinstrapAccount(args, env):
    # if args.balance:
    #     core.checkAccountBalance(args.account, args.network)
    helpers.fatal("TODO")


def main(args, env=os.environ):

    pretty.install()
    helpers.welcome_banner()
    parser = argparse.ArgumentParser(
        description=rich.print(
            ":penguin:",
            "[bold green]Chinstrap - a cute framework for \
developing Tezos Smart Contracts[/bold green]!",
        )
    )
    subparsers = parser.add_subparsers()

    parser_a = subparsers.add_parser("init", help="Initialize a new Chinstrap project")
    parser_a.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        help="Force initialize Chinstrap project in the current directory. \
Be careful, this will potentioally overwrite files that exist in the directory.",
    )
    parser_a.set_defaults(func=chinstrapInitialize)

    parser_b = subparsers.add_parser("config", help="Verify Chinstrap configuration")
    parser_b.add_argument(
        "-n", "--network", default="development", help="Select the configured network"
    )
    parser_b.set_defaults(func=chinstrapConfigVerification)

    parser_c = subparsers.add_parser(
        "networks", help="List currently available test networks"
    )
    parser_c.set_defaults(func=listCurrentlyAvailableTestnets)

    parser_d = subparsers.add_parser("compile", help="Compile contract source files")
    parser_d.add_argument(
        "-c",
        "--contract",
        help="Contract to compile. If not specified, all the contracts are compiled",
    )
    parser_d.add_argument(
        "-l",
        "--local",
        default=False,
        action="store_true",
        help="Use compiler from host machine. If not specified, Docker image is used",
    )
    parser_d.add_argument(
        "-r",
        "--werror",
        default=False,
        action="store_true",
        help="Treat Ligo compiler warnings as errors",
    )
    parser_d.add_argument(
        "-w",
        "--warning",
        default=False,
        action="store_true",
        help="Display Ligo compiler warnings",
    )
    parser_d.add_argument(
        "-e",
        "--entrypoint",
        default="main",
        type=str,
        help="Entrypoint to use when compiling Ligo contracts. Default entrypoint is main",
    )
    parser_d.set_defaults(func=chinstrapCompileContracts)

    parser_e = subparsers.add_parser("install", help="Helper to install compilers")
    parser_e.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        help="Force update compilers",
    )
    parser_e.add_argument(
        "-l",
        "--local",
        default=False,
        action="store_true",
        help="Install on local machine. If not specified, Docker is used",
    )
    parser_e.add_argument(
        "-c",
        "--compiler",
        type=Compilers,
        default=Compilers.all,
        choices=list(Compilers),
        help="Installs selected compilers",
    )
    parser_e.set_defaults(func=chinstrapInstallCompilers)

    parser_f = subparsers.add_parser(
        "create", help="Helper to create new contracts, originations and tests"
    )
    parser_f.add_argument(
        "-t",
        "--type",
        type=CreateOptions,
        choices=list(CreateOptions),
        required=True,
        help="The type of the item to create",
    )
    parser_f.add_argument(
        "-n", "--name", required=True, help="The name of the item to create"
    )
    parser_f.set_defaults(func=chinstrapCreate)

    parser_g = subparsers.add_parser(
        "templates", help="Download templates provided by SmartPy and *LIGO"
    )
    parser_g.add_argument(
        "-l",
        "--language",
        type=TemplateOptions,
        choices=list(TemplateOptions),
        required=True,
        help="The type of the item to create",
    )
    parser_g.set_defaults(func=chinstrapTemplates)

    parser_h = subparsers.add_parser("test", help="Run pytest/smartpy/ligo tests")
    parser_h.add_argument(
        "-t", "--test", help="Test to run. If not specified, all the tests are executed"
    )
    parser_h.add_argument(
        "-l",
        "--local",
        default=False,
        action="store_true",
        help="Run tests on host machine. If not specified, Docker image is preferred",
    )
    parser_h.add_argument(
        "-e",
        "--entrypoint",
        default="main",
        type=str,
        help="Entrypoint to use when compiling Ligo contracts. Default entrypoint is main",
    )
    parser_h.set_defaults(func=chinstrapRunTests)

    parser_i = subparsers.add_parser("sandbox", help="Start a Tezos local sandbox")
    parser_i.add_argument(
        "-o",
        "--port",
        default=20000,
        help="RPC Port of Tezos local sandbox",
    )
    parser_i.add_argument(
        "-i",
        "--initialize",
        default=False,
        action="store_true",
        help="Initialize Tezos sandbox",
    )
    parser_i.add_argument(
        "-d",
        "--detach",
        default=False,
        action="store_true",
        help="Start the Tezos sandbox and detach",
    )
    parser_i.add_argument(
        "-s",
        "--stop",
        default=False,
        action="store_true",
        help="Stop the currently running Tezos sandbox",
    )
    parser_i.add_argument(
        "-c",
        "--num-of-accounts",
        default=10,
        type=int,
        help="Number of accounts to bootstrap on Tezos sandbox",
    )
    parser_i.add_argument(
        "-m",
        "--minimum-balance",
        default=20_000,
        type=int,
        help="Amount of Tezos to deposit while bootstraping on Tezos local sandbox",
    )
    parser_i.add_argument(
        "-p",
        "--protocol",
        type=SandboxProtocols,
        default=SandboxProtocols.hangzhou,
        choices=list(SandboxProtocols),
        help="Protocol to start Tezos sandbox with.",
    )
    parser_i.add_argument(
        "-l",
        "--list-accounts",
        default=False,
        action="store_true",
        help="List local accounts from sandbox",
    )
    # parser_i.add_argument(
    #     "-r",
    #     "--running",
    #     default=False,
    #     action="store_true",
    #     help="Stop the currently running Tezos sandbox",
    # )
    parser_i.set_defaults(func=chinstrapSandboxHandler)

    parser_j = subparsers.add_parser(
        "develop", help="Open an interactive console for Tezos"
    )
    parser_j.add_argument(
        "-o", "--port", default=20000, help="Tezos local sandbox's RPC Port"
    )
    parser_j.add_argument(
        "-i",
        "--initialize",
        default=False,
        action="store_true",
        help="Initialize Tezos sandbox",
    )
    parser_j.add_argument(
        "-s",
        "--stop",
        default=False,
        action="store_true",
        help="Stop the currently running Tezos sandbox",
    )
    parser_j.add_argument(
        "-c",
        "--num-of-accounts",
        default=10,
        type=int,
        help="Number of accounts to bootstrap on Tezos sandbox",
    )
    parser_j.add_argument(
        "-m",
        "--minimum-balance",
        default=20_000,
        type=int,
        help="Amount of Tezos to deposit while bootstraping on Tezos local sandbox",
    )
    parser_j.add_argument(
        "-p",
        "--protocol",
        type=SandboxProtocols,
        default=SandboxProtocols.hangzhou,
        choices=list(SandboxProtocols),
        help="Protocol to start Tezos sandbox with.",
    )
    parser_j.add_argument(
        "-n",
        "--network",
        default="development",
        help="Select the configured network",
    )
    parser_j.set_defaults(func=chinstrapDevelopmentRepl)

    parser_k = subparsers.add_parser(
        "originate", help="Run originations and deploy contracts"
    )
    parser_k.add_argument(
        "-o",
        "--originate",
        help="Origination script to execute. If not specified, \
all the originations will be executed",
    )
    parser_k.add_argument(
        "-d",
        "--number",
        help="Run contracts from a specific migration. The number \
refers to the prefix of the migration file.",
    )
    parser_k.add_argument(
        "-n",
        "--network",
        default="development",
        help="Select the configured network",
    )
    parser_k.add_argument(
        "-p",
        "--port",
        default=20000,
        help="RPC Port of Tezos local sandbox",
    )
    parser_k.add_argument(
        "-r",
        "--reset",
        default=False,
        action="store_true",
        help="Run all originations from the beginning, instead of running \
from the last completed migration",
    )
    parser_k.add_argument(
        "-c",
        "--contract",
        help="Contract to compile. If not specified, all the contracts are compiled",
    )
    parser_k.add_argument(
        "-l",
        "--local",
        default=False,
        action="store_true",
        help="Use compiler from host machine. If not specified, Docker image is used",
    )
    parser_k.add_argument(
        "-s",
        "--show",
        default=False,
        action="store_true",
        help="Show addresses of originations",
    )
    parser_k.add_argument(
        "-e",
        "--entrypoint",
        default="main",
        type=str,
        help="Entrypoint to use when compiling Ligo contracts. Default entrypoint is main",
    )
    parser_k.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        help="Force originate all originations. \
Be careful, this will re-originate all the contracts even if they are already deployed.",
    )
    parser_k.add_argument(
        "-t",
        "--werror",
        default=False,
        action="store_true",
        help="Treat Ligo compiler warnings as errors",
    )
    parser_k.add_argument(
        "-w",
        "--warning",
        default=False,
        action="store_true",
        help="Display Ligo compiler warnings",
    )
    parser_k.set_defaults(func=chinstrapRunOriginations)

    parser_m = subparsers.add_parser("account", help="Tezos account")
    parser_m.add_argument(
        "-b",
        "--balance",
        default=False,
        action="store_true",
        help="check given account balance",
    )
    parser_m.add_argument("-a", "--account", help="tz/KT address")
    parser_m.add_argument(
        "-n",
        "--network",
        default="development",
        help="Select the configured network",
    )

    parser_m.set_defaults(func=chinstrapAccount)

    if not args[1:]:
        parser.print_help()
        exit(1)

    args = parser.parse_args(args[1:])
    return args.func(args, env)
