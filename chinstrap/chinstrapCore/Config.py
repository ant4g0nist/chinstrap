import os
import json
import yaml
from pytezos import pytezos
from prompt_toolkit import HTML
from chinstrap.chinstrapCore import Helpers
from prompt_toolkit import print_formatted_text

class ChinstrapConfig:
	def __init__(self, network='development', compile=False) -> None:
		if not os.path.exists('./chinstrap_config.yaml'):
			Helpers.fatal('Could not find chinstrap_config.yaml!')
		
		with open('./chinstrap_config.yaml', 'r') as f:
			confData = yaml.safe_load(f)
			self.config = Helpers.convertYamlToObject(confData).chinstrap

		self.compiler = self.config.compiler
		
		if not compile:
			if network=='development':
				self.network = self.config.networks.development
				self.network.name = 'development'
			elif network=='florencenet':
				self.network = self.config.networks.florencenet
				self.network.name = 'florencenet'
			elif network=='granada':
				self.network = self.config.networks.granada
				self.network.name = 'granada'
			elif network=='mainnet':
				self.network = self.config.networks.mainnet
				self.network.name = 'mainnet'
			elif network=='edo2':
				self.network = self.config.networks.edo2
				self.network.name = 'edo2'

			msg = HTML(f'Using network: <b>{self.network.host}:{self.network.port}</b>')
			print_formatted_text(msg)

			self.loadAccounts()

	def loadAccounts(self):
		self.accounts = []
		try:
			keyFile = self.network.accounts[0].privateKeyFile
			with open(keyFile, 'r') as f:
				self.key = f.read().rstrip("\n")
			
			self.wallet = pytezos.using(shell=f"{self.network.host}:{self.network.port}", key=self.key)

			for i in self.network.accounts:
				self.loadPrivateKeyFromFile(i.privateKeyFile)

		except Exception as e:
			print(e)
			Helpers.fatal(f'Exception occured while loading accounts! {e}')

	def loadPrivateKeyFromFile(self, keyFile):
		with open(keyFile, 'r') as f:
			key = f.read().rstrip("\n")

		self.loadPrivateKey(key)

	def loadPrivateKey(self, key):
		try:
			wallet = pytezos.using(shell=f"{self.network.host}:{self.network.port}", key=key)
		except pytezos.rpc.node.RpcError:
			Helpers.fatal(f"Failed to connect to {self.network.host}:{self.network.port}. Try again in sometime!")

		msg = HTML(f"Loaded wallet <b>{wallet.key.public_key_hash()}</b>. Balance: <b>{wallet.balance()}</b>\n")
		print_formatted_text(msg)
		self.accounts.append(wallet)

	def save(self):
		config = {'chinstrap':{'networks':{},'compiler':{}}}
		
		for i,v in self.config.__dict__['networks'].__dict__.items():
			if i[0] != "_":
				network = {'host':v.__dict__['host'], 'port':v.__dict__['port'], 'accounts':[]}
				accounts = []
				if 'accounts' in v.__dict__.keys():
					for d in v.__dict__['accounts']:
						for j, k in d.__dict__.items():
							if j[0]!="_":
								accounts.append({j:k})
				
				network['accounts'] = accounts
				config['chinstrap']['networks'][i] = network
		
		with open('./chinstrap_config.yaml', 'w') as f:
			f.write(yaml.dump(config))

class ChinstrapConfigHandler:
	# make this a repl 
	def __init__(self) -> None:
		pass