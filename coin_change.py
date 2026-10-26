import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from time import perf_counter

def coin_change_recursive(coins, amount):
    if amount == 0:
        return 0
    best=9999999999999999
    for i in coins:
        if i <= amount: 
            best=min(best, 1+coin_change_recursive(coins,amount-i))
    return best

def coin_change_memoized(coins, amount):
    memo={}

    def solve(amount):
        if amount == 0:
            return 0
        if amount in memo:
            return memo[amount]
        best=9999999999999999
        for i in coins:
            if i <= amount: 
                best=min(best,1+solve(amount-i))
        memo[amount]=best
        return best

    return solve(amount)

def coin_change_dp(coins, amount):
    dp = [9999999999999999] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for j in coins:
            if j <= i:
                dp[i] = min(dp[i], 1 + dp[i - j])

    return dp[amount]

coins=[1,2,5]
test_list=[i for i in range(0,31)]

# Function to benchmark the execution time of a given algorithm over a set of test cases

def benchmark_algo_multi(algo, coins, test_cases, repeat=1):
    times = []
    for i in test_cases:
        total_duration = 0
        for _ in range(repeat):
            start = perf_counter()
            algo(coins,i)
            end = perf_counter()
            duration = end - start
            total_duration += duration
        avg_time = total_duration / repeat
        times.append((i, avg_time))
    return times

coin_change_recursive_times = benchmark_algo_multi(coin_change_recursive, coins, test_list, repeat=10)
coin_changed_memoized_times = benchmark_algo_multi(coin_change_memoized, coins, test_list, repeat=10)
coin_change_dp_times = benchmark_algo_multi(coin_change_dp, coins, test_list, repeat=10)

print(f"recursive:{coin_change_recursive_times}")
print(f"memoized:{coin_changed_memoized_times}")
print(f"bottom-up:{coin_change_dp_times}")

df_base = pd.DataFrame(coin_change_recursive_times, columns = ["k", "time"])
df_base['algo'] = "coin_change_recursive"

df_memo = pd.DataFrame(coin_changed_memoized_times, columns = ["k", "time"])
df_memo['algo'] = "coin_change_memoized"

df_dp = pd.DataFrame(coin_change_dp_times, columns = ["k", "time"])
df_dp['algo'] = "coin_change_dp"

df = pd.concat([df_base, df_memo, df_dp], ignore_index=True)

sns.lineplot(data=df, x="k", y="time", hue="algo")
plt.xlabel("k")
plt.ylabel("time (log s)")
plt.title("Execution Time Comparison of Recursive, Memoized, and Bottom-Up Coin Change Algorithms")
plt.yscale("log")
plt.savefig("empirical_result.png")