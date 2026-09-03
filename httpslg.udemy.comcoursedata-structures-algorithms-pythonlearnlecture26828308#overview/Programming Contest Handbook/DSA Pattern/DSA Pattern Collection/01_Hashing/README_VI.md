# HASHING (BĂM DỮ LIỆU)

## Nó là gì?

Hashing là kỹ thuật ánh xạ **khóa (key)** sang **giá trị (value)** bằng một **hàm băm
(hash function)**, lưu trữ chúng trong một **bảng băm** (từ điển `dict` trong Python).
Hàm băm tính ra chỉ số (index) từ khóa, cho phép truy cập với độ phức tạp **O(1) trung
bình** — chèn, tra cứu và xóa đều rất nhanh.

Cấu trúc dữ liệu trong Python:
- `dict` (HashMap) — cặp khóa → giá trị
- `set` (HashSet) — chỉ chứa các khóa duy nhất

## Vì sao dùng?

- **Tra cứu / kiểm tra tồn tại nhanh** — kiểm tra phần tử có tồn tại trong O(1).
- **Đếm tần suất** — đếm mỗi phần tử xuất hiện bao nhiêu lần.
- **Phát hiện trùng lặp** — theo dõi những gì đã gặp.
- **Bài toán cặp / bù trừ** — tìm `b` sao cho `a + b = target` bằng cách dùng `target - a`.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Tìm xem phần tử có tồn tại" | kiểm tra thành viên O(1) bằng `set` |
| "Đếm tần suất phần tử" | `dict` với value = số lần đếm |
| "Tìm phần tử trùng" | `set` các phần tử đã thấy |
| "Tìm cặp có tổng bằng target" | lưu phần bù trong `dict` |
| "Gom nhóm theo khóa" | `dict` khóa → danh sách |

## Cách hoạt động (minh họa)

Hàm băm `h(k) = k % 7` ánh xạ các khóa vào bucket:

```
 Keys                 Bảng băm (mảng các bucket)
 ─────                ─────────────────────────────────
  42 ── h(42) ──► 0: [42]
  15 ── h(15) ──► 1: [15]
  29 ── h(29) ──► 2: []      <-- 29 % 7 = 1 à? Không...
  34 ── h(34) ──► 3: [34]

 Nhưng 29 % 7 = 1, trùng với 15!  -> XUNG ĐỘT (chaining)
 ─────────────────────────────────────────────────────
  15 ──► 1: [15] -> [29]      (danh sách liên kết, chaining)

 Tra cứu 29: tính h(29) = 1, dò bucket 1 -> tìm thấy O(1 + len)
```

Two Sum — ý tưởng cặp kinh điển:

```
 nums = [2, 7, 11, 15],  target = 9

 bước 1: x = 2  -> cần 9 - 2 = 7  (chưa thấy, lưu {2: 0})
 bước 2: x = 7  -> cần 9 - 7 = 2  (ĐÃ THẤY ở index 0!) -> đáp án (0, 1)

 seen = { 2:0, 7:1, 11:2, 15:3 }
```

## Độ phức tạp

- **Thời gian:** O(1) trung bình mỗi thao tác (tệ nhất O(n) khi xung đột, hiếm gặp)
- **Bộ nhớ:** O(n) cho bảng

## Mẫu code

```python
# 1) Đếm tần suất
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1

# 2) Trùng lặp / phần bù
seen = set()          # hoặc dict {value: index}
for x in nums:
    complement = target - x
    if complement in seen:
        return ...    # đã tìm thấy cặp
    seen.add(x)
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Two Sum | `two_sum.py` | lưu phần bù vào dict |
| Group Anagrams | `group_anagrams.py` | từ đã sắp xếp làm khóa |
| Longest Consecutive Sequence | `longest_consecutive_sequence.py` | `set` + kiểm tra phần tử bên trái |

## Luyện tập

Thử: Top K Frequent Elements, Contains Duplicate, Valid Anagram, Intersection of Two Arrays.
