### THe algo is quite simple say you have 4 currencies so k = 4
### And an exchange rate matrix that is k x k so 4 x 4
### Then you iterate the max plus product (up to k times)
### A * A * A * A or in other notation A*^3A
### This mulpication is communitive:
### C1 = A * A
### C2 = C1 * A
### C3 = C2 * A (The diagonal of the exponential is )
### final for k = 4, C=4 

# import numpy as np

# def max_plus_product(A, B):
#     n = A.shape[0]
#     RESULT = np.full((n, n), -np.inf)

#     for i in range(n):
#         for j in range(n):
#             best_k = -1
#             for k in range(n):
#                 current_value = A[i, k] + B[k, j]
#                 if current_value > RESULT[i, j]:
#                     RESULT[i, j] = current_value
#                     best_k = k
#     return RESULT
            

# def detect_arbitrage(A, cycle_length):
#     C_k = A  
#     for i in range(cycle_length-1):
#         C_k = max_plus_product(C_k, A)
#     return np.exp(np.diag(C_k))
    


# # Example Usage:
# # Assuming FX_Rates is the matrix of FX rates
# FX_Rates = np.array([
#     [1, 0.76103, 1.29853, 0.86327],
#     [1.31401, 1, 1.70628, 1.13434],
#     [0.77010, 0.58607, 1, 0.66481],
#     [1.15839, 0.88157, 1.50420, 1]
# ])
# LOG_RATES = np.log(FX_Rates)

# #print("Log Rates", LOG_RATES)

# # Detect arbitrage opportunities for a 3-cycle and 4-cycle as an example
# three_cycle_arbitrage = detect_arbitrage(LOG_RATES, 3)
# four_cycle_arbitrage = detect_arbitrage(LOG_RATES, 4)
# print("this is the k=3-cycle", max(three_cycle_arbitrage))
# print("This is the k=4-cycle", max(four_cycle_arbitrage))




import numpy as np
from getrates import * 
from krakenpairs import *
import requests
import numpy as np
import itertools

def max_plus_product_with_paths(A, B):
    n = len(A)
    RESULT = np.full((n, n), -np.inf)
    PATHS = [[[] for _ in range(n)] for __ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                val = A[i][k] + B[k][j]
                if val > RESULT[i][j]:
                    RESULT[i][j] = val
                    PATHS[i][j] = [i] + [k]

    return RESULT, PATHS

def matrix_power_with_paths(A, power):
    RESULT = np.copy(A)
    PATHS = [[[] for _ in range(A.shape[1])] for __ in range(A.shape[0])]
    
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            PATHS[i][j] = [i]
    
    for _ in range(1, power):
        RESULT, NEW_PATHS = max_plus_product_with_paths(RESULT, A)
        
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                PATHS[i][j] = PATHS[i][j] + NEW_PATHS[i][j]

    return RESULT, PATHS

def detect_arbitrage_with_paths(A, cycle_length):
    powered_matrix, paths_matrix = matrix_power_with_paths(A, cycle_length)
    arbitrage_data = {}
    
    for i in range(A.shape[0]):
        arbitrage_return = np.exp(powered_matrix[i, i]) - 1
        if arbitrage_return > 0:
            cycle_path = paths_matrix[i][i]
            arbitrage_data[i] = {"return": arbitrage_return, "path": cycle_path}
    
    return arbitrage_data

# Example
currencies = ['BTC', 'USDT', 'USD']

massa, currency_names, = build_matrix(count = 5, currencies=currencies, num_top_k=2)

print(massa)
log_FX = np.log(np.array(massa))

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

