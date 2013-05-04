#!/usr/bin/env python

import sys

m_vals = []

# input comes from STDIN (standard input)
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	if line:

		# split the line into columns
		matrix_columns = line.split()
		is_m = matrix_columns[0]

		if is_m == 'M':

			for index in range(1,len(matrix_columns)):
				m_vals.append(float(matrix_columns[index]))

		else:

			col_vector = []

			for index in range(1,len(matrix_columns)):
				col_vector.append(float(matrix_columns[index]))

			for m_val in m_vals:
				print '%s\t%s' % (m_val, col_vector)

