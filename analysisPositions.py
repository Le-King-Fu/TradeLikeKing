import pandas as pd
from lnmarkets import rest
import time
import Signal_TradingView as signal
import lnmkt as ln

total_duration = 60 * 60
time_interval = 60
start_time = time.time()
signal_rec = signal.get_main_signal()
target = 0.30

def main():
    print_trades()
    return       

##isoler
def get_trades():
    lnm = ln.connect_trades()
    trade_info = lnm.futures_get_positions({
    'type': 'running'
    #'type': 'closed'
    #'type': 'open' #tombe en erreur
    }, format = 'json')
    
    df_trades = pd.DataFrame(trade_info)
    df_trades["creation_date"] = pd.to_datetime(df_trades["creation_ts"]/1000 - 4*3600, unit='s').dt.strftime('%Y-%m-%d')
    df_trades["creation_ts"] = pd.to_datetime(df_trades["creation_ts"]/1000 - 4*3600, unit='s')
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
    df_trades["close"] = df_trades.apply(lambda row: 1 if row['pl_w_fees_pct'] > target else 0, axis = 1)
    #commenté car la colonne rec ne marche pas : """ and ['rec'] == "short"""
    #print(trade_info)
    return df_trades


def print_trades():
    df_trades = get_trades()
    selected_col = df_trades[[#"id",
                              "creation_date",
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
                              'close']]
    print(selected_col)


def rec_trx(row):
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
    df_trades = get_trades()
    for index, row in df_trades.iterrows():
        if row['margin'] == 1:
            id_list.append(row['id'])
    #print("Margin call: ",id_list)
    return id_list

def get_list_close_long():
    id_list = []
    rec = signal.get_main_signal()
    df_trades = get_trades()
    for index, row in df_trades.iterrows():
        if row['close'] == 1 and row['side'] == 'b' and rec == 'STRONG_SELL':
            id_list.append(row['id'])
    return id_list

def get_list_close_short():
    id_list = []
    rec = signal.get_main_signal()
    df_trades = get_trades()
    for index, row in df_trades.iterrows():
        if row['close'] == 1 and row['side'] == 's' and rec == 'STRONG_BUY':
            id_list.append(row['id'])
    return id_list

def last_trx():
    df_trades = get_trades()
    max_timestamp = df_trades['creation_ts'].max()
    return max_timestamp

if __name__ == "__main__":
    main()
