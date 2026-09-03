"""
Koko Eating Bananas
Koko must eat all bananas within h hours. piles[i] = bananas in pile i. She can
eat at most speed bananas per hour. Find the minimum integer speed.

Idea: binary search the speed (1..max(piles)). Feasible(speed) = total hours
needed <= h. Hours for pile p = ceil(p / speed). Monotonic: faster -> easier.

Time: O(n log m) where m = max(piles)
Space: O(1)
"""

import math


def min_eating_speed(piles, h):
    def feasible(speed):
        hours = sum(math.ceil(p / speed) for p in piles)
        return hours <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    print(min_eating_speed([3, 6, 7, 11], 8))    # 4
    print(min_eating_speed([30, 11, 23, 4, 20], 5))  # 30
    print(min_eating_speed([30, 11, 23, 4, 20], 6))  # 23
