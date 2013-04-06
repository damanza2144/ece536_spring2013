#!/usr/bin/env python

import sys
import string

# input comes from STDIN (standard input)
for line in sys.stdin:

        # remove leading and trailing whitespace
        line = line.strip()

        # split the line into words
        words = line.split()

        # increase counters
        for word in words:

                # all these cases stripped out the punctuation things 
                # in between the words

                #word = ''.join(e for e in word if e.isalpha())
                #word = "".join(e for e in word if e.isalpha())

                #exclude = set(string.punctuation)
                #word = ''.join(e for e in word if e not in exclude)

                #for c in string.punctuation:
                #word = word.replace( c, "" )

                # so I decided to use these two functions to strip out 
                # before and after the word
                word = word.rstrip( string.punctuation )
                word = word.lstrip( string.punctuation )

                if word:

                        # write the results to STDOUT (standard output);
                        # what we output here will be the input for the
                        # Reduce step, i.e. the input for reducer.py
                        #
                        # tab-delimited; the trivial word count is 1
                        print '%s\t%s' % (word, 1)
