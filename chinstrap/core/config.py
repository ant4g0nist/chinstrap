import yaml
from pytezos import pytezos
from chinstrap import Helpers

# from chinstrap.core.pytezos import pytezos
from chinstrap.Helpers import convertYamlToObject
from chinstrap.Helpers import ensureCurrentDirectoryIsChinstrapProject


class Config:
    def __init__(self, network="development", compileFlag=False) -> None:
        ensureCurrentDirectoryIsChinstrapProject()

        with open("./chinstrap-config.yml", "r") as f:
            confData = yaml.safe_load(f)
            self.config = convertYamlToObject(confData).chinstrap

            if compileFlag:
                self.compiler = self.config.compiler
                self.compiler.lang = self.compiler.lang.lower()

            elif network == "development":
                self.network = self.config.network.development
                self.network.name = "development"

            elif network == "hangzhounet":
                self.network = self.config.network.hangzhounet
                self.network.name = "hangzhounet"

            elif network == "mainnet":
                self.network = self.config.network.mainnet
                self.network.name = "mainnet"

            elif network == "ithacanet":
                self.network = self.config.network.ithacanet
                self.network.name = "ithacanet"

        if not compileFlag:
            msg = f"Using <ansiyellow><b>{self.network.name}</b></ansiyellow> network"
            Helpers.printFormatted(msg)

            if self.network.accounts:
                self.loadAccounts()

            return

    def loadAccounts(self):
        self.accounts = []
        try:
            keyFile = self.network.accounts[0].privateKeyFile
            with open(keyFile, "r") as f:
                self.key = f.read().rstrip("\n")

            self.wallet = pytezos.using(shell=f"{self.network.host}", key=self.key)

            for i in self.network.accounts:
                self.loadPrivateKeyFromFile(i.privateKeyFile)

        except Exception as e:
            print(e)
            Helpers.fatal(f"Exception occured while loading accounts! {e}")

    def loadPrivateKeyFromFile(self, keyFile):
        with open(keyFile, "r") as f:
            key = f.read().rstrip("\n")

        self.loadPrivateKey(key)

    def loadPrivateKey(self, key):
        try:
            wallet = pytezos.using(shell=f"{self.network.host}", key=key)
        except pytezos.rpc.node.RpcError:
            Helpers.fatal(
                f"Failed to connect to {self.network.host}. Try again in sometime!"
            )

        Helpers.printFormatted(
            f"""Loaded wallet <ansiyellow><b>{wallet.key.public_key_hash()}</b> \
            </ansiyellow>. Balance: <ansigreen><b>{wallet.balance()}</b></ansigreen>\n"""
        )
        self.accounts.append(wallet)

    def save(self):
        config = {"chinstrap": {"networks": {}, "compiler": {}}}

        for i, v in self.config.__dict__["networks"].__dict__.items():
            if i[0] != "_":
                network = {
                    "host": v.__dict__["host"],
                    "port": v.__dict__["port"],
                    "accounts": [],
                }
                accounts = []
                if "accounts" in v.__dict__.keys():
                    for d in v.__dict__["accounts"]:
                        for j, k in d.__dict__.items():
                            if j[0] != "_":
                                accounts.append({j: k})

                network["accounts"] = accounts
                config["chinstrap"]["networks"][i] = network

        with open("./chinstrap_config.yaml", "w") as f:
            f.write(yaml.safe_dump(config))
