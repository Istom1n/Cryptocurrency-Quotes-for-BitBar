#!/usr/bin/env python
# coding=utf-8

# <bitbar.title>Cryptocurrency quotes</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Ivan Istomin</bitbar.author>
# <bitbar.author.github>Ivan-Istomin</bitbar.author.github>
# <bitbar.desc>Displays top 10 cryptocurrency quotes.</bitbar.desc>
# <bitbar.image>https://istomin.im/gc/cc-quotes.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/Ivan-Istomin/Cryptocurrency-Quotes-for-BitBar</bitbar.abouturl>

import base64
import pickle
from collections import defaultdict
from os.path import realpath

import requests

## Get TOP 10 coin by total market cap
req_to_top = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=10').json()

## Get only symbols of this coin
symbols_of_top_ten_coins = [token['symbol'] for token in req_to_top]

## Get prices of the coins
coin_prices = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=%s&tsyms=USD,BTC' % ','.join(symbols_of_top_ten_coins)).json()['RAW']

icons_in_base64 = defaultdict(list)

## Try get icons from storage
try:
    with open(realpath('icons.pickle'), 'rb') as f:
        icons_in_base64 = pickle.load(f)
except IOError:
    ## Absents
    pass

## Fetch icons and encode it to base64 format (32x32)
if not icons_in_base64:
    lower_symbols = [s.lower() for s in symbols_of_top_ten_coins]

    for symbol in lower_symbols:
        response = requests.get('https://istomin.im/gc/icon/%s.png' % symbol)
        if response:
            icons_in_base64[symbol.upper()] = base64.b64encode(response.content)

# Save it to storage, because for persistent queries, you can get into the nose
with open(realpath('icons.pickle'), 'wb') as f:
    pickle.dump(icons_in_base64, f)
    

print('ICON TICKER USD CHANGE OPEN HIGH LOW RANK|font="Menlo"')
for i, coin in enumerate(coin_prices.keys()):
    coin_data = coin_prices[coin]['USD']
    print('{: <5} {:0<9.3f} {:0<+6.2f}% {:0<9.3f} {:0<9.3f} {:0<9.3f} {:0>3} | image={}'.format(coin, coin_data['PRICE'], coin_data['CHANGE24HOUR'], coin_data['OPEN24HOUR'], coin_data['HIGH24HOUR'], coin_data['LOW24HOUR'], i, icons_in_base64[coin]))

print('---')

print('ICON TICKER BTC CHANGE OPEN HIGH LOW RANK|font="Menlo"')
for i, coin in enumerate(coin_prices.keys()):
    coin_data = coin_prices[coin]['BTC']
    print('{: <5} {:0<9.7f} {:0<+6.2f}% {:0<9.7f} {:0<9.7f} {:0<9.7f} {:0>3} | image={}'.format(coin, coin_data['PRICE'], coin_data['CHANGE24HOUR'], coin_data['OPEN24HOUR'], coin_data['HIGH24HOUR'], coin_data['LOW24HOUR'], i, icons_in_base64[coin]))
