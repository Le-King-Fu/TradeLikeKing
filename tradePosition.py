from lnmarkets import rest
import analysisPositions as an
import Signal_TradingView as signal
import lnmkt as ln
import datetime

add_margin_amount = 1000
new_futures_amount = 2000
leverage = 50
minute_pause = 20

def main():
    #open_futures()
    #close_futures()
    #add_margin()
    return


def open_futures_long():
    #pour voir si trx dans les 5 dernieres minutes - pourrait etre ameliorer i.e. reset count apres 5m?
    last_transaction_time = an.last_trx()
    current_time = datetime.datetime.now()
    time_difference = current_time - last_transaction_time

    count = signal.get_long_seq()
    print("Consecutive STRONG BUY : ",count)

    if count == 5 and time_difference >= datetime.timedelta(minutes=minute_pause):
        lnm = ln.connect_write()        
        opened_future = lnm.futures_new_position({
            'type': 'm', # m for market of l for limit
            'side': 'b', # s for sell/short or b for buy/long
            'margin': new_futures_amount,
            'leverage': leverage,
        })
        print(opened_future)

def open_futures_short():
    #pour voir si trx dans les 5 dernieres minutes - pourrait etre ameliorer i.e. reset count apres 5m?
    last_transaction_time = an.last_trx()
    current_time = datetime.datetime.now()
    time_difference = current_time - last_transaction_time

    #nb STRONG_SELL consecutifs
    count = signal.get_short_seq()
    print("Consecutive STRONG SELL : ",count)

    if count >= 5 and time_difference >= datetime.timedelta(minutes=minute_pause):
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
    for id in id_list:
        close_position = lnm.futures_close_position({id})
        #print(close_position)

def close_futures_short():
    lnm = ln.connect_write() 
    id_list = []
    id_list = an.get_list_close_short()
    for id in id_list:
        close_position = lnm.futures_close_position({id})
        #print(close_position)

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

if __name__ == "__main__":
    main()
    