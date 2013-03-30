#!/usr/bin/env python

import sys


current_word	= None
current_count	= 0
word			= None

current_nowords	= 0

# input comes from STDIN (standard input)
for line in sys.stdin:

	# remove leading and trailing whitespace
	line = line.strip()

	# parse the input we got from reducer.py
	nowords, word, count = line.split( '\t', 2 )
	
	#print '%s\t%s\t%s' % ( nowords, word, count )


	# convert nowords (currently a string) to int
	try:

		nowords = int( nowords )

	except ValueError:

		# nowords was not a number, so silently
		# ignore/discard this line
		continue

	if nowords == current_nowords:
		
		if count > current_count:

			#print '%s\t%s\t%s' % ( current_nowords, current_word, current_count )
			current_count	= count
			current_nowords	= nowords
			current_word	= word

	elif nowords > current_nowords:

		if current_word:

			print '%s\t%s\t%s' % ( current_nowords, current_word, current_count )

		current_count	= count
		current_nowords	= nowords
		current_word	= word

	#print 'TST---%s\t%s\t%s' % ( nowords, word, count )

#print 'FNL---%s\t%s\t%s' % ( current_nowords, current_word, current_count )
print '%s\t%s\t%s' % ( current_nowords, current_word, current_count )

