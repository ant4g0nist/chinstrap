# Chinstrap

![Chinstrap](https://raw.githubusercontent.com/ant4g0nist/chinstrap/main/docs/images/logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/madhuakula/kubernetes-goat/blob/master/LICENSE)
[![Baked by ant4g0nist](https://img.shields.io/twitter/follow/ant4g0nist?style=social)](https://twitter.com/ant4g0nist)
[![docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://docs.chinstrap.io)
[![PyPI](https://img.shields.io/pypi/v/chinstrap)](https://pypi.org/project/chinstrap/)

<h2>Chinstrap is supported by <a href='https://twitter.com/ant4g0nist/status/1498751543520153604?s=20&t=ICSAOjkYsYVNuQDHmkyP7w'>Tezos Foundation Grant</a></h2>

### Community support channels
- Telegram chat: https://t.me/chinstrap_io
- Twitter      : https://twitter.com/chinstrap_io
- Twitter      : https://twitter.com/ant4g0nist

### Overview

**Chinstrap** is a development environment, testing framework, and asset pipeline focused solely on Tezos blockchain, aiming to become Swiss-Army-Knife for Tezos Smart Contract developers.

Chinstrap makes developers' lives easier by providing support for multiple contract compilations, tests, and origination on many public and private Tezos networks.

### Features

Chinstrap offers:

* End-to-end build cycle support for Creation, Compilation, Testing, and Origination of Smart Contracts
* Local sandbox environment to develop and test contracts
* Support for contracts in `SmartPy`, `JsLIGO`, `CameLIGO`, `PascaLIGO`, and `ReasonLIGO`.
* Support for tests in `Python`(SmartPy/PyTest), `JsLIGO`, `CameLIGO`, `PascaLIGO`, and `ReasonLIGO`.
* Scriptable deployment & originations framework
* Originations Management for deploying to many public & private networks
* Interactive debug console to debug and directly communicate with contracts

### Why?

Here are some reasons why I built Chinstrap:

* Development framework that solely focuses on Tezos Smart Contract development
* Easy to use and everything in place already.
* Designed focused solely to support writing contracts in `SmartPy`, `JsLIGO`, `CameLIGO`, `PascaLIGO` and `ReasonLIGO`.
* Extendable
* Tests can also be programmed in Ligo, `Python`(SmartPy/PyTest) and `JsLIGO`, `CameLIGO`, `PascaLIGO` and `ReasonLIGO`.
* Easy maintenance

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
git clone -b v1.0.2 https://github.com/ant4g0nist/chinstrap
cd chinstrap
python3 setup.py install
```

### Usage

```bash
╭─ant4g0nist@d3n ~/Desktop/Tezos/chinstrap  ‹v1.0.2›
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
╭─ant4g0nist@d3n ~/Desktop/Tezos/chinstrap  ‹v1.0.2›
╰─➤  chinstrap sandbox -h

      _     _           _
  ___| |__ (_)_ __  ___| |_ _ __ __ _ _ __
 / __| '_ \| | '_ \/ __| __| '__/ _` | '_ \
| (__| | | | | | | \__ \ |_| | | (_| | |_) |
 \___|_| |_|_|_| |_|___/\__|_|  \__,_| .__/
                                     |_|

usage: main.py [-h]
               {init,config,networks,compile,install,create,templates,test,sandbox,develop,originate,account}
               ...

positional arguments:
  {init,config,networks,compile,install,create,templates,test,sandbox,develop,originate,account}
    init                Initialize a new Chinstrap project
    config              Verify Chinstrap configuration
    networks            List currently available test networks
    compile             Compile contract source files
    install             Helper to install compilers
    create              Helper to create new contracts, originations and tests
    templates           Download templates provided by SmartPy and *LIGO
    test                Run pytest/smartpy/ligo tests
    sandbox             Start a Tezos local sandbox
    develop             Open a console with a local Flextesa development
                        environment
    originate           Run originations and deploy contracts
    account             Tezos account

optional arguments:
  -h, --help            show this help message and exit
```

To download template contracts provided Smartpy or LIGO Lang:

```bash
usage: main.py templates [-h] -l
                         {JsLIGO,PascaLIGO,CameLIGO,ReasonLIGO,SmartPy}

optional arguments:
  -h, --help            show this help message and exit
  -l {JsLIGO,PascaLIGO,CameLIGO,ReasonLIGO,SmartPy}, --language {JsLIGO,PascaLIGO,CameLIGO,ReasonLIGO,SmartPy}
                        The type of the item to create
```

To run tests:

```bash
╭─ant4g0nist@d3n ~/Desktop/Tezos/chinstrap  ‹v1.0.2›
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

## Milestones
### Milestone 1
- [x] Support the latest protocol updates of the Tezos protocol on Chinstrap.
- [x] Support and facilitate the programming of smart contracts and respective tests in Ligo.

### Milestone 2
- [x] Improve, update, and maintain comprehensive documentation of the platform for relevant stakeholders (e.g. developers and others).
- [x] Improve the sandbox and REPL (Real-Eval-Print Loop) experience of the platform.
- [x] Release version 1.0.0 of the platform.

### Milestone 3
- [ ] Provide a Visual Studio Code plugin for origination and tests.

## TODO

* [x] Add `JsLIGO`, `CameLIGO`, `PascaLIGO`, and `ReasonLIGO` support for contracts and tests
* [x] Remove dependency on migration contract
* [x] Update Chinstrap to latest protocols
* [x] Add SmartPy templates
* [x] Add Ligo templates
* [x] Update documentation to support v1.0.0
* [x] Create chinstrap.io landing page
* [x] Add repl
* [x] Improve Sandbox integrations in repl
* [ ] Release version 1.0.0 of the platform.
* [ ] Add TypeScript generation for compiled contracts
* [ ] Add support for Jest tests
* [ ] Visual studio code plugin
* [ ] Add unit tests for chinstrap
* [ ] Add a homebrew formula
* [ ] Add fig specifications

## References

* [https://smartpy.io/docs](https://smartpy.io/docs)
* [https://pytezos.org/](https://pytezos.org/)
* [https://baking-bad.org/](https://baking-bad.org/)
* [https://michelson.baking-bad.org/](https://michelson.baking-bad.org/)

## Credits

* Baking-Bad
* Tezos Foundation
* [@sengar23](https://github.com/sengar23)
