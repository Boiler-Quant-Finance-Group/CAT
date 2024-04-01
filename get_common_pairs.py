import pandas as pd
import itertools
import ccxt


exchanges = ['bequant', 'bitcoincom', 'hitbtc', 'hitbtc3', 'hollaex', 'oceanex', 'upbit']
exchange_path = "exchanges/"
exchange_save_path = "exchanges_intersection/"

count = 0
def find_intersection(exchange_combo):
    global count
    for exchange_group in exchange_combo:
        # exchange_obj = getattr(ccxt, exchange_group[0])()
        # exchange_obj.loadMarkets()
        
        df_1 = pd.read_csv(exchange_path + exchange_group[0] + "_df.csv")
        symbols1 = list(df_1['symbol'])     
        # symbols1 = exchange_obj.symbols
        #print("this is symbols1", symbols1)
        intersection_set = set(list(symbols1))
        
        table_name = '_'.join(exchange_group)
        for exchange in list(exchange_group):
            # exchange_obj = getattr(ccxt, exchange)()
            # exchange_obj.loadMarkets()
            df = pd.read_csv(exchange_path + exchange + "_df.csv")
            symbols_local = list(df['symbol'])
            # symbols_local = exchange_obj.symbols
            # intersection_set = intersection_set.intersection(list(symbols_local))
        
        df_to_save = pd.DataFrame(intersection_set, columns=['symbol'])
        df_to_save.to_csv(exchange_save_path + table_name + "_intersection.csv")
        count += 1
        print("This is count of dfs written:", count)
        

for r in range(1, len(exchanges) + 1):
    exchange_combo = list(itertools.combinations(exchanges, r))
    find_intersection(exchange_combo)
    


##psuecocode:
    #for each r 1 to 6
        # for each exchange grouping
        #