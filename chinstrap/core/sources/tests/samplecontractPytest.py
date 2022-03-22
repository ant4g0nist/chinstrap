from unittest import TestCase
from pytezos import MichelsonRuntimeError
from chinstrap.tests import getContractInterface

owner = "tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"
alice = "tz1LFuHW4Z9zsCwg1cgGTKU12WZAs27ZD14v"


class SampleContractTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = getContractInterface("SampleContract")

    def test_should_pass_if_the_return_value_is_5(self):
        value = 5
        storage = {"owner": owner, "counter": 0}
        result = self.contract.increment(value).interpret(storage=storage, source=owner)
        assert result.storage["counter"] == 5

    def test_should_fail_if_the_source_is_not_the_owner(self):
        value = 5
        storage = {"owner": owner, "counter": 0}

        with self.assertRaises(MichelsonRuntimeError) as context:
            self.contract.increment(value).interpret(storage=storage, source=alice)

        self.assertEqual(
            context.exception.args[-1].strip("\\").strip("'"),
            "Only owner can increment",
        )
