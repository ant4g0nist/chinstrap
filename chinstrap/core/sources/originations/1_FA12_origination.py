from chinstrap.originations import getContract


def deploy(chinstrapState, network, accounts):
    # if there are . in the name, please replace them with _
    # For example, to access FA1.2 contract, we use FA1_2
    contract = getContract("FA1_2")

    initial_storage = contract.storage.encode(
        {
            "administrator": accounts[0].key.public_key_hash(),
            "balances": {},
            "metadata": {},
            "paused": False,
            "token_metadata": {},
            "totalSupply": 0,
        }
    )

    return initial_storage, contract
