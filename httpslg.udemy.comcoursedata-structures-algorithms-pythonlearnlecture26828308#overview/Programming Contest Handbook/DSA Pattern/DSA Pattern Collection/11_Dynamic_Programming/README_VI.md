# DYNAMIC PROGRAMMING (QUY HOẠCH ĐỘNG)

## Nó là gì?

Quy hoạch động giải bài toán bằng cách chia thành các **bài toán con chồng lấn**, giải mỗi
bài **một lần**, rồi **tái sử dụng** kết quả. Nó đòi hỏi hai tính chất:
1. **Cấu trúc con tối ưu** — lời giải tối ưu được xây từ các lời giải con tối ưu.
2. **Bài toán con chồng lấn** — cùng một bài toán con được giải nhiều lần.

**Cách tiếp cận:** Đệ quy → Memoization → Tabulation → Tối ưu không gian.

## Vì sao dùng?

- Biến lời giải **mũ** thành **đa thức** (ví dụ O(2^n) → O(n)).
- Tốt nhất cho bài **đếm / max / min / số cách** với phép tính lặp lại.
- Dùng được mỗi khi bạn định nghĩa trạng thái `dp[i]` và công thức truy hồi
  `dp[i] = f(dp[i-1], ...)`.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Tối đa / tối thiểu ..." | tối ưu trên các lựa chọn |
| "Bao nhiêu cách để ..." | đếm đường / tổ hợp |
| "Có đến được ... không?" | khả năng tới được (DP boolean) |
| Công thức truy hồi / bài con lặp lại | memoize / tabulate |
| "Dãy con / chuỗi con (không liên tục)" | DP điển hình (khác sliding window) |

## Minh họa — Fibonacci với tabulation

```
 fib: 0 1 1 2 3 5 8
 dp[0]=0, dp[1]=1
 dp[2]=dp[1]+dp[0]=1
 dp[3]=dp[2]+dp[1]=2
 dp[4]=dp[3]+dp[2]=3
 ...

        ┌───────┐
 fib(5)│  = 5  │
        └───────┘
      /           \
  fib(4)=3     fib(3)=2
    /  \         /  \
 f(3)=2 f(2)=1 f(2)=1 f(1)=1
  / \
f(2)=1 f(1)=1        <- chồng lấn! giải một lần với memoization

 Không DP: fib(5) gọi fib(2) tới 3 lần -> O(2^n)
 Có DP:    mỗi trạng thái tính một lần -> O(n)
```

## Minh họa — coin change (số đồng tối thiểu để tạo amount)

```
 coins = [1, 2, 5], amount = 11
 dp[a] = số đồng tối thiểu tạo amount a

 dp[0] = 0
 dp[1] = 1 (1)
 dp[2] = 1 (2)
 dp[3] = 2 (1+2)
 ...
 dp[11] = min(dp[10]+1, dp[9]+1, dp[6]+1) = min(3, 3, 2+1=3) = 3  (5+5+1)

 công thức: dp[a] = min(dp[a - c] + 1 for c in coins nếu a - c >= 0)
```

## Độ phức tạp

- **Thời gian:** số trạng thái × số phép chuyển (thay đổi: O(n), O(n²), O(n×W)...)
- **Bộ nhớ:** O(số trạng thái) → thường tối ưu về O(1) hoặc O(n)

## Mẫu code

```python
# 1) Memoization (top-down)
from functools import lru_cache

@lru_cache(None)
def solve(state):
    if base_case(state):
        return ...
    best = min/max(solve(next_state) for next_state in moves(state))
    return best

# 2) Tabulation (bottom-up)
dp = [0] * (n + 1)
dp[0] = base
for i in range(1, n + 1):
    dp[i] = f(dp[i - 1], dp[i - 2], ...)
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Fibonacci | `fibonacci.py` | memo + tabulation + O(1) không gian |
| House Robber | `house_robber.py` | dp[i] = max(cướp i, bỏ qua i) |
| Coin Change | `coin_change.py` | số đồng tối thiểu cho từng amount |
| Longest Increasing Subsequence | `longest_increasing_subsequence.py` | dp[i] = dãy tốt nhất kết thúc tại i |

## Luyện tập

Thử: Edit Distance, Climbing Stairs, Unique Paths, 0/1 Knapsack, Partition Equal
Subset Sum, Word Break, Decode Ways.
