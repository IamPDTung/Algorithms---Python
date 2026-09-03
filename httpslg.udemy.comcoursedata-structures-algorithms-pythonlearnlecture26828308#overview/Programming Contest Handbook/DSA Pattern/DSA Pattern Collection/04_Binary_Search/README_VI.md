# BINARY SEARCH (TÌM KIẾM NHỊ PHÂN)

## Nó là gì?

Binary Search tìm một mục tiêu trong tập dữ liệu **đã sắp xếp** bằng cách liên tục
**loại bỏ một nửa** không gian tìm kiếm. Nó so sánh mục tiêu với phần tử ở giữa và quyết
định giữ lại nửa nào. Điều này cho độ phức tạp **O(log n)** — mỗi bước giảm một nửa bài toán.

Hai kiểu:
1. **Tìm kiếm cổ điển** — mục tiêu có trong mảng đã sắp xếp.
2. **Tìm đáp án trên vị từ đơn điệu** — "tìm x nhỏ nhất/lớn nhất sao cho f(x) đúng".

## Vì sao dùng?

- **O(log n)** vượt trội so với quét O(n) trên dữ liệu lớn (n = 1.000.000 → ~20 bước).
- Dùng được mỗi khi bạn có thể hỏi "có loại bỏ được một nửa không?".
- **Không gian tìm kiếm nằm trên giá trị đáp án** (như "tốc độ tối thiểu", "số ngày tối thiểu")
  — kể cả khi mảng không sắp xếp, miễn là hàm khả thi đơn điệu.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Mảng đã sắp xếp" | loại bỏ nửa cổ điển |
| "Tìm min/max đáp án" | tìm kiếm nhị phân trên đáp án |
| "Tính chất đơn điệu / không giảm" | vị từ đúng rồi sai (hoặc ngược lại) |
| "Có loại bỏ được một nửa không?" | đảm bảo mỗi bước loại bỏ nửa còn lại |
| Ràng buộc lớn | O(n) quá chậm, cần O(log n) |

## Minh họa — tìm kiếm 23 trong mảng đã sắp xếp

```
 index:  0   1   2   3   4   5   6
 value:  3   7   9  15  23  30  42
        lo              mid          hi
                       (15)

 15 < 23  -> tìm NỬA PHẢI: loại bỏ [0..3]
                  lo      mid    hi
                 (23)        (42)
         index 4..6, mid=5 (30)
 30 > 23  -> tìm NỬA TRÁI: loại bỏ [5..6]
            lo=4 hi=4 mid=4 (23)  -> TÌM THẤY!

 7 phần tử -> tìm thấy sau 3 lần so sánh
```

## Minh họa — tìm kiếm nhị phân trên đáp án (Koko ăn chuối)

```
 piles = [3, 6, 7, 11], h = 8.  Tốc độ có thể 1..11.
 f(speed) = "ăn xong trong <= 8 giờ"  (đơn điệu: nhanh hơn => dễ hơn)

 speed: 1  2  3  4 ... 11
 f:     F  F  T  T ...  T        <-- tìm True ĐẦU TIÊN

 lo=1, hi=11
 mid=6 -> f(6)=True  -> hi=6 (có thể nhỏ hơn vẫn chạy)
 mid=3 -> f(3)=True  -> hi=3
 mid=2 -> f(2)=False -> lo=3
 đáp án = 3  (tốc độ tối thiểu chạy được)
```

## Độ phức tạp

- **Thời gian:** O(log n)
- **Bộ nhớ:** O(1)

## Mẫu code (tìm đáp án)

```python
def feasible(x):   # vị từ đơn điệu
    ...

lo, hi = 0, MAX      # phạm vi tìm kiếm
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        hi = mid     # mid chạy được, thử nhỏ hơn (cho "True đầu tiên")
    else:
        lo = mid + 1
return lo
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Search in Rotated Sorted Array | `search_rotated_sorted_array.py` | tìm pivot hoặc rẽ theo nửa đã sắp |
| Koko Eating Bananas | `koko_eating_bananas.py` | tìm nhị phân tốc độ |
| Find Peak Element | `find_peak_element.py` | di chuyển về phía hàng xóm cao hơn |

## Luyện tập

Thử: Median of Two Sorted Arrays, Search Insert Position, First Bad Version,
Minimum in Rotated Sorted Array, Split Array Largest Sum.
