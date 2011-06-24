from wallet.models import Account

class UnimplementedVirtualFunctionError(Exception):
    pass

class IncorrectTypeError(Exception):
    pass

class DataFormatError(Exception):
    pass

class ParserNotFoundError(Exception):
    pass

parsers = dict()

def register_parser_type(parser_id, parser_class):
    """Register a parser class."""
    global parsers
    parsers[parser_id] = parser_class

def ParserFactory(parser_id, data, account):
    """Function to create a parser for parser_id.

    Create a parser object with the class variable parser_id. If the parser is
    not found it raises ParserNotFoundError.
    """
    parser_class = parsers.get(parser_id, None)
    if not parser_class:
        raise ParserNotFoundError
    return parser_class(data, account)

class Parser(object):
    """Class to parse exported data.

    This abstract class is the framework to parse exported data. Parsers
    inherit from this class and override init_parser() and parse_txn() methods.
    init_parser() is used to process self.data and store it as a list of
    transaction strings. parse() then goes through each string and invokes
    parse_txn() to convert the string into a transaction object. parse()
    returns a list of transaction objects. The caller is responsible for saving
    these objects in the data store.
    """
    def __init__(self, data, account):
        self.data = data
        self.account = account
        self.__txn_data = []

    def add_txn_data(self, line):
        """Add a transaction entry to be parsed."""
        self.__txn_data.append(line)

    def get_account(self, debug=False):
        """Return the account for transactions."""
        if debug:
            self.account = Account(name='Test')
        return self.account

    def init_parser(self):
        """Initialize parser."""
        raise UnimplementedVirtualFunctionError()

    def parse_txn(self, line):
        """Parse a transaction entry."""
        raise UnimplementedVirtualFunctionError()

    def parse(self):
        """Parse data and return a list of transaction objects."""
        txn_list = []
        self.init_parser()
        for line in self.__txn_data:
            txn_list.append(self.parse_txn(line))
        return txn_list
