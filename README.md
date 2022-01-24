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
* Node.js
* [Homebrew](https://brew.sh/) needs to be installed.

```bash
$ brew tap cuber/homebrew-libsecp256k1
$ brew install libsodium libsecp256k1 gmp
```

#### Installation

```bash
$ pip3 install chinstrap
```

or

```bash
git clone https://github.com/ant4g0nist/chinstrap
cd chinstrap
python3 setup.py install
```

or using Docker image available at https://hub.docker.com/r/ant4g0nist/chinstrap/tags

```bash
docker pull ant4g0nist/chinstrap
docker run -v `pwd`:/home --rm -it ant4g0nist/chinstrap
```

or using Dockerfile from the repo

```bash
git clone https://github.com/ant4g0nist/chinstrap
cd chinstrap
export image=chinstrap
docker build -f dockerfiles/Dockerfile.local -t $image .
docker run -v `pwd`:/home --rm -it $image
```

Note: For using docker, the Chinstrap project directory needs to be shared with the Docker.

#### Upgrade

if you installed chinstrap with pip3

```bash
pip3 install -U chinstrap
```

### Usage

```bash
╭─ant4g0nist@d3n ~/Desktop/Tezos/chinstrap  ‹v0.0.16›
╰─➤  chinstrap

      _     _           _
  ___| |__ (_)_ __  ___| |_ _ __ __ _ _ __
 / __| '_ \| | '_ \/ __| __| '__/ _` | '_ \
| (__| | | | | | | \__ \ |_| | | (_| | |_) |
 \___|_| |_|_|_| |_|___/\__|_|  \__,_| .__/
                                     |_|

usage: chinstrap [-h] {init,config,networks,compile,install,create,templates,test,sandbox} ...

Chinstrap - a cute framework for developing Tezos Smart Contracts

positional arguments:
  {init,config,networks,compile,install,create,templates,test,sandbox}
    init                Initialize a new Chinstrap project
    config              Verify Chinstrap configuration
    networks            List currently available test networks
    compile             Compile contract source files
    install             Helper to install compilers
    create              Helper to create new contracts, originations and tests
    templates           Download templates provided by SmartPy
    test                Run pytest/smartpy/ligo tests
    sandbox             Start a Tezos local sandbox

optional arguments:
  -h, --help            show this help message and exit
```

### Quickstart

To compile the smart contracts:

```bash
$ chinstrap compile
```

For Flextesa sandbox:

```bash
╭─ant4g0nist@d3n ~/Desktop/Tezos/chinstrap  ‹v0.0.16›
╰─➤  chinstrap sandbox -h

      _     _           _
  ___| |__ (_)_ __  ___| |_ _ __ __ _ _ __
 / __| '_ \| | '_ \/ __| __| '__/ _` | '_ \
| (__| | | | | | | \__ \ |_| | | (_| | |_) |
 \___|_| |_|_|_| |_|___/\__|_|  \__,_| .__/
                                     |_|

usage: chinstrap sandbox [-h] [-o PORT] [-i] [-d] [-s] [-c NUM_OF_ACCOUNTS] [-m MINIMUM_BALANCE] [-p {Hangzhou,Ithaca,Alpha}]

optional arguments:
  -h, --help            show this help message and exit
  -o PORT, --port PORT  Tezos local sandbox's RPC Port
  -i, --initialize      Initialize Tezos sandbox
  -d, --detach          Start the Tezos sandbox and detach
  -s, --stop            Stop the currently running Tezos sandbox
  -c NUM_OF_ACCOUNTS, --num-of-accounts NUM_OF_ACCOUNTS
                        Number of accounts to bootstrap on Tezos sandbox
  -m MINIMUM_BALANCE, --minimum-balance MINIMUM_BALANCE
                        Amount of Tezos to deposit while bootstraping on Tezos local sandbox
  -p {Hangzhou,Ithaca,Alpha}, --protocol {Hangzhou,Ithaca,Alpha}
                        Protocol to start Tezos sandbox with.
```

To download template contracts provided Smartpy:

```bash
╭─ant4g0nist@d3n ~/Desktop/Tezos/chinstrap  ‹v0.0.16›
╰─➤  chinstrap templates
```

To run tests:

```bash
╭─ant4g0nist@d3n ~/Desktop/Tezos/chinstrap  ‹v0.0.16›
╰─➤  chinstrap test
```

To check configuration:

```bash
╰─➤  chinstrap config

      _     _           _
  ___| |__ (_)_ __  ___| |_ _ __ __ _ _ __
 / __| '_ \| | '_ \/ __| __| '__/ _` | '_ \
| (__| | | | | | | \__ \ |_| | | (_| | |_) |
 \___|_| |_|_|_| |_|___/\__|_|  \__,_| .__/
                                     |_|

Using development network
Loaded wallet tz1cagbr5u2YdyxtWA72z3KjEL1KJ2YEs71z. Balance: 0.000000
```

### Is Chinstrap finished?

* Not at all. I will provide as much support as needed and we can work together and add important changes and improvements on a regular basis.
* Pull requests are welcome

## TODO

* [x] Add Ligo support for compilation and tests
* [ ] Add repl
* [ ] Add Ligo/SmartPy templates
* [ ] Improve Sandbox integrations in repl
* [ ] Update documentation to support v0.0.16
* [ ] Visual studio code plugin
* [ ] Add unit tests for chinstrap
* [ ] Add a homebrew formula
* [ ] Provide more options in config for Origination (fee, gas_limit, etc.)

## References

* [https://smartpy.io/docs](https://smartpy.io/docs)
* [https://pytezos.org/](https://pytezos.org/)
* [https://baking-bad.org/](https://baking-bad.org/)
* [https://michelson.baking-bad.org/](https://michelson.baking-bad.org/)

## Contact
Telegram chat: https://t.me/chinstrap_io

## Credits

* Truffle
* Baking-Bad
* logo by [@sengar23](https://github.com/sengar23)

