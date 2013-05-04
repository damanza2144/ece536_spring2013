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

# create lists for the M and P matrices -- needed for both reducer and mapper functions
mmatrix_list = []
pmatrix_list = []

### reducer code ###

def init_pmatrix( no_mrows, no_ncols ):

	#print 'no_mrows=%s, no_ncols=%s' % (no_mrows, no_ncols)
	for i in range( no_mrows ):

		interim_list = []
		for j in range( no_ncols ):

			interim_list.append( 0 )

		pmatrix_list.append( interim_list )

def assign_col_vector( col_num, col_vector ):

	counter = 0

	for col_element in col_vector:

		pmatrix_list[counter][col_num] = col_element
		counter += 1

def process_mult_add( col_num, ncol_vector ):

	#print 'ncol_vector=%s' % (ncol_vector)
	# I am assuming that the number of M columns = number of N rows
	pcol_vector = []
	for mmatrix_row in mmatrix_list:

		counter = 0
		sum = 0.0

		for mmatrix_element in mmatrix_row:

			#print 'counter=%s' % counter
			sum += mmatrix_element * ncol_vector[ counter ]
			counter += 1

		#print 'sum=%s' % sum
		pcol_vector.append( sum )

	#print 'col_num=%s, pcol_vector=%s' % (col_num, pcol_vector)
	assign_col_vector( col_num, pcol_vector )

### mapper code ###

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

# create list for the N matrix
nmatrix_list = []

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
		elif line == 'N:':

			# set the bit to signify that the next rows and columns are an N matrix
			is_m = 0

			no_mmatrix_cols = column_counter
			no_mmatrix_rows = row_counter

			# reset the row counter
			row_counter = 0
			continue

		else:

			column_counter = 0
			interim_list = []

			for matrix_column in matrix_columns:

				interim_list.append( int(matrix_column) )
				column_counter += 1

			if is_m == 1:

				# process the M matrix, just append to the M matrix list
				mmatrix_list.append( interim_list )

			if is_m == 0:

				# process the N matrix, just append to the N matrix list
				nmatrix_list.append( interim_list )

			row_counter += 1

if is_m == 1:

	no_mmatrix_cols = column_counter
	no_mmatrix_rows = row_counter

if is_m == 0:

	no_nmatrix_cols = column_counter
	no_nmatrix_rows = row_counter

#print 'no_mmatrix_cols=%s, no_mmatrix_rows=%s, mmatrix_list=%s' % (no_mmatrix_cols, no_mmatrix_rows, mmatrix_list)
#print 'no_nmatrix_cols=%s, no_nmatrix_rows=%s, nmatrix_list=%s' % (no_nmatrix_cols, no_nmatrix_rows, nmatrix_list)

### reducer code ###

init_pmatrix( no_mmatrix_rows, no_nmatrix_cols )

#print 'no_mmatrix_rows=%s, no_nmatrix_cols=%s, pmatrix_list=%s' % (no_mmatrix_rows, no_nmatrix_cols, pmatrix_list)

for column_counter in range( no_nmatrix_cols ):

	interim_list = []

	for nmatrix_row in nmatrix_list:
		
		interim_list.append( nmatrix_row[column_counter] )
		
	#print 'column_counter=%s, interim_list=%s' % (column_counter, interim_list)
	process_mult_add( column_counter, interim_list )

print 'pmatrix_list=%s' % (pmatrix_list)


