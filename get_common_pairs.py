
# import pandas as pd
# exchanges = ['gateio', 'deribit', 'bitfinex', 'bitmart', 'digifinex', 'kraken', 'bitvavo']
# exchange_path = "CAT/exchanges/" + exchanges[5] + "_df"
# print(exchange_path)
# df = pd.read_csv(exchange_path)
# print(df['symbol'])
import itertools
import os
import pandas as pd


# List of exchanges
exchanges = ['gateio', 'deribit', 'bitfinex', 'bitmart', 'digifinex', 'kraken', 'bitvavo']
exchange_path = "CAT/exchanges/"

# Function to load data and find intersection of 'symbol' column
def find_intersection(exchange_combination):
    # Load the CSV files for all exchanges in the combination
    dfs = [pd.read_csv(exchange_path + exchange + "_df.csv") for exchange in exchange_combination]
    
    # Find the intersection of the 'symbol' column for all DataFrames
    intersection = set(dfs[0]['symbol'])
    for df in dfs[1:]:
        intersection = intersection.intersection(set(df['symbol']))
    
    return intersection

# Dictionary to store the intersections
intersections = {}

# Find all combinations for 7 choose 1 to 7 choose 7
for r in range(1, 8):
    for exchange_combination in itertools.combinations(exchanges, r):
        # Find intersection
        intersection_symbols = find_intersection(exchange_combination)
        # Create a table name based on the combination
        table_name = '_'.join(exchange_combination)
        # Store the intersection in the dictionary
        intersections[table_name] = intersection_symbols

# Now `intersections` contains all the intersections
# To access the intersection for a specific combination, use:
# intersections['exchange1_exchange2_...']

# If you want to save these intersections to CSV files:
for table_name, symbols in intersections.items():
    # Convert the set of symbols to a DataFrame
    df_symbols = pd.DataFrame(list(symbols), columns=['symbol'])
    # Save to a CSV file
    df_symbols.to_csv(exchange_path + table_name + "_intersection.csv", index=False)

# Print out an example
print(intersections['gateio_deribit_bitfinex'])