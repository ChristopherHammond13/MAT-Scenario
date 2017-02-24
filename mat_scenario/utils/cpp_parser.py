from parser import input_parser
import getopt
import os.path
import sys

def main(argv):
    input_file = ""
    output_dir = ""
    help_string = "Usage: main.py -n <tests_to_run> -i <input_file> -o <output_directory>"
    try:
        opts, _ = getopt.getopt(argv, "hn:i:o:", ["number=", "ifile=", "odir="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)

    number = 30

    for opt, arg in opts:
        if opt == "-h":
            print(help_string)
            sys.exit()
        elif opt in ("-n", "--number"):
            number = int(arg)
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--odir"):
            output_dir = arg

    if not os.path.isfile(input_file):
        print("Input file does not exist")
        sys.exit(1)

    if output_dir == "":
        output_dir = "./"

    if output_dir[-1] != "/":
        output_dir = output_dir + "/"

    try:
        problemset_file = open(input_file)
        print("Opened " + input_file)
    except IOError:
        print("Unable to open input file")
        sys.exit(1)

    parse(problemset_file, number, output_dir)

def parse(problemset_file, number, output_dir):

    _parser = input_parser()

    for problem in problemset_file:
        _parser.parse(problem)
        if _parser.index in range(1, number):
            if _parser.is_valid():
                with open("{0}problem{1}.environment".format(output_dir,_parser.index), 'w+') as f:
                    f.write(_parser.print_environment())
                with open("{0}problem{1}.guards".format(output_dir,_parser.index), 'w+') as f:
                    f.write(_parser.print_guards())

if __name__ == '__main__':
    main(sys.argv[1:])
