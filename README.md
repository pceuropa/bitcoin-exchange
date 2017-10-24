# bitcoin-exchange

foreign.py - show exchange rates USD, EUR, BTC. Optionaly calculates the price of the indicated quantity.
```
usage: foreign.py [-h] amount

positional arguments:
  amount      450

optional arguments:
  -h, --help  show this help message and exit
example: python3 foreign.py btc
```

bitbay.py - show all the important dataa needed to analyze the trends and moods on the bitbay exchange
```
usage: bitbay.py [-h] [-s] currency

positional arguments:
  currency    [btc|eth|bcc]

optional arguments:
  -h, --help  show this help message and exit
  -s          Second currency. [pln|eur|usd] Default pln
example: python3 bitbay.py btc
```

bittrex/bitconsole.py - show all the important dataa needed to analyze the trends and moods on the bittrex exchange
```
usage: bitconsole.py [-h] [-c CURRENCY] [-t TYPE] service

positional arguments:
  service               [interval | markets | all | markethistory | find]

optional arguments:
  -h, --help            show this help message and exit
  -c CURRENCY, --currency CURRENCY
  -t TYPE, --type TYPE  last|volume

example: python3 bittrex/bitconsole.py interval -c btc-neo
```

inotifywait.sh - script run file of second argument every change.
```
sh inotifywaith.sh file_to_reload.py
```
