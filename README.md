# wasc

[![PyPI - Version](https://img.shields.io/pypi/v/wasc.svg)](https://pypi.org/project/wasc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wasc.svg)](https://pypi.org/project/wasc)

-----

**Table of Contents**

- [wasc](#wasc)
  - [Installation](#installation)
  - [License](#license)
  - [Developpement](#developpement)
    - [install dependencies](#install-dependencies)
    - [Running wasc with hatch](#running-wasc-with-hatch)
    - [Testing wasc with hatch](#testing-wasc-with-hatch)

## Installation

```console
pip install wasc
```

## License

`wasc` is distributed under the terms of the [CECILL-2.1](https://spdx.org/licenses/CECILL-2.1.html) license.

## Developpement

Full source code is available on github : [https://github.com/gcollet/wasc](https://github.com/gcollet/wasc)
The project is developed under hatch project manager ([hatch.pypa.io](https://hatch.pypa.io/latest/))

### install dependencies
The dependencies are managed with hatch environment system.
It is **not necessary** to install using `pip install -r requirements_dev.txt` but the file is present if needed.
### Running wasc with hatch
In `wasc` directory, use hatch to run wasc in the default environnement :
`hatch run wasc data/url_example.csv`

### Testing wasc with hatch
In `wasc` directory, use hatch to test wasc files in the default environnement :
`hatch run test test_all`