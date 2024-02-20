from algo import *

currencies = ['BTC', 'USDT', 'USD']

mat, currency_names, = build_matrix(count = 5, currencies=currencies, num_top_k=2)

print(mat)
log_FX = np.log(np.array(mat))

three_cycle_arbitrage = detect_arbitrage_with_paths(log_FX, 3)
k_cycle_arbitrage = detect_arbitrage_with_paths(log_FX, len(currencies))

print("3-cycle arbitrage opportunities:", three_cycle_arbitrage)
print("4-cycle arbitrage opportunities:", k_cycle_arbitrage)


def trades_from_path(path, currency_names):
    trades = []
    for i in range(len(path) - 1):
        trades.append(f"Trade {currency_names[path[i]]} for {currency_names[path[i+1]]}")
    return trades

print("3-cycle arbitrage opportunities:")
for node, data in three_cycle_arbitrage.items():
    print(f"Start with {currency_names[node]}:")
    for trade in trades_from_path(data['path'], currency_names):
        print(" -> ", trade)
    print(f"Return: {data['return']*100:.6f}%\n")

print("k-cycle arbitrage opportunities:")
for node, data in k_cycle_arbitrage.items():
    print(f"Start with {currency_names[node]}:")
    for trade in trades_from_path(data['path'], currency_names):
        print(" -> ", trade)
    print(f"Return: {data['return']*100:.6f}%\n")