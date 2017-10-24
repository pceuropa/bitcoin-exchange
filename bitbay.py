# !/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
For all, demo beta
"""

from urllib.request import urlopen
import json
from terminaltables import AsciiTable
import os
from foreign import rates
from poloniex import currency
import time
from datetime import datetime
import argparse
from terminalcolor import Colors


def strong(string):
    print(colors.bold(string))


def summary(currency=None, second_currency='pln'):
    colors = Colors()
    if currency is None:
        currency = 'btc'
    if second_currency is None:
        second_currency = 'pln'
    url = "https://bitbay.net/API/Public/" + currency + second_currency +"/all.json"
    data = json.load(urlopen(url))
    bids = data["bids"][0:4]
    asks = data["asks"][0:4]
    last_transactions = data['transactions']

    table1 = [
        ['Min', 'Now', 'Max'],
        [data['min'], data['last'], data['max']],
        [format(data['last'] - data['min'], '.2f'), '<==>', format(data['max'] - data['last'], '.2f')]
    ]

    table2 = [
        ['bids', 'asks'],
        [bids[0], asks[0]],
        [bids[1], asks[1]],
        [bids[2], asks[2]],
    ]

    print(colors.bold('Volumen:'), format(data['volume'], '.2f'))
    print(AsciiTable(table1).table)
    print(AsciiTable(table2).table)
    print("Stablizacja ceny:", format(asks[0][0] - bids[0][0], '.2f'))

    for x in last_transactions[0:20]:
        amount = format(x['amount'], '.3f')
        price = format(x['price'], '.1f')
        date = datetime.fromtimestamp(int(x['date']) +3600).strftime("%H:%M:%S")
        if x['type'] == 'sell':
            print('', price, amount, date)
        else:
            print('\t\t\t', price, amount, date)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("currency", help="[btc|eth|bcc]")
    p.add_argument("-s", help="Second currency. [pln|eur|usd] Default pln")
    args = p.parse_args()

    if args.currency:
        print(args.currency)
        while True:
            os.system("clear")
            try:
                usd_btc = currency(args.currency)
                pln_btc = usd_btc * rates()

                print(colors.bold('poloniex'), '%.1f' % pln_btc, '(%.1f)' % usd_btc, )
            except:
                pass
            summary(args.currency, args.s)
            time.sleep(15)
