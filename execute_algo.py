from algo import *
import concurrent.futures
from itertools import repeat

def trades_from_path(path, currency_names):
    trades = []
    for i in range(len(path) - 1):
        trades.append(f"Trade {currency_names[path[i]]} for {currency_names[path[i + 1]]}")
    return trades


if __name__ == '__main__':
    currencies = ['BTC', 'USDT', 'USD', 'EUR', 'ETH', 'LTC']
    mat, currency_names, = build_matrix(count=5, currencies=currencies, num_top_k=2)
    print(mat)
    # log_FX = np.log(np.array(mat))

    # Multithread the arbitrage detection algorithm
    cycles = list(range(3, len(currencies) + 1))
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(cycles)) as executor:
        results = executor.map(detect_arbitrage_with_paths, repeat(mat), cycles)

    for index, result in enumerate(results):
        print(f"{index + 3}-cycle arbitrage opportunities:")
        for node, data in result.items():
            print(f"Start with {currency_names[node]}:")
            for trade in trades_from_path(data['path'], currency_names):
                print(" -> ", trade)
            print(f"Return: {data['return'] * 100:.6f}%\n")
