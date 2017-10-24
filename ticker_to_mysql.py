# !/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
Btc ticker save to mysql
"""

from urllib.request import urlopen
import pymysql as my
import json

url = urlopen("https://bitbay.net/API/Public/btcpln/ticker.json")
db = my.connect("localhost", "root", "", "bitcoin")
data = json.load(url)

records = "`" + '`,`'.join(data) + "`"
values = ",".join([str(data[x]) for x in data])

cursor = db.cursor()
sql = "INSERT INTO `btc_ticker`(" + records + ") VALUES (" + values + ")"
print(sql)
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

# disconnect from server
db.close()
