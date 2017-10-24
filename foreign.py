# !/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
 Foreign exange PLN, Euro ,USDT , BTC
"""

from urllib.request import urlopen
from json import load
from argparse import ArgumentParser
from bittrex.bittrex import Ask


def rates():
    url = "http://api.fixer.io/latest?base=USD"
    rates = load(urlopen(url))
    return float(rates["rates"]["PLN"])


def all_rates():
    url = "http://api.fixer.io/latest?base=PLN"
    rates = load(urlopen(url))
    return rates["rates"]


if __name__ == '__main__':
    currencies = all_rates()
    ask = Ask('usdt-btc')
    btc = ask.marketsummary()
    btc = btc["Last"]
    pln_usd = 1 / currencies["USD"]
    pln_eur = 1 / currencies["EUR"]
    btc_pln = btc * pln_usd

    print("usd:", format(pln_usd, '.2f'))
    print("eur:", format(pln_eur, '.2f'))
    print("btc:", format(btc_pln, '.2f'))

    p = ArgumentParser()
    p.add_argument("amount", help="450")
    args = p.parse_args()

    if args.amount:
        amount = args.amount
        print(amount, "usd", format(float(amount) * pln_usd, '.1f'), 'PLN')
        print(amount, "eur", format(float(amount) * pln_eur, '.1f'), 'PLN')
        print(amount, "btc", format(float(amount) * btc, '.1f'), 'USD')
