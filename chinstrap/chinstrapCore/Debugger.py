import os
import json
import pytezos
from pygments import highlight
from prompt_toolkit import HTML
from ptpython.repl import embed
from chinstrap.chinstrapCore import Sandbox
from chinstrap import chinstrapCore
from pygments.lexers import JsonLexer
from pytezos import ContractInterface
from chinstrap.chinstrapCore import Helpers
from ptpython.prompt_style import PromptStyle
from prompt_toolkit import print_formatted_text
from pygments.formatters import TerminalFormatter
from ptpython.layout import CompletionVisualisation
from prompt_toolkit.formatted_text import AnyFormattedText
from chinstrap.chinstrapCore.Config import ChinstrapConfig
from chinstrap.chinstrapCore.Helpers import debug, handleException

__prompt__ = "chinstrap:> "

pytezoscli = None
chinstrapRoot  = os.path.expanduser("~/.chinstrap/")
historyPath = f"{chinstrapRoot}/history"

if not os.path.exists(chinstrapRoot):
	os.mkdir(chinstrapRoot)
	with open(historyPath, 'w') as f:
		f.write("")

def configure(repl):
	# Configuration method. This is called during the start-up of ptpython.

	# # Show function signature (bool).
	repl.show_signature = True

	# # Show docstring (bool).
	repl.show_docstring = True

	# # Show the "[Meta+Enter] Execute" message when pressing [Enter] only
	# # inserts a newline instead of executing the code.
	repl.show_meta_enter_message = True

	# # Show completions. (NONE, POP_UP, MULTI_COLUMN or TOOLBAR)
	repl.completion_visualisation = CompletionVisualisation.MULTI_COLUMN

	repl.completion_menu_scroll_offset = 0

	repl.show_status_bar = False
	repl.show_sidebar_help = False

	# # Highlight matching parethesis.
	repl.highlight_matching_parenthesis = True

	# # Line wrapping. (Instead of horizontal scrolling.)
	repl.wrap_lines = True

	# # Complete while typing. (Don't require tab before the
	# # completion menu is shown.)
	repl.complete_while_typing = True

	# Vi mode.
	repl.vi_mode = False

	# # Paste mode. (When True, don't insert whitespace after new line.)
	# repl.paste_mode = False

	class ClassicPrompt(PromptStyle):
		"""
		The classic Python prompt.
		"""

		def in_prompt(self) -> AnyFormattedText:
			return [("class:prompt", __prompt__)]

		def in2_prompt(self, width: int) -> AnyFormattedText:
			return [("class:prompt.dots", "...")]

		def out_prompt(self) -> AnyFormattedText:
			return []
			
	# Use the classic prompt. (Display '>>>' instead of 'In [1]'.)
	repl.all_prompt_styles["custom"] = ClassicPrompt()
	repl.prompt_style = "custom" #"ipython"  # 'classic' or 'ipython'

	# Don't insert a blank line after the output.
	repl.insert_blank_line_after_output = False

	repl.enable_history_search = True

	# Enable auto suggestions. (Pressing right arrow will complete the input,
	# based on the history.)
	repl.enable_auto_suggest = False

	# Enable open-in-editor. Pressing C-x C-e in emacs mode or 'v' in
	# Vi navigation mode will open the input in the current editor.
	repl.enable_open_in_editor = True

	# Enable system prompt. Pressing meta-! will display the system prompt.
	# Also enables Control-Z suspend.
	repl.enable_system_bindings = True

	# Ask for confirmation on exit.
	repl.confirm_exit = True

	# Enable input validation. (Don't try to execute when the input contains
	# syntax errors.)
	repl.enable_input_validation = True

	# Use this colorscheme for the code.
	repl.use_code_colorscheme("default")

	repl.color_depth = "DEPTH_8_BIT"  # The default, 256 colors.
	# repl.color_depth = "DEPTH_24_BIT"  # True color.

	# Min/max brightness
	repl.min_brightness = 0.0  # Increase for dark terminal backgrounds.
	repl.max_brightness = 1.0  # Decrease for light terminal backgrounds.

	# Syntax.
	repl.enable_syntax_highlighting = True

	# Get into Vi navigation mode at startup
	repl.vi_start_in_navigation_mode = False

	# Preserve last used Vi input mode between main loop iterations
	repl.vi_keep_last_used_mode = False

	repl.confirm_exit = False

@Helpers.handleException()
def getContract(name):
	chinstrapState = chinstrapCore.ChinstrapState(False)
	return chinstrapState.getContract(name, config.network.name, pytezoscli=config.wallet)

@Helpers.handleException()
def getContractFromFile(filename):
	if os.path.exists(filename):
		return ContractInterface.from_file(filename)
	
	debug("Please make sure file exists!")

@Helpers.handleException()
def getContractFromAddress(address):
	return config.wallet.contract(address)

@Helpers.handleException()
def getContractFromURL(url):
	return ContractInterface.from_url(url)

@Helpers.handleException()
def setConfig(key, value):
	if key == 'network':
		if isinstance(value, dict):
			config.network = Helpers.Dict2Object(value)
		else:
			Helpers.debug('value should be a dictionary')

	elif key == 'host':
		config.network.host = value
	
	elif key == 'port':
		config.network.port = value
	
	elif key == 'compiler':
		config.compiler = value
	
	config.save()

@handleException()
def compile():
	chinstrapPath = os.path.dirname(os.path.dirname(os.path.abspath( __file__ )))
	chinstrapCore.Compile(config, chinstrapPath)

@handleException()
def test():
	chinstrapCore.RunTests()

@handleException()
def originate(reset=False):
	chinstrapCore.Origination(config, reset)

@handleException()
def bake(contractCall):
	call = contractCall.inject()
	res = Helpers.waitForBaking(call['hash'], config.wallet)
	# json_str = json.dumps(res, indent=4, sort_keys=True)
	# print(highlight(json_str, JsonLexer(), TerminalFormatter()))
	operation_results = res['contents']
	for operation_result in operation_results:
		metadata = operation_result['metadata']
		operation_result = metadata["operation_result"]
		print_formatted_text(HTML(f"status: <ansigreen>{operation_result['status']}</ansigreen>"))
		json_str = json.dumps(operation_result['storage'], indent=4, sort_keys=True)
		print_formatted_text(HTML("<ansired>Storage:</ansired>"))
		print(highlight(json_str, JsonLexer(), TerminalFormatter()))

@handleException()
def debug(contract):
	"""
	Takes a contract object returned by getContractFromFile|getContractFromAddress|getContractFromURL
	"""

@handleException()
def accounts():
	"""
		list accounts generated on sandbox
	"""
	global _accounts
	if not _accounts and not os.path.exists('/tmp/chinstrapSandboxContainer'):
		print('no accounts found')
	
	if not _accounts:
		with open('/tmp/chinstrapSandboxContainer', 'r') as f:
			_accounts = json.loads(f.read())['accounts']

	print(f'\n{"":16} address {"":32} private-key')
	
	for account in _accounts:
		print(f"{account} {_accounts[account]}")

 
@handleException()
def getAccountFromKey(key):
	"""
		Get Account from key
	"""
	return pytezos.pytezos.using(key=key, shell=f"{config.network.host}:{config.network.port}")

@handleException()
def getAccountBalance(address):
	"""
		Get account balance from address
	"""
	bal = float(config.wallet.account(address)['balance'])
	print(bal/1_000_000)

@handleException()
def cExit():
	sand = Sandbox.Sandbox(stop=True)
	sand.stopSandbox()
	Helpers.hexit()

def launch(network, accnts=None) -> None:
	global config
	global _accounts
	_accounts = accnts

	config = ChinstrapConfig(network)

	if _accounts:
		#TODO
		config.key 	  = _accounts['0']['private']
		config.wallet = pytezos.pytezos.using(shell=f"{config.network.host}:{config.network.port}", key=config.key)
		for account in _accounts:
			config.loadPrivateKey(_accounts[account]['private'])
	
	Helpers.success('✓ Accounts can be accessed from config.accounts')

	functions = {
		'getContract' 				: getContract,
		'getContractFromFile' 		: getContractFromFile,
		'getContractFromURL' 		: getContractFromURL,
		'getContractFromAddress' 	: getContractFromAddress,
		'setConfig'					: setConfig,
		'compile'					: compile,
		'test'						: test,
		'originate'					: originate,
		'debug'						: debug,
		'bake'						: bake,
		'config'					: config,
		'accounts'					: accounts,
		'account'					: getAccountFromKey,
		'balance'					: getAccountBalance,
		'exit'						: cExit, #TODO,
		'pytezos'					: pytezos
	}

	embed({}, functions, configure = configure, history_filename=historyPath)