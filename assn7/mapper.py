#!/usr/bin/env python

import sys
import string

is_m = -1
row_counter = 0
column_counter = 0

# input comes from STDIN (standard input)
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	if line == 'M:':

		print 'start processing m matrix now'
		is_m = 1
		row_counter = 0
		continue
	
	if line == 'N:':

		print 'start processing n matrix now'
		is_m = 0
		row_counter = 0
		continue

	# split the line into columns
	matrix_columns = line.split()
	column_counter = 0

	for matrix_column in matrix_columns:
	
		# process the M matrix
		if is_m == 1:

			print 'M: (%s, %s), ()' % (row_counter, column_counter)

		# process the N matrix
		if is_m == 0:

			print 'N: (%s, %s), ()' % (row_counter, column_counter)

		column_counter += 1

	row_counter += 1


