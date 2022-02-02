# SmartPy Code
import smartpy as sp

# this contract is used by Chinstrap for keeping track of Originations!!
# we suggest not to modify this contract!


class Originations(sp.Contract):
    def __init__(self, value, owner):
        self.init_type(
            sp.TRecord(last_completed_originations=sp.TInt, owner=sp.TAddress)
        )
        self.init(last_completed_originations=value, owner=owner)

    @sp.entry_point
    def main(self, completed_originations):
        sp.verify(sp.sender == self.data.owner, message="Only owner can increment")
        self.data.last_completed_originations = completed_originations


@sp.add_test(name="test origination")
def test():
    c1 = Originations(0, sp.address("tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe"))
    scenario = sp.test_scenario()
    scenario += c1


sp.add_compilation_target(
    "Originations", Originations(0, sp.address("tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe"))
)
