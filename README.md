# stock-data-fetch

[![Build Status](https://travis-ci.org/fcalice/stock-data-fetch.svg?branch=master)](https://travis-ci.org/fcalice/stock-data-fetch)
[![codecov](https://codecov.io/gh/fcalice/stock-data-fetch/branch/master/graph/badge.svg)](https://codecov.io/gh/fcalice/stock-data-fetch)
[![Maintainability](https://api.codeclimate.com/v1/badges/5b83db2c856ce54d95e4/maintainability)](https://codeclimate.com/github/fcalice/stock-data-fetch/maintainability)
[![Python27](https://img.shields.io/badge/python-2.7-blue.svg)](https://travis-ci.org/fcalice/stock-data-fetch)
[![Python35](https://img.shields.io/badge/python-3.5-blue.svg)](https://travis-ci.org/fcalice/stock-data-fetch)

This is an exercise to fetch stock data from different sources with cache and sanity check,
it supports both Python 2 and 3. Feel free to create an issue if you have any question or remark.

### Run PR checks on local machine
- Check if the code respects pep8 by running the command `pep8 web` in `.`
- Run the unit tests and coverage check with
```bash
nosetests . --with-coverage --cover-package=. --cover-html --cover-erase
```
- [radon](http://radon.readthedocs.io/en/latest/commandline.html) is a useful tool to check if the code
can be easily maintained. It is recommended to keep the cyclomatic complexity of each function under 6.
You can check if you have any function passing this threshold with
```bash
radon cc . --min B -s
```
`radon cc .` shows the metric of all the code.

