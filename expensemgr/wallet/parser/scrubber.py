"""Utility tool to scrub a file to ascii encoding."""

replace_dict = dict()
replace_dict[150] = '-'
replace_dict[174] = ''

def replace(line):
    """Replace each non-conventional character in input."""
    for c in line:
        if ord(c) in replace_dict:
            line = line.replace(c, replace_dict[ord(c)])
    return line

def convert(line, encoding='ascii', error='strict'):
    """Convert to unicode with the specified encoding."""
    return unicode(line, encoding, error)

def debug(line):
    """Print debugging info."""
    count = 0
    print line
    print replace(line)
    for c in line:
	count += 1
	try:
	    unicode(c)
	except UnicodeDecodeError:
	    print count, c, ord(c)

def scrub(filename):
    """Scrub file and convert all non-ascii characters into ascii equivalent."""
    data = open(filename).read().splitlines()
    for line in data:
        success = 1
        try:
            line = convert(line)
        except UnicodeDecodeError:
            try:
                line = convert(replace(line)) # expect this to pass
            except UnicodeDecodeError:
                success = 0

        if not success:
            debug(line)
            break

import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s filename' % sys.argv[0])
        sys.exit(1)
    scrub(sys.argv[1])
