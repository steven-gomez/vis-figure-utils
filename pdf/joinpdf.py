#!/usr/bin/env python
# encoding: utf-8
"""
joinpdf.py

Created by Steven Gomez on 2013-04-27.
Copyright (c) 2013 steveg. All rights reserved.

This script will join multiple PDFs into one PDF document.
It is a python wrapper around a simple ghostscript command. 
"""

import sys
import getopt
from subprocess import call


help_message = '''
This script takes one or more input PDFs and joins them. By default, it will
create a new PDF called output.pdf that appends the input pdfs in the order
you specify them. You can provide an optional output file name.

Correct usage is:
  python joinpdf.py -o <output file name> <input pdf #1> <input pdf #2> ...

For example,
  python joinpdf.py -o MyNewMergedPDF.pdf input1.pdf input2.pdf input3.pdf
	
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	# Default output filename
	output = "output.pdf"
	
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
		
		# If there are no PDFs to join, remind the user about usage.
		if len(args) == 0:
			raise Usage(help_message)
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
	
	# Call ghostscript with the output file name and input files.
	args_list = ["gs", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite", "-sOutputFile="+output]
	args_list.extend(args)
	call(args_list)


if __name__ == "__main__":
	sys.exit(main())
