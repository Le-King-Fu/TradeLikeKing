import time
import Signal_TradingView as signal
import lnmkt as ln
import analysisPositions as an
import tradePosition as trade

total_duration = 60 * 60 * 24
time_interval = 60
start_time = time.time()

def main():
    while time.time() - start_time < total_duration:
        an.print_trades()
        print()
        ln.get_price_Binance()
        print()
        ln.get_price_LNMarket()
        print()
        signal.print_all_signal()
        print()
        print("Margin call :", an.get_list_margin())
        print("Closing time (long):", an.get_list_close_long())
        print("Closing time (short):", an.get_list_close_short())
        trade.add_margin()
        trade.close_futures_short()
        trade.close_futures_long()
        trade.open_futures_long()
        trade.open_futures_short()
        time.sleep(time_interval)    
 
if __name__ == "__main__":
    main()

