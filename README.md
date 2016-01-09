Currency Converter
==================
Application task for PythonMaster.
Simple program that converts values between currencies using daily exchange rates.

Implementation details
----------------------
Implemented using Python 3.4. App fetches currency rates from www.fixer.io API. Source of currency symbols is www.currencysymbols.in.
Result is presented in form of a JSON.

Usage
-----
```sh
$ python3 currency_converter.py --amount N --input_currency IN [ --output_currency OUT ] [-h]
```

Options
-------
* `-h`
  * prints help
* `--amount N`
  * `N` is value of `IN` currency that will be converted
  * Required
* `--input_currency IN`
  * `IN` specifies input currency type
  * `IN` should be currency symbol or ISO 4217 Code
  * Required
* `--output_currency OUT`
  * `OUT` specifies output currency type
  * `OUT` should be currency symbol or ISO 4217 Code
  * Optional

Examples
--------
```sh
$ python3 currency_converter.py --amount 500 --input_currency € --output_currency $
```
```sh
$ python3 currency_converter.py --amount 30 --input_currency USD
```
```sh
$ python3 currency_converter.py --amount 35 --input_currency EUR --output_currency GBP
```