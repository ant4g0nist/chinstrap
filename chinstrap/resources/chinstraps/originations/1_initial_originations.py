from chinstrap.chinstrapCore import getContract

def deploy(chinstrapState, network, accounts):
	contract = getContract("Originations")
	initial_storage = contract.storage.encode(0)
	return initial_storage, contract