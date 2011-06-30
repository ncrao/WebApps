class UnimplementedVirtualFunctionError(Exception):
    pass

class IncorrectTypeError(Exception):
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
    def __init__(self, data):
        self.data = data
        self.__txn_data = []

    def _add_txn_data(self, line):
        self.__txn_data.append(line)

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
