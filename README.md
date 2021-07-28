<img src="https://raw.githubusercontent.com/ant4g0nist/chinstrap/main/docs/images/logo.png" alt="Chinstrap" style="width:200px;"/>

[![Baked by ant4g0nist](https://img.shields.io/twitter/follow/ant4g0nist?style=social)](https://twitter.com/ant4g0nist)
[![docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://github.com/ant4g0nist/chinstrap/blob/main/docs/index.md)
[![PyPI](https://img.shields.io/pypi/v/chinstrap)](https://pypi.org/project/chinstrap/)

## Overview

**Chinstrap** is a development environment, testing framework and asset pipeline focused solely on Tezos, aiming to become swiss-army-knife for Tezos Smart Contract developers.

Chinstrap makes Tezos developers life easy by providing support for multiple contract compilations, tests, and originations on many public and private Tezos networks.

## Features

Chinstrap offers:
- End-to-end build cycle support for Creation, Compilation, Testing and Origination of Smart Contracts
- Local sandbox environment to develop and test contracts
- Support for writing tests in `Python` and testing with pytest
- Scriptable deployment & originations framework
- Originations Management for deploying to many public & private networks
- Interactive debug console to debug and directly communicate with contracts

## Why?
Here are several reasons why i built Chinstrap:
- Development framework that solely focuses on Tezos Smart Contract development
- Easy to use and everything in place already.
- Easy maintainance
- Extendable
- Designed focused solely to supprot writing contracts in `Python`, `SmartPy`
- Tests can also be coded in `Python`
- SmartPy is a regular python library bringing easy meta-programming faculties to smart contract development.

## Getting started

### Requirements
 * Python >= 3.7
 * Docker
 * [Homebrew](https://brew.sh/) needs to be installed.

```shell
$ brew tap cuber/homebrew-libsecp256k1
$ brew install libsodium libsecp256k1 gmp
```

### Installation

```shell
$ pip3 install chinstrap
```

or 

```shell
git clone https://github.com/ant4g0nist/chinstrap
cd chinstrap
python3 setup.py install
```

### Upgrade

if you installed chinstrap with pip3
```sh
pip3 install -U chinstrap
```

## Usage

~~~sh
$ chinstrap          

      _     _           _                   
  ___| |__ (_)_ __  ___| |_ _ __ __ _ _ __  
 / __| '_ \| | '_ \/ __| __| '__/ _` | '_ \ 
| (__| | | | | | | \__ \ |_| | | (_| | |_) |
 \___|_| |_|_|_| |_|___/\__|_|  \__,_| .__/ 
                                     |_|    


usage: chinstrap [-h] [--init] [--compile] [--create] [--debug] [--templates] [--develop] [--originate] [--reset] [--network NETWORK] [--test] [--sandbox] [--sandbox-stop] [--sandbox-detach]
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
  --test                Run PyTezos tests
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
~~~


### Quickstart

Here, we will explain the basics of creating a Chinstrap project and deploying a smart contract to a local sandbox.

#### Creating a project
First, we will create a boilerplate Chinstrap project in a new directory.

1) Create a new directory for your Chinstrap project:
```sh
mkdir Chocolates
cd Chocolates
```

2) Generate boilerplate project:
```sh
chinstrap --init
```

This command creates 3 new folders and a Chinstrap config file inside current directory. The project structure will look like this:
```sh
.
|____contracts
| |____Originations.py
| |____SampleContract.py
|____originations
| |____1_initial_originations.py
| |____2_samplecontract_origination.py
|____tests
| |____samplecontract.py
|____chinstrap_config.yaml
```

- `chinstrap_config.yaml` : Chinstrap configuration file
- `contracts/`            : Directory for SmartPy/Ligo contracts
- `originations/`         : Directory for scriptable deployment files
- `tests/`                : Directory for test files for testing your application and contracts

Open the project folder in a text editor like visual studio code.  

### contracts directory

`contracts/Originations.py` is a smart contract (written in SmartPy) that manages and updates the status of your deployed smart contracts. This file comes with every Chinstrap project, and is suggested not to edit. This keeps track of deployments to save the Gas Costs from redeployments.

`contracts/SampleContract.py` is a sample contract (written in SmartPy) that creates two entrypoints increment and decrement for storage type of `int`.

### originations directory
The scripts in `originations` directory are used to originate (deploy) a smart contract onto a selected network. The scripts in this folder start with an integer and are run in order i.e., so the file beginning with 2 will be run after the file beginning with 1.

`originations/1_initial_originations.py` file is the origination script for the `Originations` contract found in the `contracts/Originations.py` script. And similarly, `originations/2_samplecontract_origination.py` is the origination script for `SampleContract` found in the `contracts/SampleContract.py` script.

### tests directory

The tests for the contracts reside in `tests` directory. These tests are written in `Python` and Chinstrap uses `pytest` and `pytezos` to test the contracts.

## Demo

To compile the smart contracts:
```sh
$ chinstrap --compile
```

To originate (deploy) the smart contracts:
```sh
$ chinstrap --originate --network florencenet
```

To re-orignate (reset and deploy again) the smart contracts:

```sh
$ chinstrap --originate --network florencenet --reset
```

To start the local Flextesa sandbox:

```sh
$ chinstrap --sandbox
```

To start the chinstrap repl (debug):

```sh
$ chinstrap --debug --network florencenet
```

To download template contracts provided Smartpy:

```sh
$ chinstrap --templates
```

## Is Chinstrap finished?
- Not at all. I will provide as much support as needed and we can work together and add important changes and improvements on a regular basis.
- Pull requests are welcome

# TODO
- [ ] Improve documentation
- [ ] Improve Sandbox support
- [ ] Improve repl experience
- [ ] Add tests
- [ ] Add more test projects
- [ ] Add a homebrew formula

# References
- https://smartpy.io/reference.html

# Credits
- Truffle
- Baking-Bad
- logo by [@sengar23](https://github.com/sengar23)