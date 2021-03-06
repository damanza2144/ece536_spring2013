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

# This function cleans the input string into this file.
def clean_string( current_word ):

	current_word = current_word.strip()
	current_word = current_word.replace('(','')
	current_word = current_word.replace(')','')

	return current_word

mmatrix_list = []
pmatrix_list = []

no_mcols = 0
no_mrows = 0	
no_ncols = 0

# Initialize the pmatrix_list to be a multi-dimensional list (like an array)
# with the number of rows equal to the number of rows of matrix M and the 
# number of colums equal to the number of columns of matrix N.  Set all values
# to an initial value of 0.
def init_pmatrix( no_mrows, no_ncols ):

	#print 'no_mrows=%s, no_ncols=%s' % (no_mrows, no_ncols)
	for i in range( no_mrows ):

		interim_list = []
		for j in range( no_ncols ):
			
			interim_list.append(0)

		pmatrix_list.append(interim_list)

# Assign the resultant column vector from the multiplication/addition 
# to the columns in the pmatrix_list.  So the idea here is that the 
# column_vector will be a "vector" or a list with values that should 
# be inserted into a column_number in the pmatrix_list, which is the 
# resultant matrix.
def assign_col_vector( col_num, col_vector ):

	counter = 0

	for col_element in col_vector:

		pmatrix_list[counter][col_num] = col_element
		counter += 1

# This procedure processes the multiplication and addition of the 
# matrix's N column vector and the mmatrix_list (M matrix).  At the
# end, it calls the previous function to assign the resultant column
# vector the the P resultant matrix.
def process_mult_add( col_num, ncol_vector ):

	#print 'ncol_vector=%s' % (ncol_vector)

	# At this point, I am assuming that the number of M columns 
	# is equal to the number of N rows.  The check should have 
	# already happened.

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

row_counter = 0
col_counter = 0
matrix_value = 0.0
interim_list = []
prev_counter = 0
was_m = -1

# input comes from STDIN
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	if line:

		# parse the input that is comma-delimited that we got 
		# from mapper.py output.
		a, b, c, d, e = line.split( ',', 4 )

		a = clean_string(a)
		b = clean_string(b)
		c = clean_string(c)
		d = clean_string(d)
		e = clean_string(e)

		#print '%s' % (line)
		if c == 'M':

			# The following input is what we need to parse:
			#	(row i, number of columns of N), (M, column j, value at row i and column j)
			no_ncols = int(b)
			row_counter = int(a)
			col_counter = int(d)
			matrix_value = float(e)

			#print 'processing m matrix here'
			#print 'M: no_ncols=%s, row_counter=%s, col_counter=%s, matrix_value=%s' % (no_ncols, row_counter, col_counter, matrix_value)

			if row_counter > prev_counter:

				mmatrix_list.append( interim_list )
				interim_list = []
				no_mrows = row_counter + 1

			interim_list.append( matrix_value )

			prev_counter = row_counter
			was_m = 1

		if c == 'N':

			if was_m == 1:

				# The mapper will always output the M matrix stuff first and 
				# then the N matrix, even if the N matrix is depicted first.
				init_pmatrix( no_mrows, no_ncols )
				mmatrix_list.append( interim_list )
				interim_list = []

			# The following input is what we need to parse:
			#	(number of columns of M, column k), (N, row j, value at row j and column k)
			no_mcols = int(a)
			row_counter = int(d)
			col_counter = int(b)
			matrix_value = float(e)

			#print 'N: no_mcols=%s, row_counter=%s, col_counter=%s, matrix_value=%s' % (no_mcols, row_counter, col_counter, matrix_value)
			
			if col_counter > prev_counter:

				# do a multiply and add to get a pik
				process_mult_add( prev_counter, interim_list )
				
				#print 'ncol_vector_%s=%s' % (prev_counter, interim_list)
				interim_list = []

			interim_list.append( matrix_value )
			prev_counter = col_counter
			was_m = 0

if was_m == 0:

	# do a multiply and add to get a pik
	process_mult_add( prev_counter, interim_list )
	#print 'ncol_vector_%s=%s' % (prev_counter, interim_list)

#print 'pmatrix_list=%s' % (pmatrix_list)
print 'result = %s' % (pmatrix_list)

