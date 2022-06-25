import smartpy as sp

contract = sp.io.import_script_from_url("file:contracts/FA1.2.py")


@sp.add_test(name="FA12")
def test():

    scenario = sp.test_scenario()
    scenario.h1("FA1.2 template - Fungible assets")

    scenario.table_of_contents()

    # sp.test_account generates ED25519 key-pairs deterministically:
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Robert")

    # Let's display the accounts:
    scenario.h1("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h1("Contract")
    token_metadata = {
        "decimals": "18",  # Mandatory by the spec
        "name": "My Great Token",  # Recommended
        "symbol": "MGT",  # Recommended
        # Extra fields
        "icon": "https://smartpy.io/static/img/logo-only.svg",
    }
    contract_metadata = {
        "": "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
    }
    c1 = contract.FA12(
        admin.address,
        config=contract.FA12_config(support_upgradable_metadata=True),
        token_metadata=token_metadata,
        contract_metadata=contract_metadata,
    )
    scenario += c1

    scenario.h1("Offchain view - token_metadata")
    # Test token_metadata view
    offchainViewTester = contract.TestOffchainView(c1.token_metadata)
    scenario.register(offchainViewTester)
    offchainViewTester.compute(data=c1.data, params=0)
    scenario.verify_equal(
        offchainViewTester.data.result,
        sp.some(
            sp.record(
                token_id=0,
                token_info=sp.map(
                    {
                        "decimals": sp.utils.bytes_of_string("18"),
                        "name": sp.utils.bytes_of_string("My Great Token"),
                        "symbol": sp.utils.bytes_of_string("MGT"),
                        "icon": sp.utils.bytes_of_string(
                            "https://smartpy.io/static/img/logo-only.svg"
                        ),
                    }
                ),
            )
        ),
    )

    scenario.h1("Attempt to update metadata")
    scenario.verify(
        c1.data.metadata[""]
        == sp.utils.bytes_of_string(
            "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd"
        )
    )
    c1.update_metadata(key="", value=sp.bytes("0x00")).run(sender=admin)
    scenario.verify(c1.data.metadata[""] == sp.bytes("0x00"))

    scenario.h1("Entry points")
    scenario.h2("Admin mints a few coins")
    c1.mint(address=alice.address, value=12).run(sender=admin)
    c1.mint(address=alice.address, value=3).run(sender=admin)
    c1.mint(address=alice.address, value=3).run(sender=admin)
    scenario.h2("Alice transfers to Bob")
    c1.transfer(from_=alice.address, to_=bob.address, value=4).run(sender=alice)
    scenario.verify(c1.data.balances[alice.address].balance == 14)
    scenario.h2("Bob tries to transfer from Alice but he doesn't have her approval")
    c1.transfer(from_=alice.address, to_=bob.address, value=4).run(
        sender=bob, valid=False
    )
    scenario.h2("Alice approves Bob and Bob transfers")
    c1.approve(spender=bob.address, value=5).run(sender=alice)
    c1.transfer(from_=alice.address, to_=bob.address, value=4).run(sender=bob)
    scenario.h2("Bob tries to over-transfer from Alice")
    c1.transfer(from_=alice.address, to_=bob.address, value=4).run(
        sender=bob, valid=False
    )
    scenario.h2("Admin burns Bob token")
    c1.burn(address=bob.address, value=1).run(sender=admin)
    scenario.verify(c1.data.balances[alice.address].balance == 10)
    scenario.h2("Alice tries to burn Bob token")
    c1.burn(address=bob.address, value=1).run(sender=alice, valid=False)
    scenario.h2("Admin pauses the contract and Alice cannot transfer anymore")
    c1.setPause(True).run(sender=admin)
    c1.transfer(from_=alice.address, to_=bob.address, value=4).run(
        sender=alice, valid=False
    )
    scenario.verify(c1.data.balances[alice.address].balance == 10)
    scenario.h2("Admin transfers while on pause")
    c1.transfer(from_=alice.address, to_=bob.address, value=1).run(sender=admin)
    scenario.h2("Admin unpauses the contract and transferts are allowed")
    c1.setPause(False).run(sender=admin)
    scenario.verify(c1.data.balances[alice.address].balance == 9)
    c1.transfer(from_=alice.address, to_=bob.address, value=1).run(sender=alice)

    scenario.verify(c1.data.totalSupply == 17)
    scenario.verify(c1.data.balances[alice.address].balance == 8)
    scenario.verify(c1.data.balances[bob.address].balance == 9)

    scenario.h1("Views")
    scenario.h2("Balance")
    view_balance = contract.Viewer(sp.TNat)
    scenario += view_balance
    c1.getBalance((alice.address, view_balance.typed.target))
    scenario.verify_equal(view_balance.data.last, sp.some(8))

    scenario.h2("Administrator")
    view_administrator = contract.Viewer(sp.TAddress)
    scenario += view_administrator
    c1.getAdministrator((sp.unit, view_administrator.typed.target))
    scenario.verify_equal(view_administrator.data.last, sp.some(admin.address))

    scenario.h2("Total Supply")
    view_totalSupply = contract.Viewer(sp.TNat)
    scenario += view_totalSupply
    c1.getTotalSupply((sp.unit, view_totalSupply.typed.target))
    scenario.verify_equal(view_totalSupply.data.last, sp.some(17))

    scenario.h2("Allowance")
    view_allowance = contract.Viewer(sp.TNat)
    scenario += view_allowance
    c1.getAllowance(
        (
            sp.record(owner=alice.address, spender=bob.address),
            view_allowance.typed.target,
        )
    )
    scenario.verify_equal(view_allowance.data.last, sp.some(1))
