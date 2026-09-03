# GREEDY (THAM LAM)

## Nó là gì?

Thuật toán Greedy đưa ra **lựa chọn cục bộ tốt nhất tại mỗi bước**, hy vọng chuỗi các tối
ưu cục bộ tạo ra **tối ưu toàn cục**. Không quay lui, không xem xét lại — quyết định một
lần rồi đi tiếp. Nó chỉ đúng khi bài toán có **tính chất lựa chọn tham lam** (lựa chọn tốt
nhất cục bộ luôn an toàn) và **cấu trúc con tối ưu**.

## Vì sao dùng?

- **Đơn giản và nhanh** — O(n log n) hoặc O(n).
- **Ít / không tốn thêm bộ nhớ**.
- Dễ lý luận khi lựa chọn tham lam được chứng minh an toàn.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Lựa chọn tham lam |
|---|---|
| "Sắp xếp giúp ích / khoảng" | sắp theo start/end, trộn tham lam |
| "Nhảy / đến đích" | luôn nhảy xa nhất có thể |
| "Lập lịch min/max tác vụ" | sắp theo hạn chót / tần suất |
| "Luôn cải thiện bằng cách chọn tốt nhất kế tiếp?" | lựa chọn cục bộ an toàn |
| DP cũng chạy nhưng greedy đơn giản hơn | dùng greedy khi hợp lệ |

## Minh họa — jump game

```
 nums = [2, 3, 1, 1, 4]
 index: 0   1   2   3   4

 Tại index 0, max reach = 0 + 2 = 2
 Tại index 1, max reach = max(2, 1 + 3) = 4  -> có thể tới đích!

 Greedy: theo dõi chỉ số xa nhất tới được; nếu i > farthest, kẹt -> False
```

## Minh họa — merge intervals

```
 intervals: [1,3] [2,6] [8,10] [15,18]
 sau khi sắp theo start: [1,3] [2,6] [8,10] [15,18]

 [1,3] rồi [2,6]: 2 <= 3 -> trộn -> [1,6]
 [1,6] rồi [8,10]: 8 > 6 -> khoảng mới -> [8,10]
 [8,10] rồi [15,18]: 15 > 10 -> mới -> [15,18]

 kết quả: [[1,6], [8,10], [15,18]]
```

## Độ phức tạp

- **Thời gian:** O(n log n) nếu cần sắp xếp, ngược lại O(n)
- **Bộ nhớ:** O(1) hoặc O(n) cho kết quả

## Mẫu code

```python
def greedy(items):
    items.sort(key=...)                 # sắp xếp thường mở đường cho greedy
    result = khởi_tạo
    for item in items:
        if nên_lấy(item):
            lấy nó / cập nhật result    # lựa chọn cục bộ tốt nhất
    return result
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Jump Game | `jump_game.py` | theo dõi phạm vi xa nhất |
| Gas Station | `gas_station.py` | một lượt, khởi động lại khi thiếu xăng |
| Merge Intervals | `merge_intervals.py` | sắp + trộn khoảng chồng lấn |

## Luyện tập

Thử: Task Scheduler (greedy + đếm), Non-overlapping Intervals, Candy,
Jump Game II, Interval Scheduling, Meeting Rooms II.
