import pytest
from pytezos import MichelsonRuntimeError, ContractInterface

michelson_contract = "./build/contracts/samplecontract/step_000_cont_0_contract.tz"

owner = "tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"
alice = "tz1LFuHW4Z9zsCwg1cgGTKU12WZAs27ZD14v"

@pytest.fixture
def counterContract():
	return ContractInterface.from_file(michelson_contract)

def test_should_pass_if_the_return_value_is_5(counterContract):
	value = 5
	storage = {"owner": owner, "counter": 0}
	result = counterContract.increment(value).interpret(storage=storage, source=owner)
	assert result.storage["counter"] == 5
		
def test_should_fail_if_the_source_is_not_the_owner(counterContract):
	value = 5
	storage = {"owner": owner, "counter": 0}

	with pytest.raises(MichelsonRuntimeError) as e:
		counterContract.increment(value).interpret(storage=storage, source=alice)

	assert "Only owner can increment" == str(e.value.args[-1].strip("\\").strip("'"))