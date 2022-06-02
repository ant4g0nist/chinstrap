import os
import re
import glob
import halo
import pathlib
import requests
from chinstrap import helpers
from prompt_toolkit import HTML
from chinstrap.languages import TemplateOptions
from chinstrap.helpers.container import pullImage
from chinstrap.helpers.container import runLigoContainer


class Ligo:
    def __init__(self, args, config, _) -> None:
        self.config = config
        self.args = args
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
        os.makedirs("build/contracts/", exist_ok=True)
        for contract in contracts:
            self.compileOne(contract, self.entrypoint)
        return self.status

    def compileOne(self, contract, entrypoint="main"):
        path = pathlib.Path(contract)
        name = path.name
        spinner = halo.Halo(text=f"Compiling {name}", spinner="dots")
        spinner.start()

        success, msg = Ligo.runCompiler(
            contract,
            entrypoint,
            werror=self.args.werror,
            warnings=self.args.warning,
            local=self.args.local,
        )
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
        if local:
            helpers.ensureOSisNotDarwin()
            fullPath = os.path.expanduser("~/chinstrap/bin")
            create = True
            if os.path.exists(fullPath):
                if spin:
                    spin.stop()

                if not helpers.checkToCreateDir(fullPath, force):
                    create = False

            if create:
                os.makedirs(fullPath)

                spin = helpers.startSpinner("Installing Ligo")
                helpers.ensurePathExists(fullPath)
                commands = [
                    "curl --output /tmp/ligo https://gitlab.com/ligolang/\
ligo/-/jobs/2507456718/artifacts/raw/ligo",
                    "mv /tmp/ligo ~/chinstrap/bin/",
                    "chmod +x ~/chinstrap/bin/ligo",
                ]

                for cmd in commands:
                    proc = helpers.runCommand(cmd, shell=True)
                    proc.wait()

                spin.stop_and_persist("🎉", "Ligo installed")

            return

        else:
            suc, msg = pullImage("ligolang/ligo", "0.34.0")
            if not suc:
                spin.fail(f"Failed to install compiler. {msg}")
                return

            return spin

    @staticmethod
    def runCompiler(
        contract, entrypoint="main", werror=False, warnings=False, local=False
    ):
        name = pathlib.Path(contract).name

        output = ""
        options = ""

        if werror:
            options += " --werror "

        if not warnings:
            options += " --no-warn "

        options += f"--entry-point {entrypoint}"

        if local:
            ligo = helpers.checkIfLigoIsInstalled()
            command = f"{ligo} compile contract {contract} {options}"

            proc = helpers.runCommand(command, shell=True)
            proc.wait()

            output = proc.stdout.read().decode()
            error = proc.stderr.read().decode()

            if f'File "{name}"' in error:
                return False, error

            if error:
                return False, error

        else:
            command = f"compile contract {name} {options}"
            container = runLigoContainer(
                command,
                [contract],
                volumes={
                    f"{os.getcwd()}/contracts/": {"bind": "/contracts/", "mode": "ro"},
                    f"{os.getcwd()}/tests/": {"bind": "/tests/", "mode": "ro"},
                    f"{os.getcwd()}/build/contracts/": {
                        "bind": "/build/",
                        "mode": "rw",
                    },
                    f"{os.getcwd()}": {"bind": "/home/", "mode": "ro"},
                },
            )

            for line in container.logs(stream=True, stdout=True, stderr=True):
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
            suc, msg = self.runSingleLigoTest(test, local=self.args.local)
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

    def runSingleLigoTest(self, test, local=False):
        name = pathlib.Path(test).name
        command = f"run test /home/tests/{name}"

        if local:
            command = f"ligo run test {test}"

            proc = helpers.runCommand(command, shell=True)
            proc.wait()

            output = proc.stdout.read().decode()
            error = proc.stderr.read().decode()

            if "File " in error:
                return False, error

            if error:
                return False, error

        else:

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
        helpers.fatal("Not implemented yet")

    @staticmethod
    def compileStorage(contract, storage, output, entrypoint="main", werror=False):
        name = pathlib.Path(contract).name
        command = f"compile storage {name} '{storage}' -o /contracts/{output} "

        if werror:
            command += "--werror "

        command += f"--entry-point {entrypoint}"
        container = runLigoContainer(
            command,
            [contract],
            volumes={
                f"{ os.getcwd()}/contracts/": {"bind": "/contracts/", "mode": "rw"},
                f"{os.getcwd()}/tests/": {"bind": "/tests/", "mode": "ro"},
                f"{os.getcwd()}/build/contracts/": {
                    "bind": "/build/",
                    "mode": "rw",
                },
                f"{os.getcwd()}": {"bind": "/home/", "mode": "ro"},
            },
        )

        output = ""

        for line in container.logs(stream=True):
            output += line.decode("utf-8")

        error = f'File "{name}"'
        if error in output[: len(error)]:
            return False, output

        return True, output


class LigoLangTemplates:
    server = "https://ide.ligolang.org"

    def __init__(self) -> None:
        pass

    @staticmethod
    def getExtension(language):
        if language == TemplateOptions.jsligo:
            return "jsligo"

        elif language == TemplateOptions.religo:
            return "religo"

        elif language == TemplateOptions.cameligo:
            return "mligo"

        elif language == TemplateOptions.pascaligo:
            return "ligo"

    @staticmethod
    def listAvailableTemplates(language):
        url = f"{LigoLangTemplates.server}/static/examples/list"
        req = requests.get(url)
        options = {}
        for i in req.json():
            if f"({language})" in i["name"]:
                options[i["name"]] = i["id"]
        return options

    @staticmethod
    def templates(language):
        contracts = LigoLangTemplates.listAvailableTemplates(language)
        prom = helpers.SelectionPrompt(sideBySide=False)
        templateType = prom.prompt(
            HTML("<ansired>Available categories:</ansired>"), options=contracts.keys()
        )

        templateId = contracts[templateType]
        LigoLangTemplates.fetchContract(templateId, language)

    @staticmethod
    def fetchContract(templateId, language):
        url = f"https://ide.ligolang.org/static/examples/{templateId}"

        req = requests.get(url)
        resp = req.json()

        code = resp["editor"]["code"]
        extension = LigoLangTemplates.getExtension(language)
        deployScript = resp["generateDeployScript"]
        storage = deployScript["storage"]

        name = resp["name"]
        name = re.sub("[^a-zA-Z0-9\n]", "_", name)

        contract_file = f"contracts/{name}.{extension}"
        storage_file = f"contracts/{name}.{extension}.storage"

        with open(contract_file, "w") as f:
            f.write(code)

        with open(storage_file, "w") as f:
            if type(storage) == int:
                storage = f"{storage}"
            f.write(storage)

        print(f"File saved to {helpers.GRN}{contract_file}{helpers.RST}!\n")
