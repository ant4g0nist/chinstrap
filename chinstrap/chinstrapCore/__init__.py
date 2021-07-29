import os
import io
import sys
import glob
import time
import json
import pytest
import docker
import pytezos
import logging
import subprocess
from halo import Halo
from pathlib import Path
from prompt_toolkit import HTML
from pytezos import ContractInterface
from chinstrap.chinstrapCore import Helpers
from pytezos.cli.cli import cli as pytezosCli
from prompt_toolkit.shortcuts.prompt import prompt
from prompt_toolkit.shortcuts.utils import print_formatted_text

logging.getLogger().setLevel(logging.ERROR)
# curdir = Path(__file__).parent.absolute()
# sys.path.append(f"{curdir}/smartpyCli")

currentContractName = None
def getContract(contractName):
	global currentContractName
	currentContractName = contractName
	return ContractInterface.from_file(f"build/contracts/{contractName}/step_000_cont_0_contract.tz")

class InitChinstrap:
	def __init__(self, chinstrapPath) -> None:
		self.chinstrapPath = chinstrapPath
		
		Helpers.debug('Setting up Chinstrap - Tezos project...')

		if self.checkToCreateDir("./contracts"):
			self.initContracts()

		if self.checkToCreateDir("./originations"):
			self.initOriginations()

		if self.checkToCreateDir("./tests"):
			self.initTests()

		self.initChinstrapConfigFile()

	def initContracts(self):
		''' 
			create contracts
		''' 
		Helpers.mkdir('contracts')
		
		Helpers.copyFile(f'{self.chinstrapPath}/resources/chinstraps/contracts/Originations.py','contracts/Originations.py')
		Helpers.copyFile(f'{self.chinstrapPath}/resources/chinstraps/contracts/SampleContract.py','contracts/SampleContract.py')

	def initOriginations(self):
		''' 
			create origination scripts
		'''
		Helpers.mkdir('originations')
		Helpers.copyFile(f'{self.chinstrapPath}/resources/chinstraps/originations/1_initial_originations.py', 'originations/1_initial_originations.py')
		Helpers.copyFile(f'{self.chinstrapPath}/resources/chinstraps/originations/2_samplecontract_origination.py','originations/2_samplecontract_origination.py')

	def initTests(self):
		'''
			create pytezos test scripts
		'''
		Helpers.mkdir('tests')
		Helpers.copyFile(f'{self.chinstrapPath}/resources/chinstraps/tests/samplecontractPytest.py','tests/samplecontractPytest.py')
		Helpers.copyFile(f'{self.chinstrapPath}/resources/chinstraps/tests/sampleContractSmartPy.py','tests/sampleContractSmartPy.py')

	def checkToCreateDir(self, dir):
		if os.path.exists(dir):
			if Helpers.promptOverwrite(dir):
				Helpers.rmdir(dir)
			else:
				return False

		return True

	def initChinstrapConfigFile(self):
		'''
			Create Chinstrap Config file
		'''
		config = """
chinstrap:
 networks:
  development:
   host: "http://localhost"
   port: 20000
   accounts:
      - privateKeyFile: "./.priv.tz"
 
  florencenet:
   host: "https://florencenet.smartpy.io"
   port: 443
   accounts:
      - privateKeyFile: "./.priv.tz"

  mainnet:
   host: "https://mainnet.smartpy.io"
   port: 443

  zeronet:
   host: "https://zeronet.smartpy.io"
   port: 443

 compiler:
  lang: smartpy
"""
		if self.checkToCreateDir("./chinstrap_config.yaml"):
			with open('./chinstrap_config.yaml', 'w') as f:
				f.write(config)

class Create:
	def __init__(self) -> None:
		Helpers.debug('Creating a new file...')
		prom = Helpers.SelectionPrompt()
		choice = prom.prompt(HTML('Please select type of file:'), options=['contract', 'origination', 'test'])
		filename   = prompt(HTML(f'<b>{choice}</b> name: '))
		
		if choice=='contract':
			self.createContract(filename)

		elif choice=='origination':
			self.createOrigination(filename)

		elif choice=='test':
			self.createTest(filename)

	def createContract(self, filename):
		'''
			Create a barebone contract
		'''
		bones = """
import smartpy as sp

class SampleContract(sp.Contract):
	def __init__(self, value):
		self.init_type(sp.TRecord(counter = sp.TInt))
		self.init(counter = value)

	@sp.entry_point
	def increment(self, value):
		self.data.counter += value
"""
		contractName = ''.join(x for x in filename.title() if x.isalpha())
		bones = bones.replace('SampleContract', contractName)
		with open(f'./contracts/{contractName}.py' ,'w') as f:
			f.write(bones)

	def createOrigination(self, filename):
		'''
			Create a barebone contract
		'''
		bones="""from chinstrap.chinstrapCore import getContract

def deploy(chinstrapState, network, accounts):
	contract = getContract("ContractName")
	initial_storage = contract.storage.encode(0)
	return initial_storage, contract"""

		origination = ''.join(x for x in filename.title() if x.isalpha())
		with open(f'./originations/{origination}.py' ,'w') as f:
			f.write(bones)

	def createTest(self, filename):
		'''
			Create a barebone contract
		'''
		bones="""
from unittest import TestCase, skip
from pytezos import MichelsonRuntimeError, ContractInterface
michelson_contract = "./build/contracts/Contract/Contract.tz"

class TestCounterContract(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.counterContract = ContractInterface.from_file(michelson_contract)

	def test_storage_counter_is_zero(self):
		self.assertEqual(result.storage["counter"], 0)
		"""
		with open(f'./tests/{filename}.py' ,'w') as f:
			f.write(bones)

class Compile:
	def __init__(self, chinstrapConfig, chinstrapPath) -> None:
		self.config = chinstrapConfig
		self.chinstrapPath 	= chinstrapPath
		self.cwd = os.getcwd()
		contracts = glob.iglob("contracts/*.py")

		self.initBuildFolder()
		# self.updateCompiler()
		
		for contract in contracts:
			self.compile(contract)

		print()

	def initBuildFolder(self):
		Helpers.mkdir("./build")
		Helpers.mkdir("./build/contracts/")

	def updateCompiler(self):
		'''
			get the smartpy container for pytezos
		'''
		try:
			if self.config.compiler.lang.lower()=='smartpy':
				self.runPytezosCliCommand(['update-smartpy'])

		except docker.errors.DockerException as e:
			Helpers.fatal("\nPlease make sure Docker is running!")

	def compile(self, contract):
		"""
			Compile a given contract
		"""
		spinner = Halo(text=f'Compiling {contract}', spinner='dots')
		spinner.start()
		
		command = [f"{self.chinstrapPath}/chinstrapCore/smartpyCli/SmartPy.sh", "compile", str(contract), f'{self.cwd}/build/contracts/']
		if not self.runSubprocess(command):
			spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"Compilation Failed!")
			return

		sys.path.append('./contracts/')
		name = os.path.splitext(os.path.basename(contract))[0]

		spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"{name} compilation successful!")

	def runSubprocess(self, command):
		"""
			Compile with local SmartPy-cli
		"""
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		while True:
			line = proc.stdout.readline()
			if not line:
				break

			if b'[error]' in line:
				return False


		return True

	def runPytezosCliCommand(self, cmd=[]):
		"""
			support for compiling with docker
		"""
		try:
			pytezosCli(cmd, standalone_mode=False)
		except docker.errors.DockerException as e:
			Helpers.fatal("\nPlease make sure Docker is running!")

class RunTests:
	def __init__(self, chinstrapPath, _pytest=None) -> None:
		sys.path.append('./tests')
		self.cwd = os.getcwd()
		self.chinstrapPath = chinstrapPath
		tests = glob.iglob("./tests/*.py")
		passedTests = []
		failedTests = []

		for file in tests:
			msg = HTML(f'Running tests on <ansigreen>{file}</ansigreen>')
			if _pytest:
				stdoutOrig = sys.stdout
				stdoutTemp = io.StringIO()
				sys.stdout = stdoutTemp
				
				res = pytest.main(['--co','-x', '-q' , f'{file}'])
				sys.stdout = stdoutOrig
				if "no tests collected" in stdoutTemp.getvalue():
					pass

				else:
					print_formatted_text(msg)
					pytest.main(["--no-header", f'{file}'])

			else:
				print_formatted_text(msg)
				command = [f"{self.chinstrapPath}/chinstrapCore/smartpyCli/SmartPy.sh", "test", str(file), f'{self.cwd}/build/tests/']
				passed = self.runSubprocess(command)
				if passed:
					passedTests.append(file)			
				else:
					failedTests.append(file)

		print()

		if not _pytest:
			for file in passedTests:
				msg = HTML(f'<ansigreen>[P]</ansigreen> Tests passed on <ansigreen>{file}</ansigreen>')
				print_formatted_text(msg)		
			
			for file in failedTests:
				msg = HTML(f'<ansired>[F]</ansired> Tests failed for <ansired>{file}</ansired>')
				print_formatted_text(msg)					
		print()

	def runSubprocess(self, command):
		"""
			Compile with local SmartPy-cli
		"""
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		result = True
		printLine = False

		while True:
			line = proc.stdout.readline().decode().strip("\n")

			if not line:
				break
			
			if '[error]' in line and not 'Target "test" not found' in line:
				printLine = True
				result = False

			if printLine:
				print(line)
			
		return result

class Origination:
	def __init__(self, config, reset=False, compile=False) -> None:
		self.config = config
		self.originations = None

		self.pytezoscli = pytezos.pytezos.using(key=self.config.key, shell=f"{self.config.network.host}:{self.config.network.port}")
		
		# compile all contracts before origination
		if compile:
			Compile(config)

		# get previous migrations state if any!
		self.chinstrapState = ChinstrapState(reset)

		contracts = sorted(glob.glob("./originations/*.py"), key=lambda x: int(os.path.basename(x).split('_')[0]) if os.path.basename(x).split('_')[0].isdigit() else 0)
		
		if not reset:
			self.checkIfNetworkUpToDate(contracts[-1], config.network.name)

		self.totalCost = 0
		self.initialWalletBalance = self.config.wallet.balance()

		sys.path.append('originations')

		for contract in contracts:
			filename = os.path.basename(contract)
			# ignore files that don't start with a number
			if filename.split("_")[0].isdigit() and not self.isAlreadyDeployed(int(filename.split("_")[0])):
				self.orignate(os.path.splitext(filename)[0])
				self.incrementOrigination()
				self.displayCostUpdate()

		msg = HTML(f'<ansired>ꜩ</ansired> Total Cost of originations: <ansigreen>{self.totalCost}</ansigreen> <ansired>ꜩ</ansired>')
		print_formatted_text(msg)
		print()

	def displayCostUpdate(self):
		currentBalance = self.config.wallet.balance()
		msg = HTML(f"<ansired>ꜩ</ansired> Cost for deploying <ansigreen>{self.initialWalletBalance - currentBalance}</ansigreen> <ansired>ꜩ</ansired>")
		print_formatted_text(msg)
		self.totalCost += self.initialWalletBalance - currentBalance
		self.initialWalletBalance = currentBalance

	def checkIfNetworkUpToDate(self, lastOriginationFile, network):
		filename = os.path.basename(lastOriginationFile).split("_")[0]
		
		if self.isAlreadyDeployed(int(filename)):
			msg = HTML(f"Network <ansigreen>{network}</ansigreen> up to date!")
			print_formatted_text(msg)
			Helpers.fatal("")

	def incrementOrigination(self):
		spinner = Halo(text=f'Saving origination of {currentContractName} to chain', spinner='dots')
		spinner.start()

		if not self.originations:
			self.originations = self.chinstrapState.getContract("Originations", self.config.network.name, self.pytezoscli)

		lastDeployment = self.originations.storage()
		op = self.originations.main(lastDeployment+1).inject()

		spinner.stop()

		self.waitForBaking(op['hash'])

		self.chinstrapState.dump()
		print(f"✓ Successful saved origination of {currentContractName}!")
		balance = self.config

	def isAlreadyDeployed(self, originationNum):

		if not self.config.network.name in self.chinstrapState.chinstrap["networks"].keys():
			return False

		if len(self.chinstrapState.chinstrap["networks"][self.config.network.name])==0:
			return False

		if not self.originations:
			self.originations = self.chinstrapState.getContract("Originations", self.config.network.name, self.pytezoscli)

		lastDeployment = self.originations.storage()
		
		if originationNum > lastDeployment:
			return False

		return True

	def orignate(self, contract):
		orig = __import__(contract)
		storage, contract = orig.deploy(self.chinstrapState, self.config.network, self.config.accounts)

		try:
			spinner = Halo(text=f'Origination of {currentContractName} in progress', spinner='dots')
			spinner.start()

			res = self.config.wallet.origination(script=dict(code=contract.code, storage=storage)).autofill().sign().inject(_async=False)

			spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"{currentContractName}'s origination transaction at: {res['hash']}")

			hash = res['hash']
			bakingRes = self.waitForBaking(hash)
			addr = bakingRes['contents'][0]['metadata']['operation_result']['originated_contracts'][0]

			if self.config.network.name == 'development':
				if not "development" in self.chinstrapState.chinstrap["networks"]:
					self.chinstrapState.chinstrap["networks"] = {"development":[ ]}
				self.chinstrapState.chinstrap["networks"]["development"].append({'orignation_hash': hash, 'address':addr, 'name': currentContractName})
			elif self.config.network.name =='florencenet':
				if not "florencenet" in self.chinstrapState.chinstrap["networks"]:
					self.chinstrapState.chinstrap["networks"] = {"florencenet":[]}
				self.chinstrapState.chinstrap["networks"]["florencenet"].append({'orignation_hash': hash, 'address':addr, 'name': currentContractName})
			elif self.config.network.name =='granada':
				if not "granada" in self.chinstrapState.chinstrap["networks"]:
					self.chinstrapState.chinstrap["networks"] = {"granada":[]}
				self.chinstrapState.chinstrap["networks"]["granada"].append({'orignation_hash': hash, 'address':addr, 'name': currentContractName})
			elif self.config.network.name =='mainnet':
				if not "mainnet" in self.chinstrapState.chinstrap["networks"]:
					self.chinstrapState.chinstrap["networks"] = {"mainnet":[]}
				self.chinstrapState.chinstrap["networks"]["mainnet"].append({'orignation_hash': hash, 'address':addr, 'name': currentContractName})
			elif self.config.network.name =='edo2':
				if not "edo2" in self.chinstrapState.chinstrap["networks"]:
					self.chinstrapState.chinstrap["networks"] = {"edo2":[]}
				self.chinstrapState.chinstrap["networks"]["edo2"].append({'orignation_hash': hash, 'address':addr, 'name': currentContractName})

			msg = HTML(f"✓ <ansired>{currentContractName}</ansired> address at: <ansigreen>{addr}</ansigreen>")
			print_formatted_text(msg)

		except pytezos.rpc.node.RpcError as e:
			Helpers.fatal('\nrpcerror:. Please try again after sometime!')

	def waitForBaking(self, ophash):
		spinner = Halo(text='Baking...', spinner='dots')
		spinner.start()
		while 1:
			try:
				opg = self.config.wallet.shell.blocks[-5:].find_operation(ophash)
				break
			except StopIteration:
				continue
			except pytezos.rpc.node.RpcError:
				Helpers.debug('rpcerror: sleeping for sometime!')
				time.sleep(5)
				continue
			except Exception as e:
				Helpers.fatal(e)
		
		spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"Baking successful!")
		return opg

class ChinstrapState:
	def __init__(self, reset) -> None:
		if (reset and os.path.exists('./build/.chinstrapState.json')) or not os.path.exists('./build/.chinstrapState.json'):
			with open('./build/.chinstrapState.json', 'w') as f:
				f.write("""{
  "chinstrap": {
    "networks": {
      
    }
  }
}""")
		with open('./build/.chinstrapState.json','r') as f:
			state = json.loads(f.read())
		
		self.chinstrap = state['chinstrap']
	
	def dump(self):
		res = {
			'chinstrap': self.chinstrap
		}

		with open('./build/.chinstrapState.json','w') as f:
			f.write(json.dumps(res))
	
	def getContract(self, name, network, pytezoscli):
		if network in self.chinstrap["networks"].keys():
			for cont in self.chinstrap["networks"][network]:
				if cont["name"] == name:
					try:
						contract = pytezoscli.contract(cont["address"])
						return contract
					except pytezos.rpc.node.RpcError as e:
						Helpers.fatal('rpcerror: Please try again after sometime!')
					except Exception as e:
						Helpers.fatal(e)

		return False

	def displayAddresses(self, network):
		if network in self.chinstrap["networks"].keys():
			for cont in self.chinstrap["networks"][network]:
				print(f"Contract {cont['name']} is originated at {cont['address']}")
			
		print()