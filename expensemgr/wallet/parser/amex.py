from wallet.parser.base import Parser
from wallet.parser.base import DataFormatError
from wallet.models import Account
from wallet.models import Transaction

import re
import datetime

NUM_VALUES_PER_LINE = 14

class AmexParser(Parser):
    """Parser for Amex transactions."""

    def __init__(self, data, account_id, debug=False):
        super(AmexParser, self).__init__(data, account_id)
        self.debug = debug

    def init_parser(self):
        """Initialize data for Amex transactions.

        Parses CSV downloaded Amex statements. You can download these templates
        from the top-right corner of the account info page.
        """
        self.data = self.data.splitlines()
        for line in self.data:
            if len(line.split(',')) != NUM_VALUES_PER_LINE:
                raise DataFormatError
            self.add_txn_data(line)

    def parse_txn(self, line):
        """Parse a transaction.

        Amex transactions are CSV separated and follow the following format:
        06/25/2011  Sat,,"FOG HILL MARKET 5429SAN FRANCISCO       CA","ADITYA C RAO","XXXX-XXXXXX-21023",,,12.74,,,,,,
        """
        parts = line.split(',')
        posted_date = datetime.datetime.strptime(parts[0].split()[0], '%m/%d/%Y')
        description = parts[2]
        amount = float(parts[7])

        # create txn object here. this is not saved in the datastore at this
        # point. the caller is responsible for saving this object.
        txn = Transaction(date=posted_date.strftime('%Y-%m-%d'), amount=amount,
                          account=self.get_account(debug=self.debug),
                          description=description)

        return txn

def test(filename):
    """Define a routine for validation."""
    data = open(filename).read()
    parser = AmexParser(data, 0, debug=True)

    def print_txn(txn):
        """Print a transaction."""
        print('%-12s  %-50s  %-8s %s' % (txn.date, txn.description, txn.amount,
                                         txn.account.name))

    txn_list = parser.parse()
    for txn in txn_list:
        print_txn(txn)
