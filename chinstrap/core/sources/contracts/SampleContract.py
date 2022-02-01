import smartpy as sp


class SampleContract(sp.Contract):
    def __init__(self, value, owner):
        self.init_type(sp.TRecord(counter=sp.TInt, owner=sp.TAddress))
        self.init(counter=value, owner=owner)

    @sp.entry_point
    def increment(self, value):
        sp.verify(sp.sender == self.data.owner, message="Only owner can increment")
        self.data.counter += value

    @sp.entry_point
    def decrement(self, value):
        sp.verify(sp.sender == self.data.owner, message="Only owner can decrement")
        self.data.counter -= value


sp.add_compilation_target(
    "SampleContract",
    SampleContract(0, sp.address("tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe")),
)
