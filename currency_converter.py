from argparse import ArgumentParser
from urllib.request import urlopen
import html
import json
import re


class Converter(object):

    def __init__(self, value, in_c, out_c):
        self.amount = 0.0
        self.outC = out_c
        self.inC = in_c

        self.symbols = Converter.get_currency_symbols()
        self.set_amount(value)
        self.set_input_currency(in_c)
        self.set_output_currency(out_c)

    def set_amount(self, amount):
        if float(amount) < 0:
            AttributeError("Invalid amount value")
        self.amount = float(amount)

    def set_input_currency(self, in_c):
        pass

    def set_output_currency(self, out_c):
        self.outC = [out_c]

    def convert(self, value, in_c, out_c):
        if not self._validate(value, in_c, out_c):
            pass
        self.convert()

    def convert(self):
        data = self._get_data()

        result = Converter._get_output_structure()
        result["input"]["amount"] = self.amount
        result["input"]["currency"] = self.inC

        if len(self.outC) == 0:
            for currency, rate in data["rates"].items():
                result["output"][currency] = self.amount * rate
        else:
            for currency in self.outC:
                rate = data["rates"][currency]
                result["output"][currency] = self.amount * rate
        return result

    def _get_data(self):
        url = "http://api.fixer.io/latest?base={0}".format(self.inC)
        response = urlopen(url)
        string = response.read().decode('utf-8')
        return json.loads(string)

    def _validate(self, value, in_c, out_c):
        self.amount = value
        self.inC = Converter._check_sign(in_c)
        self.outC = dict()

        if out_c is not None:
            self.outC = Converter._check_sign(out_c)

    @staticmethod
    def _check_sign(currency):
        if len(currency) == 1:
            pass
        elif len(currency) == 3:
            pass
        else:
            pass
        return currency

    @staticmethod
    def _get_output_structure():
        structure = dict()
        structure["input"] = dict()
        structure["output"] = dict()
        return structure

    @staticmethod
    def get_currency_symbols():
        result = dict()
        url = "http://www.currencysymbols.in"
        request = urlopen(url)
        content = request.read().decode('utf-8')

        table = re.search(r'(<table.*table>)', content, re.DOTALL).group(0)

        items = re.findall(r'<tr>(.*?)</tr>', table, re.DOTALL)[1:]
        for item in items:
            info = re.findall(r'<th>(.*?)</th>', item)
            result[info[3]] = html.unescape(info[4])

        return result


def parse_args():
    parser = ArgumentParser(description="Currency converter")
    parser.add_argument('--amount', required=True, type=float, help='amount which we want to convert')
    parser.add_argument('--input_currency', required=True, help='input currency')
    parser.add_argument('--output_currency', required=False, help='requested/output currency')
    return parser.parse_args()


def main():
    args = parse_args()
    converter = Converter(args.amount, args.input_currency, args.output_currency)
    output = converter.convert()
    print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    main()