from lnmarkets import rest
from lnmarkets import websockets
import requests
import logging
import os
import json
import pandas as pd

# Get the current working directory
current_directory = os.getcwd()

# Define the output directory and file name
output_dir = os.path.join(current_directory, 'output_data')
signal_current = 'info.json'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Construct the full file path
file_path_summ = os.path.join(output_dir, signal_current)

#apprendre a utiliser logging
logging.basicConfig(level=logging.INFO)

minimum_balance = 100000
maximum_trade = 45

def main():
    #get_info()
    #check_balance()
    #get_nb_trx()
    #get_price_Alpha()
    #get_price_Binance()
    #get_price_LNMarket()
    return

def connect_read():
    options = {'key': 'key',
            'secret': 'secret',
            'passphrase': 'passphrase',
            'network': 'mainnet'}
    lnm = rest.LNMarketsRest(**options)
    return lnm

def connect_write():
    options = {'key' : 'key',
                'secret' : 'secret',
                'passphrase' : 'passphrase',
                'network' : 'mainnet'}
    lnm = rest.LNMarketsRest(**options)
    return lnm

def connect_trades():
    options = {'key': 'key',
            'secret': 'secret',
            'passphrase': 'passphrase',
            'network': 'mainnet'}
    lnm = rest.LNMarketsRest(**options)
    return lnm

def get_info():
    info = connect_read()
    user_info = info.get_user(format='json')
    #print(user_info)

    with open(file_path_summ, 'w') as json_file:
        json.dump(user_info, json_file, indent=2)
    #return username, balance, nb_trx
    
def get_price_LNMarket():
    info = connect_read()
    #data = []
    data = info.futures_get_ticker(format='json')
    #print(data['lastPrice'])
    bitcoin_price = float(data['lastPrice'])
    bitcoin_price_formatted = "{:.2f}".format(bitcoin_price)
    print("LN Market : "+ bitcoin_price_formatted)

def check_balance():
    with open(file_path_summ, 'r') as json_file:
        info = pd.read_json(json_file)
    balance = info["balance"]["wallet"]
    if balance > minimum_balance and maximum_trade <= 45:
        balance = "OK"
        return balance
    else:
        balance = "NOT OK"
        return balance

def get_nb_trx():
    with open(file_path_summ, 'r') as json_file:
       user_info = pd.read_json(json_file)   
    
    nb_trx_buy = user_info['metrics']['futures']['buy']['running_positions']
    nb_trx_sell = user_info['metrics']['futures']['sell']['running_positions']
    nb_trx = int(nb_trx_buy) + int(nb_trx_sell)
    #print(nb_trx_buy)
    #print(nb_trx_sell)
    #print(nb_trx)
    return nb_trx

##Alpha Avantage, les prix laguent un peu
def get_price_Alpha():
    url_alpha = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=RALBYJ0V1990DLKG'
    r = requests.get(url_alpha)
    data = r.json()
    bitcoin_price = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    bitcoin_price_formatted = "{:.2f}".format(bitcoin_price)
    print("AlphaAvantage : "+ bitcoin_price_formatted)

def get_price_Binance():
    url_binance = 'https://api.binance.com/api/v3/ticker/price'
    params = {'symbol': 'BTCUSDT'}
    response = requests.get(url_binance, params=params)
    if response.status_code == 200:
        data = response.json()
        bitcoin_price = float(data['price'])
        bitcoin_price_formatted = "{:.2f}".format(bitcoin_price)
        print("Binance : "+ bitcoin_price_formatted)
    else:
        print('Erreur API Binance')
        
if __name__ == "__main__":
    main()