import os
import halo
import json
import docker
import pathlib
from enum import Enum
from chinstrap import helpers
from chinstrap.helpers import IsChinstrapProject, fatal
from chinstrap.helpers.container import (
    getDockerClient,
    pullImage,
    runCommandInAlreadyRunningContainer,
)
from chinstrap.helpers.container import runCommandInContainer

FlextesaImage = "oxheadalpha/flextesa"
FlextesaImageTag = "latest"

CryptoNames = [
    "Alice",
    "Bob",
    "Carol",
    "Chuck",
    "Craig",
    "Dan",
    "Dave",
    "David",
    "Erin",
    "Eve",
    "Faythe",
    "Frank",
    "Grace",
    "Heidi",
    "Judy",
    "Mallory",
    "Michael",
    "Mike",
    "Niaj",
    "Olivia",
    "Oscar",
    "Peggy",
    "Pat",
    "Sybil",
    "Trent",
    "Ted",
    "Trudy",
    "Victor",
    "Vanna",
    "Walter",
    "Wendy",
]


def giveMeAName(index):
    if index < len(CryptoNames):
        return CryptoNames[index]
    else:
        return f"{CryptoNames[index%len(CryptoNames)]}{int(index/len(CryptoNames))}"


class SandboxProtocols(Enum):
    hangzhou = "Hangzhou"
    ithaca = "Ithaca"
    alpha = "Alpha"

    def __str__(self):
        return self.value


class Sandbox:
    def __init__(self, args) -> None:
        self.args = args

    def initialize(self):
        self.state = {"accounts": {}, "port": self.args.port}

    def download(self):
        spinner = halo.Halo(
            text="Setting up Flextesa sandbox. This might take a while!",
            spinner="dots",
        )
        spinner.start()

        suc, msg = pullImage(FlextesaImage, FlextesaImageTag)
        if not suc:
            spinner.fail(f"Failed to install compiler. {msg}")
            return

        spinner.succeed("Flextesa sandbox ready to use")

    @staticmethod
    @IsChinstrapProject()
    def dumpSandboxState(state):
        with open("build/chinstrap_sandbox_state", "w") as f:
            f.write(json.dumps(state))

    @staticmethod
    @IsChinstrapProject()
    def getSandboxState(spinner=None):
        path = pathlib.Path("build/chinstrap_sandbox_state")
        if path.exists():
            with open(path, "r") as f:
                return json.loads(f.read())
        else:
            if spinner:
                spinner.fail("Please run the command form inside Chinstrap project")

        return False

    @staticmethod
    @IsChinstrapProject()
    def isRunning(port=None):
        state = Sandbox.getSandboxState()

        if not state:
            return False

        try:
            client = getDockerClient()
            statePort = state["port"]
            containerId = state["containerId"]
            container = client.containers.get(containerId)
            if port == statePort:
                print(
                    f"Sandbox is already {container.status} \
on port: {helpers.RED}{port}{helpers.RST}"
                )
            else:
                print(
                    f"Sandbox is already {container.status} \
on different port: {helpers.RED}{port}{helpers.RST}"
                )
            return True

        except Exception:
            return False

    @IsChinstrapProject()
    def run(self):
        if not Sandbox.isRunning(self.args.port):
            self.generateAccounts()
            os.makedirs("build/", exist_ok=True)
            self.launchSandbox()

    @staticmethod
    @IsChinstrapProject()
    def listAccounts():
        state = Sandbox.getSandboxState()
        if not state:
            return False
        accounts = state["accounts"]
        title = f'\nname {"":32} address {"":32} publicKey {"":46} privateKey'
        print("_" * len(title))
        print(title)
        print("-" * len(title))
        for name in accounts:
            address = accounts[name]["address"]
            privateKey = accounts[name]["privateKey"]
            publicKeyHash = accounts[name]["publicKey"]
            print(
                f" {helpers.RED}{name: <16}{helpers.RST}{address:36} \
{helpers.GRN}{publicKeyHash}{helpers.RST} {helpers.YEL}\
{privateKey}{helpers.RST}"
            )

        print("_" * len(title))

    @IsChinstrapProject()
    def halt(self):
        spinner = halo.Halo(text="Halting Tezos sandbox...", spinner="dots")
        spinner.start()

        state = Sandbox.getSandboxState(spinner)

        if not state:
            return False

        client = getDockerClient()

        try:
            containerId = state["containerId"]
            self.container = client.containers.get(containerId)
            self.container.remove(force=True)

        except Exception as e:
            print(e)

        state["containerId"] = ""
        Sandbox.dumpSandboxState(state)
        spinner.succeed("Halted the sandbox")

    def generateAccount(self, index=0):
        name = giveMeAName(index)
        cmd = f"flextesa key {name}"
        container = runInFlextesaContainerCli(cmd, detach=False)

        for line in container.logs(stream=True):
            line = line.decode("utf-8").rstrip()
            name = line.split(",")[0]
            privateKey = line.split(",")[-1]

        container.remove()

        return name, privateKey, line

    def generateAccounts(self):
        spinner = halo.Halo(
            text=f"Creating {self.args.num_of_accounts} accounts...", spinner="dots"
        )
        spinner.start()

        self.accounts = []

        for i in range(self.args.num_of_accounts):
            name, privateKey, account = self.generateAccount(i)
            self.accounts.append(f"{account}")

        spinner.succeed(text="Accounts created!\n")

        title = f'\nname {"":32} address {"":32} publicKey {"":46} privateKey'
        print("_" * len(title))
        print(title)
        print("-" * len(title))

        for account in self.accounts:
            name, publicKeyHash, address, privateKey = account.split(",")
            print(
                f" {helpers.RED}{name: <16}{helpers.RST}{address:36} \
{helpers.GRN}{publicKeyHash}{helpers.RST} {helpers.YEL}\
{privateKey.replace('unencrypted:','').split('@')[0]}{helpers.RST}"
            )
            self.state["accounts"][name] = {
                "address": address,
                "publicKey": publicKeyHash,
                "privateKey": privateKey.replace("unencrypted:", "").split("@")[0],
            }

        print("-" * len(title))
        print(
            f"{helpers.RED}WARNING:{helpers.RST} Please do not use these accounts on mainnet!"
        )

    def launchSandbox(self):
        spinner = halo.Halo(text="Starting sandbox", spinner="dots")
        spinner.start()

        command = f"""flextesa mini-net --root "/tmp/mini-box" --size 1 --set-history-mode N000:archive \
--number-of-b 5 --time-b 5 --until-level 200_000_000 \
--protocol-kind {self.args.protocol.value} --keep-root \
--balance-of-bootstrap-accounts=tz:2_000_000.42 """

        for account in self.accounts:
            command += f' --add-bootstrap-account="{account}"@{self.args.minimum_balance*1_000_000} \
--no-daemons-for={account.split(",")[0]} '

        client = getDockerClient()

        self.container = client.containers.create(
            image=f"{FlextesaImage}:{FlextesaImageTag}",
            command=command,
            detach=self.args.detach,
            auto_remove=False,
            ports={"20000": self.args.port},
        )
        try:
            self.container.start()
        except Exception as e:
            if "port is already allocated" in str(e):
                spinner.fail(f"\nPort {self.args.port} already in use")
            else:
                spinner.fail(e)

            self.container.remove(force=True)
            fatal("")

        self.state["containerId"] = self.container.id

        Sandbox.dumpSandboxState(self.state)

        self.started = False

        for line in self.container.logs(stream=True):
            op = line.decode("utf-8").rstrip()
            level = op.split("attempt ")[-1].split("/")[0]
            if "attempt " in op:
                spinner.text = f"Flextesa: {op}"
                if int(level) >= 20 and not self.started:
                    spinner.succeed(
                        text=f"Sandbox is at level: {level} and ready for use!\n"
                    )
                    self.started = True
                    if self.args.detach:
                        break


def runTezosClient(command, container):
    # tezos-client
    command = f"tezos-client {command}"
    return runCommandInAlreadyRunningContainer(container, command)


def runInFlextesaContainerCli(command, detach=True):
    try:
        return runCommandInContainer(
            FlextesaImage, FlextesaImageTag, command, [], detach, {}, False
        )
    except docker.errors.ImageNotFound:
        fatal("\nFlextesa sandbox docker image not found")

    except docker.errors.NotFound:
        fatal("docker.errors.NotFound")
