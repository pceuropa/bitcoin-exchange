# !/usr/bin/env python3.6
#-*- coding:utf-8 -*-
"""
File: bittrex.py
Author: Rafal Marguzewicz
Email: info@pceuropa.net
Github: https://github.com/pceuropa
Description: Console to bittrex
"""

from os import system
from datetime import datetime
from urllib.request import urlopen
from time import sleep, time
from json import load
from terminaltables import AsciiTable
from terminalcolor import Colors
# import pandas as ps


class Ask(Colors):
    """Docstring for MyClass. """

    data = []
    colors = Colors()
    url_ver1 = 'https://bittrex.com/api/v1.1/public/'
    url_ver2 = 'https://bittrex.com/Api/v2.0/pub/market/'
    bittrexUrl = 'https://bittrex.com/Market/Index?MarketName='
    url_rest = '&tickInterval=thirtyMin&_='
    market = 'usdt-neo'
    last_id = 0
    #?marketName=BTC-NEO&tickInterval=thirtySek&_=1503140278790

    def __init__(self, market):
        if market is not None:
            self.market = market

    def read_url(self, url, **kwargs):
        """ Get json from http """
        ver = kwargs.get('ver', 2)
        timestamp = format(time() * 1000, '.0f')

        if ver == 1:
            url = self.url_ver1 + url
        else:
            url = self.url_ver2 + url + self.url_rest + timestamp

        response = urlopen(url)
        data = load(response)
        return data['result']

    def orderbook(self):
        """ Orderbook """
        url = 'getorderbook?market='+ self.market + '&type=both'
        result = self.read_url(url, ver=1)
        buy = result['buy'][:9]
        sell = result['sell'][:9]

        sum_buy = 0
        sum_sell = 0
        sum_fiat_buy = 0
        sum_fiat_sell = 0

        for b in buy:
            sum_buy += b['Quantity']
            sum_fiat_buy += b['Quantity'] * b['Rate']

        for b in sell:
            sum_sell += b['Quantity']
            sum_fiat_sell += b['Quantity'] * b['Rate']

        first_buy = buy[0]['Rate']
        first_sell = sell[0]['Rate']

        need = int(sum_buy - sum_sell)

        sum_buy = int(sum_buy)
        sum_sell = int(sum_sell)
        sum_fiat_buy = int(sum_fiat_buy)
        sum_fiat_sell = int(sum_fiat_sell)
        ratio = sum_buy / sum_sell
        return {'First_buy': first_buy, 'First_sell': first_sell, 'Sum_buy': sum_buy, 'Sum_sell': sum_sell, 'Need': need,
                'Ratio': ratio}

    def marketsummary(self):
        """ Market summary """
        url = 'getmarketsummary?marketName=' + self.market
        return self.read_url(url)

    def markethistory(self):
        """ Market history"""
        #{"Id":1,"TimeStamp":"2017-08-19T10:52:33.94","Quantity":6.25187874,"Price":0.00925000,"Total":1,"FillType":"FILL","OrderType":"BUY"}
        url = 'getmarkethistory?marketName=' + self.market
        count_buy, count_sell, sum_buy, sum_sell = (0, 0, 0, 0)
        data = self.read_url(url)

        for i in data:
            if i['Id'] == self.last_id:
                break

            if i['OrderType'] == 'BUY':
                count_buy += 1
                sum_buy += i['Quantity']
            else:
                count_sell += 1
                sum_sell += i['Quantity']

            #print(i['OrderType'], i['Quantity'], i['Price'], i['Total'])
        self.last_id = data[0]['Id']
        return {"Last_trade_id": self.last_id,
                "Count_buy": count_buy,
                "Count_sell": count_sell,
                "Trade": count_buy - count_sell
                }

        #print([count_buy, count_sell, last_id ])

    def all(self):
        """ Concact all data to one json"""
        """Orderbook | marketsummary and history"""
        o = self.orderbook()
        o.update(self.markethistory())
        o.update(self.marketsummary())
        return o

    def interval(self):
        """ Check one market every 6 seconds"""
        volume = 0
        system("clear")
        print(Colors.HEAD + self.market + Colors.END)
        while True:
            o = self.all()
            volume = float(o['BaseVolume'])
            try:
                last_volume = float(self.data[-1]['BaseVolume'])
            except:
                last_volume = volume
            finally:
                o['ChangeVolume'] = volume - last_volume

            self.data.append(o)
            self.print_row(o)
            sleep(6)

    def print_row(self, data):
        """ Return one row of data """
        # date = datetime.fromtimestamp(time()).strftime("%H:%M:%S")

        c = Colors()
        if data['Last'] == data['Bid']:
            data['Bid'] = c.bold(data['Bid'], '.8f')
        else:
            data['Bid'] = format(data['Bid'], '.8f')

        if data['Last'] == data['Ask']:
            data['Ask'] = c.bold(data['Ask'], '.8f')
        else:
            data['Ask'] = format(data['Ask'], '.8f')

        data['Last'] = format(data['Last'], '.7f')

        data['Need'] = c.zero(data['Need']).rjust(6)

        if data['Ratio'] > 3:
            data['Ratio'] = c.bold(data['Ratio'], '2.1f')
        else:
            data['Ratio'] = format(data['Ratio'], '2.1f')

        data['Trade'] = c.zero(data['Trade']).rjust(4)

        data['BaseVolume'] = format(data['BaseVolume'], '.2f')

        ChangeVolume = float(data['ChangeVolume'])

        if ChangeVolume < 0:
            data['ChangeVolume'] = c.fail(ChangeVolume, '2.3f').rjust(4)
        elif ChangeVolume == 0:
            data['ChangeVolume'] = ''
        else:
            data['ChangeVolume'] = c.green(ChangeVolume, '2.3f')

        data = (data['Bid'], data['Last'], data['Ask'],
                data['Sum_buy'], data['Sum_sell'], data['Need'], data['Ratio'],
                data['Count_buy'], data['Count_sell'], data['Trade'],
                data['BaseVolume'], data['ChangeVolume'])

        print('%s | %s | %s | %i/%i|%s | %s | %3i | %3i | %4s | %s %s' % data)

    def markets(self, type):
        """ Search anomalie on all makrets"""
        system("clear")
        print(self.colors.head(type))
        while True:
            result = self.read_url('getmarketsummaries', ver=1)
            row = {}
            for i in result:
                if 'BTC-' in i['MarketName']:
                    i['ChangeVolume'], i['ChangeLast'] = (0, 0)
                    baseVolume, last = (float(i['BaseVolume']), float(i['Last']))
                    try:
                        last_volume = float(self.data[-1][i['MarketName']]['BaseVolume'])
                        last = float(self.data[-1][i['MarketName']]['Last'])
                    except:
                        last_volume = baseVolume
                    finally:
                        i['ChangeVolume'] = int(baseVolume - last_volume)
                        baseVolume = int(i['BaseVolume'])
                        i['ChangeLast'] = i['Last'] - last
                        row[i['MarketName']] = i
                        date = datetime.fromtimestamp(time()).strftime("%H:%M:%S")

                    if type == 'volume':
                        percent = i['ChangeVolume'] / i['BaseVolume'] * 100
                        if i['ChangeVolume'] > 4 and percent != 0 and percent > 0.1:
                            percent = format(percent, '.2f').ljust(4)
                            changeVolume = str(i['ChangeVolume']).ljust(3)

                            print(changeVolume, percent, baseVolume, self.bittrexUrl + i['MarketName'], date)

                    if type == 'last':
                        percent = int(i['ChangeLast'] / i['Last'] * 100)
                        if percent >= 4 or percent <= -4:
                            last = self.colors.zero(format(i['Last'], '.8f'))
                            changeLast = format(i['ChangeLast'], '.8f')
                            print(last, changeLast, percent, date, self.bittrexUrl + i['MarketName'],)

            self.data.append(row)
            sleep(180)

    def table(self, table_data):
        """ Return table with data """
        print(AsciiTable(table_data).table)
