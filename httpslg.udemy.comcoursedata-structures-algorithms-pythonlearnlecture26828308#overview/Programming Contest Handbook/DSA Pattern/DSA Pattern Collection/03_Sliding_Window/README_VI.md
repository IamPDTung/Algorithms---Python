# SLIDING WINDOW (CỬA SỔ TRƯỢT)

## Nó là gì?

Sliding Window duy trì một **cửa sổ liên tục** (mảng con / chuỗi con) và **trượt** cạnh
phải vào trong, đồng thời co cạnh trái khi cần, để giữ một cửa sổ thỏa mãn điều kiện
của bài toán. Nó biến bài toán kiểm tra mọi mảng con một cách ngây thơ (O(n²)) thành
**một lượt duyệt O(n)**.

## Vì sao dùng?

- Các bài **mảng con / chuỗi con** thường tìm dài nhất / ngắn nhất / đếm số cửa sổ.
- Tính lại từ đầu từng cửa sổ là lãng phí — mỗi bước trượt chỉ thêm/bớt **một phần tử**,
  trạng thái cửa sổ được **cập nhật tăng dần**.
- Hai kiểu: **cửa sổ cố định** và **cửa sổ biến đổi**.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Kiểu |
|---|---|
| "Chuỗi/mảng con dài nhất ..." | cửa sổ biến đổi (nới, rồi co) |
| "Chuỗi con ngắn nhất ... chứa ..." | cửa sổ biến đổi |
| "... có kích thước k ..." | cửa sổ cố định |
| "Tối đa / tối thiểu k ..." | cửa sổ biến đổi |
| Đoạn liên tục | cửa sổ (không phải dãy con!) |

## Minh họa — cửa sổ biến đổi (chuỗi con dài nhất không lặp ký tự)

```
 s = "a b c a b c b b"        cửa sổ chứa: a b c
        L R                   dài nhất = 3

 "a b c a" -> trùng 'a', co trái
        L   R
  L vượt qua 'a' đầu: "b c a"   dài nhất vẫn 3

 "b c a b" -> trùng 'b', co trái -> "c a b"
                L R

 ...tiếp tục trượt; dài nhất = 3. Đáp án: 3
```

Cửa sổ = đoạn giữa `L` (trái) và `R` (phải). Mỗi bước thêm `R` và có thể bỏ bớt từ `L`:

```
 Cửa sổ cố định k = 3, mảng [2, 1, 5, 1, 3, 2]
 tổng lớn nhất:
  [2 1 5] -> 8
   [1 5 1] -> 7
    [5 1 3] -> 9   <-- max
     [1 3 2] -> 6

  trượt: cộng phải mới, trừ trái cũ
  sum += nums[right] - nums[right - k]
```

## Độ phức tạp

- **Thời gian:** O(n) — mỗi phần tử vào một lần, ra một lần
- **Bộ nhớ:** O(k) hoặc O(|bảng chữ cái|) tùy cửa sổ lưu gì

## Mẫu code (cửa sổ biến đổi)

```python
left = 0
best = 0
window_state = {}          # hoặc cấu trúc đếm
for right in range(len(s)):
    thêm s[right] vào window_state
    while cửa sổ không hợp lệ:   # co từ bên trái
        bỏ s[left] khỏi window_state
        left += 1
    best = max(best, right - left + 1)
return best
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Longest Substring Without Repeating | `longest_substring_without_repeating.py` | set ký tự trong cửa sổ |
| Minimum Window Substring | `minimum_window_substring.py` | đếm + bộ đếm nhu cầu |
| Maximum Average Subarray | `maximum_average_subarray.py` | cửa sổ cố định kích thước k |

## Luyện tập

Thử: Permutation in String, Longest Repeating Character Replacement, Fruit Into Baskets,
Maximum Sum of Distinct Subarrays With Length K.
