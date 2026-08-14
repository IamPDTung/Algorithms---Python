
---

# Quy Hoạch Động (Dynamic Programming)

## 1. Quy Hoạch Động là gì?

**Quy hoạch động (Dynamic Programming - DP)** là một kỹ thuật tối ưu hóa dùng để giải các bài toán phức tạp bằng cách chia nhỏ chúng thành các **bài toán con (subproblems)**, giải mỗi bài toán con **chỉ một lần duy nhất**, và **lưu trữ** kết quả để tái sử dụng sau này.

Về bản chất, đây là sự tối ưu hóa so với **đệ quy thuần túy**. Bất cứ khi nào ta thấy một lồi giải đệ quy lặp đi lặp lại việc gọi hàm với cùng một đầu vào, ta có thể tối ưu nó bằng Quy hoạch động.

### Ý tưởng cốt lõi:
> "Những kẻ không thể ghi nhớ quá khứ sẽ bị lên án phải lặp lại nó."
> — Quy hoạch động ghi nhớ quá khứ (lưu trữ đáp án) để không bao giờ phải giải lại cùng một bài toán hai lần.

### Hai điều kiện bắt buộc:
Một bài toán chỉ có thể giải bằng Quy hoạch động khi nó có **CẢ HAI** tính chất sau:

1. **Bài toán con chồng lặp (Overlapping Subproblems)** — cùng một bài toán con bị giải đi giải lại nhiều lần.
2. **Cấu trúc con tối ưu (Optimal Substructure)** — lồi giải tối ưu của bài toán lớn có thể được xây dựng từ lồi giải tối ưu của các bài toán con.

### Quy hoạch động được dùng ở đâu?
* Dãy Fibonacci
* Bài toán đường đi ngắn nhất (ví dụ: Google Maps)
* Bài toán cái túi (Knapsack)
* Dãy con chung dài nhất (LCS - Longest Common Subsequence)
* Bài toán đổi tiền xu (Coin Change)

```
        +--------------------------------------------------+
        |          QUY HOẠCH ĐỘNG (DYNAMIC PROGRAMMING)    |
        +--------------------------------------------------+
        |                                                  |
        |   Điều kiện 1            Điều kiện 2             |
        |   +------------------+   +--------------------+  |
        |   |  BÀI TOÁN CON    |   |   CẤU TRÚC CON     |  |
        |   |   CHỒNG LẶP      | + |     TỐI ƯU         |  |
        |   +------------------+   +--------------------+  |
        |                                                  |
        |   Hai cách cài đặt:                              |
        |   +------------------+   +--------------------+  |
        |   |    GHI NHỚ       |   |    TỪ DƯỚI LÊN     |  |
        |   |  (Memoization)   |   |   (Bottom-Up)      |  |
        |   |  Từ trên xuống   |   |   (Lập bảng)       |  |
        |   +------------------+   +--------------------+  |
        +--------------------------------------------------+
```

---

## 2. Bài toán con chồng lặp (Overlapping Subproblems)

Một bài toán có **Bài toán con chồng lặp** nếu quá trình tìm lồi giải phải giải **cùng một bài toán con nhiều lần**.

### Ví dụ: Cây đệ quy của Fibonacci

Hãy xem điều gì xảy ra khi ta tính `fib(5)` bằng đệ quy thuần túy:

```
                            fib(5)
                           /      \
                    fib(4)          fib(3)
                   /     \          /    \
              fib(3)    fib(2)  fib(2)  fib(1)
              /   \     /    \   /   \
         fib(2) fib(1) .................
          /  \
     fib(1) fib(0)
```

### Đếm số lần tính toán bị lặp lại:

```
    fib(5)  ->  được tính 1 lần
    fib(4)  ->  được tính 1 lần
    fib(3)  ->  được tính 2 lần   <== BỊ LẶP LẠI!
    fib(2)  ->  được tính 3 lần   <== BỊ LẶP LẠI!
    fib(1)  ->  được tính 5 lần   <== BỊ LẶP LẠI!
    fib(0)  ->  được tính 3 lần   <== BỊ LẶP LẠI!
```

Cây con `fib(3)` bị tính **hai lần**, `fib(2)` bị tính **ba lần**... Khi `n` tăng lên, khối lượng công việc lặp lại này bùng nổ theo **hàm mũ** — độ phức tạp `O(2^n)`!

```
    n = 5    ->   khoảng 15 lờ gọi hàm
    n = 10   ->   khoảng 177 lờ gọi hàm
    n = 20   ->   khoảng 21.000 lờ gọi hàm
    n = 50   ->   khoảng 20 TỶ lờ gọi hàm  (quá chậm!)
```

### Ý tưởng then chốt của DP:
> Tại sao phải tính lại `fib(3)` lần thứ hai? Ta đã biết đáp án rồi!
> **Giải mỗi bài toán con MỘT LẦN, lưu lại đáp án, và tra cứu nó vào lần sau.**

```
    +-------------------+        +------------------------+
    |  KHÔNG DÙNG DP    |        |  DÙNG DP               |
    +-------------------+        +------------------------+
    | fib(3) -> tính    |        | fib(3) -> tính,        |
    | fib(3) -> tính    |   =>   |           LƯU kết quả  |
    | fib(3) -> tính    |        | fib(3) -> TRA CỨU (O(1))|
    | fib(3) -> tính    |        | fib(3) -> TRA CỨU (O(1))|
    +-------------------+        +------------------------+
       Thờ gian O(2^n)              Thờ gian O(n)
```

---

## 3. Cấu trúc con tối ưu (Optimal Substructure)

Một bài toán có **Cấu trúc con tối ưu** nếu **lồi giải tối ưu** của bài toán có thể được xây dựng từ **lồi giải tối ưu của các bài toán con**.

### Ví dụ: Fibonacci

```
    fib(5) = fib(4) + fib(3)
      |         |        |
      |         |        +-- đáp án đúng cho bài toán con 3
      |         +----------- đáp án đúng cho bài toán con 4
      +--------------------- đáp án đúng cho bài toán 5
```

Đáp án đúng (tối ưu) của `fib(5)` được **xây dựng trực tiếp** từ đáp án đúng của `fib(4)` và `fib(3)`. Không cần thêm thông tin nào khác.

### Ví dụ thực tế: Đường đi ngắn nhất

```
    Nếu đường đi ngắn nhất từ A đến D đi qua B:

        A --------> B --------> C --------> D
         \_________ Đường đi ngắn nhất _________/

    Thì:  Ngắn nhất(A, D) = Ngắn nhất(A, B) + Ngắn nhất(B, D)

    Đường đi ngắn nhất A->D CHỨA đường đi ngắn nhất của
    các bài toán con (A->B và B->D).
```

### Phản ví dụ (KHÔNG có cấu trúc con tối ưu):
Bài toán **Đường đi dài nhất** KHÔNG có cấu trúc con tối ưu — đường đi dài nhất từ A đến D không nhất thiết được tạo thành từ các đường đi dài nhất giữa các đỉnh trung gian (vì có thể tạo ra chu trình). Do đó **không thể** áp dụng DP cho bài toán này.

### Tóm tắt:

```
    +----------------------------------------------------------+
    |  BẢNG KIỂM TRA CẤU TRÚC CON TỐI ƯU                       |
    +----------------------------------------------------------+
    |  Tôi có thể chia bài toán thành các bài toán con?   CÓ   |
    |  Tôi có thể xây dựng lờ giải tối ưu từ lờ giải           |
    |  tối ưu của các bài toán con không?                 CÓ   |
    |                                                          |
    |  => Có thể dùng Quy hoạch động!                          |
    +----------------------------------------------------------+
```

---

## 4. Dãy Fibonacci (Fibonacci Sequence)

**Dãy Fibonacci** là ví dụ "Hello World" kinh điển của Quy hoạch động. Mỗi số là **tổng của hai số liền trước nó**.

```
    Chỉ số:  0    1    2    3    4    5    6    7
             |    |    |    |    |    |    |    |
    Giá trị: 0    1    1    2    3    5    8    13
                          \___|___/
                              |
                    fib(4) = fib(3) + fib(2)
                           =   2    +   1
                           =   3
```

### Định nghĩa đệ quy:

```
                    |  0                       nếu n = 0
    fib(n) =        |  1                       nếu n = 1
                    |  fib(n-1) + fib(n-2)     nếu n > 1
```

### Lồi giải đệ quy ngây thơ (Naive Recursion):

```python
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)
```

### Vấn đề — Thờ gian hàm mũ `O(2^n)`:

Mỗi lờ gọi hàm tách thành **hai** lờ gọi khác, tạo ra một cây tăng trưởng theo hàm mũ:

```
    Tầng 0:                      fib(n)                     1 lờ gọi
                                /        \
    Tầng 1:              fib(n-1)        fib(n-2)           2 lờ gọi
                        /       \        /       \
    Tầng 2:         fib(n-2) fib(n-3) fib(n-3) fib(n-4)     4 lờ gọi
                    ...              ...                    8 lờ gọi
                                                                 |
    Cây NHÂN ĐÔI ở mỗi tầng  =>  O(2^n)  <=  BÙNG NỔ!           v
```

### Phân tích Big O (Đệ quy ngây thơ):

| Độ phức tạp | Giá trị | Lý do |
|:---|:---|:---|
| **Thờ gian** | `O(2^n)` | Mỗi lờ gọi tạo ra 2 lờ gọi nữa; cây có khoảng 2^n nút |
| **Không gian** | `O(n)` | Ngăn xếp đệ quy (call stack) sâu `n` tầng |

> Với `n = 50`, đó là khoảng **2^50 = 1 triệu tỷ phép tính**. Máy tính của bạn sẽ cần hàng năm trờ. Đây chính xác là lý do ta cần Quy hoạch động.

---

## 5. Ghi nhớ - Memoization (Từ trên xuống / Top-Down)

**Memoization** là cách tiếp cận **Từ trên xuống (Top-Down)** của Quy hoạch động:
* Bắt đầu từ **đỉnh** (bài toán gốc, `fib(n)`)
* Đệ quy đi **xuống** đến các trường hợp cơ sở (base cases)
* **Lưu trữ (cache)** mọi kết quả vào một bảng ngay lần đầu tiên nó được tính
* Trước khi tính bất cứ thứ gì, **kiểm tra bảng trước**

> **Memoization = Đệ quy + Bộ nhớ đệm (Cache)**

### Minh họa — Bảng ghi nhớ hoạt động thế nào:

```
    Tính fib(5) bằng memoization:

    Bước 1: fib(5) -> chưa có trong memo, cần fib(4) + fib(3)
    Bước 2: fib(4) -> chưa có trong memo, cần fib(3) + fib(2)
    Bước 3: fib(3) -> chưa có trong memo, cần fib(2) + fib(1)
    Bước 4: fib(2) -> chưa có trong memo, cần fib(1) + fib(0)
    Bước 5: fib(1) -> TRƯỜNG HỢP CƠ SỞ, trả về 1
    Bước 6: fib(0) -> TRƯỜNG HỢP CƠ SỞ, trả về 0
    Bước 7: fib(2) = 1 + 0 = 1  ->  LƯU memo[2] = 1
    Bước 8: fib(3) = 1 + 1 = 2  ->  LƯU memo[3] = 2
    Bước 9: fib(4) -> fib(3) ĐÃ CÓ TRONG MEMO! Chỉ cần tra cứu (2)
            fib(4) = 2 + 1 = 3  ->  LƯU memo[4] = 3
    Bước 10: fib(5) -> fib(3) ĐÃ CÓ TRONG MEMO! Chỉ cần tra cứu (2)
             fib(5) = 3 + 2 = 5 ->  LƯU memo[5] = 5
```

### Cây đệ quy sau khi được cắt tỉa:

```
                            fib(5)
                           /      \
                    fib(4)          [fib(3)] -----> TRA CỨU TRONG MEMO (O(1))
                   /     \                ^
              fib(3)    [fib(2)] ---------+---> TRA CỨU TRONG MEMO (O(1))
              /   \           ^
         fib(2)  [fib(1)] ----+---> TRA CỨU TRONG MEMO (O(1))
          /  \
     fib(1) fib(0)     <--- TRƯỜNG HỢP CƠ SỞ

    [trong khung] = không bao giờ bị tính lại, chỉ là một phép tra cứu!
```

Chỉ có **nhánh ngoài cùng bên trái** của cây thực sự được tính toán. Mọi thứ khác chỉ là tra cứu. **Mỗi giá trị `fib(k)` chỉ được tính đúng MỘT LẦN.**

### Code:

```python
memo = [None] * 100

def fib_memo(n):
    # Đã tính rồi? Chỉ cần tra cứu! O(1)
    if memo[n] is not None:
        return memo[n]

    # Trường hợp cơ sở
    if n == 0 or n == 1:
        return n

    # Tính MỘT LẦN, rồ LƯU vào bảng memo
    memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]
```

### Bảng memo (sau khi tính fib(5)):

```
    Chỉ số:   0     1     2     3     4     5
            +-----+-----+-----+-----+-----+-----+
    memo:   |  -  |  -  |  1  |  2  |  3  |  5  |
            +-----+-----+-----+-----+-----+-----+
                              ^
                  Mỗi ô được điền ĐÚNG MỘT LẦN
                  => n phép tính thay vì 2^n
```

### Phân tích Big O (Memoization):

| Độ phức tạp | Trước (Ngây thơ) | Sau (Memoization) |
|:---|:---|:---|
| **Thờ gian** | `O(2^n)` | **`O(n)`** — mỗi bài toán con chỉ giải một lần |
| **Không gian** | `O(n)` | `O(n)` — bảng memo + ngăn xếp đệ quy |

---

## 6. Từ dưới lên - Bottom-Up (Lập bảng / Tabulation)

**Bottom-Up** là cách tiếp cận **lặp (iterative)** của Quy hoạch động:
* Bắt đầu từ **đáy** (các trường hợp cơ sở nhỏ nhất, `fib(0)` và `fib(1)`)
* Xây dựng **dần lên** một bảng lồi giải, từng bước một
* Dùng **vòng lặp** thay vì đệ quy — không cần ngăn xếp cuộc gọi
* Đến khi bạn cần `fib(k)`, thì `fib(k-1)` và `fib(k-2)` đã có sẵn trong bảng

> **Bottom-Up = Vòng lặp + Bảng (Table)**

### Minh họa — Xây dựng bảng từ dưới lên:

```
    MỤC TIÊU: tính fib(7)

    Bắt đầu với các trường hợp cơ sở, rồ xây dựng LÊN:

    Chỉ số:   0     1     2     3     4     5     6     7
            +-----+-----+-----+-----+-----+-----+-----+-----+
    fib:    |  0  |  1  |     |     |     |     |     |     |
            +-----+-----+-----+-----+-----+-----+-----+-----+
              ^     ^
        trường hợp  trường hợp
          cơ sở      cơ sở

    i = 2:  fib[2] = fib[1] + fib[0] = 1 + 0 = 1
    i = 3:  fib[3] = fib[2] + fib[1] = 1 + 1 = 2
    i = 4:  fib[4] = fib[3] + fib[2] = 2 + 1 = 3
    i = 5:  fib[5] = fib[4] + fib[3] = 3 + 2 = 5
    i = 6:  fib[6] = fib[5] + fib[4] = 5 + 3 = 8
    i = 7:  fib[7] = fib[6] + fib[5] = 8 + 5 = 13

    BẢNG CUỐI CÙNG:
            +-----+-----+-----+-----+-----+-----+-----+-----+
    fib:    |  0  |  1  |  1  |  2  |  3  |  5  |  8  |  13 |
            +-----+-----+-----+-----+-----+-----+-----+-----+
                                                            ^
                                                    ĐÁP ÁN: fib(7) = 13
```

### Hướng tính toán — Top-Down vs Bottom-Up:

```
    MEMOIZATION (Từ trên xuống):         BOTTOM-UP (Lập bảng):

    fib(7)  <---- BẮT ĐẦU ở đây          fib(0), fib(1)  <---- BẮT ĐẦU ở đây
       |                                        |
    fib(6)                                   fib(2)
       |                                        |
    fib(5)                                   fib(3)
       |                                        |
      ...                                     ...
       |                                        |
    fib(1)  <---- trường hợp cơ sở         fib(7)  <---- ĐÁP ÁN

    Đệ quy đào sâu XUỐNG                   Vòng lặp leo LÊN
    rồ nổi bọt ngược LÊN                   từng bước một
```

### Code:

```python
def fib_bottom_up(n):
    # Tạo bảng và gieo mầm các trường hợp cơ sở
    fib_list = [0, 1]

    # Xây dựng LÊN từ đáy đến n
    for index in range(2, n + 1):
        next_fib = fib_list[index - 1] + fib_list[index - 2]
        fib_list.append(next_fib)

    return fib_list[n]
```

### Phân tích Big O (Bottom-Up):

| Độ phức tạp | Giá trị | Lý do |
|:---|:---|:---|
| **Thờ gian** | **`O(n)`** | Một vòng lặp duy nhất từ 2 đến n |
| **Không gian** | `O(n)` | Bảng lưu trữ `n+1` giá trị |

### Nâng cao — Tối ưu không gian xuống `O(1)`:

Vì ta chỉ cần **hai giá trị gần nhất**, ta không cần cả cái bảng:

```python
def fib_optimized(n):
    if n == 0 or n == 1:
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr
```

```
    Thay vì lưu TẤT CẢ n giá trị:

    Bảng:  [0, 1, 1, 2, 3, 5, 8, 13, ...]   <- không gian O(n)

    Chỉ cần giữ một cửa sổ trượt gồm 2 phần tử:

    i=2:   prev=0, curr=1  ->  mớ = 0+1 = 1
    i=3:   prev=1, curr=1  ->  mớ = 1+1 = 2
    i=4:   prev=1, curr=2  ->  mớ = 1+2 = 3
    i=5:   prev=2, curr=3  ->  mớ = 2+3 = 5
                    \________/
                 cửa sổ trượt sang phải  <- không gian O(1)!
```

---

## 7. So sánh Memoization và Bottom-Up

```
    +-----------------------+-----------------------+-----------------------+
    |                       |    MEMOIZATION        |     BOTTOM-UP         |
    |                       |    (Từ trên xuống)    |     (Lập bảng)        |
    +-----------------------+-----------------------+-----------------------+
    | Cách tiếp cận         | Đệ quy                | Lặp (vòng lặp)        |
    +-----------------------+-----------------------+-----------------------+
    | Hướng đi              | n -> 0 (xuống)        | 0 -> n (lên)          |
    +-----------------------+-----------------------+-----------------------+
    | Nơi lưu trữ           | Dictionary / list     | List (bảng)           |
    +-----------------------+-----------------------+-----------------------+
    | Bài toán con được giải| Chỉ những bài CẦN     | TẤT CẢ bài toán con   |
    +-----------------------+-----------------------+-----------------------+
    | Rủ ro ngăn xếp        | Tràn stack nếu n      | Không có (không đệ quy)|
    |                       | quá lớn               |                       |
    +-----------------------+-----------------------+-----------------------+
    | ĐPT Thờ gian         | O(n)                  | O(n)                  |
    +-----------------------+-----------------------+-----------------------+
    | ĐPT Không gian       | O(n) (bảng + stack)   | O(n), có thể tối ưu   |
    |                       |                       | xuống O(1)            |
    +-----------------------+-----------------------+-----------------------+
```

---

## 8. Toàn bộ quá trình tiến hóa của Fibonacci

```
    +------------------------+------------+------------+--------------------+
    |      CÁCH TIẾP CẬN     |  THỜ GIAN  | KHÔNG GIAN |      KỸ THUẬT      |
    +------------------------+------------+------------+--------------------+
    | Đệ quy ngây thơ        |   O(2^n)   |    O(n)    | Chỉ đệ quy thuần   |
    +------------------------+------------+------------+--------------------+
    | Memoization            |    O(n)    |    O(n)    | Đệ quy + cache     |
    | (Từ trên xuống)        |            |            |                    |
    +------------------------+------------+------------+--------------------+
    | Bottom-Up (Lập bảng)   |    O(n)    |    O(n)    | Vòng lặp + bảng    |
    +------------------------+------------+------------+--------------------+
    | Bottom-Up tối ưu       |    O(n)    |    O(1)    | Chỉ 2 biến         |
    +------------------------+------------+------------+--------------------+

    Từ 1 TRIỆU TỶ phép tính (n=50) xuống chỉ còn 50. Đó chính là
    sức mạnh của Quy hoạch động.
```

---

## 9. Công thức giải MỌI bài toán DP

```
    Bước 1:  NHẬN DIỆN — Bài toán có Bài toán con chồng lặp
             VÀ Cấu trúc con tối ưu không?

    Bước 2:  ĐỊNH NGHĨA trạng thái — fib(n) / dp[i] đại diện
             cho cái gì?

    Bước 3:  VIẾT công thức truy hồi —
             ví dụ: fib(n) = fib(n-1) + fib(n-2)

    Bước 4:  XÁC ĐỊNH các trường hợp cơ sở —
             ví dụ: fib(0) = 0, fib(1) = 1

    Bước 5:  CHỌN cách cài đặt —
             Memoization (từ trên xuống) hay Lập bảng (từ dưới lên)?

    Bước 6:  (Tùy chọn) TỐI ƯU không gian nếu bạn chỉ cần
             một vài giá trị trước đó.
```

---

**Bước tiếp theo:** Bây giờ hãy luyện tập áp dụng Quy hoạch động vào các bài toán phỏng vấn kinh điển như Leo cầu thang (Climbing Stairs), Đổi tiền xu (Coin Change), và bài toán Cái túi (Knapsack)!
