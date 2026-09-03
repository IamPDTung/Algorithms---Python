# MONOTONIC STACK (NGĂN XẾP ĐƠN ĐIỆU)

## Nó là gì?

Monotonic Stack là một **ngăn xếp luôn giữ các phần tử theo thứ tự đã sắp xếp** (tăng
nghiêm ngặt hoặc giảm nghiêm ngặt) tại mọi thời điểm. Trước khi đẩy phần tử mới, ta
**pop mọi phần tử vi phạm thứ tự**. Vì mỗi phần tử được đẩy một lần và pop một lần, tổng
công việc là **O(n)** — đây là lý do nó giải bài "phần tử lớn/nhỏ kế tiếp" trong thời gian tuyến tính.

## Vì sao dùng?

- Cách ngây thơ "với mỗi phần tử, quét phần còn lại" là **O(n²)**. Monotonic stack giúp **O(n)**.
- Nó trả lời: với mỗi chỉ số, phần tử **lớn hơn kế tiếp** (hoặc nhỏ hơn) bên **phải** (hoặc trái).
- Rất hợp cho bài **histogram / diện tích**, khi phạm vi của một thanh phụ thuộc vào các
  thanh nhỏ hơn gần nhất hai bên.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Phần tử lớn hơn kế tiếp / trước đó" | ứng dụng kinh điển |
| "Phần tử nhỏ hơn kế tiếp / trước đó" | ý tưởng tương tự, đảo thứ tự |
| "Histogram / diện tích hình chữ nhật lớn nhất" | phần tử nhỏ hơn gần nhất trái & phải |
| "Tích nước mưa" | ranh giới cao hơn gần nhất |
| Cấu trúc lồng nhau / kiểu ngoặc | monotonic stack giữ lịch sử hữu ích |

## Minh họa — phần tử lớn hơn kế tiếp

```
 nums = [2, 1, 4, 3]
                kết quả (lớn hơn kế tiếp)
  index 0: 2 -> 4
  index 1: 1 -> 4
  index 2: 4 -> -1
  index 3: 3 -> -1

 Ngăn xếp giữ các chỉ số với giá trị giảm dần (đáy -> đỉnh): đỉnh là phần tử nhỏ.

 Bước i=0: stack []  -> đẩy 0       stack: [0]      (giá trị 2)
 Bước i=1: nums[1]=1 < 2 -> đẩy 1   stack: [0,1]    (2,1)
 Bước i=2: nums[2]=4 > 1 -> pop 1,  result[1]=4
           nums[2]=4 > 2 -> pop 0,  result[0]=4
           đẩy 2                    stack: [2]       (4)
 Bước i=3: nums[3]=3 < 4 -> đẩy 3   stack: [2,3]
 Xong: các phần tử còn lại trong stack không có phần tử lớn hơn -> -1
```

```
 2  1  4  3
 |  |  |  |
 |  |  |  -1
 |  |  4
 |  4
 4
```

## Độ phức tạp

- **Thời gian:** O(n) — mỗi phần tử đẩy một lần, pop một lần
- **Bộ nhớ:** O(n) — ngăn xếp

## Mẫu code (phần tử lớn hơn kế tiếp)

```python
result = [-1] * len(nums)
stack = []                     # chỉ số, giá trị giảm dần
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:   # x lớn hơn đỉnh stack
        result[stack.pop()] = x
    stack.append(i)
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Daily Temperatures | `daily_temperatures.py` | ngày ấm hơn kế tiếp = chỉ số lớn hơn kế tiếp |
| Largest Rectangle in Histogram | `largest_rectangle_histogram.py` | nhỏ hơn gần nhất trái & phải |
| Trapping Rain Water | `trapping_rain_water.py` | chặn bởi min(max trái, max phải) |

## Luyện tập

Thử: Next Greater Element I/II, Sum of Subarray Minimums, Remove K Digits,
Asteroid Collision.
