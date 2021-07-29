# Chinstrap

![Chinstrap](https://raw.githubusercontent.com/ant4g0nist/chinstrap/main/docs/images/logo.png)

[![Baked by ant4g0nist](https://img.shields.io/twitter/follow/ant4g0nist?style=social)](https://twitter.com/ant4g0nist) [![docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://docs.chinstrap.io) [![PyPI](https://img.shields.io/pypi/v/chinstrap)](https://pypi.org/project/chinstrap/)

### Overview

**Chinstrap** is a development environment, testing framework, and asset pipeline focused solely on Tezos, aiming to become Swiss-Army-Knife for Tezos Smart Contract developers.

Chinstrap makes Tezos developers' life easy by providing support for multiple contract compilations, tests, and originations on many public and private Tezos networks.

### Features

Chinstrap offers:

* End-to-end build cycle support for Creation, Compilation, Testing and Origination of Smart Contracts
* Local sandbox environment to develop and test contracts
* Support for writing tests in `Python` and testing with `pytest`
* Scriptable deployment & originations framework
* Originations Management for deploying to many public & private networks
* Interactive debug console to debug and directly communicate with contracts

### Why?

Here are some reasons why I built Chinstrap:

* Development framework that solely focuses on Tezos Smart Contract development
* Easy to use and everything in place already.
* Easy maintenance
* Extendable
* Designed focused solely to support writing contracts in `Python`, `SmartPy`
* Tests can also be programmed in `Python`

### Getting started

#### Requirements

* Python &gt;= 3.7
* Docker
* [Homebrew](https://brew.sh/) needs to be installed.

```text
$ brew tap cuber/homebrew-libsecp256k1
$ brew install libsodium libsecp256k1 gmp
```

#### Installation

```text
$ pip3 install chinstrap
```

or

```text
git clone https://github.com/ant4g0nist/chinstrap
cd chinstrap
python3 setup.py install
```

#### Upgrade

if you installed chinstrap with pip3

```bash
pip3 install -U chinstrap
```

### Usage

```bash
$ chinstrap          

      _     _           _                   
  ___| |__ (_)_ __  ___| |_ _ __ __ _ _ __  
 / __| '_ \| | '_ \/ __| __| '__/ _` | '_ \ 
| (__| | | | | | | \__ \ |_| | | (_| | |_) |
 \___|_| |_|_|_| |_|___/\__|_|  \__,_| .__/ 
                                     |_|    


usage: main.py [-h] [--init] [--compile] [--create] [--debug] [--templates] [--develop] [--originate] [--reset] [--network NETWORK] [--test TEST] [--sandbox] [--sandbox-stop] [--sandbox-detach]
               [--sandbox-port SANDBOX_PORT] [--sandbox-protocol SANDBOX_PROTOCOL] [--accounts ACCOUNTS] [--account-balance ACCOUNT_BALANCE] [--version]

Chinstrap - a cute framework for developing Tezos Smart Contracts

optional arguments:
  -h, --help            show this help message and exit
  --init                Initialize new and empty Tezos SmartPy project
  --compile             Compile contract source files
  --create              Helper to create new contracts, origination and tests
  --debug               Interactively debug contracts.
  --templates           Download from templates provided SmartPy
  --develop             Open a console with a local development blockchain
  --originate           Run originations to deploy contracts
  --reset               Run originations to deploy contracts
  --network NETWORK     Show addresses for deployed contracts on each network
  --test TEST           Run [smartpy] or [pytest] tests.
  --sandbox             Start a Tezos local sandbox
  --sandbox-stop        Tezos local sandbox's RPC Port
  --sandbox-detach      Start a Tezos local sandbox and detach
  --sandbox-port SANDBOX_PORT
                        Tezos local sandbox's RPC Port
  --sandbox-protocol SANDBOX_PROTOCOL
                        Tezos local sandbox's RPC Port
  --accounts ACCOUNTS   Number of accounts to bootstrap on Tezos local sandbox
  --account-balance ACCOUNT_BALANCE
                        Amount of Tezos to deposit while bootstraping on Tezos local sandbox
  --version             Show version number and exit
```

### Quickstart

To compile the smart contracts:

```bash
$ chinstrap --compile
```

To originate \(deploy\) the smart contracts:

```bash
$ chinstrap --originate --network florencenet
```

To re-originate \(reset and deploy again\) the smart contracts:

```bash
$ chinstrap --originate --network florencenet --reset
```

To start the local Flextesa sandbox:

```bash
$ chinstrap --sandbox
```

To start the chinstrap repl \(debug\):

```bash
$ chinstrap --debug --network florencenet
```

To download template contracts provided Smartpy:

```bash
$ chinstrap --templates
```

### Is Chinstrap finished?

* Not at all. I will provide as much support as needed and we can work together and add important changes and improvements on a regular basis.
* Pull requests are welcome

## TODO

* [ ] Improve documentation
* [ ] Improve Sandbox support
* [ ] Improve repl experience
* [ ] Add tests
* [ ] Add more test projects
* [ ] Add a homebrew formula

## References

* [https://smartpy.io/reference.html](https://smartpy.io/reference.html)
* [https://pytezos.org/](https://pytezos.org/)
* [https://baking-bad.org/](https://baking-bad.org/)
* [https://michelson.baking-bad.org/](https://michelson.baking-bad.org/)

## Credits

* Truffle
* Baking-Bad
* logo by [@sengar23](https://github.com/sengar23)

