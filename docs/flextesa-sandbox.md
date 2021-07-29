# Flextesa Sandbox

In this section, we will see how to start a local Flextesa sandbox. 

To start the local Flextesa sandbox with 5 bootstrapped accounts:

```text
$ chinstrap --sandbox --accounts 5
```

Chinstrap provides extra options to pass to the sandbox while starting.

```text
$ chinstrap --sandbox --accounts 5
$ chinstrap --sandbox --accounts 5 --account-balance 2_000
$ chinstrap --sandbox-detach
$ chinstrap --sandbox --accounts 10 --sandbox-port 1337
```

To stop the sandbox:

```text
$ chinstrap --sandbox-stop
```

![sandbox-demo](https://raw.githubusercontent.com/ant4g0nist/chinstrap/main/docs/images/sandbox.gif)

## 

