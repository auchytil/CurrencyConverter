#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# good to have ^

from argparse import ArgumentParser
from urllib.error import URLError
from urllib.request import urlopen
import html
import json
import re


# Class that takes care of conversion between the currencies
class Converter:

    def __init__(self):
        """ Constructor """
        self.amount = None
        self.outC = None # naming (out_c)
        self.inC = None # naming (in_c)
        self.symbols = Converter.get_currency_symbols() # should be in 'load' section

    def set_amount(self, amount):
        """ Sets currency amount. """
        if float(amount) < 0:
            raise AttributeError("Invalid amount value") # nice
        self.amount = float(amount)

    def set_input_currency(self, in_c):
        """ Sets input currency.

        @param in_c -- type of input currency
        """
        value = self._get_currencies_from_symbol(in_c)
        if len(value) == 1:
            self.inC = value[0]
        else:
            raise AttributeError("Input symbol '{0}' is ambiguous".format(in_c))

    def set_output_currency(self, out_c):
        """ Sets output currency.

        @param out_c -- type of output currency
        """
        self.outC = []
        if out_c is not None and len(out_c) != 0: # why 'out_c is not None'.. same is just 'if out_c' not? :)
            self.outC = self._get_currencies_from_symbol(out_c)

    def _get_currencies_from_symbol(self, symbol):
        """ Converts currency symbol to its ISO 4217 representation.

        @param symbol -- one letter representing the currency or the ISO code
        """
        result = []
        if len(symbol) == 1:
            for k,v in self.symbols.items():
                if v == symbol:
                    result.append(k)
        elif len(symbol) == 3:
            result.append(symbol.upper())
        else:
            raise AttributeError("Unsupported symbol")
        if len(result) == 0:
            raise AttributeError("Unsupported currency")
        return result

    def convert(self, value, in_c, out_c):
        """ Performs conversion between currencies.

        @param value -- amount to convert
        @param in_c  -- type of the input currency
        @param out_c -- type of the output currency
        """
        self.set_amount(value)
        self.set_input_currency(in_c)
        self.set_output_currency(out_c)

        data = self._get_data()

        result = Converter._get_output_structure()
        result["input"]["amount"] = self.amount
        result["input"]["currency"] = self.inC

        if len(self.outC) == 0:
            for currency, rate in data["rates"].items():
                result["output"][currency] = self.amount * rate
        else:
            for currency in self.outC:
                if currency in data["rates"]:
                    rate = data["rates"][currency]
                    result["output"][currency] = self.amount * rate
        return result

    def _get_data(self):
        """ Downloads data of currency conversion rates from API. """
        url = "http://api.fixer.io/latest?base={0}".format(self.inC)
        response = urlopen(url)
        string = response.read().decode('utf-8')
        return json.loads(string)

    @staticmethod
    def _get_output_structure():
        """ Prepares data-structure for output. """
        structure = dict() # return {"input": {}, "output": {}} looks better for me.. but ok
        structure["input"] = dict()
        structure["output"] = dict()
        return structure

    @staticmethod
    def get_currency_symbols():
        """ Fetches data containing currency symbols from Web. """
        result = dict()
        url = "http://www.currencysymbols.in"
        request = urlopen(url)
        content = request.read().decode('utf-8')

        table = re.search(r'(<table.*table>)', content, re.DOTALL).group(0)

        items = re.findall(r'<tr>(.*?)</tr>', table, re.DOTALL)[1:] # nice
        for item in items:
            info = re.findall(r'<th>(.*?)</th>', item)
            result[info[3]] = html.unescape(info[4])

        return result


def parse_args():
    """ Sets up ArgumentParser and parses arguments. """
    parser = ArgumentParser(description="Currency converter")
    parser.add_argument('--amount', required=True, type=float, help='amount which we want to convert')
    parser.add_argument('--input_currency', required=True, help='input currency')
    parser.add_argument('--output_currency', required=False, help='requested/output currency')
    return parser.parse_args()


def main():
    """ Entry point of the application. """
    args = parse_args()
    try:
        converter = Converter()
        output = converter.convert(args.amount, args.input_currency, args.output_currency)
        print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))
    except AttributeError as e: #nice
        print(e)
    except URLError: # nice
        print("Problem with connection to the remote service.")
    except Exception:
        print("Something broke down.")


if __name__ == "__main__":
    main()
    
    
albert.uchytil@windowslive.com	
doc:9/10	code:8.5/10	 creativity_bonus:3/inf
