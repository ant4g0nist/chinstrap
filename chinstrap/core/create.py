import glob
from enum import Enum


class CreateOptions(Enum):
    test = "test"
    contract = "contract"
    origination = "origination"

    def __str__(self):
        return self.value


class Create:
    def __init__(self, args, config) -> None:
        if args.type == "origination":
            Create.createOrigination(args.name)

        else:
            if config.compiler.lang == "jsligo":
                Create.createJsLigo(args.name, args.type)

            elif config.compiler.lang == "reasonligo":
                Create.createReasonLigo(args.name, args.type)

            elif config.compiler.lang == "cameligo":
                Create.createCameLigo(args.name, args.type)

            elif config.compiler.lang == "pascaligo":
                Create.createPascaLigo(args.name, args.type)

            elif config.compiler == "smartpy":
                if args.type == CreateOptions.contract:
                    Create.createSmartpy(args.name, args.type)

                elif args.type == CreateOptions.test:
                    Create.createPyTest(args.name)

    @staticmethod
    def createPyTest(name):
        """
        Create a barebone contract
        """
        bones = """
from unittest import TestCase, skip
from pytezos import MichelsonRuntimeError, ContractInterface
michelson_contract = "./build/contracts/Contract/Contract.tz"

class TestCounterContract(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counterContract = ContractInterface.from_file(michelson_contract)

    def test_storage_counter_is_zero(self):
        self.assertEqual(result.storage["counter"], 0)
        """
        with open(f"./tests/{name}.py", "w") as f:
            f.write(bones)

    @staticmethod
    def createOrigination(name):
        """
        Create a barebone contract
        """
        bones = """from chinstrap.chinstrapCore import getContract

def deploy(chinstrapState, network, accounts):
    contract = getContract("ContractName")
    initial_storage = contract.storage.encode(0)
    return initial_storage, contract"""

        count = glob.glob("./originations/*.py").__len__()
        origination = "".join(x for x in name.title() if x.isalpha())
        with open(f"./originations/{count+1}_{origination.lower()}.py", "w") as f:
            f.write(bones)

    @staticmethod
    def createSmartpy(name):
        contract = """import smartpy as sp

class SampleContract(sp.Contract):
    def __init__(self, value):
        self.init_type(sp.TRecord(counter = sp.TInt))
        self.init(counter = value)

    @sp.entry_point
    def increment(self, value):
        self.data.counter += value"""
        with open(f"./contracts/{name}.py", "w") as f:
            f.write(contract)

    @staticmethod
    def createJsLigo(name, type):
        if type == CreateOptions.contract:
            content = """type storage = int;

type parameter =
  ["Increment", int]
| ["Decrement", int]
| ["Reset"];

type return_ = [list<operation>, storage];

let main = ([action, store]: [parameter, storage]) : return_ => {
  return [
    list([]) as list<operation>,
    match(action, {
      Increment: (n: int) => store + n,
      Decrement: (n: int) => store - n,
      Reset:     ()       => 0
    })
  ];
};"""

        elif type == CreateOptions.test:
            content = """#include "./contracts/SampleContract.jsligo"
let x = Test.reset_state ( 5 as nat, list([]) as list <tez> );"""

        with open(f"./{type}s/{name}.jsligo", "w") as f:
            f.write(content)

    @staticmethod
    def createPascaLigo(name, type):
        if type == CreateOptions.contract:
            content = """type storage is int

type parameter is
  Increment of int
| Decrement of int
| Reset

type return is list (operation) * storage

function main (const action : parameter; const store : storage) : return is
 ((nil : list (operation)),
  case action of
    Increment (n) -> store + n
  | Decrement (n) -> store - n
  | Reset         -> 0
 end)"""

        elif type == CreateOptions.test:
            content = """#include "./contracts/SampleContract.ligo"
let x = Test.reset_state ( 5 as nat, list([]) as list <tez> );"""

        with open(f"./{type}s/{name}.ligo", "w") as f:
            f.write(content)

    @staticmethod
    def createReasonLigo(name, type):
        if type == CreateOptions.contract:
            content = """type storage = int;

type parameter =
  Increment (int)
| Decrement (int)
| Reset;

type return = (list (operation), storage);

let main = ((action, store): (parameter, storage)) : return => {
  (([] : list (operation)),
  (switch (action) {
   | Increment (n) => store + n
   | Decrement (n) => store - n
   | Reset         => 0}));
};"""

        elif type == CreateOptions.test:
            content = """#include "./contracts/SampleContract.religo"
let x = Test.reset_state ( 5 as nat, list([]) as list <tez> );"""

        with open(f"./{type}s/{name}.religo", "w") as f:
            f.write(content)

    @staticmethod
    def createCameLigo(name, type):
        if type == CreateOptions.contract:
            content = """type storage = int

type parameter =
  Increment of int
| Decrement of int
| Reset

type return = operation list * storage

let main (action, store : parameter * storage) : return =
  ([] : operation list),
  (match action with
     Increment n -> store + n
   | Decrement n -> store - n
   | Reset       -> 0)"""

        elif type == CreateOptions.test:
            content = """#include "./contracts/SampleContract.mligo"
let x = Test.reset_state ( 5 as nat, list([]) as list <tez> );"""

        with open(f"./{type}s/{name}.mligo", "w") as f:
            f.write(content)
