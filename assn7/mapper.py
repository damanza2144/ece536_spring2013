#!/usr/bin/env python

#############################################
# definitions:
#	M is a matrix with element mij in row i and column j
#	N is a matrix with element njk in row j and column k
#	P is a matrix = MN with element pik in row i and column k, where pik = sum( mij * njk )
#
# map algorithm:
#	For each element mij of M, emit a key-value pair (i, k), (M, j, mij) for k=1,2,... number of columns of N.
#							(row i, number of columns of N), (M, column j, value at row i and column j)
#	For each element njk of N, emit a key-value pair (i, k), (N, j, njk) for i=1,2,... number of columns of M.
#							(number of columns of M, column k), (N, row j, value at row j and column k)
#
# reduce algorithm:
#	For each key (i, k), emit the key-value pair (i, k), pik where pik = sumj( mij * njk )
#
#############################################

import sys

# this will signify if we are processing an M (set to 1) or an N (set to 0) matrix
is_m = -1

# my row counter for all matrices
row_counter = 0

# my column counter for all matrices
column_counter = 0

# number of rows and columns for N and M matrices
no_mmatrix_cols = 0
no_mmatrix_rows = 0
no_nmatrix_cols = 0
no_nmatrix_rows = 0

# create lists for the M and N matrices
mmatrix_list = list()
nmatrix_list = list()

# input comes from STDIN (standard input)
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	# split the line into columns
	matrix_columns = line.split()

	if matrix_columns:

		# there must be a line with only "M:" signifying we are starting the M matrix
		if line == 'M:':

			# set the bit to signify that the next rows and columns are an M matrix
			is_m = 1

			no_nmatrix_cols = column_counter
			no_nmatrix_rows = row_counter

			# reset the row counter
			row_counter = 0
			continue

		# there must be a line with only "N:" signifying we are starting the N matrix
		if line == 'N:':

			# set the bit to signify that the next rows and columns are an N matrix
			is_m = 0

			no_mmatrix_cols = column_counter
			no_mmatrix_rows = row_counter

			# reset the row counter
			row_counter = 0
			continue

		column_counter = 0

		for matrix_column in matrix_columns:

			if is_m == 1:

				# process the M matrix, just append to the M matrix list
				mmatrix_list.append(matrix_column)

			if is_m == 0:

				# process the N matrix, just append to the N matrix list
				nmatrix_list.append(matrix_column)

			column_counter += 1

		row_counter += 1

if is_m == 1:

	no_mmatrix_cols = column_counter
	no_mmatrix_rows = row_counter

if is_m == 0:

	no_nmatrix_cols = column_counter
	no_nmatrix_rows = row_counter

column_counter = 0
row_counter = 0

for matrix_column in mmatrix_list:
	
	#(row i, number of columns of N), (M, column j, value at row i and column j)
	print '(%s, %s), (M, %s, %s)' % (row_counter, no_nmatrix_cols, column_counter, matrix_column)

	if column_counter == (no_mmatrix_cols - 1):

		column_counter = 0
		row_counter += 1

	else:

		column_counter += 1
	
column_counter = 0
row_counter = 0

for matrix_column in nmatrix_list:
	
	#(number of columns of M, column k), (N, row j, value at row j and column k)
	print '(%s, %s), (N, %s, %s)' % (no_mmatrix_cols, column_counter, row_counter, matrix_column)

	if column_counter == (no_nmatrix_cols - 1):

		column_counter = 0
		row_counter += 1

	else:

		column_counter += 1

