#### The goal of this is to query information about all the cryptocurrencies that can be traded on kraken.com
#### Build a pandas dataframe with the format :Name of trading pair, 24h volume, 24h hi, 24low, 24h percent change, 1 week change. 
                                            #  BTC, [BTCUSD, BTCGBP, BTCEUR], 160M, 35,000, 34,000, 12%, 14%
### since kraken always uses pairs lets just compare to USD


import requests
import pandas as pd
import numpy as np
from CAT.archived_scripts.krakenpairs import *
import openpyxl


### how to find 
columns = ["CurrencyName", "current_exchange_rate", "volume_last_24h", "weighted_avg_price_last_24h", "number_of_trades_last_24h", "low_last_24h", "high_last_24h", "opening_price"]


single_crypto_tup_list = get_pairs_kraken(pair_tups=True)
data = []
for pair1, pair2 in single_crypto_tup_list:
    request_string = 'https://api.kraken.com/0/public/Ticker?pair=' + pair1 + pair2
    resp = requests.get(request_string)
    data_dict = dict(resp.json())
    
    row = []
    print("request string", request_string)
    print("Response:", data_dict)
    if 'result' in data_dict.keys():
        crypto_key = next(iter(data_dict['result']))
        crypto_details = data_dict['result'][crypto_key]
    
        last_trade_price, last_trade_volume = crypto_details['c']
        volume_last_24h, volume_previous_24h = crypto_details['v']
        weighted_avg_price_last_24h, weighted_avg_price_previous_24h = crypto_details['p']
        number_of_trades_last_24h, number_of_trades_previous_24h = crypto_details['t']
        low_last_24h, low_previous_24h = crypto_details['l']
        high_last_24h, high_previous_24h = crypto_details['h']
        opening_price = crypto_details['o']
    
        row.append((pair1, pair2))
        row.append((last_trade_price))
        row.append((volume_last_24h))
        row.append((weighted_avg_price_last_24h))
        row.append((number_of_trades_last_24h))
        row.append((low_last_24h))
        row.append((high_last_24h))
        row.append((opening_price))
    
        data.append(row)
        print("Current Row for:", (pair1+pair2), ":", row)
    else:
        print("This currency isnt real")
    

    
df = pd.DataFrame(data, columns=columns)

# Display the DataFrame
print(df)

#### save the df:
df.to_excel("krakendata.xlsx")  
    