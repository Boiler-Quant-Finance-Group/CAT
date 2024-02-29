import ccxt
import pandas as pd
import os

### This block of code gets exchange info from kraken
### This needs to be repeated for the exchanges we chose

# kraken = ccxt.kraken()
# kraken_json = (kraken.fetch_tickers())
# kraken_df = pd.DataFrame.from_dict(kraken_json, orient='index')
# kraken_df.to_csv("CAT/exchanges/kraken_df")
# print(kraken_df.index)

# List of exchanges
exchanges = ['binance', 'bitbank', 'gateio', 'deribit', 'bitfinex', 'bitmart', 'bitmex', 'digifinex', 'kraken', 'bitvavo']

for exchange_name in exchanges:
    # Dynamically create exchange object using ccxt
    exchange_class = getattr(ccxt, exchange_name)()
    
    # Fetch tickers
    try:
        tickers_json = exchange_class.fetch_tickers()
        # Convert to DataFrame
        tickers_df = pd.DataFrame.from_dict(tickers_json, orient='index')
        
        # Create directory if it doesn't exist
        print(tickers_df)
        directory = f"CAT/exchanges/{exchange_name}_df"
        print("directory", directory)

        # Save to CSV
        tickers_df.to_csv(f"{directory}")
        
        print(f"Data for {exchange_name} saved. Index: {tickers_df.index}")
    except Exception as e:
        print(f"Could not fetch data for {exchange_name}: {str(e)}")


