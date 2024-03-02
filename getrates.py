### kestan was here
### Complex problem -- Have to first query rates from API then find best exchange rate quote 
#### approach #1 rates from just 

#### Following is kraken public api 
#from CAT.archived_scripts.krakenpairs import *
import requests
import numpy as np
import itertools
import ccxt
import numpy as np


#### get all currencies -> then filter to a certain number of currencies by some metric(s) -> we should be getting a list of currencies -> then query the pairs -> build matrix -? 
#### Then run the detection algorithm

def kraken_request(cur1, cur2, count):
    request_string = "https://api.kraken.com/0/public/Depth?pair="
    full_request_string = request_string + cur1 + cur2 + "&count=" + str(count)
                
    resp = requests.get(full_request_string)
    print("This is request stirng:", full_request_string)
    print("This is response:", resp.json())
    
    return dict(resp.json())
    
def get_rates_generic(exchange_id='kraken', count=100, pairs=[("BTC", "USD")], k=5):
    # Ensure the exchange ID is supported by CCXT
    assert exchange_id in ccxt.exchanges, f"{exchange_id} is not supported by CCXT."
    
    # Initialize the exchange
    exchange = getattr(ccxt, exchange_id)()
    
    data_final = {}
    for cur1, cur2 in pairs:
        symbol = f"{cur1}/{cur2}"  # Format the symbol as expected by CCXT
        
        # Fetch the order book for the symbol
        order_book = exchange.fetch_order_book(symbol, limit=count)
        
        # Extract ask and bid prices
        ask_prices = np.array([ask[0] for ask in order_book['asks']])
        bid_prices = np.array([bid[0] for bid in order_book['bids']])
        
        # Calculate the averages of the top k asks and bids
        best_k_asks = np.partition(ask_prices, k)[:k]
        top_k_bids = np.partition(bid_prices, -k)[-k:]
        
        average_low_k_asks = best_k_asks.mean()
        average_top_k_bids = top_k_bids.mean()
        
        # Store the results
        data_final[(cur1, cur2)] = average_low_k_asks
        data_final[(cur2, cur1)] = 1 / average_top_k_bids  # Inverse of average top k bids for reverse pair
        
    return data_final

                

### Function takes in a list of tradable currency pairs then returns the kth highest ask price
def build_matrix(count =100, currencies = ["BTC", "USD", "USDT"], num_top_k = 10):
# pairs = (list(get_pairs_kraken(True)))
# print(pairs)
    
    currency_pairs = list(itertools.combinations(currencies, 2))
    print("currency pairs:",  currency_pairs)
    
    rates = (get_rates_kraken(count = count, pairs=currency_pairs, k = num_top_k))

# Create a square matrix filled with zeros
    #currencies = list(set([currency for pair in rates.keys() for currency in pair]))
    

# Sort currencies to ensure consistent matrix structure
    currencies.sort()
    print("Currencies in matrix order:", currencies)

# Create a square matrix filled with zeros
    matrix_size = len(currencies)
    rate_matrix = np.zeros((matrix_size, matrix_size))
    print("this is rates dict:", rates)
# Populate the matrix with rates from the dictionary
    for i, from_currency in enumerate(currencies):
        for j, to_currency in enumerate(currencies):
            if from_currency == to_currency:
                rate_matrix[i, j] = 1  # Diagonal entries
            elif (from_currency, to_currency) in rates:
                rate_matrix[i, j] = rates[(from_currency, to_currency)]

    return np.log(np.array(rate_matrix)), currencies
        
