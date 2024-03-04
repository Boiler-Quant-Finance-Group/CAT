
### This block of code gets exchange info from kraken
### This needs to be repeated for the exchanges we chose

# kraken = ccxt.kraken()
# kraken_json = (kraken.fetch_tickers())
# kraken_df = pd.DataFrame.from_dict(kraken_json, orient='index')
# kraken_df.to_csv("CAT/exchanges/kraken_df")
# print(kraken_df.index)

import ccxt
import pandas as pd
import os

# List of exchanges
exchanges = ['binance', 'bitbank', 'gateio', 'deribit', 'bitfinex', 'bitmart', 'digifinex', 'kraken', 'bitvavo']

for exchange_name in exchanges:
    # Dynamically create exchange object using ccxt
    exchange_class = getattr(ccxt, exchange_name)()
    
    # Fetch tickers
    try:
        tickers_json = exchange_class.fetch_tickers()
        # Convert to DataFrame
        tickers_df = pd.DataFrame.from_dict(tickers_json, orient='index')
        
        
        # Create directory if it doesn't exist
        print("THIS is exxchange name:" + exchange_name, tickers_df)
        directory = f"CAT/exchanges"
        file_path = f"{directory}/{exchange_name}_df.csv"
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        print("directory", directory)

        # Save to CSV
        tickers_df.to_csv(f"{file_path}")
        
        print(f"Data for {exchange_name} saved. Index: {tickers_df.index}")
    except Exception as e:
        print(f"Could not fetch data for {exchange_name}: {str(e)}")


