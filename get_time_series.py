#### idea is to create a timed I/O s.t 
import sys
import ccxt
import time
import pandas as pd
import threading
# supported_exchanges = []
# exchange_names = ccxt.exchanges
# for exchange_id in exchange_names:
#     exchange_kraken = getattr(ccxt, exchange_id)()
#     if exchange_kraken.has['fetchOrderBooks']:
#         supported_exchanges.append(exchange_id)
# print(supported_exchanges)
# print(symbols)

# euth = exchange_kraken.markets['ETH/USDT']
# print(euth)

# greeks = exchange_kraken.fetchGreeks('ETH/USDT')
# print(greeks)
# print("VOLOTILIY", exchange_kraken.fetchVolatilityHistory('BTC'))
#print(supported_exchanges)

# Calculate the duration by subtracting the start time from the current time

# exchange_list = ['gateio', 'bitfinex', 'bitmart', 'digifinex', 'kraken', 'bitvavo']
# for exchagnge_id in exchange_list:
#     exchange_obj = getattr(ccxt, exchange_id)()
#     start_time = time.time()
    
#     exchange_obj.loadMarkets()
    
#     symbols = exchange_obj.symbols
#     for symbol in symbols:
#         order_book = exchange_obj.fetchOrderBook(symbol, limit = 5)
#         print(order_book)
#     duration = time.time() - start_time
    
#     print(duration)
# exchanges_list = ['bequant', 'bitcoincom', 'hitbtc', 'hitbtc3', 'hollaex', 'oceanex', 'upbit']
# # exchanges_list = ['bequant', 'bitcoincom', 'hitbtc', 'hitbtc3', 'hollaex', 'oceanex', 'upbit']
# # taken out = yobit, and fmfwio
# row_num = 500
# interval = 5 ### number of secinds intervals
# def queryTimeSeries(exchange_name):
#     exchange_obj = getattr(ccxt, exchange_name)()


#     df = pd.DataFrame(columns=['Timestamp', 'OrderBook'])
    
# # Target interval between starts of data collection iterations (5 seconds)
#     index = 0
#     #new_list = []
#     while True:
#         start_time = time.time()
#         timestamp = int(start_time)

#         order_book =  exchange_obj.fetchOrderBooks()
#         #new_list.append(order_book)
        
#         df_new = pd.DataFrame({'Timestamp': timestamp, 'OrderBook': str(order_book)}, index = [index])
    
#         df = pd.concat([df, df_new])
#         execution_time = time.time() - start_time
#         print("this is execution time:", execution_time)
#         time_to_sleep = max(0, interval - execution_time)
#         print("BAD IF ALWAYS 0:", time_to_sleep)
#         time.sleep(time_to_sleep)
#         index +=1

#         if len(df) >= row_num:
             
#            # print(str(sys.getsizeof(new_list))) 
#             return df
#             break

# full_start_time = time.time()
# for exchange_name in exchanges_list:
#     df = queryTimeSeries(exchange_name)
    
#     file_path = './time_series/' + exchange_name + '_time_series_order_book.csv'
#     df.to_csv(file_path, index=False)
    
# full_end_time =  time.time()

# total_time = full_end_time - full_start_time

# print(total_time)
exchanges_list = ['bequant', 'bitcoincom', 'hitbtc', 'hitbtc3', 'hollaex', 'oceanex', 'upbit']

# Function to query timeseries data for a given exchange
def queryTimeSeries(exchange_name):
    exchange_obj = getattr(ccxt, exchange_name)()
    df = pd.DataFrame(columns=['Timestamp', 'OrderBook'])
    index = 0
    while True:
        start_time = time.time()
        timestamp = int(start_time)

        # Assuming this is a pseudo method for demonstration; replace with actual method to fetch order book
        order_book = exchange_obj.fetchOrderBooks()
        
        df_new = pd.DataFrame({'Timestamp': timestamp, 'OrderBook': str(order_book)}, index=[index])
        df = pd.concat([df, df_new])
        execution_time = time.time() - start_time
        print(f"Execution time for {exchange_name}: {execution_time}")
        time_to_sleep = max(0, interval - execution_time)
        time.sleep(time_to_sleep)
        index += 1

        if len(df) >= row_num:
            file_path = f'./timeseries/{exchange_name}_time_series_order_book.csv'
            df.to_csv(file_path, index=False)
            break

# Number of rows to collect and interval
row_num = 5
interval = 5  # Number of seconds intervals

# Main function to start threads for each exchange
def main():
    threads = []
    for exchange_name in exchanges_list:
        thread = threading.Thread(target=queryTimeSeries, args=(exchange_name,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    full_start_time = time.time()
    main()
    full_end_time = time.time()
    total_time = full_end_time - full_start_time
    print(f"Total execution time: {total_time}")