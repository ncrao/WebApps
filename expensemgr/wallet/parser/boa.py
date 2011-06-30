from wallet.parser.base import Parser
from wallet.models import Account
from wallet.models import Transaction

import re
import datetime

INIT = 0
COLLECT = 1
STOP = 2

SECTION_HEADERS = [
    u'Payments and Other Credits',
    u'Purchases and Adjustments',
]

PAGE_MARKERS = [
    u'continued on next page...',
    u'continuedonnextpage...',
]

MIN_ELEMENTS_PER_LINE = 7

class ParseError(Exception):
    pass

class UnknownStateError(Exception):
    pass

class TxnParseError(Exception):
    pass

class BOAParser(Parser):
    """Parser for BOA transactions."""

    def __init__(self, data, year=None, exception_on_parse_error=False,
                 verbose=False):
        super(BOAParser, self).__init__(data)
        self.state = INIT
        if not year:
            year = datetime.datetime.now().year
        self.year = year
        self.exception_on_parse_error = exception_on_parse_error
        self.verbose = verbose

    def is_section_header(self, line):
        """Check if a line is a section header."""
        return line.strip() in SECTION_HEADERS

    def is_end_of_section(self, line):
        """Check if a line is the end of a section.

        Sections terminate with a single dollar amount entry.
        """
        if len(line.strip().split()) > 1:
            return False
        if not re.match(u'\u2013?\$\d+\.\d+', line.strip()):
            return False
        return True

    def is_end_of_page(self, line):
        """Check if we reach the end of the page.

        Pages terminate with one of the phrases in PAGE_MARKERS.
        """
        if line.strip() in PAGE_MARKERS:
            return True
        return False

    def is_valid_txn(self, line):
        """Check if a line is a valid transaction."""
        assert self.state == COLLECT
        if len(line.strip().split()) < MIN_ELEMENTS_PER_LINE:
            return False
        return True

    def can_ignore(self, line):
        """Ignore certain types of lines such as references."""
        if len(line.strip()) == 1:
            return True
        return False

    def init_parser(self):
        """Initialize data for BOA transactions.

        BOA transactions are a PITA to parse. Steps involved in preparing data:
        - Ignore all lines until a section header -- i.e. either "Payments and
          Other Credits" or "Purchases and Adjustments" is seen on the line
          (and nothing else). A transaction starts on the following line.
        - Ignore reference numbers (i.e. lines with just one number/entry).
        - Collect transaction data until we see "continuedonnextpage..." and
          nothing else on the line.
        - Ignore lines until you see a section header.
        - Continue collecting transaction data until you hit a line with only
          a dollar amount on it. This is the total amount for that section.
        - Stop parsing until you see another section header.
        - Terminate when you reach end of file.
        """
        self.state = INIT
        self.data = [unicode(line, 'utf-8') for line in self.data.splitlines()]

        for line in self.data:
            if self.state == INIT:
                if self.is_section_header(line):
                    self.state = COLLECT
            elif self.state == COLLECT:
                if self.is_end_of_section(line) or self.is_end_of_page(line):
                    self.state = STOP
                elif self.is_valid_txn(line):
                    self._add_txn_data(line)
                elif self.can_ignore(line):
                    continue
                elif self.exception_on_parse_error:
                    raise ParseError, line.encode('ascii')
                elif self.verbose:
                    print('warning: %s' % line.encode('ascii'))
            elif self.state == STOP:
                if self.is_section_header(line):
                    self.state = COLLECT
            else:
                raise UnknownStateError

    def parse_txn(self, line):
        """Parse a transaction.

        BOA transactions are not CSV; so this is a little harder to parse. Rules
        for parsing these transactions:
        - Use transaction date (instead of posting date) for txn date
        - Discard posting date
        - Use the last field as amount
        - Use the second last field to identify the account
        - Use the remaining fields as the description. Discard the last few
          digits in the description (txn reference).

        Example transaction:
        05/16  05/17  SWATHI TIFFINS    SUNNYVALE    CA0700      8811      13.39
        """
        parts = line.split()

        month, day = parts[0].split('/')
        date = '%s-%s-%s' % (self.year, month, day)
        amount = float(parts[-1].replace(u'\u2013', '-').replace('$', '').replace(',', ''))
        txn_id = parts[-2]
        description = ' '.join(parts[2:-2]).rstrip('0123456789')

        # lookup account from txn_id
        #account = Account.objects.get(txn_id=txn_id)
        account = Account(name='test')

        # create txn object here. this is not saved in the datastore at this
        # point. the caller is responsible for saving this object.
        txn = Transaction(date=date, amount=amount, account=account,
                          description=description)
        return txn

def test(filename):
    """Define a routine for validation."""
    data = open(filename).read()
    parser = BOAParser(data)

    def print_txn(txn):
        """Print a transaction."""
        print('%-12s  %-50s  %-8s %s' % (txn.date, txn.description, txn.amount,
                                         txn.account.name))

    txn_list = parser.parse()
    for txn in txn_list:
        print_txn(txn)
