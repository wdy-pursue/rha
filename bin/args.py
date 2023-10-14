import argparse
import re

def convert_to_byte(size):
    result = re.search('(\d+\.?\d*)(b|kb|mb|gb|tb)', size.lower())
    if (result and result.groups()):
        unit = result.groups()[1]
        amount = float(result.groups()[0])
        index = ['b', 'kb', 'mb', 'gb', 'tb'].index(unit)
        return amount * pow(1024, index)
    raise ValueError("Invalid size provided, value is " + size)

parser = argparse.ArgumentParser()
parser.add_argument('--configjson',type=str)
parser.add_argument('--redrawcount', type=int)
parser.add_argument('--redraw_methods', type=int)
parser.add_argument('--redrawcamplitude', type=str)
parser.add_argument('--fixcount', type=int)
parser.add_argument('--control_methods', type=int)
parser.add_argument('--t', type=int)
args = parser.parse_args()