from tradingview_ta import TA_Handler, Interval, Exchange

interval_list = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1W', '1M']
interval_main = "5m"

count_long = 0
count_short = 0

def main():
    #print_all_signal()
    print(get_main_signal())
    print(get_long_seq())
    print(get_short_seq())



def print_all_signal():
    for interval in interval_list:
        signal = get_ta(
            symbol='XBTUSD.P',
            screener='CRYPTO',
            exchange='BITMEX',
            interval=interval,
        )
        print("Signal_" + interval + " " + str(signal) + " ==> " + str(signal['RECOMMENDATION']))
    
#je devrais le sauvegarder et l'utiliser, car delais donne des droles de results
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

# Get trading signal from trading view https://www.tradingview.com/symbols/XBTUSD/technicals/
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

def get_long_seq():
    global count_long
    signal = get_main_signal()
    if signal == "STRONG_BUY":
        count_long += 1
    else:
        count_long = 0
    return count_long

def get_short_seq():
    global count_short
    signal = get_main_signal()
    if  signal == "STRONG_SELL":
        count_short += 1
    else:
        count_short = 0
    return count_short

if __name__ == "__main__":
    main()