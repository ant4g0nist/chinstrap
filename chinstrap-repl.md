# Chinstrap repl

Chinstrap provides a powerful repl, exposing `pytezos`, `accounts`, `contracts` to the `repl` making the interaction with the Tezos network much easier.

To start the chinstrap repl \(\`debug\`\):

```text
$ chinstrap --debug --network florencenet
```

If the network option is not passed, by default it will expect that an instance of local sandbox is already running!

```text
$ chinstrap --debug
```

The repl makes use of the powerful `ptpython` and will suggest the available functions as you start typing.

![debug-demo](https://raw.githubusercontent.com/ant4g0nist/chinstrap/main/docs/images/debug.gif)

Currently exposed functions, besides the default powerful `Python` modules, are:

```text
getContract(name)
getContractFromFile(filename)
getContractFromAddress(address)
getContractFromURL(url)
setConfig(key, value)
compile()
test()
originate(reset=False)
bake(contractCall)
accounts()
getAccountFromKey(key)
getAccountBalance(address)
```



