#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	# this is just a dummy mapper where it just outputs what it is given
	print '%s' % (line)

