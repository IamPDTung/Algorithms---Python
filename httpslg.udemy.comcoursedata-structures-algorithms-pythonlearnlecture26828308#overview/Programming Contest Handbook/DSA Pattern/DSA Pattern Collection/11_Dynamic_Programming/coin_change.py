"""
Coin Change
You are given coins of different denominations and an integer amount. Return the
fewest number of coins needed to make up that amount, or -1 if impossible.

Idea: dp[a] = min coins to make amount a.
dp[a] = min(dp[a - c] + 1 for c in coins if a - c >= 0)

Time: O(amount * len(coins))
Space: O(amount)
"""


def coin_change(coins, amount):
    INF = float("inf")
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a >= c:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1


if __name__ == "__main__":
    print(coin_change([1, 2, 5], 11))     # 3  (5 + 5 + 1)
    print(coin_change([2], 3))            # -1
    print(coin_change([1], 0))            # 0
