import os
import sys
import glob
import json
import time
import pathlib
import pytezos
from halo import Halo
from pytezos import ContractInterface
from chinstrap.Helpers import fatal, debug, printFormatted

currentContractName = None


def getContract(contractName):
    global currentContractName
    currentContractName = contractName
    return ContractInterface.from_file(
        f"build/contracts/{contractName}/step_000_cont_0_contract.tz"
    )


class Originations:
    def __init__(self, config, args):
        self.args = args
        self.config = config
        self.totalCost = 0
        self.initialWalletBalance = self.config.wallet.balance()

    def loadOriginationState(self):
        self.state = ChinstrapOriginationState(self.args.reset)

    def getOriginations(self):
        self.originations = sorted(
            glob.glob("./originations/*.py"),
            key=lambda x: int(os.path.basename(x).split("_")[0])
            if os.path.basename(x).split("_")[0].isdigit()
            else 0,
        )

    def getOrigination(self, file):
        if not os.path.exists(file):
            fatal(f"File {file} not found")

        self.originations = [file]

    def originate(self, origination):
        origination = pathlib.Path(origination).stem

        orig = __import__(origination)

        try:
            spinner = Halo(
                text=f"Origination {origination} in progress", spinner="dots"
            )
            spinner.start()

            storage, contract = orig.deploy(
                self.state, self.config.network, self.config.accounts
            )

            res = (
                self.config.wallet.origination(
                    script=dict(code=contract.code, storage=storage)
                )
                .autofill()
                .sign()
                .inject(_async=False)
            )

            txhash = res["hash"]

            spinner.succeed(
                text=f"{currentContractName}'s origination transaction at: {txhash}"
            )

            bakingRes = self.waitForBaking(txhash)
            addr = bakingRes["contents"][0]["metadata"]["operation_result"][
                "originated_contracts"
            ][0]
            if self.config.network.name in self.state.networks:
                self.state.networks[self.config.network.name].append(
                    {
                        "orignation_hash": txhash,
                        "address": addr,
                        "name": currentContractName,
                    }
                )
            else:
                self.state.networks[self.config.network.name] = [
                    {
                        "orignation_hash": txhash,
                        "address": addr,
                        "name": currentContractName,
                    }
                ]

            printFormatted(
                f"<ansigreen>✔</ansigreen> <ansired>{currentContractName}</ansired> address: \
<ansigreen>{addr}</ansigreen>"
            )

            return

        except pytezos.rpc.node.RpcError as e:
            if (
                "Not found: /chains/main/" in e.args[0]
                and self.config.network == "development"
            ):
                spinner.fail("\nPlease wait for the Sandbox to reach at-least level 20")
            else:
                spinner.fail(e)

        except Exception as e:
            spinner.fail(e)

        fatal("")

    def originateAll(self):
        sys.path.append("originations")
        for origination in self.originations:
            self.originate(origination)
            self.updateCosts()

        self.state.save()

    def waitForBaking(self, tx):
        spinner = Halo(text=f"Baking {tx}...", spinner="dots")
        spinner.start()
        while 1:
            try:
                res = self.config.wallet.shell.blocks[-5:].find_operation(tx)
                spinner.succeed(text="Baking successful!")
                return res
            except StopIteration:
                continue
            except pytezos.rpc.node.RpcError:
                debug("rpcerror: sleeping for sometime!")
                time.sleep(5)
                continue
            except Exception as e:
                fatal(e)

    def updateCosts(self):
        currentBalance = self.config.wallet.balance()
        self.totalCost += self.initialWalletBalance - currentBalance
        self.initialWalletBalance = currentBalance

    def showCosts(self):
        printFormatted(
            f"<ansigreen>✔</ansigreen> Total Cost of originations:  \
<ansired>ꜩ</ansired> <ansigreen>{self.totalCost}</ansigreen>"
        )


class ChinstrapOriginationState:
    def __init__(self, reset) -> None:
        if reset or not os.path.exists("./build/.state.json"):
            with open("./build/.state.json", "w") as f:
                f.write(
                    """{
  "chinstrap": {
    "networks": {

    }
  }
}"""
                )
        with open("./build/.state.json", "r") as f:
            state = json.loads(f.read())

        self.networks = state["chinstrap"]["networks"]

    def save(self):
        res = {"chinstrap": {"networks": self.networks}}

        with open("./build/.state.json", "w") as f:
            f.write(json.dumps(res))
