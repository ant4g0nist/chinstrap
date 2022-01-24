"""
Welcome to PyTezos!

To start playing with the Tezos blockchain you need to get a PyTezosClient instance.
Just type:

>>> from chinstrap.core.pytezos import pytezos
>>> pytezos

And follow the interactive documentation.
"""

from chinstrap.core.pytezos.client import PyTezosClient
from chinstrap.core.pytezos.contract.interface import Contract, ContractInterface
from chinstrap.core.pytezos.crypto.key import Key
from chinstrap.core.pytezos.logging import logger
from chinstrap.core.pytezos.michelson.forge import forge_micheline, unforge_micheline
from chinstrap.core.pytezos.michelson.format import micheline_to_michelson
from chinstrap.core.pytezos.michelson.micheline import MichelsonRuntimeError
from chinstrap.core.pytezos.michelson.parse import michelson_to_micheline
from chinstrap.core.pytezos.michelson.types.base import MichelsonType, Undefined
from chinstrap.core.pytezos.michelson.types.core import Unit

__version__ = '3.3.4'

pytezos = PyTezosClient()
