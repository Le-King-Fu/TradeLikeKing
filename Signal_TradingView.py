from tradingview_ta import TA_Handler, Interval, Exchange  as tr
import os
import json
import pandas as pd
import datetime as dt

# Get the current working directory
current_directory = os.getcwd()

# Define the output directory and file name
output_dir = os.path.join(current_directory, 'output_data')
signal_current = 'signal_current.json'
signal_histo = 'signal_histo.json'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Construct the full file path
file_path_summ = os.path.join(output_dir, signal_current)
file_path_summ_h = os.path.join(output_dir, signal_histo)

interval_list = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1W', '1M']
interval_main = "5m"

count_long = 0
count_short = 0

def main():
    #get_all_signal(interval_list)
    #print_all_signal()
    #get_main_signal()
    #print(get_long_seq())
    #print(get_short_seq())
    #get_historic_signal()
    #print_histo_signal()
    return

def get_all_signal(interval_list):
    all_signal_data = {}
    for interval in interval_list:
        signal = get_ta(
            symbol='XBTUSD.P',
            screener='CRYPTO',
            exchange='BITMEX',
            interval=interval,
        )
        #print("Signal_" + interval + " " + str(signal) + " ==> " + str(signal['RECOMMENDATION']))
        all_signal_data[interval] = signal
        
    # Step 3: Write the list of signal data to a JSON file
    all_signal_data["Timestamp"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with open(file_path_summ, 'w') as json_file:
        json.dump(all_signal_data, json_file, indent=2)
    

"""
def print_all_signal():
    for interval in interval_list:
        signal = get_ta(
            symbol='XBTUSD.P',
            screener='CRYPTO',
            exchange='BITMEX',
            interval=interval,
        )
        print("Signal_" + interval + " " + str(signal) + " ==> " + str(signal['RECOMMENDATION']))
"""

def print_all_signal():
    with open(file_path_summ, 'r') as json_file:
        data = pd.read_json(json_file)
    data_col = data[["Timestamp", "1m","5m","15m","30m","1h","2h","1W","1M"]]
    print(data_col)


###Bogue avec gestion fichier
def get_main_signal_new():
    with open(file_path_summ, 'r') as json_file:
        data = json.load(json_file)
    rec = data[interval_main]['RECOMMENDATION']
    #print(signal['RECOMMENDATION'])
    return rec
    
"""
def get_main_signal():
    #interval = ""
    signal = get_ta(
    symbol='XBTUSD.P',
    screener='CRYPTO',
    exchange='BITMEX',
    interval=interval_main,
        )
    #print(signal['RECOMMENDATION'])
    return signal['RECOMMENDATION']
"""
    
#https://www.tradingview.com/charting-library-docs/latest/api/interfaces/
# Get trading signal from trading view https://www.tradingview.com/symbols/XBTUSD/technicals/
#Doc pour API : https://python-tradingview-ta.readthedocs.io/en/latest/
def get_ta(symbol, screener, exchange, interval):
    ta_interval_list = [Interval.INTERVAL_1_MINUTE,
                        Interval.INTERVAL_5_MINUTES,
                        Interval.INTERVAL_15_MINUTES,
                        Interval.INTERVAL_30_MINUTES,
                        Interval.INTERVAL_1_HOUR,
                        Interval.INTERVAL_2_HOURS,
                        Interval.INTERVAL_4_HOURS,
                        Interval.INTERVAL_1_DAY,
                        Interval.INTERVAL_1_WEEK,
                        Interval.INTERVAL_1_MONTH]

    ta_interval = ta_interval_list[interval_list.index(interval)]

    return TA_Handler(
    symbol=symbol,
    screener=screener,
    exchange=exchange,
    interval=ta_interval,
    ).get_analysis().summary

def get_historic_signal():
    #current_time = dt.datetime.now()
    with open(file_path_summ, 'r') as json_file:
        data = json.load(json_file)
    try:
        with open(file_path_summ_h, "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []
    data["Timestamp_insert"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
    existing_data.append(data)
    
    with open(file_path_summ_h, "w") as f:
        json.dump(existing_data, f, indent=4)

def print_histo_signal():
    with open(file_path_summ_h, 'r') as json_file:
        data = pd.read_json(json_file)
    data_col = ["Timestamp", "1m","5m","15m","30m","1h","2h","1W","1M"]
    df_select = data[data_col]
    #print(df_select)
    print(data)


def get_long_seq():
    global count_long
    signal = get_main_signal_new()
    if signal == "STRONG_BUY":
        count_long += 1
    else:
        count_long = 0
    return count_long

def get_short_seq():
    global count_short
    signal = get_main_signal_new()
    if  signal == "STRONG_SELL":
        count_short += 1
    else:
        count_short = 0
    return count_short

if __name__ == "__main__":
    main()