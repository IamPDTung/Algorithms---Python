# BACKTRACKING (QUAY LUI)

## Nó là gì?

Backtracking là cách **sinh ra toàn bộ khả năng một cách có hệ thống** bằng cách xây dựng
lời giải từng phần một. Ở mỗi bước ta **chọn** một phương án, **khám phá** hậu quả bằng
đệ quy, rồi **bỏ chọn (quay lui)** để thử phương án tiếp theo. Về bản chất nó là DFS trên
**cây quyết định**, có cắt tỉa khi lời giải từng phần vi phạm ràng buộc.

**Mẫu: Choose → Explore → Unchoose (Chọn → Khám phá → Bỏ chọn)**

## Vì sao dùng?

- Khi đáp án là **toàn bộ tổ hợp / hoán vị / tập con / cấu hình** và vét cạn (vòng lặp lồng)
  không thích nghi được với độ sâu thay đổi.
- Tự nhiên cho bài **ràng buộc**: Sudoku, N-Queens, ô chữ, so khớp kiểu regex.
- Ngăn xếp đệ quy cho cơ chế "hoàn tác" thanh lịch để dựng đường đi.

## Khi nào dùng?

| Dấu hiệu trong đề bài | Vì sao |
|---|---|
| "Sinh tất cả / tìm tất cả ..." | liệt kê mọi khả năng |
| "Tổ hợp / hoán vị / tập con" | chọn từ các phần tử còn lại |
| "Thỏa mãn ràng buộc" | cắt tỉa lời giải từng phần sai |
| "Khám phá lưới / bàn cờ" | đặt & kiểm tra (N-Queens, Sudoku) |

## Minh họa — tập con của [1, 2]

```
                  []                       (bắt đầu: tập rỗng)
        chọn 1          bỏ 1
          /                    \
        [1]                    []
        /  \                  /  \
 chọn 2   bỏ 2          chọn 2   bỏ 2
      /        \            /        \
   [1,2]      [1]        [2]         []

 Tất cả 4 tập con: [], [1], [2], [1,2]
 Cây đệ quy có 2^n lá.
```

## Minh họa — N-Queens (4x4), đặt hậu theo từng hàng

```
 Q . . .     Q . . .     . Q . .     . Q . .
 . . Q .     . . . Q     Q . . .     . . . Q
 . . . Q     Q . . .     . . Q .     Q . . .
 . Q . .     . Q . .     . . . Q     . . Q .

 (4 lời giải hợp lệ cho 4-Hậu; mỗi hậu kiểm tra cột + hai đường chéo)
```

## Độ phức tạp

- **Thời gian:** mũ — O(2^n) tập con, O(n!) hoán vị (cắt tỉa giúp ích rất nhiều)
- **Bộ nhớ:** O(n) ngăn xếp đệ quy

## Mẫu code

```python
def backtrack(path, choices):
    if is_solution(path):
        thêm bản sao path vào result
        return
    for option in choices:
        if valid(path, option):
            path.append(option)          # chọn
            backtrack(path, choices_mới)  # khám phá
            path.pop()                   # bỏ chọn (quay lui)
```

## Bài tập mẫu trong thư mục này

| Bài toán | File | Ý tưởng |
|---|---|---|
| Subsets | `subsets.py` | chọn / bỏ từng phần tử |
| Combination Sum | `combination_sum.py` | dùng lại không giới hạn, thứ tự tăng dần |
| N-Queens | `n_queens.py` | đặt theo hàng, kiểm tra xung đột |

## Luyện tập

Thử: Sudoku Solver, Permutations, Letter Combinations of a Phone Number,
Word Search, Palindrome Partitioning.
