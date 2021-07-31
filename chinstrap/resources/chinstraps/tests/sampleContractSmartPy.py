import smartpy  as sp

contract = sp.io.import_script_from_url("file:contracts/SampleContract.py")

@sp.add_test(name = "First Test")
def test():
	scenario = sp.test_scenario()
	c1 = contract.SampleContract(0, sp.address('tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe'))
	scenario += c1
	scenario += c1.increment(1).run(sender=sp.address('tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe'))