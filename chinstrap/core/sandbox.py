import halo
import json
import docker
import pathlib
from enum import Enum
from chinstrap import Helpers
from chinstrap.Helpers import ensureCurrentDirectoryIsChinstrapProject, fatal
from chinstrap.core.container import getDockerClient, pullImage
from chinstrap.core.container import runCommandInContainer

FlextesaImage = "oxheadalpha/flextesa"
FlextesaImageTag = "latest"

class SandboxProtocols(Enum):
    hangzhou    = "Hangzhou"
    ithaca      = "Ithaca"
    alpha       = "Alpha"

    def __str__(self):
        return self.value

class Sandbox:
    def __init__(self, args) -> None:
        self.args = args
        self.state = {'accounts':{}}
        
    def download(self):
        spinner = halo.Halo(text=f'Setting up Flextesa sandbox. This might take a while!', spinner="dots")
        spinner.start()
        
        suc, msg = pullImage(FlextesaImage, FlextesaImageTag)
        if not suc:
            spinner.fail(f"Failed to install compiler. {msg}")
            return
        
        spinner.succeed("Flextesa sandbox ready to use")

    def run(self):
        self.generateAccounts()
        self.launchSandbox()

    def halt(self):
        ensureCurrentDirectoryIsChinstrapProject()

        spinner = halo.Halo(text=f'Halting Tezos sandbox...', spinner="dots")
        spinner.start()

        path = pathlib.Path('build/chinstrap_sandbox_state')
        if path.exists():
            with open(path,'r') as f:
                state = json.loads(f.read())
            
            client = getDockerClient()
            
            try:
                containerId = state["containerId"]
                self.container = client.containers.get(containerId)
                self.container.remove(force=True)
            except Exception as e:
                print(e)
        
        spinner.succeed("Halted the sandbox")

    def generateAccounts(self):
        
        spinner = halo.Halo(text=f'Creating {self.args.num_of_accounts} accounts...', spinner="dots")
        spinner.start()
        
        self.accounts = [ ]

        for i in range(self.args.num_of_accounts):
            cmd = f"flextesa key {i}"
            container = runInFlextesaContainer(cmd, detach=False)
            for line in container.logs(stream=True):
                account = line.decode('utf-8').rstrip()
                self.accounts.append(f"{account}@{self.args.minimum_balance*1_000_000}")

            container.remove()

        spinner.succeed( text=f"Accounts created!\n")

        print(f'\nid {"":16} address {"":32} publicKey {"":46} privateKey')
        for account in self.accounts:
            name, publicKeyHash, address, privateKey = account.split(",")
            print(f" {Helpers.RED}{name: <4}{Helpers.RST}{address:36} {Helpers.GRN}{publicKeyHash}{Helpers.RST} {Helpers.YEL}{privateKey.replace('unencrypted:','').split('@')[0]}{Helpers.RST}")
            self.state['accounts'][name] = {'address':address, 'private':privateKey.replace('unencrypted:','').split('@')[0]}

    def launchSandbox(self):
        spinner = halo.Halo(text=f"Starting sandbox", spinner="dots")
        spinner.start()
        
        command = f'''flextesa mini-net --root "/tmp/mini-box" --size 1 --set-history-mode N000:archive --number-of-b 5 --time-b 5 --until-level 200_000_000 --protocol-kind {self.args.protocol.value} --keep-root '''
        for account in self.accounts:
            command += f' --add-bootstrap-account="{account}" --no-daemons-for={account.split(",")[0]} '

        client = getDockerClient()

        self.container = client.containers.create(image=f'{FlextesaImage}:{FlextesaImageTag}', command=command, detach=self.args.detach, auto_remove=False, ports={'20000': self.args.port})
        self.container.start()

        self.state['containerId'] = self.container.id

        with open('build/chinstrap_sandbox_state', 'w') as f:
            f.write(json.dumps(self.state))

        spinner.succeed( text=f"Sandbox up and running!\n")

        self.started = False
        if not self.args.detach:
            print("*"*20)
            for line in self.container.logs(stream=True):
                op = line.decode('utf-8').rstrip()
                # if develop and 'Network started' in op:
                #     self.started = True
                #     return
                print(op)
                # if not develop:
                #     print(op)
                    

def runInFlextesaContainer(command, detach=True):
    try:
        return runCommandInContainer(FlextesaImage, FlextesaImageTag, command, [], detach, {}, False)
    except docker.errors.ImageNotFound:
        fatal('\nFlextesa sandbox docker image not found')

    except docker.errors.NotFound:
        fatal("docker.errors.NotFound")
