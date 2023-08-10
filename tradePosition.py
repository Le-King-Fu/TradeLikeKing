from lnmarkets import rest
import analysisPositions as an
import Signal_TradingView as signal
import lnmkt as ln
import datetime
import pandas as pd
import yaml

with open("config.yml", "r") as yaml_file:
    config_data = yaml.safe_load(yaml_file)

# Access the data as a regular Python dictionary
add_margin_amount = config_data['add_margin_amount']
new_futures_amount = config_data['new_futures_amount']
leverage = config_data['leverage']
minute_pause = config_data['minute_pause']
minimum_balance = config_data['minimum_balance']
maximum_trade = config_data['maximum_trades']
sell_seq = config_data['sell_seq']
buy_seq = config_data['buy_seq']

def main():
    #open_futures()
    #close_futures_long()
    #close_futures_long_aggro()
    #get_time_diff()
    #add_margin()
    return

def get_time_diff():
   last_transaction_time = an.last_trx()
   #print(last_transaction_time)
   last_transaction_time_dt = pd.to_datetime(last_transaction_time/1000 - 4*3600, unit='s')
   #print(last_transaction_time_dt)
   current_time = datetime.datetime.now()
   #print(current_time)
   time_difference = current_time - last_transaction_time_dt
   #print(time_difference)
   return time_difference

def open_futures_long(count_lg):
    balance = ln.check_balance()
    time_difference = get_time_diff()
    #count = signal.get_long_seq()
    print("Consecutive STRONG BUY : ",count_lg)
    if int(count_lg) == 5 and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK":
        lnm = ln.connect_trades()        
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 'b', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        print(opened_future)

def open_futures_short(count_sh):
    balance = ln.check_balance()
    time_difference = get_time_diff()
    #nb STRONG_SELL consecutifs
    #count = signal.get_short_seq()
    print("Consecutive STRONG SELL : ",count_sh)
    if int(count_sh) >= 5 and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK":
        lnm = ln.connect_trades()  
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 's', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        #print(opened_future)

def close_futures_long():
    lnm = ln.connect_trades()  
    id_list = []
    id_list = an.get_list_close_long()   
    for id in id_list:
        close_position = lnm.futures_close_position({'id': id})
        print(close_position)
        #print(id)
#il y a un bogue, pas réussi à le noter...
def close_futures_short():
    lnm = ln.connect_trades() 
    id_list = []
    id_list = an.get_list_close_short()
    #print(id_list)
    for id in id_list:
        #close_position = lnm.futures_close_position(id[0])
        close_position = lnm.futures_close_position({'id': id})
        print(close_position)

#well, ça n'a pas fonctionné.. liquidé !
#2e tentative, ca l'a marché, juste pas assez de margin.. liquidé!
def add_margin():
    lnm = ln.connect_trades() 
    id_list = []
    id_list = an.get_list_margin()
    #id_list = ["ed9325ae-aaa2-4cdf-87f8-b2be709a5629"]
    for id in id_list:
        add_margin = lnm.futures_add_margin_position({
            'amount': add_margin_amount, # s for sell/short or b for buy/long
            'id': id, # m for market of l for limit
        })
        #print(add_margin)

"""
J'essaie plus agressif, j'ouvre apres 2 strong et je ferme quand ca change.
"""
#min_n_aggro = 3

def open_futures_long_aggro(count_lg):
    balance = ln.check_balance()
    time_difference = get_time_diff()
    #count = signal.get_long_seq()
    nb_trx = ln.get_nb_trx()
    print("Consecutive STRONG BUY : ",count_lg)
    if int(count_lg) >= buy_seq and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK" and nb_trx < maximum_trade:
        lnm = ln.connect_trades()        
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 'b', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        print(opened_future)
        signal.reset_seq()

def open_futures_short_aggro(count_sh):
    balance = ln.check_balance()
    time_difference = get_time_diff()
    #nb STRONG_SELL consecutifs
    #count = signal.get_short_seq()
    print("Consecutive STRONG SELL : ",count_sh)
    nb_trx = ln.get_nb_trx()
    if int(count_sh) >= sell_seq and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK" and nb_trx < maximum_trade:
        lnm = ln.connect_trades()  
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 's', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        print(opened_future)
        signal.reset_seq()

def close_futures_long_aggro():
    lnm = ln.connect_trades()  
    id_list = []
    id_list = an.get_list_close_long_aggro()
    #print(id_list)   
    for id in id_list:
        close_position = lnm.futures_close_position({'id': id})
        #print(close_position)
        #print(str(id))   

def close_futures_short_aggro():
    lnm = ln.connect_trades() 
    id_list = []
    id_list = an.get_list_close_short_aggro()
    #print(id_list)
    for id in id_list:
        #id = str(id)
        close_position = lnm.futures_close_position({'id': id})
        #print(str(close_position))

if __name__ == "__main__":
    main()
    