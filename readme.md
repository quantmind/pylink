# pyslink

[![PyPI version](https://badge.fury.io/py/pyslink.svg)](https://badge.fury.io/py/pyslink)
[![Python versions](https://img.shields.io/pypi/pyversions/pyslink.svg)](https://pypi.org/project/pyslink)
[![release](https://github.com/quantmind/pyslink/actions/workflows/release.yml/badge.svg)](https://github.com/quantmind/pyslink/actions/workflows/release.yml)
[![Downloads](https://img.shields.io/pypi/dd/pyslink.svg)](https://pypi.org/project/pyslink/)


Soft link a file/directory with python site-packages directory.
Useful during development.

Currently only projects that use `setup` to package releases are supported.

Installation via pip:
```bash
pip install pyslink
```
Create soft link a package:
```bash
pyslink create path/to/main/module
```
Remove soft link a package
```
pyslink remove path/to/main/module
```

## TODO

- [ ] Support pyproject.toml
