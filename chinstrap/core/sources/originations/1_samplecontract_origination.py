from chinstrap.originations import getContract


def deploy(chinstrapState, network, accounts):
    contract = getContract("SampleContract")
    initial_storage = contract.storage.encode(
        {"counter": 0, "owner": accounts[0].key.public_key_hash()}
    )
    return initial_storage, contract
