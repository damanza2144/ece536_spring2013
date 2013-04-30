#!/usr/bin/env python

#############################################
# definitions:
#	M is a matrix with element mij in row i and column j
#	N is a matrix with element njk in row j and column k
#	P is a matrix = MN with element pik in row i and column k, where pik = sum( mij * njk )
#
# map algorithm:
#	For each element mij of M, emit a key-value pair (i, k), (M, j, mij) for k=1,2,... number of columns of N.
#	For each element njk of N, emit a key-value pair (i, k), (N, j, njk) for i=1,2,... number of columns of M.
#
# reduce algorithm:
#	For each key (i, k), emit the key-value pair (i, k), pik where pik = sum( mij * njk )
#
#############################################

import sys
import string

row_counter = 0

# input comes from STDIN (standard input)
for line in sys.stdin:

        # remove leading and trailing whitespace
        line = line.strip()

        # split the line into columns
        columns = line.split()

		column_counter = 0

        # increase counters
        for column in columns:

			if column:

				#print '%s\t%s' % (column, 1)
				#print '(%s, %s), (%s, %s, %s)' % (row_counter, column_counter, ..)
				print '(%s, %s), ()' % (row_counter, column_counter)

			column_counter += 1

		row_counter += 1

