import os
import json
import docker
from halo import Halo
from prompt_toolkit import HTML
from chinstrap.chinstrapCore import Helpers
from prompt_toolkit import print_formatted_text

class Sandbox:
	"""
	Sandbox:
		- Used to launch a Tezos local sandbox! This class uses docker to pull and launch tqtezos/flextesa image
		- takes number of accounts as input to generate accounts using flextesa
		- keeps of the state in /tmp/chinstrapSandboxContainer file!
	
	WARNING: Please do not use these accounts on mainnet!

	"""
	def __init__(self, accounts=5, stop=False) -> None:
		self.accounts = []
		self.container = None
		self.state = {}

		if not stop:
			self.pullDocker()

	def stopSandbox(self):
		if os.path.exists("/tmp/chinstrapSandboxContainer"):
			with open("/tmp/chinstrapSandboxContainer",'r') as f:
				container_id = json.loads(f.read())['container_id']

			if container_id:
				client = docker.from_env()
				try:
					self.container = client.containers.get(container_id)
					self.killContainer()
				except Exception as e:
					pass
				
				os.remove("/tmp/chinstrapSandboxContainer")
				return

		Helpers.debug('Nothing todo!')

	def pullDocker(self):
		image = "tqtezos/flextesa:20210602"
		client = docker.from_env()
		try:
			spinner = Halo(text=f'Fetching Flextesa sandbox. This might take a while!', spinner='dots')
			spinner.start()
			client.images.get(image)
			spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"{image} ready to use!\n")

		except docker.errors.ImageNotFound:
			client.images.pull(image)

	def generateAccounts(self, count=5, balance=None, develop=False):
		command = 'flextesa key %s'

		msg = HTML(f"<b>WARNING: </b><ansired>Please do not use these accounts on mainnet!</ansired>\n")
		print_formatted_text(msg)
		
		spinner = Halo(text=f'Creating {count} accounts...', spinner='dots')
		spinner.start()
		
		self.state['accounts'] = {}
		for i in range(count):
			cmd = command%i
			container = self.runFlextesaCommandInDocker(cmd)
			for line in container.logs(stream=True):
				account = line.decode('utf-8').rstrip()
				self.accounts.append(f"{account}@{balance*1_000_000}")
				
		spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"Accounts created!\n")
		
		print(f'\nname {"":16} address {"":32} publicKey {"":46} privateKey')
		for account in self.accounts:
			name, publicKeyHash, address, privateKey = account.split(",")
			print(f" {name: <4}{address:36} {publicKeyHash} {privateKey.replace('unencrypted:','').split('@')[0]}")
			self.state['accounts'][name] = {'address':address, 'private':privateKey.replace('unencrypted:','').split('@')[0]}
		
		print("*"*20)

	def runFlextesaCommandInDocker(self, command, detach=False, auto_remove=True):
		client = docker.from_env()
		container = client.containers.create(image='tqtezos/flextesa:20210602', command=command, detach=detach, auto_remove=auto_remove)
		container.start()
		return container
	
	def flextesa(self, port=20000, protocol_kind='Florence', manual=True, detach=False, accounts=5, balance=None, develop=False):
		Helpers.success(f'Starting local:{protocol_kind} sandbox')

		self.generateAccounts(accounts, balance=balance)
		
		spinner = Halo(text=f'Starting sandbox', spinner='dots')
		spinner.start()

		command = f'''flextesa mini-net --root "/tmp/mini-box" --size 1 --set-history-mode N000:archive --number-of-b 5 --time-b 5 --minimal-block-delay 5 --until-level 200_000_000 --protocol-kind {protocol_kind} --keep-root '''

		for account in self.accounts:
			command += f' --add-bootstrap-account="{account}" --no-daemons-for={account.split(",")[0]} '

		client = docker.from_env()

		self.container = client.containers.create(image='tqtezos/flextesa:20210602', command=command, detach=detach, auto_remove=True, ports={'20000': port})
		self.container.start()
		
		self.state['container_id'] = self.container.id
		
		with open('/tmp/chinstrapSandboxContainer', 'w') as f:
			f.write(json.dumps(self.state))

		spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"Sandbox up and running!\n")

		self.started = False
		if not detach:
			print("*"*20)
			for line in self.container.logs(stream=True):
				op = line.decode('utf-8').rstrip()
				if develop and 'Network started' in op:
					self.started = True
					return

				if not develop:
					print(op)
	
	def killContainer(self):
		Helpers.debug("\nPlease wait while I clean up!")
		try:
			self.container.remove(force=True)
		except:
			Helpers.fatal(f"Sorry, failed to remove {self.container.id} container! Please do it manually using docker stop command")
		
		Helpers.success("Cleanup crew finished their job!")