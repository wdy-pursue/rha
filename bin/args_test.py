import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument('--is_test', type=int, default=0)
args_test = parser.parse_args()