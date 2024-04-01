import pandas as pd
import json
import os
import ast
# Function to calculate top k mean and weighted mean prices
def calculate_means(orderbook, k):
    data = ast.literal_eval(orderbook)
    results = {}
    for symbol, book in data.items():
        # Process asks
        asks = book['asks']
        asks_top_k = asks[:k]
        asks_volumes = [ask[1] for ask in asks_top_k]
        asks_prices = [ask[0] for ask in asks_top_k]

        # Calculate means for asks
        mean_ask_price = sum(asks_prices) / len(asks_prices) if asks_prices else None
        weighted_mean_ask_price = sum(p[0] * p[1] for p in asks_top_k) / sum(asks_volumes) if asks_volumes else None

        # Process bids
        bids = book['bids']
        bids_top_k = bids[:k]
        bids_volumes = [bid[1] for bid in bids_top_k]
        bids_prices = [bid[0] for bid in bids_top_k]

        # Calculate means for bids
        mean_bid_price = sum(bids_prices) / len(bids_prices) if bids_prices else None
        weighted_mean_bid_price = sum(p[0] * p[1] for p in bids_top_k) / sum(bids_volumes) if bids_volumes else None

        results[symbol] = {
            'mean_ask_price': mean_ask_price,
            'weighted_mean_ask_price': weighted_mean_ask_price,
            'mean_bid_price': mean_bid_price,
            'weighted_mean_bid_price': weighted_mean_bid_price
        }
    return results

# Specify the number of top orders to consider for mean calculations
k = 5  # for example, top 5

# List of exchanges
exchanges_list = ['bequant', 'bitcoincom', 'hitbtc', 'hitbtc3', 'hollaex', 'oceanex', 'upbit']

# Create the output directory if it doesn't exist
output_dir = './timeseries_postprocess'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each exchange
for exchange_name in exchanges_list:
    # File paths
    input_file_path = f'./timeseries/{exchange_name}_time_series_order_book.csv'
    output_file_path = f'./timeseries_postprocess/{exchange_name}_processed_time_series_order_book.csv'

    # Read CSV
    df = pd.read_csv(input_file_path)

    # Process each row in the DataFrame and store results
    processed_data = []
    for index, row in df.iterrows():
        order_book = row['OrderBook']
        timestamp = row['Timestamp']
        means = calculate_means(order_book, k)
        means['Timestamp'] = timestamp
        processed_data.append(means)
        print("Currented processed Index for:", exchange_name, index)

    # Convert processed data to DataFrame
    processed_df = pd.DataFrame(processed_data)
    
    # Save the processed DataFrame to CSV
    print(processed_df['Timestamp'])
    processed_df.to_csv(output_file_path, index=False)