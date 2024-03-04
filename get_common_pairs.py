import pandas as pd
import itertools



exchanges = ['gateio', 'bitfinex', 'bitmart', 'digifinex', 'kraken', 'bitvavo']
exchange_path = "CAT/exchanges/"
exchange_save_path = "CAT/exchanges_intersection/"

def find_intersection(exchange_combo):
    for exchange_group in exchange_combo:
        df_1 = pd.read_csv(exchange_path + exchange_group[0] + "_df.csv")
        intersection_set = set(list(df_1['symbol']))
        table_name = '_'.join(exchange_group)
        for exchange in list(exchange_group):
            df = pd.read_csv(exchange_path + exchange + "_df.csv")
            symbols = list(df['symbol'])
            intersection_set = intersection_set.intersection(list(symbols))
        
        df_to_save = pd.DataFrame(intersection_set, columns=['symbol'])
        df_to_save.to_csv(exchange_save_path + table_name + "_intersection.csv")

for r in range(2, len(exchanges) + 1):
    exchange_combo = list(itertools.combinations(exchanges, r))
    find_intersection(exchange_combo)


##psuecocode:
    #for each r 1 to 6
        # for each exchange grouping
        #