import time
import Signal_TradingView as signal
import lnmkt as ln
import analysisPositions as an
import tradePosition as trade
import datetime

total_duration = 60 * 60 * 24
time_interval = 45
interval_list = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1W', '1M']
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
            an.get_closing_msg_long()
            an.get_closing_msg_long()
 
        trade.open_futures_long_aggro()
        trade.open_futures_short_aggro()
        print()
        signal.get_historic_signal()
        time.sleep(time_interval)    
 
if __name__ == "__main__":
    main()