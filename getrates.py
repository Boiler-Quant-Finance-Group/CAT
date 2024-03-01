### kestan was here
### Complex problem -- Have to first query rates from API then find best exchange rate quote 
#### approach #1 rates from just 

#### Following is kraken public api 
# from CAT.archived_scripts.krakenpairs import *
import requests
import numpy as np
import itertools


# ### get all currencies -> then filter to a certain number of currencies by some metric(s) -> we should be getting a
# list of currencies -> then query the pairs -> build matrix -? ### Then run the detection algorithm

def kraken_request(cur1, cur2, count):
    request_string = "https://api.kraken.com/0/public/Depth?pair="
    full_request_string = request_string + cur1 + cur2 + "&count=" + str(count)

    resp = requests.get(full_request_string)
    print("This is request stirng:", full_request_string)
    print("This is response:", resp.json())

    return dict(resp.json())


def get_rates_kraken(count=100, pairs=[("BTC", "USD")], k=5):
    data_final = {}
    data_set = set()
    ### for each currency in pairs return the average of the kth highest asks and return a
    for cur1, cur2 in pairs:
        print("this is dataset:", data_set)
        if (cur1 + cur2) not in data_set:
            json_dict = kraken_request(cur1=cur1, cur2=cur2, count=count)
            if 'result' in json_dict.keys():
                crypto_key = next(iter(json_dict['result']))
                ask_prices = np.array([float(ask[0]) for ask in json_dict['result'][crypto_key]['asks']])
                bid_prices = np.array([float(ask[0]) for ask in json_dict['result'][crypto_key]['bids']])

                # Use NumPy's partitioning function to get the top k highest ask prices
                # This avoids having to sort the entire array

                best_k_asks = np.partition(ask_prices, k)[:k]

                top_k_bids = np.partition(bid_prices, -k)[-k:]

                # Calculate the average of the top k prices
                average_low_k_asks = best_k_asks.mean()
                average_top_k_bids = top_k_bids.mean()

                data_final[(cur1, cur2)] = average_low_k_asks
                data_final[(cur2, cur1)] = 1 / average_top_k_bids
                # data_final[(cur2, cur1)] = 1/average_low_k_asks

                data_set.add(cur1 + cur2)
                data_set.add(cur2 + cur1)

                ###BTC/USD -> good,
                #### code addds btc/usd and usd/btc
                ### we do not want to query again
                ### as usd/btc is in this pairwise list
                ### MK/USD
                ### USD/MK both do not exist
        if (cur2 + cur1) not in data_set:
            json_dict = kraken_request(cur1=cur2, cur2=cur1, count=count)
            if 'result' in json_dict.keys():
                crypto_key = next(iter(json_dict['result']))
                ask_prices = np.array([float(ask[0]) for ask in json_dict['result'][crypto_key]['asks']])
                bid_prices = np.array([float(ask[0]) for ask in json_dict['result'][crypto_key]['bids']])

                best_k_asks = np.partition(ask_prices, k)[:k]
                top_k_bids = np.partition(bid_prices, -k)[-k:]
                average_low_k_asks = best_k_asks.mean()
                average_top_k_bids = top_k_bids.mean()

                data_final[(cur2, cur1)] = average_low_k_asks
                data_final[(cur1, cur1)] = 1 / average_top_k_bids
                data_set.add(cur2 + cur1)
                data_set.add(cur1 + cur2)

    return data_final


### Function takes in a list of tradable currency pairs then returns the kth highest ask price
def build_matrix(count=100, currencies=["BTC", "USD", "USDT"], num_top_k=10):
    # pairs = (list(get_pairs_kraken(True)))
    # print(pairs)

    currency_pairs = list(itertools.combinations(currencies, 2))
    print("currency pairs:", currency_pairs)

    rates = (get_rates_kraken(count=count, pairs=currency_pairs, k=num_top_k))

    # Create a square matrix filled with zeros
    # currencies = list(set([currency for pair in rates.keys() for currency in pair]))

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
