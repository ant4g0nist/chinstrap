import os
from chinstrap import Helpers

class InitChinstrap:
    def __init__(self, chinstrapPath, name, path, force) -> None:
        self.name = name 
        self.path = path
        self.chinstrapPath = chinstrapPath

        Helpers.debug('Setting up Chinstrap project...')

        if not Helpers.isChinstrapProject(path):
            with open(f"{path}/.chinstrap", 'a'):
                os.utime(f"{path}/.chinstrap", None)
                
        if Helpers.checkToCreateDir(f"{path}/contracts", force):
            self.initContracts()
        
        if Helpers.checkToCreateDir(f"{path}/originations", force):
            self.initOriginations()

        if Helpers.checkToCreateDir(f"{path}/tests", force):
            self.initTests()

        if Helpers.checkToCreateFile(f"{path}/chinstrap-config.yml", force):
            self.initConfig()

        Helpers.success('Done. Happy coding :)')

    def initContracts(self):
        Helpers.mkdir(f'{self.path}/contracts')
        Helpers.copyFile(f'{self.chinstrapPath}/core/sources/contracts/Originations.py', f'{self.path}/contracts/Originations.py')
        Helpers.copyFile(f'{self.chinstrapPath}/core/sources/contracts/SampleContract.py',f'{self.path}/contracts/SampleContract.py')

    def initOriginations(self):
        ''' 
            create origination scripts
        '''
        Helpers.mkdir(f'{self.path}/originations')
        Helpers.copyFile(f'{self.chinstrapPath}/core/sources/originations/1_initial_originations.py', f'{self.path}/originations/1_initial_originations.py')
        Helpers.copyFile(f'{self.chinstrapPath}/core/sources/originations/2_samplecontract_origination.py',f'{self.path}/originations/2_samplecontract_origination.py')

    def initTests(self):
        '''
            create pytezos test scripts
        '''
        Helpers.mkdir(f'{self.path}/tests')
        Helpers.copyFile(f'{self.chinstrapPath}/core/sources/tests/samplecontractPytest.py',f'{self.path}/tests/samplecontractPytest.py')
        Helpers.copyFile(f'{self.chinstrapPath}/core/sources/tests/sampleContractSmartPy.py',f'{self.path}/tests/sampleContractSmartPy.py')

    def initConfig(self):
        Helpers.copyFile(f'{self.chinstrapPath}/core/sources/chinstrap-config.yml',f"{self.path}/chinstrap-config.yml")

