import os
from chinstrap import helpers


class InitChinstrap:
    def __init__(self, chinstrapPath, name, path, force) -> None:
        self.name = name
        self.path = path
        self.chinstrapPath = chinstrapPath

        if not helpers.isChinstrapProject(path):
            with open(f"{path}/.chinstrap", "a"):
                os.utime(f"{path}/.chinstrap", None)

        if helpers.checkToCreateDir(f"{path}/contracts", force):
            self.initContracts()

        if helpers.checkToCreateDir(f"{path}/originations", force):
            self.initOriginations()

        if helpers.checkToCreateDir(f"{path}/tests", force):
            self.initTests()

        if helpers.checkToCreateFile(f"{path}/chinstrap-config.yml", force):
            self.initConfig()

        helpers.success("Done. Happy coding 🐧")

    def initContracts(self):
        helpers.mkdir(f"{self.path}/contracts")
        helpers.copyFile(
            f"{self.chinstrapPath}/core/sources/contracts/SampleContract.py",
            f"{self.path}/contracts/SampleContract.py",
        )

    def initOriginations(self):
        """
        create origination scripts
        """
        helpers.mkdir(f"{self.path}/originations")
        helpers.copyFile(
            f"{self.chinstrapPath}/core/sources/originations/1_samplecontract_origination.py",
            f"{self.path}/originations/1_samplecontract_origination.py",
        )

    def initTests(self):
        """
        create pytezos test scripts
        """
        helpers.mkdir(f"{self.path}/tests")
        helpers.copyFile(
            f"{self.chinstrapPath}/core/sources/tests/samplecontractPytest.py",
            f"{self.path}/tests/samplecontractPytest.py",
        )
        helpers.copyFile(
            f"{self.chinstrapPath}/core/sources/tests/sampleContractSmartPy.py",
            f"{self.path}/tests/sampleContractSmartPy.py",
        )

    def initConfig(self):
        helpers.copyFile(
            f"{self.chinstrapPath}/core/sources/chinstrap-config.yml",
            f"{self.path}/chinstrap-config.yml",
        )
