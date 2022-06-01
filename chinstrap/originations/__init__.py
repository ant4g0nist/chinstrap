import os
import sys
import glob
import json
import time
import pathlib
import pytezos
from halo import Halo
from pprint import pformat
from chinstrap import helpers
from datetime import datetime
from pytezos import ContractInterface
from chinstrap.helpers import fatal, debug, printFormatted, calculateHash

contractHash = None
currentContractName = None


def getContract(contractName):
    global contractHash
    global currentContractName
    currentContractName = contractName
    contractPath = f"build/contracts/{contractName}/step_000_cont_0_contract.tz"

    if not pathlib.Path(contractPath).exists():
        return None

    with open(contractPath) as f:
        contractHash = calculateHash(f.read().encode())

    return ContractInterface.from_file(contractPath)


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

    def ensureIsNotOriginated(self, spinner, force):
        """
        Checks if the current contract is already originated
        """
        if (
            self.config.network.name in self.state.networks
            and contractHash in self.state.networks[self.config.network.name].keys()
        ):
            origination = self.state.networks[self.config.network.name][contractHash]
            # TODO: check on the network if the address exists
            try:
                self.config.wallet.contract(origination["address"])
                if not force:
                    spinner.succeed(
                        f"Contract {currentContractName} is already \
originated at {origination['address']} on {origination['date']}"
                    )

                    return True, origination

            except Exception:
                pass

            return True, origination

        return False, ""

    def originate(self, origination):
        origination = pathlib.Path(origination).stem

        orig = __import__(origination)

        try:
            spinner = Halo(
                text=f"Origination {origination} in progress", spinner="dots"
            )
            spinner.start()

            try:
                storage, contract = orig.deploy(
                    self.state, self.config.network, self.config.accounts
                )
            except Exception as e:
                contractPath = (
                    f"build/contracts/{currentContractName}/step_000_cont_0_contract.tz"
                )
                if not pathlib.Path(contractPath).exists():
                    spinner.fail(
                        f"Failed to run {origination}. Unable to find \
{currentContractName} in contracts."
                    )
                    return

                spinner.fail(str(e))
                return

            originated, _origination = self.ensureIsNotOriginated(
                spinner, self.args.force
            )
            if originated:
                addr = _origination["address"]
                txhash = _origination["orignation_hash"]
                spinner.succeed(
                    text=f"{currentContractName}'s origination transaction at: {txhash}"
                )
                printFormatted(
                    f"<ansigreen>✔</ansigreen> <ansired>{currentContractName}</ansired> address: \
<ansigreen>{addr}</ansigreen>"
                )
                return

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
                self.state.networks[self.config.network.name][contractHash] = {
                    "orignation_hash": txhash,
                    "address": addr,
                    "name": currentContractName,
                    "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                }
            else:
                self.state.networks[self.config.network.name] = {
                    contractHash: {
                        "orignation_hash": txhash,
                        "address": addr,
                        "name": currentContractName,
                        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                    }
                }

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
                spinner.fail(pformat(e))

        except Exception as e:
            spinner.fail(e)

        fatal("")

    def originateAll(self):
        sys.path.append("originations")

        if len(self.originations) == 0:
            fatal("No originations found in originations folder")

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
        if reset or not os.path.exists("./build/chinstrap_deployments.json"):
            with open("./build/chinstrap_deployments.json", "w") as f:
                f.write(
                    """{
  "chinstrap": {
    "networks": {

    }
  }
}"""
                )
        with open("./build/chinstrap_deployments.json", "r") as f:
            state = json.loads(f.read())

        self.networks = state["chinstrap"]["networks"]

    def save(self):
        res = {"chinstrap": {"networks": self.networks}}

        with open("./build/chinstrap_deployments.json", "w") as f:
            f.write(json.dumps(res))

    def showOriginations(self, network):
        if network in self.networks:
            originations = self.networks[network]
            title = f'\nNetwork {"":16} Address {"":32} Date {"":36} Tx {"":32} Name '
            print("_" * len(title))
            print(title)
            for _hash, origination in originations.items():
                # TODO:
                print(
                    f"{helpers.YEL}{network:16} {helpers.RED}{origination['address']:32}\
 {helpers.WHT}{origination['date']:32} \
{helpers.GRN}{origination['orignation_hash']:46} {helpers.YEL}{origination['name']}{helpers.RST}"
                )
            print("_" * len(title))
