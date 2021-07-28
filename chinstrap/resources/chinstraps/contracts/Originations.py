# SmartPy Code
import smartpy as sp

# this contract is used by Chinstrap for keeping track of Originations!!
# we suggest not to modify this contract!

class Originations(sp.Contract):
	def __init__(self, value = 0):
		self.init_type(sp.TRecord(last_completed_originations = sp.TInt))
		self.init(last_completed_originations = value)

	@sp.entry_point
	def main(self, completed_originations):
		self.data.last_completed_originations = completed_originations

@sp.add_test(name = "test origination")
def test():
	c1 = Originations()
	scenario = sp.test_scenario()
	scenario += c1

sp.add_compilation_target('Originations', Originations())