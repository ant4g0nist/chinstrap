# Introduction

![Chinstrap](https://raw.githubusercontent.com/ant4g0nist/chinstrap/main/docs/images/logo.png)

#### Quickstart

Here, we will explain the basics of creating a Chinstrap project and deploying a smart contract to a local sandbox.

**Creating a project**

First, we will create a boilerplate Chinstrap project in a new directory.

1\) Create a new directory for your Chinstrap project:

```bash
mkdir Chocolates
cd Chocolates
```

2\) Generate boilerplate project:

```bash
chinstrap --init
```

This command creates 3 new folders and a Chinstrap config file inside the current directory. The project structure will look like this:

```bash
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

* `chinstrap_config.yaml` : Chinstrap configuration file
* `contracts/`            : Directory for SmartPy/Ligo contracts
* `originations/`         : Directory for scriptable deployment files
* `tests/`                : Directory for test files for testing your application and contracts

Open the project folder in a text editor like visual studio code.

#### contracts directory

`contracts/Originations.py` is a smart contract \(written in SmartPy\) that manages and updates the status of your deployed smart contracts. This file comes with every Chinstrap project and is suggested not to edit. This keeps track of deployments to save the Gas Costs from redeployments.`contracts/SampleContract.py` is a sample contract \(written in SmartPy\) that creates two entrypoints increment and decrement for storage type of `int`.

#### originations directory

The scripts in the `originations` directory are used to `originate` \(deploy\) a smart contract onto a selected network. The scripts in this folder start with an integer and are run in order i.e., so the file beginning with 2 will be run after the file beginning with 1.

`originations/1_initial_originations.py` file is the origination script for the `Originations` contract found in the `contracts/Originations.py` script. And similarly, `originations/2_samplecontract_origination.py` is the origination script for `SampleContract` found in the `contracts/SampleContract.py` script.

#### tests directory

The tests for the contracts reside in `tests` directory. These tests are written in `Python` and Chinstrap uses `pytest` and `pytezos` to test the contracts.

With `--init`, Chinstrap creates 2 tests files one for `smartpy` and one for `pytest` `sampleContractSmartPy.py`, `samplecontractPytest.py`.

### Demo

To compile the smart contracts:

```bash
$ chinstrap --compile
```

To originate \(deploy\) the smart contracts:

```bash
$ chinstrap --originate --network florencenet
```

![compile-demo](https://raw.githubusercontent.com/ant4g0nist/chinstrap/main/docs/images/compile-originate.gif)

To `re-originate` \(reset local state and deploy again\) the smart contracts:

```bash
$ chinstrap --originate --network florencenet --reset
```

To run `SmartPy` tests from `tests` folder:

```shell
$ chinstrap --test smartpy
```

To run `Pytest` tests from `tests` folder:

```shell
$ chinstrap --test pytest
```
