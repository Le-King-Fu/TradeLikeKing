from lnmarkets import rest
from lnmarkets import websockets
import requests
import logging

#apprendre a utiliser logging
logging.basicConfig(level=logging.INFO)

minimum_balance = 100000
maximum_trade = 45

def main():
    get_info()
    #get_price_Alpha()
    get_price_Binance()
    get_price_LNMarket()

def connect_read():
    options = {'key': 'HNhmV3BkqPQfuV/IdX2c5ORp71+JxFvq1eXRi6rmsNw=',
            'secret': '4rgJHL3kDF56Yo21DJSpbSvKxWnmP0goYXUvc73hLdO3/28JF1dPxUki4/FDrf1lZ8EfAn3M00Wyp3KtTfVC2A==',
            'passphrase': 'f9c759a29ic1',
            'network': 'mainnet'}
    lnm = rest.LNMarketsRest(**options)
    return lnm

def connect_write():
    options = {'key' : 'IlDl2Vsh+huaL+NG+bXIXeeMDiKh2xZlK0Kkc1WwjUE=',
                'secret' : 'T/V4kklazjmqwBQUK6M0PuaPjWt0k1zCwVg+n+nidEOpAsynMz4b5xDxZBOCUhRzlXIZHmfNfwmEm+MfZATUew==',
                'passphrase' : 'i590d0hbhh5j',
                'network' : 'mainnet'}
    lnm = rest.LNMarketsRest(**options)
    return lnm

def connect_trades():
    options = {'key': 'DEbJ3mDzukA8trPwUCzwnh1K5x8n476lEvrLic+XCkM=',
            'secret': 'ueQPWd7hMXudJxHLRboQPIvsYhHNp0lsB6DF/e+VnEE1/0E0MtiY3/IspReWfgN4FbLDSrDGrmk0rzDGUtPuMw==',
            'passphrase': 'j8g6ec2h2c2e',
            'network': 'mainnet'}
    lnm = rest.LNMarketsRest(**options)
    return lnm

def get_info():
    info = connect_read()
    user_info = info.get_user(format='json')
    username = user_info['username']
    balance = user_info['balance']
    #print(user_info)
    nb_trx_buy = user_info['metrics']['futures']['buy']['running_positions']
    nb_trx_sell = user_info['metrics']['futures']['sell']['running_positions']
    nb_trx = int(nb_trx_buy) + int(nb_trx_sell)
    print(nb_trx_buy)
    print(nb_trx_sell)
    print(nb_trx)
    #nb_trx = user_info['running_positions']
    return username, balance, nb_trx
    
def get_price_LNMarket():
    info = connect_read()
    #data = []
    data = info.futures_get_ticker(format='json')
    #print(data['lastPrice'])
    bitcoin_price = float(data['lastPrice'])
    bitcoin_price_formatted = "{:.2f}".format(bitcoin_price)
    print("LN Market : "+ bitcoin_price_formatted)

def check_balance():
    username, balance, nb_trx = get_info()
    if balance > minimum_balance and maximum_trade <= 45:
        balance = "OK"
        return balance
    else:
        balance = "NOT OK"
        return balance

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