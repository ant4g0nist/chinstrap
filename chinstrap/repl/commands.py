import os
from pytezos import pytezos
from chinstrap import helpers
from chinstrap import sandbox
from chinstrap import originations

@helpers.handleException()
def cExit():
	helpers.hexit()

@helpers.handleException()
def stopSandbox():
	sand = sandbox.Sandbox("")
	sand.halt()

@helpers.handleException()
def getContract(name):
	return originations.getContract(name)

@helpers.handleException()
def getContractFromFile(filename):
	if os.path.exists(filename):
		return pytezos.ContractInterface.from_file(filename)
	
	helpers.debug("Please make sure file exists!")

# @Helpers.handleException()
# def getContractFromAddress(address):
# 	return config.wallet.contract(address)