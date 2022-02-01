import os
import rich
import logging
import argparse
import requests
from rich import pretty
from pathlib import Path
from chinstrap import Helpers
from chinstrap.core.tests import Tests
from chinstrap.core.config import Config
from chinstrap.core.create import Create
from chinstrap.core.repl import launchRepl
from chinstrap.core.sandbox import Sandbox
from chinstrap.core.smartpy import SmartPy
from chinstrap.core.compiler import Compiler
from chinstrap.core.compiler import Compilers
from chinstrap.core.create import CreateOptions
from chinstrap.core.sandbox import SandboxProtocols
from chinstrap.core.initialize import InitChinstrap
from chinstrap.core.compiler import installCompiler

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
            Helpers.printFormatted(msg)


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
    SmartPy.templates()


def chinstrapSandboxHandler(args, _):
    sandbox = Sandbox(args)
    if args.initialize:
        return sandbox.download()

    if args.stop:
        return sandbox.halt()

    sandbox.run()


def chinstrapDevelopmentRepl(args, env):
    sandbox = Sandbox(args)
    sandbox.run(detach=True)
    launchRepl()


def main(args, env=os.environ):

    pretty.install()
    Helpers.welcome_banner()
    parser = argparse.ArgumentParser(
        description=rich.print(
            "[bold green]Chinstrap - a cute framework for \
developing Tezos Smart Contracts[/bold green]!",
            ":penguin:",
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
        "templates", help="Download templates provided by SmartPy"
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
        "-o", "--port", default=20000, help="Tezos local sandbox's RPC Port"
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
    parser_i.set_defaults(func=chinstrapSandboxHandler)

    parser_j = subparsers.add_parser(
        "develop", help="Open a console with a local Flextesa development environment"
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
    parser_j.set_defaults(func=chinstrapDevelopmentRepl)

    if not args[1:]:
        parser.print_help()
        exit(1)

    args = parser.parse_args(args[1:])
    return args.func(args, env)
