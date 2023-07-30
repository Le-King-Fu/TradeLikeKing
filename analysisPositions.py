import pandas as pd
from lnmarkets import rest
import requests
import time
import Signal_TradingView as signal
import lnmkt as ln
import os
import json
import nostrTrade as ns

total_duration = 60 * 60
time_interval = 60
start_time = time.time()
target = 0.10

# Get the current working directory
current_directory = os.getcwd()

# Define the output directory and file name
output_dir = os.path.join(current_directory, 'output_data')
trade_summary = 'trade_summary.json'
trade_summary_closed = 'trade_closed_summary.json'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Construct the full file path
file_path_summ = os.path.join(output_dir, trade_summary)
file_path_summ_closed = os.path.join(output_dir, trade_summary_closed)
# Export the DataFrame to the JSON file
trades_json = ''

def main():
    #get_test()
    #get_trades_running()
    #print_trades_running()
    #get_trades_closed()
    #get_closing_msg_short()
    #get_trades_json()
    #print_trades()
    print()
    #return       


"""
Erreur pogné 2023-07-28 - 
Traceback (most recent call last):
  File "/home/max/.local/lib/python3.10/site-packages/requests/models.py", line 971, in json
    return complexjson.loads(self.text, **kwargs)
  File "/usr/lib/python3.10/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3.10/json/decoder.py", line 340, in decode
    raise JSONDecodeError("Extra data", s, end)
json.decoder.JSONDecodeError: Extra data: line 1 column 5 (char 4)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/max/Documents/Code/btc/DEV/launch.py", line 58, in <module>
    main()
  File "/home/max/Documents/Code/btc/DEV/launch.py", line 30, in main
    an.get_trades()
  File "/home/max/Documents/Code/btc/DEV/analysisPositions.py", line 41, in get_trades
    trade_info = lnm.futures_get_positions({
  File "/home/max/.local/lib/python3.10/site-packages/lnmarkets/rest.py", line 162, in futures_get_positions
    return self.before_request_api(method, path, params, credentials, format)
  File "/home/max/.local/lib/python3.10/site-packages/lnmarkets/rest.py", line 100, in before_request_api
    return self.request_api(method, path, params, credentials, format)
  File "/home/max/.local/lib/python3.10/site-packages/lnmarkets/rest.py", line 93, in request_api
    return response.json()
  File "/home/max/.local/lib/python3.10/site-packages/requests/models.py", line 975, in json
    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
requests.exceptions.JSONDecodeError: Extra data: line 1 column 5 (char 4)

"""
def get_trades_running():
    lnm = ln.connect_trades()
    trade_info = lnm.futures_get_positions({
    'type': 'running'
    #'type': 'closed'
    #'type': 'open' #tombe en erreur
    }, format = 'json')
    #print(trade_info)
    df_trades = pd.DataFrame(trade_info)
    #print(df_trades)
    df_trades["creation_date"] = pd.to_datetime(df_trades["creation_ts"]/1000 - 4*3600, unit='s').dt.strftime('%Y-%m-%d')
    df_trades["created_on"] = pd.to_datetime(df_trades["creation_ts"]/1000 - 4*3600, unit='s').dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    df_trades["total_fees"] = df_trades.apply(
    lambda row: row["opening_fee"] + row["closing_fee"] + row["sum_carry_fees"] if row["type"] == "closed" else row["pl"] + row["opening_fee"]*2 + row["sum_carry_fees"],
    axis=1
    )
    df_trades["pl_w_fees"] = df_trades.apply(
    lambda row: row["pl"] - row["opening_fee"] - row["closing_fee"] - row["sum_carry_fees"] if row["type"] == "closed" else row["pl"] - row["opening_fee"]*2 - row["sum_carry_fees"],
    axis=1
    )
    df_trades["pl_w_fees_pct"] = df_trades.apply(
    lambda row: row["pl_w_fees"] / row["margin"],
    axis=1
    )
    df_trades["pl_pct"] = df_trades.apply(
    lambda row: row["pl"] / row["margin"],
    axis=1
    )
    #compare trx a la recommandation selon interval main
    #!BOGUE! La resultat de la fonction ne se mets pas a jour !
    #remplacé en splittant les 2 fct de Close
    #df_trades["rec"] = df_trades.apply(rec_trx, axis = 1)
    df_trades["margin_call"] = df_trades.apply(lambda row: 1 if row['pl_pct'] < -90/100 else 0, axis = 1)
    df_trades["in_profit"] = df_trades.apply(lambda row: 1 if row['pl_w_fees_pct'] > target else 0, axis = 1)
    #commenté car la colonne rec ne marche pas : """ and ['rec'] == "short"""
    #print(trade_info)
    df_trades.to_json(file_path_summ)
    return df_trades

def get_trades_closed():
    lnm = ln.connect_trades()
    trade_info = lnm.futures_get_positions({
    'type': 'closed'
    }, format = 'json')
    #print(trade_info)
    df_trades = pd.DataFrame(trade_info)
    #print(df_trades)
    df_trades["creation_date"] = pd.to_datetime(df_trades["creation_ts"]/1000 - 4*3600, unit='s').dt.strftime('%Y-%m-%d')
    df_trades["closed_date"] = pd.to_datetime(df_trades["closed_ts"]/1000 - 4*3600, unit='s').dt.strftime('%Y-%m-%d')
    df_trades["pl_w_fees"] = df_trades.apply(
    lambda row: row["pl"] - row["opening_fee"] - row["closing_fee"] - row["sum_carry_fees"] if row["type"] == "closed" else row["pl"] - row["opening_fee"]*2 - row["sum_carry_fees"],
    axis=1
    )
    df_trades["total_fees"] = df_trades.apply(
    lambda row: row["opening_fee"] + row["closing_fee"] + row["sum_carry_fees"] if row["type"] == "closed" else row["pl"] + row["opening_fee"]*2 + row["sum_carry_fees"],
    axis=1
    )
    
    df_trades.to_json(file_path_summ_closed)
    return df_trades

def print_trades_running():
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    #df_trades = get_trades()
    #print(df_trades)
    df_trades_running = df_trades[["created_on",
                              "opening_fee",
                              "closing_fee",
                              "sum_carry_fees",
                              "side",
                              "quantity",
                              "price",
                              "margin",
                              "leverage",
                              "pl",
                              "pl_pct",
                              "pl_w_fees",
                              'pl_w_fees_pct',
                              'margin_call',
                              'in_profit']]
    print(df_trades_running)

def rec_trx(row):
    signal_rec = signal.get_main_signal_new()
    if signal_rec == "STRONG_BUY" and row['side'] == "b":
        return "long"
    elif signal_rec == "STRONG_SELL" and row['side'] == "s":
        return "long"
    elif signal_rec == "STRONG_BUY" and row['side'] == "s":
        return "short"
    elif signal_rec == "STRONG_SELL" and row['side'] == "b":
        return "short"
    else:
        return "neutral"

def get_list_margin():
    id_list = []
    #df_trades = get_trades()
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    
    for index, row in df_trades.iterrows():
        if row['margin'] == 1:
            id_list.append(row['id'])
    #print("Margin call: ",id_list)
    return id_list

def get_list_close_long():
    id_list = []
    rec = signal.get_main_signal_new()
    #df_trades = get_trades()
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    for index, row in df_trades.iterrows():
        if row['in_profit'] == 1 and row['side'] == 'b' and rec == 'STRONG_SELL':
            id_list.append(row['id'])
    return id_list

def get_list_close_short():
    id_list = []
    rec = signal.get_main_signal_new()
    #df_trades = get_trades()
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    for index, row in df_trades.iterrows():
        if row['in_profit'] == 1 and row['side'] == 's' and rec == 'STRONG_BUY':
            id_list.append(row['id'])
    return id_list

#Version agressive
#chg : éviter les closures trop rapide, check ROI a compensé par margin check et close sur signal plus rapide (1m)

def get_list_close_long_aggro():
    id_list = []
    rec = signal.get_main_signal_new()
    rec_1m = signal.get_1m_signal_new()
    closeif = ['BUY','STRONG_BUY','NEUTRAL']
    #df_trades = get_trades()
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)

    for index, row in df_trades.iterrows():
        #on enleve control sur profit
        if row['in_profit'] == 1 and row['side'] == 'b' and rec_1m not in closeif:
        #if row['side'] == 'b' and rec not in closeif:
            id_list.append(row['id'])
    return id_list

def get_list_close_short_aggro():
    id_list = []
    rec = signal.get_main_signal_new()
    rec_1m = signal.get_1m_signal_new()
    closeif = ['SELL','STRONG_SELL','NEUTRAL']
    #df_trades = get_trades()
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    for index, row in df_trades.iterrows():
        #j'ai remis le profit check, mais baissé ROI = 10

        if row['in_profit'] == 1 and row['side'] == 's' and rec_1m not in closeif:
        #if row['side'] == 's' and rec not in closeif:
            id_list.append(row['id'])
    return id_list

 ##a corriger pcq stuck sur l'ancienne trx lorsque no trx
def last_trx():
    #df_trades = get_trades()
    if ln.get_nb_trx() == 0:
        return 0
    else:
        with open(file_path_summ, 'r') as json_file:
            df_trades = pd.read_json(json_file)
        max_timestamp = df_trades['creation_ts'].max()
        #print(max_timestamp)
        return max_timestamp

def get_closing_msg_short():
    id_list_closing = get_list_close_short_aggro()
    id_list_closing = ["1250b616-bb89-4dbb-8be1-3ea4411dbae1","ed3af214-f8ed-41ee-8512-64a76aa308ba"]
    with open(file_path_summ_closed, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    
    
    for index, row in df_trades.iterrows():
        if row['id'] in id_list_closing:
            msg = f"I just closed a short! I bought at {row['price']} with a {row['leverage']}x and I closed at {row['exit_price']}, for a pnl of {row['pl_w_fees']} (total fees = {row['total_fees']})."
            print(msg)
            ns.send_msg(msg)

def get_closing_msg_long():
    id_list_closing = get_list_close_short_aggro()
    #id_list_closing = ["1250b616-bb89-4dbb-8be1-3ea4411dbae1","ed3af214-f8ed-41ee-8512-64a76aa308ba"]
    with open(file_path_summ_closed, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    
    
    for index, row in df_trades.iterrows():
        if row['id'] in id_list_closing:
            msg = f"I just closed a short! I bought at {row['price']} with a {row['leverage']}x and I closed at {row['exit_price']}, for a pnl of {row['pl_w_fees']} (total fees = {row['total_fees']})."
            print(msg)
            ns.send_msg(msg)          

if __name__ == "__main__":
    main()