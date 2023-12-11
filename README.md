# Web Accessibility Simple Checker

[![PyPI - Version](https://img.shields.io/pypi/v/wasc.svg)](https://pypi.org/project/wasc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wasc.svg)](https://pypi.org/project/wasc)
[![Docs](https://github.com/atelierPartage/wasc/actions/workflows/docs.yml/badge.svg)](https://github.com/atelierPartage/wasc/actions/workflows/docs.yml)
-----

**Table of Contents**

- [Web Accessibility Simple Checker](#web-accessibility-simple-checker)
  - [](#)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Documentation](#documentation)
  - [License](#license)
  - [Developpement](#developpement)
    - [Dependencies](#dependencies)
    - [Running wasc with hatch](#running-wasc-with-hatch)
    - [Testing wasc with hatch](#testing-wasc-with-hatch)

## Installation

Attention, l'utilisation de python > 3.12 est nécessaire car il y a des soucis d'encodage pour les versions inférieures.
```console
pip install wasc
```
## Usage

```bash
Usage: wasc [OPTIONS] WEBSITES

  Websites Accessibility Criteria Checker, helps to 
  evaluate accessibility on a list of websites

  WEBSITES is a CSV file containing a list of websites 
  as couples "label";"URL"

Options:
  -c, --checkers PATH             Path to the list of checkers
  -f, --output_format [json|csv]  Output format [default=json]
  -o, --output FILENAME           Output file [default=stdout]
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.
```

Example files are given in `data` directory

## Documentation

Documentation is available [here](https://atelierpartage.github.io/wasc/)
## License

`wasc` is distributed under the terms of the [CECILL-2.1](https://spdx.org/licenses/CECILL-2.1.html) license by the following licensors :
* Juliette Francis
* François le Berre
* Guillaume Collet

`wasc` main contact is [contact@latelierpartage.fr](mailto:contact@latelierpartage.fr)

For details about the license, see file [LICENSE.txt](https://github.com/atelierPartage/wasc/blob/main/LICENSE.txt)

## Developpement

Full source code is available on github : [https://github.com/gcollet/wasc](https://github.com/gcollet/wasc)
The project is developed under hatch project manager ([hatch.pypa.io](https://hatch.pypa.io/latest/))

### Dependencies
`hatch` project manager is mandatory. The other dependencies are managed with hatch environment system.

It is **not necessary** to install dependencies using `pip install -r requirements_dev.txt` but the file is present if needed.
### Running wasc with hatch
In `wasc` directory, use hatch to run wasc in the default environnement :

`hatch run wasc data/url_example.csv`

### Testing wasc with hatch
In `wasc` directory, use hatch to test wasc files in the default environnement :

`hatch run test_all`
