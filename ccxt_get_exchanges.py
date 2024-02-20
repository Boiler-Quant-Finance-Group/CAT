import ccxt
import pandas as pd

### This block of code gets exchange info from kraken
### This needs to be repeated for the exchanges we chose

kraken = ccxt.kraken()
kraken_json = (kraken.fetch_tickers())
kraken_df = pd.DataFrame.from_dict(kraken_json, orient='index')
kraken_df.to_csv("CAT/exchanges/kraken_df")
print(kraken_df.index)

