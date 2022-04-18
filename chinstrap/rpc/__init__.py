from pytezos.rpc.query import RpcQuery, RpcNode
from pytezos.rpc import ShellQuery, RpcNode

server = f"https://api.tzkt.io/v1"

# class Account:
#     def __init__(self, address) -> None:
#         self.address  = address
#         self.getAccount()

#     def getAccount(self):
#         url = f"{server}/accounts/{self.address}"
#         response = requests.get(url)
#         if response.status_code==200:
#             # print(response.json())
#             pass
#         else:
#             print(Errors(response.json()))


# class Errors:
#     def __init__(self, error) -> None:
#         self.code   = error["code"]
#         self.errors = error["errors"]

#     def __str__(self) -> str:
#         error = ""
#         for i in self.errors.items():
#             error += f"{i[0]}: {i[1]}"
#         return error


class AccountRPC(RpcQuery, path=""):
    def __init__(self, address):
        # super().__init__(node, path, params, timeout)
        # shell = ShellQuery(RpcNode('https://mainnet-tezos.giganode.io/'))
        # path = "/chains/{}/blocks/{}/context/contracts/"+address+"/balance"

        # return self().get('address', {address})
        # def getBalance(self, address):
        #     # url = f"{self.server}/chains/{self.chain}/blocks/{self.block}/context/contracts/{address}/balance"
        #     return

        pass
