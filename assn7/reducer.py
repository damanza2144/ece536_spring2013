#!/usr/bin/env python

#############################################
# definitions:
#	M is a matrix with element mij in row i and column j
#	N is a matrix with element njk in row j and column k
#	P is a matrix = MN with element pik in row i and column k, where pik = sum( mij * njk )
#
# map algorithm:
#	For each element mij of M, emit a key-value pair (i, k), (M, j, mij) for k=1,2,... number of columns of N.
#												(row i, number of columns of N), (M, column j, value at row i and column j)
#	For each element njk of N, emit a key-value pair (i, k), (N, j, njk) for i=1,2,... number of columns of M.
#												(number of columns of M, column k), (N, row j, value at row j and column k)
#
# reduce algorithm:
#	For each key (i, k), emit the key-value pair (i, k), pik where pik = sumj( mij * njk )
#
#############################################

import sys
import string

def clean_string( current_word ):

	current_word = current_word.strip()
	current_word = current_word.replace('(','')
	current_word = current_word.replace(')','')

	return current_word

no_ncols = 0
no_mcols = 0

no_nrows = 0
no_mrows = 0

row_counter = 0
col_counter = 0

matrix_value = 0.0



mmatrix_list = []
nmatrix_list = []
pmatrix_list = []

interim_list = []
prev_counter = 0

was_m = -1

# input comes from STDIN
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	if line:

		# parse the input we got from mapper.py
		a, b, c, d, e = line.split( ',', 4 )

		a = clean_string(a)
		b = clean_string(b)
		c = clean_string(c)
		d = clean_string(d)
		e = clean_string(e)

		#print '%s' % (line)
		if c == 'M':

			#(row i, number of columns of N), (M, column j, value at row i and column j)
			no_ncols = int(b)
			row_counter = int(a)
			col_counter = int(d)
			matrix_value = float(e)

			#print 'processing m matrix here'
			#print 'M: no_ncols=%s, row_counter=%s, col_counter=%s, matrix_value=%s' % (no_ncols, row_counter, col_counter, matrix_value)

			if row_counter > prev_counter:

				mmatrix_list.append( interim_list )
				interim_list = []

			interim_list.append( matrix_value )

			prev_counter = row_counter
			was_m = 1

		if c == 'N':

			if was_m == 1:

				mmatrix_list.append( interim_list )
				interim_list = []

			#(number of columns of M, column k), (N, row j, value at row j and column k)
			no_mcols = int(a)
			row_counter = int(d)
			col_counter = int(b)
			matrix_value = float(e)

			#print 'processing n matrix here'
			#print 'N: no_mcols=%s, row_counter=%s, col_counter=%s, matrix_value=%s' % (no_mcols, row_counter, col_counter, matrix_value)
			
			if col_counter > prev_counter:

				# do a multiply and add to get a pik???
				print 'ncol_vector_%s=%s' % (prev_counter, interim_list)
				interim_list = []

			interim_list.append( matrix_value )
			prev_counter = col_counter
			was_m = 0

if was_m == 0:

	# do a multiply and add to get a pik???
	print 'ncol_vector_%s=%s' % (prev_counter, interim_list)

#print 'mmatrix_list=%s' % (mmatrix_list)
#for matrix_column in mmatrix_list:
#	print 'matrix_column=%s' % (matrix_column)


