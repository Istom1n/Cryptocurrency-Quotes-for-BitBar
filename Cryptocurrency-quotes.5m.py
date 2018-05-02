#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>Cryptocurrency quotes</bitbar.title>
# <bitbar.version>v1.1</bitbar.version>
# <bitbar.author>Ivan Istomin</bitbar.author>
# <bitbar.author.github>Ivan-Istomin</bitbar.author.github>
# <bitbar.desc>Displays top 10 cryptocurrency quotes.</bitbar.desc>
# <bitbar.image>https://istomin.im/gc/cc-quotes.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/Ivan-Istomin/Cryptocurrency-Quotes-for-BitBar</bitbar.abouturl>

import base64
import pickle
from collections import defaultdict

import requests

class Icons:
    ## Cache path
    ICONS_PATH = '/var/tmp/icons.pickle'
    
    def __init__(self):
        ## Get TOP 10 coin by total market cap
        req_to_top = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=10').json()

        ## Get only symbols of this coin
        self.symbols_of_top_ten_coins = [token['symbol'] for token in req_to_top]

        ## Try get icons from storage
        self.load_icons()

        ## IOTA/MIOTA, блять
        index_of_miota = self.symbols_of_top_ten_coins.index('MIOTA')
        if index_of_miota != -1:
            self.symbols_of_top_ten_coins[index_of_miota] = 'IOTA'
        
        ## Fetch icons and encode it to base64 format
        # Resolition: 32x32
        # DPI: 144
        lower_symbols = [s.lower() for s in self.symbols_of_top_ten_coins]
        for symbol in lower_symbols:            
            if symbol not in self.icons_in_base64:
                response = requests.get('https://istomin.im/gc/icon/{}.png'.format(symbol))
                if response:
                    self.icons_in_base64[symbol] = base64.b64encode(response.content)

        ## Save it to storage, because for persistent queries, you can get into the nose
        self.save_icons()

    def load_icons(self):
        try:
            with open(self.ICONS_PATH, 'rb') as f:
                self.icons_in_base64 = pickle.load(f)
        except IOError:
            self.icons_in_base64 = defaultdict(list)

    def save_icons(self):
        with open(self.ICONS_PATH, 'wb') as f:
            pickle.dump(self.icons_in_base64, f)
        
    def get_base64_icon(self, icon):
        return self.icons_in_base64[icon]


icons = Icons()

## Get prices of the coins
coin_prices = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD'.format(','.join(icons.symbols_of_top_ten_coins))).json()['RAW']

def add_dollar(price):
    return '${:.2f}'.format(price)

for i, coin in enumerate(icons.symbols_of_top_ten_coins):
    coin_data = coin_prices[coin]['USD']
    ohlc = '[{:<10}{:<10}{}]'.format(
        add_dollar(coin_data['OPEN24HOUR']),
        add_dollar(coin_data['HIGH24HOUR']),
        add_dollar(coin_data['LOW24HOUR'])
    )
    
    print('{:<6}{:<10}{:<10}{:<30}{:>5} | font="Menlo" image={}'.format(
        coin,
        add_dollar(coin_data['PRICE']),
        '{:+.2f}%'.format(coin_data['CHANGEPCT24HOUR']),
        ohlc,
        '↑{}'.format(i + 1),
        icons.get_base64_icon(coin)
        ))