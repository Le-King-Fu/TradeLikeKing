import pandas as pd
from lnmarkets import rest
import requests
import time
import Signal_TradingView as signal
import lnmkt as ln
import os
import json
import nostrTrade as ns
import yaml

# Load data from a YAML file
with open("config.yml", "r") as yaml_file:
    config_data = yaml.safe_load(yaml_file)

# Access the data as a regular Python dictionary
total_duration = config_data['total_duration']
time_interval = config_data['time_interval']
target = config_data['target']
min_margin = config_data['min_margin']
min_leverage = config_data['min_leverage']
nb_seq_reversal = int(config_data['nb_seq_reversal'])
pnl_loss = config_data['pnl_loss']


start_time = time.time()

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
    #get_fees()
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
    while True:
        try:
            lnm = ln.connect_trades()
            trade_info = lnm.futures_get_positions({
            'type': 'running'
            }, format = 'json')
            #print(trade_info)
            df_trades = pd.DataFrame(trade_info)
            #print(df_trades)
            df_trades["creation_date"] = pd.to_datetime(df_trades["creation_ts"]/1000 - 4*3600, unit='s').dt.strftime('%Y-%m-%d')
            df_trades["created_on"] = pd.to_datetime(df_trades["creation_ts"]/1000 - 4*3600, unit='s').dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            #estimation : opening fee = closing
            df_trades["total_fees_est"] = df_trades.apply(
            lambda row: row["opening_fee"]*2 + row["sum_carry_fees"],
            axis=1
            )
            df_trades["pl_w_fees_est"] = df_trades.apply(
            lambda row: row["pl"] - row["opening_fee"]*2 - row["sum_carry_fees"],
            axis=1
            )
            df_trades["pl_w_fees_pct"] = df_trades.apply(
            lambda row: row["pl_w_fees_est"] / row["margin"],
            axis=1
            )
            df_trades["pl_pct"] = df_trades.apply(
            lambda row: row["pl"] / row["margin"],
            axis=1
            )
            df_trades["margin_call"] = df_trades.apply(lambda row: 1 if row['pl_pct'] < min_margin else 0, axis = 1)
            df_trades["in_profit"] = df_trades.apply(lambda row: 1 if row['pl_w_fees_pct'] > target else 0, axis = 1)
            df_trades["take_a_L"] = df_trades.apply(lambda row: 1 if row['pl_pct'] <= pnl_loss else 0, axis = 1)
            df_trades["total_fees"] = df_trades.apply(
            lambda row: row["opening_fee"] + row["closing_fee"] + row["sum_carry_fees"],
            axis=1
            )
            #commenté car la colonne rec ne marche pas : """ and ['rec'] == "short"""
            #print(trade_info)
            df_trades.to_json(file_path_summ)
            return df_trades
        except Exception as e:
            print(f"Error : {e}")
            print("Try again next loop")

def get_trades_closed():
    lnm = ln.connect_trades()
    #API limite a 100, voir comment contourner
    trade_info = lnm.futures_get_positions({
    'type': 'closed','limit':10000
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
    lambda row: row["opening_fee"] + row["closing_fee"] + row["sum_carry_fees"],
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
                              "total_fees_est",
                              "side",
                              "quantity",
                              "liquidation",
                              "price",
                              "margin",
                              "leverage",
                              "pl",
                              "pl_pct",
                              "pl_w_fees_est",
                              'pl_w_fees_pct',
                              'margin_call',
                              'in_profit']]
    print(df_trades_running)
    return df_trades_running

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
        if row['margin_call'] == 1:
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
        if row['take_a_L'] == 1 and row['side'] == 'b' and rec == 'STRONG_SELL':
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
        elif row['take_a_L'] == 1 and row['side'] == 's' and rec == 'STRONG_BUY':
            id_list.append(row['id'])
    return id_list

#Version agressive
#chg : éviter les closures trop rapide, check ROI a compensé par margin check et close sur signal plus rapide (1m)

def get_list_close_long_aggro(count_sh):
    id_list = []
    count_sh = int(count_sh)
    rec = signal.get_main_signal_new()
    rec_1m = signal.get_1m_signal_new()
    #on enleve NEUTRAL pr profit- idealement, va permettre de collecter profit plus tôt
    closeif = ['BUY','STRONG_BUY']
    closeif_loss = ['BUY','STRONG_BUY','NEUTRAL']
    #df_trades = get_trades()
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    for index, row in df_trades.iterrows():
        #close initial i.e. seulement si profit and trend reversed
        #problematique pcq ne close pas assez, et les pertes creusent leur trou
        if row['in_profit'] == 1 and row['side'] == 'b' and rec_1m not in closeif:
            id_list.append(row['id'])
        #alternative, si leverage trop bas (a cause ajout margin), alors on close
        #elif row['take_a_L'] == 1 and row['side'] == 'b':
        #    id_list.append(row['id'])
        #on essaie d'ajouter une fermeture plus agressive sur changement de tendance
        #idealement frais perdu losing trade < gain sur winners
        #trop agressif, j'ajoute une perte minimum dans take_a_L pour garder un peu en vie        
        elif row['take_a_L'] == 1 and row['side'] == 'b' and count_sh >= nb_seq_reversal:
            id_list.append(row['id'])
    return id_list

def get_list_close_short_aggro(count_lg):
    id_list = []
    count_lg = int(count_lg)
    rec = signal.get_main_signal_new()
    rec_1m = signal.get_1m_signal_new()
    #on enleve NEUTRAL pr profit - idealement, va permettre de collecter profit plus tôt
    closeif = ['SELL','STRONG_SELL']
    closeif_loss = ['SELL','STRONG_SELL','NEUTRAL']
    #df_trades = get_trades()
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    for index, row in df_trades.iterrows():
        #close initial i.e. seulement si profit and trend reversed
        #problematique pcq ne close pas assez, et les pertes creusent leur trou
        if row['in_profit'] == 1 and row['side'] == 's' and rec_1m not in closeif:
            id_list.append(row['id'])
        #on essaie d'ajouter une fermeture plus agressive sur changement de tendance
        #idealement frais perdu losing trade < gain sur winners
        #trop agressif, j'ajoute une perte minimum dans take_a_L pour garder un peu en vie
        elif row['take_a_L'] == 1 and row['side'] == 's'and count_lg >= nb_seq_reversal:
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
    #id_list_closing = ["1250b616-bb89-4dbb-8be1-3ea4411dbae1","ed3af214-f8ed-41ee-8512-64a76aa308ba"]
    with open(file_path_summ_closed, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    
    
    for index, row in df_trades.iterrows():
        if row['id'] in id_list_closing:
            msg = f"I just closed a short! I bought at {row['price']} with a {row['leverage']}x and I closed at {row['exit_price']}, for a pnl of {row['pl_w_fees']} (total fees = {row['total_fees']})."
            print(msg)
            return msg
            #ns.send_msg(msg)

def get_closing_msg_long():
    id_list_closing = get_list_close_long_aggro()
    #id_list_closing = ["1250b616-bb89-4dbb-8be1-3ea4411dbae1","ed3af214-f8ed-41ee-8512-64a76aa308ba"]
    with open(file_path_summ_closed, 'r') as json_file:
        df_trades = pd.read_json(json_file)
    
    
    for index, row in df_trades.iterrows():
        if row['id'] in id_list_closing:
            msg = f"I just closed a long! I bought at {row['price']} with a {row['leverage']}x and I closed at {row['exit_price']}, for a pnl of {row['pl_w_fees']} (total fees = {row['total_fees']})."
            print(msg)
            #ns.send_msg(msg)   
            return msg

def get_closed_results():
    with open(file_path_summ_closed, 'r') as json_file:
        df_trades = pd.read_json(json_file)
        # Calculate the total fees for day trading trades
    nb_trx_closed = len(df_trades)
    total_fee = df_trades['total_fees'].sum()
    total_opening_fee = df_trades['opening_fee'].sum()
    total_closing_fee = df_trades['closing_fee'].sum()
    total_carry_fee = df_trades['sum_carry_fees'].sum()
    #print(total_opening_fee)
    #print(total_closing_fee)
    #print(total_carry_fee)
    #total_fee = total_opening_fee + total_opening_fee + total_carry_fee
    #print(total_fee)

    # Calculate the average fees per trade
    #average_fees_per_trade = df_trades['fees'].mean()
    average_opening_fee = df_trades['opening_fee'].mean()
    average_closing_fee = df_trades['closing_fee'].mean()
    average_carry_fee = df_trades['sum_carry_fees'].mean()
    total_average_fee = df_trades['total_fees'].mean()
    #total_average_fee = average_opening_fee + average_closing_fee + average_carry_fee

    # Calculate the highest fee amount in a single trade
    #highest_fee = df_trades['fees'].max()
    max_opening_fee = df_trades['opening_fee'].max()
    max_closing_fee = df_trades['closing_fee'].max()
    max_carry_fee = df_trades['sum_carry_fees'].max()
    total_max_fee = df_trades['total_fees'].max()
    # Calculate the lowest fee amount in a single trade
    #lowest_fee = df_trades['fees'].min()
    min_opening_fee = df_trades['opening_fee'].min()
    min_closing_fee = df_trades['closing_fee'].min()
    min_carry_fee = df_trades['sum_carry_fees'].min()
    total_min_fee = df_trades['total_fees'].min()
    # Calculate the number of day trading trades
    #num_day_trades = len(df_trades)

    nb_trx_closed_long = len(df_trades.loc[df_trades['side']== 'b'])
    nb_trx_closed_short = len(df_trades.loc[df_trades['side']== 's'])
    nb_trx_closed = len(df_trades)
    total_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].sum()
    total_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].sum()
    total_pnl = df_trades['pl'].sum()
    average_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].mean()
    average_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].mean() 
    average_pnl = df_trades['pl'].mean() 
    max_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].max()
    max_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].max() 
    max_pnl = df_trades['pl'].max() 
    min_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].min()
    min_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].min() 
    min_pnl = df_trades['pl'].min()


    results = {
    'total_opening_fee': total_opening_fee,
    'total_closing_fee': total_closing_fee,
    'total_carry_fee': total_carry_fee,
    "total_fee" : total_fee,
    'average_opening_fee': average_opening_fee,
    'average_closing_fee': average_closing_fee,
    'average_carry_fee': average_carry_fee,
    'total_average_fee' : total_average_fee,
    'max_opening_fee': max_opening_fee,
    'max_closing_fee': max_closing_fee,
    'max_carry_fee': max_carry_fee,
    'total_max_fee': total_max_fee,
    'min_opening_fee': min_opening_fee,
    'min_closing_fee': min_closing_fee,
    'min_carry_fee': min_carry_fee,
    'total_min_fee': total_min_fee,
    'nb_trx_closed': nb_trx_closed,
    'nb_trx_closed_long': nb_trx_closed_long,
    'nb_trx_closed_short': nb_trx_closed_short,
    'total_pnl_long': total_pnl_long,
    'total_pnl_short': total_pnl_short,
    'total_pnl': total_pnl,
    'average_pnl_long': average_pnl_long,
    'average_pnl_short': average_pnl_short,
    'average_pnl': average_pnl,
    'max_pnl_long': max_pnl_long,
    'max_pnl_short': max_pnl_short,
    'max_pnl': max_pnl,
    'min_pnl_long': min_pnl_long,
    'min_pnl_short': min_pnl_short,
    'min_pnl': min_pnl,
    }
    return results

def get_running_results():
    with open(file_path_summ, 'r') as json_file:
        df_trades = pd.read_json(json_file)
        # Calculate the total fees for day trading trades
    nb_trx_running = len(df_trades)
    total_fee = df_trades['total_fees'].sum()
    total_opening_fee = df_trades['opening_fee'].sum()
    total_closing_fee = df_trades['closing_fee'].sum()
    total_carry_fee = df_trades['sum_carry_fees'].sum()
    #print(total_opening_fee)
    #print(total_closing_fee)
    #print(total_carry_fee)
    #total_fee = total_opening_fee + total_opening_fee + total_carry_fee
    #print(total_fee)

    # Calculate the average fees per trade
    #average_fees_per_trade = df_trades['fees'].mean()
    average_opening_fee = df_trades['opening_fee'].mean()
    average_closing_fee = df_trades['closing_fee'].mean()
    average_carry_fee = df_trades['sum_carry_fees'].mean()
    total_average_fee = df_trades['total_fees'].mean()
    #total_average_fee = average_opening_fee + average_closing_fee + average_carry_fee

    # Calculate the highest fee amount in a single trade
    #highest_fee = df_trades['fees'].max()
    max_opening_fee = df_trades['opening_fee'].max()
    max_closing_fee = df_trades['closing_fee'].max()
    max_carry_fee = df_trades['sum_carry_fees'].max()
    total_max_fee = df_trades['total_fees'].max()
    # Calculate the lowest fee amount in a single trade
    #lowest_fee = df_trades['fees'].min()
    min_opening_fee = df_trades['opening_fee'].min()
    min_closing_fee = df_trades['closing_fee'].min()
    min_carry_fee = df_trades['sum_carry_fees'].min()
    total_min_fee = df_trades['total_fees'].min()
    # Calculate the number of day trading trades
    #num_day_trades = len(df_trades)

    nb_trx_closed_long = len(df_trades.loc[df_trades['side']== 'b'])
    nb_trx_closed_short = len(df_trades.loc[df_trades['side']== 's'])
    nb_trx_closed = len(df_trades)
    total_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].sum()
    total_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].sum()
    total_pnl = df_trades['pl'].sum()
    average_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].mean()
    average_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].mean() 
    average_pnl = df_trades['pl'].mean() 
    max_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].max()
    max_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].max() 
    max_pnl = df_trades['pl'].max() 
    min_pnl_long = df_trades.loc[df_trades['side'] == 'b','pl'].min()
    min_pnl_short = df_trades.loc[df_trades['side'] == 's','pl'].min() 
    min_pnl = df_trades['pl'].min()


    results = {
    'total_opening_fee': total_opening_fee,
    'total_closing_fee': total_closing_fee,
    'total_carry_fee': total_carry_fee,
    "total_fee" : total_fee,
    'average_opening_fee': average_opening_fee,
    'average_closing_fee': average_closing_fee,
    'average_carry_fee': average_carry_fee,
    'total_average_fee' : total_average_fee,
    'max_opening_fee': max_opening_fee,
    'max_closing_fee': max_closing_fee,
    'max_carry_fee': max_carry_fee,
    'total_max_fee': total_max_fee,
    'min_opening_fee': min_opening_fee,
    'min_closing_fee': min_closing_fee,
    'min_carry_fee': min_carry_fee,
    'total_min_fee': total_min_fee,
    'nb_trx_running': nb_trx_closed,
    'nb_trx_running_long': nb_trx_closed_long,
    'nb_trx_running_short': nb_trx_closed_short,
    'total_pnl_long': total_pnl_long,
    'total_pnl_short': total_pnl_short,
    'total_pnl': total_pnl,
    'average_pnl_long': average_pnl_long,
    'average_pnl_short': average_pnl_short,
    'average_pnl': average_pnl,
    'max_pnl_long': max_pnl_long,
    'max_pnl_short': max_pnl_short,
    'max_pnl': max_pnl,
    'min_pnl_long': min_pnl_long,
    'min_pnl_short': min_pnl_short,
    'min_pnl': min_pnl,
    }
    return results

if __name__ == "__main__":
    main()