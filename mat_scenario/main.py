#!/usr/bin/python

from visibility import graph
from utils import parser
import sys
import getopt
import os.path


def main(argv):
    '''
    Parses command line args and calls appropriate function
    '''
    input_file = ""
    output_file = ""
    help_string = "Usage: main.py -i <input_file> -o <output_file>"

    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(help_string)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    if not os.path.isfile(input_file):
        print("Input file does not exist")
        sys.exit(1)

    if output_file == "":
        output_file = "output.mat"

    if os.path.isfile(output_file):
        print("Specified output file already exists")
        sys.exit(1)

    try:
        problemset_file = open(input_file)
        print("Opened " + input_file)
    except IOError:
        print("Unable to open input file")
        sys.exit(1)

    solve(problemset_file)


def solve(problemset_file):
    """
    Solves a problem given to it
    """
    _parser = parser.input_parser()
    _parsed_string = "Problems parsed: "
    """
    Our problems are stored in a map<int, (robots:[point],polygons:[[point]])>
    """
    _problemset = {}

    for problem in problemset_file:
        _parser.parse(problem)
        _parsed_string += str(_parser.index) + ";"
        _problemset[_parser.index] = (_parser.robots, _parser.polygons)

    print(_parsed_string)


if __name__ == '__main__':
    main(sys.argv[1:])
