import time
import Signal_TradingView as signal
import lnmkt as ln
import analysisPositions as an
import tradePosition as trade
import datetime

import yaml

# Load data from a YAML file
with open("config.yml", "r") as yaml_file:
    config_data = yaml.safe_load(yaml_file)

# Access the data as a regular Python dictionary
total_duration = config_data['total_duration']
time_interval = config_data['time_interval']
interval_list = config_data['interval_list']
start_time = time.time()

def main():
    while time.time() - start_time < total_duration:
        ln.get_info()
        ln.get_price_Binance()
        print()
        ln.get_price_LNMarket()
        print()
        print(datetime.datetime.now())
        signal.get_all_signal(interval_list)
        print()
        signal.print_all_signal()
        signal.get_main_signal_new()
        print()
        if ln.get_nb_trx() == 0:
            print("No transaction")
            print()
        else: 
            an.get_trades_running()
            an.print_trades_running()
            print()
            print("Margin call :", an.get_list_margin())
            trade.add_margin()
            print("Closing time (long):", an.get_list_close_long_aggro())
            print("Closing time (short):", an.get_list_close_short_aggro())
            """
            print("Closing time (long):", an.get_list_close_long())
            print("Closing time (short):", an.get_list_close_short())
            trade.add_margin()
            trade.close_futures_short()
            trade.close_futures_long()
            trade.open_futures_long()
            trade.open_futures_short()

            """
            ### Version Agressive ###
            trade.close_futures_short_aggro()
            trade.close_futures_long_aggro()
            an.get_trades_closed()
            an.get_closing_msg_long()
            an.get_closing_msg_long()
 
        trade.open_futures_long_aggro()
        trade.open_futures_short_aggro()
        print()
        signal.get_historic_signal()
        time.sleep(time_interval)    
 


if __name__ == "__main__":
    main()