#!/bin/python3

# Takes in input and output as stdin,
# prints json formatted string to stdout

import sys
from utils.parser import *

ip = input_parser()
op = output_parser()

is_input = True

data = {}

lines = sys.stdin.readlines()
if not len(lines) == 2:
    raise Exception()
ip.parse(lines[0])
op.parse(lines[1])
if (not ip.is_valid()) or (not op.is_valid()):
    raise Exception()

print('{ "input": '+ip.to_json()+', "output": '+op.to_json()+'}')
