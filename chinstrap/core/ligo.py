import os
import glob
import halo
import pathlib
from chinstrap import Helpers
from chinstrap.core.container import pullImage
from chinstrap.core.container import runLigoContainer


class Ligo:
    def __init__(self, args, config, _) -> None:
        self.config = config
        self.entrypoint = args.entrypoint

        if self.config.compiler.lang == "jsligo":
            self.ext = "jsligo"

        elif self.config.compiler.lang == "reasonligo":
            self.ext = "religo"

        elif self.config.compiler.lang == "cameligo":
            self.ext = "mligo"

        elif self.config.compiler.lang == "pascaligo":
            self.ext = "ligo"

        self.status = 0

    def compileSources(self):
        contracts = glob.iglob(f"contracts/*.{self.ext}")
        for contract in contracts:
            self.compileOne(contract, self.entrypoint)
        return self.status

    def compileOne(self, contract, entrypoint="main"):
        path = pathlib.Path(contract)
        name = path.name
        spinner = halo.Halo(text=f"Compiling {name}", spinner="dots")
        spinner.start()
        success, msg = self.runCompiler(contract, entrypoint)
        if not success:
            self.status = 1
            spinner.fail(text=f"Compilation of {str(name)} Failed!")
            print("\nReason:")
            print(msg)
            return 1
        else:
            spinner.succeed(text=f"{name} compilation successful!")

        os.makedirs(f"build/contracts/{path.stem}", exist_ok=True)
        with open(f"build/contracts/{path.stem}/step_000_cont_0_contract.tz", "w") as f:
            f.write(msg)

        return 0

    @staticmethod
    def installCompiler(local=False, force=False, spin=None):
        suc, msg = pullImage("ligolang/ligo", "0.34.0")
        if not suc:
            spin.fail(f"Failed to install compiler. {msg}")
            return
        return spin

    def runCompiler(self, contract, entrypoint="main"):
        name = pathlib.Path(contract).name
        command = f"compile contract {name} --entry-point {entrypoint}"
        container = runLigoContainer(command, [contract])
        output = ""

        for line in container.logs(stream=True):
            output += line.decode("utf-8")

        error = f'File "{name}"'
        if error in output[: len(error)]:
            return False, output

        return True, output

    def runAllTests(self):
        if (
            self.config.compiler.test == "smartpy"
            or self.config.compiler.test == "pytest"
        ):
            tests = glob.iglob("./tests/*.py")

        elif "ligo" in self.config.compiler.test:
            tests = glob.iglob(f"./tests/*.test.{self.ext}")

        for test in tests:
            if self.runSingleTest(test):
                self.status = 1

        return self.status

    def runSingleTest(self, test):
        name = pathlib.Path(test).name
        spinner = halo.Halo(text=f"Running {name} test", spinner="dots")
        spinner.start()

        if "ligo" in self.config.compiler.test:
            suc, msg = self.runSingleLigoTest(test)
            if not suc:
                spinner.fail(text=f"Test {str(name)} Failed!\n{msg}")
                return 1

            spinner.succeed(text=msg)
            return 0

        else:
            spinner.fail(
                f"{self.config.compiler.test} tests not supported for Contracts made in Ligo"
            )
            return 1

    def runSingleLigoTest(self, test):
        name = pathlib.Path(test).name
        command = f"run test /home/tests/{name}"

        container = runLigoContainer(
            command, [test], volumes={os.getcwd(): {"bind": "/home/", "mode": "ro"}}
        )
        output = ""

        for line in container.logs(stream=True):
            output += line.decode("utf-8")

        error = "File "
        if error in output[: len(error)]:
            return False, output

        return True, output

    def dryRuns(self):
        Helpers.fatal("Not implemented yet")
