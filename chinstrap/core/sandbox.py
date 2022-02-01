import halo
import rich
import json
import docker
import pathlib
from enum import Enum
from chinstrap import Helpers
from chinstrap.Helpers import ensureCurrentDirectoryIsChinstrapProject, fatal
from chinstrap.core.container import (
    getDockerClient,
    pullImage,
    runCommandInAlreadyRunningContainer,
)
from chinstrap.core.container import runCommandInContainer

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
        return f"account_{index}"


class SandboxProtocols(Enum):
    hangzhou = "Hangzhou"
    ithaca = "Ithaca"
    alpha = "Alpha"

    def __str__(self):
        return self.value


class Sandbox:
    def __init__(self, args) -> None:
        self.args = args
        self.state = {"accounts": {}}

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

    def run(self, detach=False):
        self.generateAccounts()
        self.launchSandbox(detach)

    def halt(self):
        ensureCurrentDirectoryIsChinstrapProject()

        spinner = halo.Halo(text="Halting Tezos sandbox...", spinner="dots")
        spinner.start()

        path = pathlib.Path("build/chinstrap_sandbox_state")
        if path.exists():
            with open(path, "r") as f:
                state = json.loads(f.read())

            client = getDockerClient()

            try:
                containerId = state["containerId"]
                self.container = client.containers.get(containerId)
                self.container.remove(force=True)
            except Exception as e:
                print(e)
        else:
            spinner.fail("Please run the command form inside Chinstrap project")
            return 1
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

        print(f'\nname {"":32} address {"":32} publicKey {"":46} privateKey')
        for account in self.accounts:
            name, publicKeyHash, address, privateKey = account.split(",")
            print(
                f" {Helpers.RED}{name: <16}{Helpers.RST}{address:36} \
{Helpers.GRN}{publicKeyHash}{Helpers.RST} {Helpers.YEL}\
{privateKey.replace('unencrypted:','').split('@')[0]}{Helpers.RST}"
            )
            self.state["accounts"][name] = {
                "address": address,
                "private": privateKey.replace("unencrypted:", "").split("@")[0],
            }

    def launchSandbox(self, detach=False):
        spinner = halo.Halo(text="Starting sandbox", spinner="dots")
        spinner.start()

        command = f"""flextesa mini-net --root "/tmp/mini-box" --size 1 --set-history-mode N000:archive \
--number-of-b 5 --time-b 5 --until-level 200_000_000 \
--protocol-kind {self.args.protocol.value} --keep-root """

        client = getDockerClient()

        self.container = client.containers.create(
            image=f"{FlextesaImage}:{FlextesaImageTag}",
            command=command,
            detach=self.args.detach,
            auto_remove=False,
            ports={"20000": self.args.port},
        )
        self.container.start()

        self.state["containerId"] = self.container.id

        with open("build/chinstrap_sandbox_state", "w") as f:
            f.write(json.dumps(self.state))

        spinner.succeed(text="Sandbox up and running!\n")

        self.started = False
        print("*" * 20)
        for line in self.container.logs(stream=True):
            op = line.decode("utf-8").rstrip()
            if "Network started" in op:
                for account in self.accounts:
                    name = account.split(",")[0]
                    privateKey = account.split(",")[-1]
                    cmd = f"import secret key {name} {privateKey}"
                    runTezosClient(cmd, self.container)

                    if detach:
                        break

            rich.print(op)


def runTezosClient(command, container):
    # tezos-client
    # try:
    command = f"tezos-client {command}"
    return runCommandInAlreadyRunningContainer(container, command)
    # except docker.errors.ImageNotFound:
    #     fatal('\nContainer not running')

    # except docker.errors.NotFound:
    #     fatal("docker.errors.NotFound")


def runInFlextesaContainerCli(command, detach=True):
    try:
        return runCommandInContainer(
            FlextesaImage, FlextesaImageTag, command, [], detach, {}, False
        )
    except docker.errors.ImageNotFound:
        fatal("\nFlextesa sandbox docker image not found")

    except docker.errors.NotFound:
        fatal("docker.errors.NotFound")
