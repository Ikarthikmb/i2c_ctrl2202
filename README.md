# I2C - Inter Integrated Circuit

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![UPRJ_CI](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml) [![Caravel Build](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml)


## I2C Controller

I2C bus, the controller transmits 8-bit data with the
target receiving those 8-bits.

Modes of Operation:

```
 #------------------------------------#
 | i_read 	| Controller 	| Target 		|
 |----------|-------------|-----------|
 | 0				| Transmit		| Receive 	|
 | 1				| Receive			| Transmit	|
 #------------------------------------#
```

Frequency of operation 	= 5 Mbps

---

References: 

* [I2C wikipedia](https://en.wikipedia.org/wiki/I%C2%B2C)
