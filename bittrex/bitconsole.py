#  !/usr/bin/env python3.6
#-*- coding:utf-8 -*-
"""
File: bitconsole.py
Author: Rafal Marguzewicz
Email: info@pceuropa.net
Github: https://github.com/pceuropa/bittrex
Description: Console to bittrex
"""

from argparse import ArgumentParser
from bittrex import Ask

if __name__ == '__main__':
    Arg = ArgumentParser()
    Arg.add_argument("service", help="[interval | markets | all | markethistory | find]")
    Arg.add_argument("-c", '--currency')
    Arg.add_argument("-t", '--type', help="last|volume")
    Args = Arg.parse_args()

    bittrex = Ask(Args.currency)

    if 'service' in Args:
        if Args.service == "interval":
            bittrex.interval()

        if Args.service == "markets":
            bittrex.markets(Args.type)

        if Args.service == "all":
            print(bittrex.all())

        if Args.service == "markethistory":
            bittrex.markethistory()

        if Args.service == "find":
            bittrex.find()
    else:
        print('bad service')
