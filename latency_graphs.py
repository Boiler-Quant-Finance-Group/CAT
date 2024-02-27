import requests
import time
import matplotlib.pyplot as plt

# Kraken API URL
API_URL = "https://api.kraken.com/0/public/Ticker"

# Currency pairs
currency_pairs = [
    'XXBTZUSD', 'XETHZUSD', 'XXRPZUSD', 'XLTCZUSD', 'BCHUSD',
    'ADAUSD', 'DOTUSD', 'EOSUSD', 'XXMRZUSD', 'XTZUSD'
]

# Function to fetch and measure latency
def fetch_latency(pair, additional_pairs):
    pairs = [pair] + additional_pairs
    pair_string = ','.join(pairs)
    start_time = time.time()
    response = requests.get(API_URL, params={'pair': pair_string})
    end_time = time.time()
    return end_time - start_time

# Initialize a dictionary to hold latency data for each currency pair
latency_data = {pair: [] for pair in currency_pairs}

# Collect latency data
for pair in currency_pairs:
    for i in range(10):  # Up to 9 additional pairs
        additional_pairs = currency_pairs[:i] if i > 0 else []
        if pair in additional_pairs:
            additional_pairs.remove(pair)  # Ensure the main pair is not duplicated
        latency = fetch_latency(pair, additional_pairs)
        latency_data[pair].append(latency)

# Plotting
plt.figure(figsize=(12, 8))
for pair, latencies in latency_data.items():
    plt.plot(range(1, 11), latencies, marker='o', label=pair)

plt.title('Latency Across Different Currency Pairs with 1-10 Transactions')
plt.xlabel('Number of Transactions (1 main + additional pairs)')
plt.ylabel('Latency (seconds)')
plt.xticks(range(1, 11))
plt.legend()
plt.grid(True)
plt.show()
