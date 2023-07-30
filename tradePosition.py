from lnmarkets import rest
import analysisPositions as an
import Signal_TradingView as signal
import lnmkt as ln
import datetime
import pandas as pd

add_margin_amount = 1000
new_futures_amount = 2000
leverage = 100
minute_pause = 60
minimum_balance = 100000
maximum_trades = 45


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

def open_futures_long():
    balance = ln.check_balance()
    time_difference = get_time_diff()
    count = signal.get_long_seq()
    print("Consecutive STRONG BUY : ",count)
    if count == 5 and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK":
        lnm = ln.connect_write()        
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 'b', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        print(opened_future)

def open_futures_short():
    balance = ln.check_balance()
    time_difference = get_time_diff()
    #nb STRONG_SELL consecutifs
    count = signal.get_short_seq()
    print("Consecutive STRONG SELL : ",count)
    if count >= 5 and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK":
        lnm = ln.connect_write()  
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 's', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        #print(opened_future)

def close_futures_long():
    lnm = ln.connect_write()  
    id_list = []
    id_list = an.get_list_close_long()   
    for id in id_list:
        close_position = lnm.futures_close_position({'id': id})
        print(close_position)
        #print(id)
#il y a un bogue, pas réussi à le noter...
def close_futures_short():
    lnm = ln.connect_write() 
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
    lnm = ln.connect_write() 
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
min_n_aggro = 3

def open_futures_long_aggro():
    balance = ln.check_balance()
    time_difference = get_time_diff()
    count = signal.get_long_seq()
    print("Consecutive STRONG BUY : ",count)
    if count >= min_n_aggro and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK":
        lnm = ln.connect_write()        
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 'b', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        print(opened_future)

def open_futures_short_aggro():
    balance = ln.check_balance()
    time_difference = get_time_diff()
    #nb STRONG_SELL consecutifs
    count = signal.get_short_seq()
    print("Consecutive STRONG SELL : ",count)
    if count >= min_n_aggro and time_difference >= datetime.timedelta(minutes=minute_pause) and balance == "OK":
        lnm = ln.connect_write()  
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 's', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        #print(opened_future)

def close_futures_long_aggro():
    lnm = ln.connect_write()  
    id_list = []
    id_list = an.get_list_close_long_aggro()
    #print(id_list)   
    for id in id_list:
        close_position = lnm.futures_close_position({'id': id})
        #print(close_position)
        #print(str(id))   

def close_futures_short_aggro():
    lnm = ln.connect_write() 
    id_list = []
    id_list = an.get_list_close_short_aggro()
    #print(id_list)
    for id in id_list:
        #id = str(id)
        close_position = lnm.futures_close_position({'id': id})
        #print(str(close_position))

if __name__ == "__main__":
    main()
    