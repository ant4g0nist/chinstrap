from chinstrap.core.originations import getContract


def deploy(state, network, accounts):
    contract = getContract("Originations")
    initial_storage = contract.storage.encode(
        {"last_completed_originations": 0, "owner": accounts[0].key.public_key_hash()}
    )
    return initial_storage, contract
