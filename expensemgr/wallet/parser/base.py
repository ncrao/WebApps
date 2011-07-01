from wallet.models import Account

class UnimplementedVirtualFunctionError(Exception):
    pass

class IncorrectTypeError(Exception):
    pass

class DataFormatError(Exception):
    pass

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
    def __init__(self, data, account_id):
        self.data = data
        self.account_id = account_id
        self.__txn_data = []
        self.__account = None

    def add_txn_data(self, line):
        """Add a transaction entry to be parsed."""
        self.__txn_data.append(line)

    def __get_account(self, debug):
        if debug:
            self.__account = Account(name='True')
        else:
            self.__account = Account.objects.get(account_id=self.account_id)
        return self.__account

    def get_account(self, debug=False):
        """Return the account for transactions."""
        if self.__account:
            return self.__account
        return self.__get_account(debug)

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
