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
#import argparse
from optparse import OptionParser

row_counter = 0

#parser = argparse.ArgumentParser(description='Process matrix multiplication')
#parser.add_argument('-m', help='M matrix')
#parser.add_argument('-n', help='N matrix')
#args = parser.parse_args()

parser = OptionParser()
parser.add_option('-m', action='store', dest='mfile', help='M matrix', metavar='FILE')
parser.add_option('-n', action='store', dest='nfile', help='N matrix', metavar='FILE')
(options, args) = parser.parse_args()
#print '%s\t%s' % (options, args)

print 'M matrix:'
for line in open(options.mfile):
	print '%s' % (line)

print 'N matrix:'
for line in open(options.nfile):
	print '%s' % (line)




