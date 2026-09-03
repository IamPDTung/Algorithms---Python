# HEAP (HÀNG ĐỢI ƯU TIÊN)

## Nó là gì?

Heap là một **cây nhị phân đầy đủ** trong đó mọi nút cha ≤ (min-heap) hoặc ≥ (max-heap)
các nút con. `heapq` của Python triển khai **min-heap**. Phần tử nhỏ nhất luôn nằm ở gốc
và có thể lấy ra trong **O(log n)**; chèn cũng mất **O(log n)**.

Lưu ý: `heapq` chỉ là min-heap — để có max-heap, hãy lưu **giá trị âm**.

## Vì sao dùng?

- Ta chỉ quan tâm tới **k phần tử nhỏ nhất / lớn nhất**, không cần thứ tự đầy đủ.
- Duy trì cấu trúc "luôn sắp xếp ở đỉnh" dưới các thao tác **chèn và xóa** — lý tưởng cho
  dữ liệu **dòng / động**.
- Giải quyết **Top K**, **Kth lớn/nhỏ nhất**, **merge k danh sách đã sắp**, **median động**.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Top K thường xuyên / lớn / nhỏ" | pop k phần tử từ heap |
| "Kth lớn nhất / nhỏ nhất" | min-heap kích thước k |
| "Merge k danh sách đã sắp xếp" | đẩy đầu danh sách, mỗi lần pop phần tử nhỏ nhất |
| "Median động / median trong luồng" | hai heap (max + min) |
| "Phần tử nhỏ nhất / rẻ nhất mỗi bước" | greedy + heap |

## Minh họa — min-heap và dạng mảng

```
           1
         /   \
       3      2
      / \    / \
     6   5  7   4

 mảng (heapq): [1, 3, 2, 6, 5, 7, 4]
 index:         [0, 1, 2, 3, 4, 5, 6]
 con của i:     2i+1, 2i+2
 cha của i:     (i-1)//2
```

Hai heap cho median động:

```
 các số đã có: 5, 15, 1, 3
 max-heap (trái) | min-heap (phải)
   [5]           | [15]
   [1,5]         | [15]     sau 1
   [1,3,5]  <--> [15]       -> cân bằng: chuyển 5 sang
   [1,3]         | [5,15]
 median = (max(trái) + min(phải)) / 2 = (3 + 5) / 2 = 4
```

## Độ phức tạp

- **Thời gian:** O(log n) mỗi push / pop; O(1) để xem phần tử nhỏ nhất
- **Bộ nhớ:** O(n)

## Mẫu code

```python
import heapq

heap = []                       # min-heap
heapq.heappush(heap, x)
smallest = heapq.heappop(heap)
top = heap[0]

# mẹo max-heap:
heapq.heappush(heap, -x)        # lưu giá trị âm
largest = -heapq.heappop(heap)

# Kth lớn nhất: giữ heap kích thước k
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Kth Largest Element in Array | `kth_largest_element.py` | min-heap kích thước k |
| Merge K Sorted Lists | `merge_k_sorted_lists.py` | heap chứa các đầu danh sách |
| Find Median from Data Stream | `find_median_from_data_stream.py` | hai heap |

## Luyện tập

Thử: Top K Frequent Elements, K Closest Points to Origin, Task Scheduler,
Kth Smallest Element in a Sorted Matrix.
