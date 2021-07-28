# BLS12-381 Abstraction For Tezos
![CI](https://github.com/RomarQ/tezos-bls12-381/workflows/CI/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/RomarQ/tezos-bls12-381/badge.svg?branch=main&t=bN86Fp)](https://coveralls.io/github/RomarQ/tezos-bls12-381?branch=main)

Special thanks to Paul Miller, for his fantastic library [noble-bls12-381](https://github.com/paulmillr/noble-bls12-381).

## Install

```bash
npm install tezos-bls12-381
# or
yarn add tezos-bls12-381
```

## Usage
```ts
import Bls12 from 'tezos-bls12-381';

const point_1 = "0572cbea904d67468808c8eb50a9450c9721db309128012543902d0ac358a62ae28f75bb8f1c7c42c39a8c5529bf0f4e166a9d8cabc673a322fda673779d8e3822ba3ecb8670e461f73bb9021d5fd76a4c56d9d4cd16bd1bba86881979749d28";

const point_2 = "17f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb08b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1";

const newPoint = Bls12.addG1(point_1, point_2);

console.log("New Point: \n", newPoint);

>>>
New Point: 
0572cbea904d67468808c8eb50a9450c9721db309128012543902d0ac358a62ae28f75bb8f1c7c42c39a8c5529bf0f4e166a9d8cabc673a322fda673779d8e3822ba3ecb8670e461f73bb9021d5fd76a4c56d9d4cd16bd1bba86881979749d28
```

`Michelson translation of the example above`
```lisp
"""
ADD: Add two G1 points.

:: bls12_381_g1 : bls12_381_g1 : 'S -> bls12_381_g1 : 'S
"""

PUSH bls12_381_g1 0x0572cbea904d67468808c8eb50a9450c9721db309128012543902d0ac358a62ae28f75bb8f1c7c42c39a8c5529bf0f4e166a9d8cabc673a322fda673779d8e3822ba3ecb8670e461f73bb9021d5fd76a4c56d9d4cd16bd1bba86881979749d28; # bls12_381_g1

PUSH bls12_381_g1 0x17f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb08b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1; # bls12_381_g1 : bls12_381_g1

ADD;        # bls12_381_g1
```

Check the [tests](src/__tests__/index.test.ts) for more examples.

## References

[SmartPy BLS12-381 Contract Template](https://smartpy.io/ide?template=bls12_381.py)

<img height="48" href="https://smartpy.io" src="https://smartpy.io/static/img/logo.png">