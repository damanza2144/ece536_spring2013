#!/usr/bin/env python

import sys

# This function cleans the input string into this file.
def clean_string( current_word ):

	current_word = current_word.strip()
	current_word = current_word.replace('[','')
	current_word = current_word.replace(']','')
	current_word = current_word.replace(',','')

	return current_word

# input comes from STDIN
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	if line:

		# parse the input that is tab-delimited that we got 
		# from mapper.py output and sort.
		str_matrix_val, my_str_vector = line.split( '\t', 1 )

		# the str_matrix_val is the M scalar
		matrix_val = float( str_matrix_val )

		# this will contain the column vector for x
		my_vector = []

		# split the str_vector into "words"
		elements = my_str_vector.split()

		for val in elements:

			# each of the words will have some characters that should not be there
			val = clean_string( val )
			
			# append to the my_vector list the floating point value
			my_vector.append( float(val) )

		result_vector = []
		for element in my_vector:
		
			# for each of the floating point values in my_vector list, multiply by the M scalar
			result_vector.append(matrix_val * element)

		# output the M scalar, the x vector, and the resultant vector
		print '%s\t%s\t%s' % (matrix_val, my_vector, result_vector)

