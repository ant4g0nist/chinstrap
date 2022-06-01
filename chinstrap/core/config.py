import json
import yaml
import pathlib
from pytezos import pytezos
from chinstrap import helpers

# from chinstrap.core.pytezos import pytezos
from chinstrap.helpers import convertYamlToObject
from chinstrap.helpers import IsChinstrapProject


class Config:
    @IsChinstrapProject()
    def __init__(self, network="development", compileFlag=False) -> None:
        with open("./chinstrap-config.yml", "r") as f:
            confData = yaml.safe_load(f)
            self.config = convertYamlToObject(confData).chinstrap

            if compileFlag:
                self.compiler = self.config.compiler
                self.compiler.lang = self.compiler.lang.lower()

            if network == "development":
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
            helpers.printFormatted(msg)

        if self.network.accounts:
            self.loadAccounts(compileFlag)

    def loadAccounts(self, compileFlag=False):
        self.accounts = []
        try:
            keyFile = self.network.accounts[0].privateKeyFile
            self.key = self.getKeyFromFile(keyFile)

            self.wallet = pytezos.using(shell=f"{self.network.host}", key=self.key)

            for i in self.network.accounts:
                self.loadPrivateKeyFromFile(i.privateKeyFile, compileFlag)

        except Exception as e:
            helpers.error("Exception occurred while loading accounts!")
            print(e)
            helpers.fatal("")

    def loadPrivateKeyFromFile(self, keyFile, compileFlag=False):
        key = self.getKeyFromFile(keyFile)
        self.loadPrivateKey(key, compileFlag)

    def loadPrivateKey(self, key, compileFlag=False):
        try:
            wallet = pytezos.using(shell=f"{self.network.host}", key=key)
        except pytezos.rpc.node.RpcError:
            helpers.fatal(
                f"Failed to connect to {self.network.host}. Try again in sometime!"
            )

        if not compileFlag:
            helpers.printFormatted(
                f"""Loaded wallet <ansiyellow><b>{wallet.key.public_key_hash()}</b> \
    </ansiyellow>. Balance: <ansired>ꜩ</ansired> <ansigreen><b>\
{wallet.balance()}</b></ansigreen>\n"""
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

    def getKeyFromFile(self, file):
        if not pathlib.Path(file).exists():
            helpers.fatal(f"Provided account file {file} missing!")

        with open(file, "r") as f:
            key = f.read().rstrip("\n")

        try:
            return json.loads(key)
        except Exception:
            return key

    def __str__(self):
        msg = ""
        msg += f"Network  : {helpers.RED}{self.network.name}{helpers.RST}\n"
        msg += f"Host     : {helpers.YEL}{self.network.host}{helpers.RST}\n"
        msg += f"Account  : {helpers.GRN}{self.wallet.key.public_key_hash()}{helpers.RST}\n"
        msg += f"Balance  : {helpers.RED}ꜩ {helpers.GRN}{self.wallet.balance()}{helpers.RST}\n"
        msg += f"Compiler : {helpers.RED}{self.compiler.lang}{helpers.RST}\n"
        return msg
