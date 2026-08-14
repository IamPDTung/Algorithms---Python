
---

# Ký hiệu Big O (Big O Notation)

## 1. Big O là gì?

**Ký hiệu Big O (Big O Notation)** là ngôn ngữ dùng để mô tả **mức độ hiệu quả của một thuật toán** — cụ thể là **thờii gian chạy** hoặc **dung lượng bộ nhớ** của nó **tăng trưởng như thế nào** khi kích thước đầu vào `n` tăng lên.

Big O **KHÔNG** đo thờii gian bằng giây. Nó đo **số lượng phép toán** như một hàm của kích thước đầu vào, tập trung vào điều xảy ra khi `n` trở nên **thực sự lớn**.

### Hai thứ mà Big O đo:

1. **Độ phức tạp thờii gian (Time Complexity)** — *số lượng phép toán* tăng trưởng thế nào khi `n` tăng.
2. **Độ phức tạp không gian (Space Complexity)** — thuật toán cần thêm *bao nhiêu bộ nhớ* khi `n` tăng.

```
        +------------------------------------------------------+
        |                 KY HIEU BIG O                        |
        +------------------------------------------------------+
        |                                                      |
        |   +----------------------+  +----------------------+ |
        |   |  DO PHUC TAP         |  |  DO PHUC TAP         | |
        |   |  THOI GIAN           |  |  KHONG GIAN          | |
        |   |  "Bao nhieu phep?"   |  |  "Bao nhieu bo nho?" | |
        |   +----------------------+  +----------------------+ |
        |                                                      |
        |   Ca hai deu do theo kich thuoc dau vao n            |
        +------------------------------------------------------+
```

### Trường hợp tốt nhất, trung bình và xấu nhất — Ba chữ cái Hy Lạp:

```
        +------------------------------------------------------+
        |              BA CHU CAI HY LAP                       |
        +------------------------------------------------------+
        |  Omega   (Omega)  ->  TOT NHAT     (lan chay may man)|
        |  Theta   (Theta)  ->  TRUNG BINH   (lan chay thuong) |
        |  Omicron (O)      ->  XAU NHAT     (== "Big O")      |
        +------------------------------------------------------+
```

### Ví dụ — Tìm kiếm trong danh sách:

```
    Tim so 1 trong:   [1, 2, 3, 4, 5, 6, 7]
                       ^
                       tim thay ngay LAN DAU -> Omega(1) tot nhat

    Tim so 7 trong:   [1, 2, 3, 4, 5, 6, 7]
                                              ^
                       tim thay o LAN CUOI    -> O(n) xau nhat
```

> Khi mọi ngườii nói "Big O", họ hầu như luôn ám chỉ **trường hợp xấu nhất (worst case)** — vì trường hợp xấu nhất là **sự đảm bảo** mà ta có thể dựa vào.

---

## 2. Tại sao Big O được tạo ra?

### Vấn đề khi đo thờii gian trực tiếp

Bạn có thể bấm giờ một thuật toán... nhưng kết quả phụ thuộc hoàn toàn vào **chiếc máy tính** chạy nó:

```
    CUNG mot thuat toan, CUNG mot dau vao, ba chiec may:

    +---------------------------+--------------------+
    |  MAY TINH                 |  THOI GIAN DO DUOC |
    +---------------------------+--------------------+
    |  PC gaming 2024           |  0.03 giay         |
    |  Laptop van phong 2010    |  1.20 giay         |
    |  Raspberry Pi             |  8.50 giay         |
    +---------------------------+--------------------+

    Con so nao moi la "thoii gian chay" that?  Khong con so nao.
```

Thờii gian đồng hồ thực phụ thuộc vào: **tốc độ CPU, RAM, hệ điều hành, tiến trình chạy ngầm, ngôn ngữ lập trình, trình biên dịch**... Phép đo này không thể mang từ máy này sang máy khác.

### Giải pháp của Big O:

> **Đếm số phép toán, đừng đếm giây. Đo TỐC ĐỘ TĂNG TRƯỞNG (growth rate), đừng đo thờii gian tuyệt đối.**

```
    CACH BAM GIO:                      CACH BIG O:

    "Mat 1.2 giay"                     "Thuc hien ~n phep toan"
            |                                  |
            v                                  v
    Vo nghia tren moi may khac,        Dung tren MOI may tinh,
    tham chi gay hieu nham             voi MOI kich thuoc
    tren chinh may nay ngay mai.       dau vao n.
```

### Big O cho phép ta làm gì:

```
    +----------------------------------------------------------+
    |  "Khi n tang gap doi, thuat toan cua toi bi anh huong    |
    |   the nao?"                                              |
    +----------------------------------------------------------+
    |  O(1)    ->  khong thay doi gi        (giu nguyen)       |
    |  O(n)    ->  cong viec tang gap doi   (ti le thuan)      |
    |  O(n^2)  ->  cong viec tang gap BON   (bung no)          |
    |  O(2^n)  ->  cong viec BINH PHUONG    (tham hoa)         |
    +----------------------------------------------------------+
```

---

## 3. Big O giải quyết những vấn đề gì?

### 1. Lựa chọn giữa các thuật toán

Hai hàm giải cùng một bài toán. Bạn nên dùng hàm nào? Big O đưa ra câu trả lờii **khách quan, độc lập với phần cứng**.

### 2. Giao tiếp trong phỏng vấn

Big O là **từ vựng chung** của các buổi phỏng vấn kỹ thuật. Nói *"cái này là O(n²), nhưng tôi có thể cải thiện thành O(n log n)"* đã truyền tải trọn vẹn một ý tưởng trong một câu.

### 3. Dự đoán khả năng mở rộng (scalability)

Code chạy tốt hôm nay có thể sụp đổ ngày mai. Big O cho bạn biết **trước khi điều đó xảy ra**:

```
    Code cua ban chay tot hom nay voi n = 100 nguoii dung.
    No co song sot voi n = 1,000,000 nguoii dung khong?

    +---------------+---------------------------+------------------+
    |  THUAT TOAN   |  SO PHEP VOI n = 1.000.000|  DANH GIA        |
    +---------------+---------------------------+------------------+
    |  O(n)         |  1,000,000                |  on              |
    |  O(n log n)   |  ~20,000,000              |  on              |
    |  O(n^2)       |  1,000,000,000,000        |  lam chay server |
    +---------------+---------------------------+------------------+
```

---

## 4. O(1) — Thờii gian hằng số (Constant Time)

**O(1)** nghĩa là số lượng phép toán là **hằng số** — **không** phụ thuộc vào kích thước đầu vào `n`. Dù `n` là 10 hay 10 triệu, khối lượng công việc vẫn như nhau.

### Code:

```python
def add_items(n):
    return n + n + n
 
 
print add_items(10)
```

### Phân tích:

```
    add_items(n):
        n + n + n      <- 2 phep cong (co tai lieu tinh la 1 phep)

    n = 10        ->  so phep toan khong doi
    n = 1,000,000 ->  so phep toan khong doi

    Ke ca khi ta noi "2 phep toan", O(2) van rut gon thanh O(1).
    "O(1)" don gian nghia la: HANG SO theo n.
```

### Minh họa — Đường phẳng nhất trong tất cả:

```
    so phep toan
      ^
    2 +--------------------------------------------
      |   \________________ O(1): duong nam ngang
    1 +--------------------------------------------
      |
      +------+------+------+------+------+------+-------> n
             10     100    1k     10k    100k   1M

    Dau vao tang len. Cong viec khong he tang.
```

> **O(1) là Big O hiệu quả nhất.** Ví dụ: cộng hai số, tra cứu một khóa trong từ điển (dictionary), `push`/`pop` trên ngăn xếp (stack).

---

## 5. O(n) — Thờii gian tuyến tính (Linear Time)

**O(n)** nghĩa là số lượng phép toán tăng **tỉ lệ thuận** với kích thước đầu vào. Đầu vào tăng gấp đôi, công việc tăng gấp đôi.

### Code:

```python
def print_items(n):
    for i in range(n):
        print(i)

print_items(10)
```

### Phân tích:

```
    print_items(n):
        for i in range(n):      <- chay n lan
            print(i)            <- 1 phep toan moi vong lap

    n = 10   ->  10  phep in
    n = 100  ->  100 phep in
    n = 1000 ->  1000 phep in

    so phep toan = n   =>   O(n)  "tuyen tinh"
```

### Minh họa — Một đường chéo thẳng:

```
    so phep toan
      ^
 1000 +                                              *
      |                                         *
  100 +                                  *
      |                             *
   10 +                     *
      |              *
    1 +      *
      |  *
      +------+------+------+------+------+------+-------> n
             10     100    1k

    Mot duong thang: n tang -> cong viec tang CUNG TOC DO.
```

---

## 6. O(n^2) — Thờii gian bậc hai (Quadratic Time)

**O(n²)** xuất hiện khi một vòng lặp nằm **bên trong một vòng lặp khác**. Với mỗi một trong `n` lần lặp ngoài, vòng lặp trong chạy `n` lần: `n * n = n²` phép toán.

### Code:

```python
def print_items(n):
    for i in range(n):
        for j in range(n):
            print(i,j) 

print_items(10)
```

### Minh họa — Vòng lặp lồng nhau dưới dạng lưới (n = 4):

```
    Vong ngoai i chon mot HANG, vong trong j di qua moi COT:

              j=0     j=1     j=2     j=3
            +-------+-------+-------+-------+
      i=0   | (0,0) | (0,1) | (0,2) | (0,3) |   <- vong trong chay
            +-------+-------+-------+-------+      n lan...
      i=1   | (1,0) | (1,1) | (1,2) | (1,3) |   <- ...cho MOI lan
            +-------+-------+-------+-------+      lap cua vong ngoai
      i=2   | (2,0) | (2,1) | (2,2) | (2,3) |
            +-------+-------+-------+-------+
      i=3   | (3,0) | (3,1) | (3,2) | (3,3) |
            +-------+-------+-------+-------+
              \_____________________________/
                 n hang x n cot = n^2 o

    n = 4    ->  4  x 4    =  16  phep in
    n = 10   ->  10 x 10   =  100 phep in
    n = 1000 ->  1000x1000 =  1,000,000 phep in
```

### Tại sao nó đau — Sự bùng nổ:

```
    so phep toan
      ^
 1M   +                                                    *
      |                                              *
 10k  +                                       *
      |                                *
  100 +                        *
      |                 *
   10 +         *
      |    *
    1 + *
      +------+------+------+------+------+------+-------> n
             10     100    1k

    Duong cong vom LEN TREN. n gap doi -> cong viec gap BON.
```

> **Quy tắc nhẩm:** một vòng lặp trên `n` là `O(n)`; một vòng lặp **lồng trong** vòng lặp trên `n` là `O(n²)`; ba vòng lặp lồng nhau là `O(n³)` — và mỗi tầng thêm vào đều tệ hơn rất nhiều.

---

## 7. Quy tắc — Loại bỏ hằng số (Drop the Constants)

### Code:

```python
def print_items(n):
    for i in range(n):
        print(i)

    for j in range(n):
        print(j)

print_items(10)
```

### Phân tích:

```
    Vong lap thu nhat  ->  n phep toan
    Vong lap thu hai   ->  n phep toan
                           ___________
    Tong                 ->  n + n = 2n phep toan   =>  O(2n)
```

### Quy tắc:

> **Loại bỏ hệ số nhân hằng số.** `O(2n)` rút gọn thành `O(n)`.

### Tại sao? Vì Big O quan tâm đến HÌNH DẠNG, không phải độ dốc:

```
    so phep toan
      ^
      |                                       O(2n)  -,
      |                                  ,-''        |
      |                             ,-''             |  CA HAI deu
      |                       ,-''                   |  la duong
      |                 ,-''       O(n)  -,          |  thang voi
      |            ,-''           ,-''               |  CUNG mot
      |       ,-''         ,-''                      |  hinh dang
      |  ,-''       , -''
      +--------------------------------------------------> n

    Khi n -> vo cung, "2n" va "n" tang truong GIONG NHAU.
    Hang so "2" khong lien quan den TOC DO tang truong.
```

### Bảng rút gọn:

| Số phép chính xác | Loại bỏ hằng số | Big O |
|:---|:---|:---|
| `2n` | `2` là hằng số | **`O(n)`** |
| `3n + 5` | bỏ `3` và `5` | **`O(n)`** |
| `500` | mọi số cố định | **`O(1)`** |
| `4n²` | `4` là hằng số | **`O(n²)`** |

---

## 8. Quy tắc — Loại bỏ các số hạng không trội (Drop the Non-Dominant Terms)

### Code:

```python
def print_items(n):
    for i in range(n):
        for j in range(n):
            print(i,j)
    
    for k in range(n):
        print(k)

print_items(10)
```

### Phân tích:

```
    Vong lap long nhau  ->  n * n = n^2 phep toan   <- so hang TROI
    Vong lap don        ->  n phep toan             <- khong troi
                            ___________
    Tong                ->  n^2 + n phep toan   =>  O(n^2 + n)
```

### Quy tắc:

> **Chỉ giữ lại số hạng TRỘI (dominant term)** — số hạng tăng nhanh nhất. `O(n² + n)` rút gọn thành **`O(n²)`**.

### Tại sao? Hãy nhìn `+n` trở nên vô nghĩa:

```
    +-----------+-----------------+-----------------+----------------+
    |     n     |      n^2        |      + n        |  % do n gay ra |
    +-----------+-----------------+-----------------+----------------+
    |     10    |       100       |    100 + 10     |     9.1%       |
    |    100    |    10,000       |  10,000 + 100   |     0.99%      |
    |   1000    | 1,000,000       | 1,000,000+1000  |     0.099%     |
    +-----------+-----------------+-----------------+----------------+

    Khi n tang, so hang "n" dong gop gan nhu KHONG DANG KE.
    So hang n^2 THONG TRI -> chi no moi quan trong.
```

```
    O(n^2 + n)  --bo so hang khong troi-->  O(n^2)
    O(n + 1)    --bo so hang khong troi-->  O(n)
    O(n^2 + n log n) ------------------->   O(n^2)
```

---

## 9. Quy tắc — Các số hạng khác nhau cho các đầu vào khác nhau (Different Terms for Different Inputs)

Khi một hàm nhận **hai đầu vào khác nhau**, bạn phải theo dõi chúng bằng **hai biến khác nhau** — không thể gọi tất cả là `n` nữa.

### Code:

```python
def print_items(a,b):
    for i in range(a):
        print(i)

    for j in range(b):
        print(j)

print_items(1, 10)
```

### Phân tích — Các vòng lặp riêng biệt: `O(a + b)`

```
    Vong lap thu nhat  ->  chay a lan
    Vong lap thu hai   ->  chay b lan
                           __________
    Tong                 ->  a + b phep toan   =>  O(a + b)

    KHONG THE viet O(n): a va b la HAI dau vao KHAC NHAU.
    Khong co quy tac nao "rut gon" no thanh O(a) hay O(b).
```

### Biến thể lồng nhau: `O(a * b)`

```
    Neu cac vong lap LONG NHAU thay vi rieng biet:

        for i in range(a):        <- chay a lan
            for j in range(b):    <- chay b lan cho MOI i
                print(i, j)       <- tong a * b phep toan

    Tong -> a * b   =>  O(a * b)   (KHONG phai O(n^2) — dau vao khac nhau!)
```

### So sánh cạnh nhau:

```
    VONG LAP RIENG BIET:               VONG LAP LONG NHAU:

    for i in range(a):  --+            for i in range(a):   --+
        print(i)          | a phep         for j in range(b): | a x b
    for j in range(b):  --+                  print(i,j)       |   phep
        print(j)          | b phep
                          |                                   |
    O(a + b)  <-----------+               O(a * b)  <---------+

    +------------------------+-------------------------+
    |  Cau truc              |  Big O                  |
    +------------------------+-------------------------+
    |  vong lap canh nhau    |  O(a + b)               |
    |  vong lap long nhau    |  O(a * b)               |
    +------------------------+-------------------------+
```

---

## 10. Biểu đồ tốc độ tăng trưởng của Big O

### Tất cả các độ phức tạp trên một hình:

```
    so phep toan
      ^
      |                                              __-- O(2^n)
      |                                         __---
      |                                   __---
      |                              __--            __-- O(n^2)
      |                         __--            __---
      |                    __--            __--         __-- O(n log n)
      |               __--            __--         __--
      |          __--            __--         __--         __-- O(n)
      |     __--            __--         __--         __--      O(log n)
      | __--           __--        __--         __--        __-   O(1)
      +----------------------------------------------------------> n
                     kich thuoc dau vao tang  ------->

    Tu TOT NHAT den TE NHAT:
    O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n)
```

### Cùng ý tưởng với các con số cụ thể:

| Big O | n = 10 | n = 100 | n = 1,000 |
|:---|---:|---:|---:|
| **O(1)** | 1 | 1 | 1 |
| **O(log n)** | ~3 | ~7 | ~10 |
| **O(n)** | 10 | 100 | 1,000 |
| **O(n log n)** | ~33 | ~664 | ~9,966 |
| **O(n²)** | 100 | 10,000 | 1,000,000 |
| **O(2ⁿ)** | 1,024 | ~1.27 x 10³⁰ | ~1.07 x 10³⁰¹ |

> Tại `n = 100`, `O(2ⁿ)` đã vượt quá số nguyên tử trong vũ trụ quan sát được. Tốc độ tăng trưởng — chứ không phải phần cứng — mới là thứ quan trọng.

---

## 11. Bảng tóm tắt Big O (Cheat Sheet)

### Các lớp độ phức tạp:

| Ký hiệu | Tên gọi | Ví dụ điển hình | Đánh giá |
|:---|:---|:---|:---|
| `O(1)` | Hằng số | `add_items`, tra cứu dict | Tuyệt vờii |
| `O(log n)` | Logarit | Tìm kiếm nhị phân (Binary Search) | Rất tốt |
| `O(n)` | Tuyến tính | Vòng lặp đơn | Tốt |
| `O(n log n)` | Tuyến tính-logarit | Merge Sort, Quick Sort | Khá |
| `O(n²)` | Bậc hai | Vòng lặp lồng nhau | Kém |
| `O(2ⁿ)` | Mũ | Fibonacci đệ quy ngây thơ | Rất tệ |

### Các quy tắc rút gọn:

| Quy tắc | Trước | Sau |
|:---|:---|:---|
| **Bỏ hằng số** | `O(2n)` | `O(n)` |
| **Bỏ số hạng không trội** | `O(n² + n)` | `O(n²)` |
| **Đầu vào khác nhau (riêng biệt)** | vòng lặp trên `a` rồi `b` | `O(a + b)` |
| **Đầu vào khác nhau (lồng nhau)** | vòng lặp `b` trong vòng lặp `a` | `O(a * b)` |

### Mẹo ghi nhớ một dòng:

```
    "Dem so phep toan khi n -> vo cung,
     roi chi giu lai phan TANG NHANH NHAT."
```

---

**Bước tiếp theo:** Bây giờ hãy xây dựng nền tảng cho mọi cấu trúc dữ liệu trong khóa học này — Lớp (Class) và Con trỏ (Pointer)!
