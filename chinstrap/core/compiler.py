from enum import Enum
from chinstrap.core import ligo
from chinstrap.core import smartpy
from chinstrap.Helpers import startSpinner
from chinstrap.Helpers import ensureCurrentDirectoryIsChinstrapProject


class Compiler:
    def __init__(self, args, config, chinstrapPath) -> None:
        ensureCurrentDirectoryIsChinstrapProject()

        if config.compiler.lang == "smartpy":
            self.compile = smartpy.SmartPy(args, config, chinstrapPath)

        elif "ligo" in config.compiler.lang:
            self.compile = ligo.Ligo(args, config, chinstrapPath)

    def compileSources(self):
        return self.compile.compileSources()

    def compileOne(self, contract):
        return self.compile.compileOne(contract)


class Compilers(Enum):
    all = "all"
    smartpy = "smartpy"
    ligo = "ligo"

    def __str__(self):
        return self.value


def installSmartPyCompiler(local: bool, force: bool):
    spin = startSpinner("Installing SmartPy")
    spin = smartpy.SmartPy.installCompiler(local, force, spin)
    if spin:
        spin.stop_and_persist("🎉", "SmartPy installed")


def installLigoCompiler(local: bool, force: bool):
    spin = startSpinner("Installing Ligo")
    # Currently ligo is compiled only for Linux
    # and is available as docker for mac.
    # For consistency, we just use docker for linux and mac
    spin = ligo.Ligo.installCompiler(local, force, spin)
    if spin:
        spin.stop_and_persist("🎉", "Ligo installed")


def installCompiler(compiler: Compilers, local: bool, force: bool):

    if compiler == Compilers.all:
        installLigoCompiler(local, force)
        installSmartPyCompiler(local, force)

    elif compiler == Compilers.smartpy:
        installSmartPyCompiler(local, force)

    elif compiler == Compilers.ligo:
        installLigoCompiler(local, force)
