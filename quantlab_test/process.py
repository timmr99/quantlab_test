#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import csv
from itertools import dropwhile, takewhile

def parse_command_line ():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', dest='file', help='file to process')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='debug')
    parser.add_argument('-o', '--output', dest='output', help='output')

    options = parser.parse_args()

    return options


def reader(filename, criterion=None, element=None):
    with open(filename, "r") as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if criterion is None:
                yield row
            else:
                if row[element] == criterion:
                    yield row
    return


def get_symbols(filename):
    syms = {}
    for row in reader(filename):
        syms[row[1]] = 0;

    return syms


def accumulate(filename, symbols):
    for s in sorted(symbols.keys()):
        values = {}
        cnt = 0
        for r in reader(filename, s,1):
            t = int(r[0])
            values[t] = {}
            values[t]['q'] = int(r[2])
            values[t]['c'] = int(r[3])
            cnt += 1
        yield (s,values)


def get_min_gap(times):
    _min = times[0]
    _max = 0
    for i in range(len(times)):
        if(times[i] < _min):
            _min = times[i]
        elif (times[i] - _min > _max):
            _max = times[i] - _min
    return _max


def calc_values_by_sym(filename,symbols,output):
    max_gap = 0
    total_volume = 0
    max_trade = 0
    w_avg = 0

    with open(output, "w+") as output:
        for v in accumulate(filename, symbols):
            main_key = v[0]
            max_gap = get_min_gap(sorted(v[1].keys()))
            for _,z in v[1].items():
                total_volume += z['q']
                max_trade = z['c'] if z['c'] > max_trade else max_trade

            top_weight_avg = 0
            bot_weight_avg = 0
            for _,z in v[1].items():
                top_weight_avg += z['c'] * z['q']
                bot_weight_avg += z['q']

            weighted_avg = int(top_weight_avg / bot_weight_avg)

            output.write('{},{},{},{},{}\n'.format(main_key,max_gap, total_volume, max_trade, weighted_avg))


def main():
    options = parse_command_line()

    if not options.file:
        raise SystemExit('Required file name not specified, add --file')

    if not options.output:
        raise SystemExit('Required output file name not specified, add --output')

    symbols = get_symbols(options.file)

    calc_values_by_sym(options.file,symbols,options.output)

    return 0

if __name__ == '__main__':
    sys.exit(main())

# eos
