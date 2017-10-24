# !/usr/bin/env python3.6
#-*- coding:utf-8 -*-

"""
POloniex
"""

from urllib.request import urlopen
from json import load

url ='https://poloniex.com/public?command=returnTicker'


def currency(currency):
    try:
        ticker = load(urlopen(url))
    except:
        print('problem connection poloniex')

    code = 'USDT_' + currency.upper()
    c = float(ticker[code]["last"])
    return c


if __name__ == '__main__':
    print(currency('BTC'))
    print(currency('ETH'))
