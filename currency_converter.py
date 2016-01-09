from argparse import ArgumentParser
from urllib.request import urlopen
import json


class Converter:

    def convert(self, value, in_c, out_c):
        if not self._validate(value, in_c, out_c):
            pass
        data = self._get_data()

        if self.outC is not None:
            print(self.amount * data["rates"][self.outC])

    def _get_data(self):
        url = "http://api.fixer.io/latest?base={0}".format(self.inC)
        response = urlopen(url)
        string = response.read().decode('utf-8')
        return json.loads(string)

    def _validate(self, value, in_c, out_c):
        self.amount = value
        self.inC = Converter._check_sign(in_c)
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


def parse_args():
    parser = ArgumentParser(description="Currency converter")
    parser.add_argument('--amount', required=True, type=float, help='amount which we want to convert')
    parser.add_argument('--input_currency', required=True, help='input currency')
    parser.add_argument('--output_currency', required=False, help='requested/output currency')
    return parser.parse_args()


def main():
    args = parse_args()
    converter = Converter()
    output = converter.convert(args.amount, args.input_currency, args.output_currency)
    print(output)

if __name__ == "__main__":
    main()