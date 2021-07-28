# Download Tempaltes from SmartPy
import os
import halo
import errno
import gitlab
from prompt_toolkit import HTML
from chinstrap.chinstrapCore import Helpers
from prompt_toolkit import print_formatted_text

repo = "SmartPy/smartpy"

contracts = {
	"Token Contracts": [{
		'fileName'   : "FA1.2.py",
		'name' 		 : "FA1.2: Fungible Assets",
		'description' : 'FA1.2 refers to an ERC20-like fungible token standard for Tezos. Proposed in <a href="https://gitlab.com/tzip/tzip/blob/master/proposals/tzip-7/tzip-7.md" target="_blank">TZIP-7</a>.'
	}, {
		'fileName'   : "FA2.py",
		'name' 		 : "FA2: Fungible, Non-fungible, Multiple or Single Assets",
		'description' : 'FA2 exposes a unified token contract interface, supporting a wide range of token types and implementations. Proposed in <a href="https://gitlab.com/tzip/tzip/blob/master/proposals/tzip-12/tzip-12.md" target="_blank">TZIP-12</a>.'
	}, {
		'fileName'   : "oracle.py",
		'name' 		 : "Chainlink Oracles",
		'description' : "Building Chainlink oracles on Tezos - still experimental"
	}],
	"Simple Examples": [{
		'fileName'   : "storeValue.py",
		'name' 		 : "Store Value",
		'description' : "Store some data in the storage of a contract and change its value by calling its entry points."
	},  {
		'name' 		 : "Calculator",
		'fileName' :  "calculator.py",
		'description' : "A simple calculator on the blockchain."
	}, {
		'fileName'   : "worldCalculator.py",
		'name' 		 : "World Calculator",
		'description' : "A simple expression calculator on the blockchain (with parsing and pretty-printing)."
	}, {
		'fileName'   : "fifo.py",
		'name' 		 : "Fifo",
		'description' : "Contracts storing user defined first-in first-out data structures."
	}],
	"Protocols": [{
		'fileName'   : "atomicSwap.py",
		'name' 		 : "Atomic Swap",
		'description' : "A simple, and naive, atomic swap contract."
	}, {
		'fileName'   : "escrow.py",
		'name' 		 : "Escrow",
		'description' : "A simple escrow contract."
	}, {
		'fileName'   : "multisig.py",
		'name' 		 : "Multisig",
		'description' : "A complex contract handling several multisig sub-contracts, each have several groups of several participants with extensive parametrization."
	}, {
		'fileName'   : "stateChannels.py",
		'name' 		 : "State Channels (obsolete version)",
		'description' : "A contract transforming a simple game into a state channel for this game."
	}],
	"State Channels": [{
		'fileName'   : "state_channel_games/game_platform.py",
		'contract'	 : True,
		'name' 		 : "Game platform",
		'description' : "State channel based game platform."
	}, {
		'fileName'   : "state_channel_games/game_tester.py",
		'name' 		 : "Game tester",
		'description' : "Small contract to test game models."
	}, {
		'fileName'   : "state_channel_games/model_wrap.py",
		'name' 		 : "Game wrapper",
		'description' : "Helper to prepare models for contracts."
	}, {
		'fileName'   : "state_channel_games/types.py",
		'name' 		 : "Game types",
		'description' : "Type definitions for games."
	}, {
		'fileName'   : "state_channel_games/models/head_tail.py",
		'name' 		 : "Game: Head and Tail model",
		'description' : "Game model for head and tail."
	}, {
		'fileName'   : "state_channel_games/models/nim.py",
		'name' 		 : "Game: Nim model",
		'description' : "Game model for nim."
	}, {
		'fileName'   : "state_channel_games/models/tictactoe.py",
		'name' 		 : "Game: tic-tac-toe model",
		'description' : "Game model for tic-tac-toe."
	}, {
		'fileName'   : "state_channel_games/models/transfer.py",
		'name' 		 : "Game: transfer model",
		'description' : "Very simple model, transfer only."
	}],
	"Small Games": [{
		'fileName'   : "chess.py",
		'name' 		 : "Chess game",
		'description' : "Example template with moves for a few pieces."
	}, {
		'fileName'   : "game_of_life.py",
		'name' 		 : "Game of Life",
		'description' : "Example template for a game of life simulator."
	}, {
		'fileName'   : "jingleBells.py",
		'name' 		 : "Jingle Bells",
		'description' : "A minimalistic contract to sing Jingle Bells. Dashing through the snow, ..."
	}, {
		'fileName'   : "minikitties.py",
		'name' 		 : "Mini Kitties",
		'description' : "Small example freely inspired by crypto-kitties"
	}, {
		'fileName'   : "nim.py",
		'name' 		 : "Nim game",
		'description' : '\n            Implementation of a Nim game (wikipedia <a href="https://en.wikipedia.org/wiki/Nim" target="_blank">page<a>).\n            <br/>Use of arrays.\n            <br/>One contract handles one game.\n            '
	}, {
		'fileName'   : "nimLift.py",
		'name' 		 : "Nim game repository",
		'description' : "\n            Implementation of a Nim game (wikipedia <a href='https://en.wikipedia.org/wiki/Nim' target=\"_blank\">page</a>).\n            <br/>One contract can handle many games in parallel.\n            "
	}, {
		'fileName'   : "tictactoe.py",
		'name' 		 : "TicTacToe game",
		'description' : "A simple TicTacToe game showing many regular concepts for simple games."
	}, {
		'fileName'   : "tictactoeFactory.py",
		'name' 		 : "TicTacToe game factory",
		'description' : "A factory to handle several simple TicTacToe games showing many regular concepts for simple games."
	}]
}

class SmartPyDownloader:
	def __init__(self):
		self.gl = gitlab.Gitlab('https://gitlab.com')
		self.project = self.gl.projects.get(repo)

	def displayTemplateCategories(self):
		prom = Helpers.SelectionPrompt()
		templateType = prom.prompt(HTML('<ansired>Available categories:</ansired>'), options=contracts.keys())

		if templateType=='State Channels':
			for i in contracts[templateType]:
				if 'contract' in i.keys():
					self.downloadContractTemplate(f"python/templates/{i['fileName']}", True)
				else:
					self.downloadContractTemplate(f"python/templates/{i['fileName']}")
			
			return

		options = []
		for i in contracts[templateType]:
			options.append(i['name'])

		print()

		prom = Helpers.SelectionPrompt(sideBySide=False)
		contractChoice = prom.prompt(HTML('<ansigreen>Available contracts:</ansigreen>'), options=options)
		
		for i in contracts[templateType]:
			if i['name'] == contractChoice:
				self.downloadContractTemplate(f"python/templates/{i['fileName']}")

	def getListOfTemplates(self):
		templates = self.project.repository_tree(path='python/templates', per_page=200)
		for template in templates:
			if template['type']=='blob':
				yield template['id'], template['name'], template['path']
	
	def showAvailableFiles(self):
		msg =HTML(f"<u>name {'':<16}|{'':<16} path</u>")
		print_formatted_text(msg)
		
		for i in self.getListOfTemplates():
			msg =HTML(f"<b><ansigreen>{i[1]:32}</ansigreen></b> {i[2]}")
			print_formatted_text(msg)

	def mkdir_p(self, path):
		try:
			os.makedirs(path)
		except OSError as exc: # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else: raise
			
	def downloadContractTemplate(self, path, contract=False):
		basename = os.path.basename(path)
		spinner = halo.Halo(text=f'Fetching file!', spinner='dots')
		spinner.start()

		localFilePath = f'contracts/'
		if contract:
			localFilePath += basename
		else:
			localFilePath += path.replace("python/templates/","")
		
		self.mkdir_p(os.path.dirname(localFilePath))
		

		with open(localFilePath, 'wb') as f:
			self.project.files.raw(file_path=path, ref='master', streamed=True, action=f.write)

		spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"File saved to {localFilePath}!\n")