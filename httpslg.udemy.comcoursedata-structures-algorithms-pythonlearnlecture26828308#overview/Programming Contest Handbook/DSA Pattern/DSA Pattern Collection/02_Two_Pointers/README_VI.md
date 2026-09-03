# TWO POINTERS (HAI CON TRỎ)

## Nó là gì?

Two Pointers dùng **hai chỉ số (con trỏ)** di chuyển qua cấu trúc dữ liệu — thường là
mảng — từ hai đầu hoặc với tốc độ khác nhau, để giải bài toán trong **một lượt duyệt**.
Thay vì vòng lặp lồng nhau (O(n²)), mỗi phần tử chỉ được chạm vài lần.

## Vì sao dùng?

- Biến **vòng lặp lồng O(n²) thành O(n)**.
- **Không tốn thêm bộ nhớ** — xử lý tại chỗ, O(1) không gian.
- Phù hợp tự nhiên với **mảng đã sắp xếp** khi hướng di chuyển có ý nghĩa.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| Mảng **đã sắp xếp** | di chuyển trái/phải dựa trên so sánh tổng |
| "Tìm cặp / bộ ba" | tổng quá lớn → lùi phải, quá nhỏ → tiến trái |
| "Xóa trùng tại chỗ" | con trỏ chậm giữ vị trí |
| "Đảo ngược / palindrome" | so sánh từ hai đầu |
| Yêu cầu O(1) không gian | không được dùng bảng băm |

## Hai kiểu con trỏ

**1) Hai đầu ngược chiều (squeeze)**

```
 nums = [-4, -1, 0, 1, 2, 5]   tổng cần tìm = 3
        ┌───────────────────────────────┐
 left = 0                          right = n-1

 sum = -4 + 5 = 1  < 3   -> quá nhỏ, tiến trái  →
 sum = -1 + 5 = 4  > 3   -> quá lớn, lùi phải ←
 sum = -1 + 2 = 1  < 3   -> quá nhỏ, tiến trái  →
 sum =  0 + 2 = 2  < 3   -> quá nhỏ, tiến trái  →
 sum =  1 + 2 = 3  == 3  -> TÌM THẤY (chỉ số 3, 5)
```

**2) Cùng chiều (chậm & nhanh)**

```
 Xóa trùng:  nums = [0, 0, 1, 1, 1, 2, 2, 3]
                           s
                           f
   nums[f] != nums[s]  -> s++, chép nums[s] = nums[f]
 kết quả: [0, 1, 2, 3]
```

**3) Kiểm tra palindrome (so sánh hai đầu)**

```
 "racecar"
  l →             ← r
  r == r, a == a, c == c ... -> là palindrome
```

## Độ phức tạp

- **Thời gian:** O(n) — mỗi con trỏ di chuyển tối đa n lần
- **Bộ nhớ:** O(1)

## Mẫu code (hai đầu ngược chiều)

```python
left, right = 0, len(arr) - 1
while left < right:
    if condition(arr[left], arr[right]):
        right -= 1        # cần nhỏ hơn
    elif condition(arr[left], arr[right]):
        left += 1         # cần lớn hơn
    else:
        break             # đã tìm thấy
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| 3Sum | `three_sum.py` | sắp xếp + cố định 1 số, hai con trỏ cho phần còn lại |
| Container With Most Water | `container_with_most_water.py` | di chuyển bức tường ngắn hơn vào trong |
| Valid Palindrome | `valid_palindrome.py` | so sánh từ hai đầu |

## Luyện tập

Thử: Remove Duplicates from Sorted Array, Trapping Rain Water, Two Sum II, Sort Colors.
