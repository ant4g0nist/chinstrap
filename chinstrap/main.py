#!/usr/bin/env python3
import os
import sys
import halo
import time
import pytezos
import argparse
from chinstrap import version
from chinstrap import chinstrapCore
from chinstrap.chinstrapCore import SmartPy
from chinstrap.chinstrapCore import Sandbox
from chinstrap.chinstrapCore import Helpers
from chinstrap.chinstrapCore import Debugger
from chinstrap.chinstrapCore.Config import ChinstrapConfig
from prompt_toolkit.formatted_text.html import HTML
from prompt_toolkit.shortcuts.utils import print_formatted_text

def main():
	parser = argparse.ArgumentParser(description='Chinstrap - a cute framework for developing Tezos Smart Contracts')
	parser.add_argument("--init", action='store_true', help="Initialize new and empty Tezos SmartPy project", required=False)
	parser.add_argument("--compile", action='store_true', help="Compile contract source files", required=False)
	parser.add_argument("--create", action='store_true', help="Helper to create new contracts, origination and tests", required=False)
	parser.add_argument("--debug", action='store_true', help="Interactively debug contracts.", required=False)
	parser.add_argument("--templates", action='store_true', help="Download from templates provided SmartPy", required=False)
	parser.add_argument("--develop", action='store_true', help="Open a console with a local development blockchain", required=False)
	parser.add_argument("--originate", action='store_true', help="Run originations to deploy contracts", required=False)
	parser.add_argument("--reset", default=False, action='store_true', help="Run originations to deploy contracts", required=False)
	parser.add_argument("--network", default='development', help="Show addresses for deployed contracts on each network", required=False)
	parser.add_argument("--test", default='pytest', help="Run [smartpy] or [pytest] tests. ", required=False)
	parser.add_argument("--sandbox", action='store_true', help="Start a Tezos local sandbox", required=False)
	parser.add_argument("--sandbox-stop", action='store_true',  help="Tezos local sandbox's RPC Port", required=False)
	parser.add_argument("--sandbox-detach", default=False,  action='store_true', help="Start a Tezos local sandbox and detach", required=False)
	parser.add_argument("--sandbox-port", default=20000, help="Tezos local sandbox's RPC Port", required=False)
	parser.add_argument("--sandbox-protocol", default='Florence', help="Tezos local sandbox's RPC Port", required=False)
	parser.add_argument("--accounts", default=10, type=int, help="Number of accounts to bootstrap on Tezos local sandbox", required=False)
	parser.add_argument("--account-balance", default=20000, type=int, help="Amount of Tezos to deposit while bootstraping on Tezos local sandbox", required=False)
	parser.add_argument("--version", action='store_true', help="Show version number and exit", required=False)

	args = parser.parse_args()
	
	Helpers.welcome_banner()

	sand = None
	try:	
		if len(sys.argv)==1:
			parser.print_help()
			sys.exit()
		
		if args.version:
			msg = HTML(f"Chinstrap version: <b>{version.version}</b>")
			print_formatted_text(msg)
			return

		chinstrapPath = os.path.dirname(os.path.abspath( __file__ ))

		if args.init:
			chinstrapCore.InitChinstrap(chinstrapPath)
			Helpers.success('All done. Enjoy')
			return
		
		if args.sandbox_detach:
			sand = Sandbox.Sandbox()
			sand.flextesa(accounts=args.accounts, port=args.sandbox_port, protocol_kind=args.sandbox_protocol, balance=args.account_balance, detach=True)
			return

		if args.sandbox:
			sand = Sandbox.Sandbox()
			sand.flextesa(accounts=args.accounts, port=args.sandbox_port, protocol_kind=args.sandbox_protocol, balance=args.account_balance)
			return

		if args.sandbox_stop:
			sand = Sandbox.Sandbox(stop=True)
			sand.stopSandbox()
			return

		Helpers.confirmChinstrapProjectDirectory()

		if args.develop:
			sand = Sandbox.Sandbox()

			sand.flextesa(accounts=args.accounts, port=args.sandbox_port, protocol_kind=args.sandbox_protocol, balance=args.account_balance, develop=True)

			spinner = halo.Halo(text=f'Waiting for development network to start!', spinner='dots')
			spinner.start()

			while not sand.started:
				time.sleep(2)

			spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"network started!\n")

			Debugger.launch(args.network, sand.state['accounts'])

		elif args.create:
			chinstrapCore.Create()

		elif args.templates:
			downloader = SmartPy.SmartPyDownloader()
			downloader.displayTemplateCategories()

		elif args.compile:
			chinstrap = ChinstrapConfig(args.network, compile=True)
			chinstrapCore.Compile(chinstrap, chinstrapPath=chinstrapPath)

		elif args.test:
			if args.test=='pytest':
				chinstrapCore.RunTests(chinstrapPath, True)
			else:
				chinstrapCore.RunTests(chinstrapPath, False)

		elif args.originate:
			chinstrap = ChinstrapConfig(args.network)
			chinstrapCore.Origination(chinstrap, args.reset)

		elif args.debug:
			Debugger.launch(args.network)
			
		elif args.network:
			chinstrap = chinstrapCore.ChinstrapState(False)
			chinstrap.displayAddresses(args.network)

	except KeyboardInterrupt:
		pass

	if sand:
		sand.killContainer()

	Helpers.hexit()

if __name__ == "__main__":
	main()