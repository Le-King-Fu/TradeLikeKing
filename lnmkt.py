from lnmarkets import rest
import requests
import logging

logging.basicConfig(level=logging.INFO)

def main():
    get_info()
    #get_price_Alpha()
    get_price_Binance()
    get_price_LNMarket()

def connect_read():
    options = {'key': 'key',
            'secret': 'secret',
            'passphrase': 'passphrase',
            'network': 'mainnet'}
    lnm = rest.LNMarketsRest(**options)
    return lnm

def connect_write():
    options = {'key': 'key',
            'secret': 'secret',
            'passphrase': 'passphrase',
            'network': 'mainnet'}
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