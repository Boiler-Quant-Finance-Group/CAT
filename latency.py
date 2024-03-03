import ccxt
import time
import matplotlib.pyplot as plt


# Define the exchanges to query
#exchange_ids = ['binance', 'bitbank', 'gateio', 'deribit', 'bitfinex', 'bitmart', 'bitmex', 'digifinex', 'kraken', 'bitvavo']
exchange_ids = ['bitbank', 'gateio', 'deribit', 'bitfinex', 'bitmart', 'bitmex', 'digifinex', 'kraken', 'bitvavo']


# Initialize the exchanges
exchanges = {exchange_id: getattr(ccxt, exchange_id)() for exchange_id in exchange_ids}

# Select some universal currency pairs available on most exchanges
# Note: Ensure these pairs are available on the exchanges you're querying to avoid errors
currency_pairs = [
    'BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT', 'BCH/USDT',
    'ADA/USDT', 'DOT/USDT', 'EOS/USDT', 'XMR/USDT', 'XTZ/USDT'
]

# Initialize a dictionary to store latency data
latency_data = {exchange_id: [] for exchange_id in exchange_ids}

# Function to measure and return the query latency
def measure_query_latency(exchange, pairs):
    start_time = time.time()
    for pair in pairs:
        try:
            exchange.fetch_order_book(pair)
        except Exception as e:
            print(f"Error fetching {pair} from {exchange.id}: {e}")
            return None # Or handle error appropriately
    end_time = time.time()
    return end_time - start_time

# Collect latency data for each exchange and number of currency pairs
for exchange_id, exchange in exchanges.items():
    for i in range(1, 11):  # From 1 to 10 currency pairs
        pairs_to_query = currency_pairs[:i]
        latency = measure_query_latency(exchange, pairs_to_query)
        if latency is not None:  # Ensure successful measurement
            latency_data[exchange_id].append((len(pairs_to_query),latency))

print(latency_data)
# Plotting
plt.figure(figsize=(12, 8))
for exchange_id, latencies in latency_data.items():
    if latencies:  # Ensure there's data to plot
        plt.plot(range(1, len(latencies) + 1), latencies, marker='o', label=exchange_id)

plt.title('Query Latency vs. Number of Currency Pairs Queried')
plt.xlabel('Number of Currency Pairs Queried')
plt.ylabel('Latency (seconds)')
plt.xticks(range(1, 11))
plt.legend()
plt.grid(True)
plt.show()

