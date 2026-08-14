
---

# Đệ quy (Recursion)

## 1. Đệ quy là gì?

**Đệ quy (Recursion)** là một kỹ thuật lập trình trong đó một hàm **tự gọi chính nó** để giải quyết một bài toán. Mỗi lần gọi xử lý một **phần nhỏ hơn** của bài toán cho đến khi bài toán trở nên đủ nhỏ để có thể trả lờ i trực tiếp.

Mọi hàm đệ quy **BẮT BUỘC** phải có hai phần:

1. **Trường hợp cơ sở (Base Case)** — điều kiện **DỪNG** đệ quy. Nó trả về giá trị trực tiếp, không gọi thêm lần đệ quy nào nữa.
2. **Trường hợp đệ quy (Recursive Case)** — phần mà hàm **tự gọi chính nó** với đầu vào nhỏ hơn, tiến một bước gần hơn tới trường hợp cơ sở.

### Quy tắc vàng:
> Không có trường hợp cơ sở = không có điểm dừng = hàm tự gọi chính nó mãi mãi...
> cho đến khi Python "giết" nó bằng lỗi **Tràn ngăn xếp (Stack Overflow)** (`RecursionError`).

```
        +--------------------------------------------------+
        |                ĐỆ QUY (RECURSION)                |
        +--------------------------------------------------+
        |                                                  |
        |   Phần 1                   Phần 2                |
        |   +------------------+     +------------------+  |
        |   |   BASE CASE      |     |  RECURSIVE CASE  |  |
        |   |  "dừng gọi lại"  |     |  "tự gọi chính  |  |
        |   |  trả về trực tiếp|     |  mình với input  |  |
        |   |                  |     |  NHỎ HƠN"        |  |
        |   +------------------+     +------------------+  |
        |                                                  |
        |   Thiếu base case?                               |
        |   +------------------+                           |
        |   |  STACK OVERFLOW  |  <== đệ quy vô hạn        |
        |   +------------------+                           |
        +--------------------------------------------------+
```

### Đệ quy trông như thế nào?

```
    factorial(4)
        |
        +-- 4 * factorial(3)
                  |
                  +-- 3 * factorial(2)
                            |
                            +-- 2 * factorial(1)
                                      |
                                      +-- 1   <== BASE CASE (dừng!)
```

Hãy để ý: mỗi lần gọi là **cùng một bài toán**, chỉ **nhỏ hơn** thôi. Đó chính là trái tim của đệ quy.

---

## 2. Tại sao Đệ quy được tạo ra?

Một số bài toán vốn dĩ **tự giống chính nó (self-similar)** — bài toán lớn chứa các bản sao nhỏ hơn của chính nó:

* **Giai thừa (Factorial) / Fibonacci** — `factorial(n)` được định nghĩa *qua* `factorial(n-1)`.
* **Cây (Trees)** — con trái của một cây là... một cây. Con phải cũng là một cây.
* **Thư mục tập tin** — một thư mục chứa các tập tin *và các thư mục khác*, vốn lại chứa thêm thư mục...
* **Chia để trị (Divide-and-Conquer)** — Merge Sort và Quick Sort chia đôi danh sách, sắp xếp từng nửa (đệ quy!), rồi gộp lại.

Cố giải các bài toán này bằng vòng lặp lồng nhau đòi hỏi bạn phải **biết trước độ sâu của sự lồng nhau**. Với đệ quy thì không cần — hàm cứ tự gọi chính nó cho đến khi chạm đáy.

```
    +------------------------+------------------------------------------+
    |  TƯ DUY VÒNG LẶP       |         TƯ DUY ĐỆ QUY                    |
    +------------------------+------------------------------------------+
    | "Tôi cần lồng bao      | "Phiên bản nhỏ nhất của bài toán này     |
    |  nhiêu vòng lặp? Nếu   |  mà tôi trả lờ i được ngay là gì? Làm    |
    |  cây sâu 100 tầng?"    |  sao quy mọi thứ khác về nó?"            |
    +------------------------+------------------------------------------+
    | Phức tạp, dễ hỏng      | Vài dòng code dễ đọc                     |
    +------------------------+------------------------------------------+
```

### Đệ quy là nền tảng cho:

```
        Đệ quy (Recursion)
            |
    +-------+--------+-----------+-----------+
    |                |           |           |
 Duyệt cây/đồ thị  Merge Sort  Quick Sort   Quy hoạch động
 (folder 13)      (folder 14)  (folder 14)  (Dynamic
                                            Programming,
                                            folder 15)
```

Mọi thứ ở các folder tiếp theo — duyệt cây, sắp xếp, Quy hoạch động (Dynamic Programming) — đều được xây dựng trên mô hình tư duy mà bạn xây dựng ở đây.

---

## 3. Đệ quy giải quyết những bài toán nào?

| Lĩnh vực | Ví dụ | Tại sao đệ quy phù hợp |
|:---|:---|:---|
| **Định nghĩa toán học** | `factorial(n)`, `fibonacci(n)` | Được định nghĩa qua chính nó |
| **Cấu trúc cây** | BST search/insert/delete (folder 12) | Con của cây cũng là cây |
| **Hệ thống tập tin** | Duyệt thư mục lồng nhau | Thư mục chứa thư mục |
| **Dữ liệu lồng nhau** | Phân tích JSON, XML, list lồng nhau | Đối tượng chứa đối tượng |
| **Chia để trị** | Merge Sort, Quick Sort | Chia -> giải từng nửa -> gộp |
| **Quay lui (Backtracking)** | Sudoku, mê cung, N-Queens | Thử một đường, lùi lại, thử đường khác |

```
    Duyệt cây thư mục:

    /project
        |-- main.py
        |-- src/
        |       |-- utils.py
        |       |-- core/
        |       |       |-- engine.py     <== nó sâu tới đâu?
        |-- tests/
                |-- test_core.py

    Với vòng lặp:  bạn phải hardcode độ sâu... nhưng độ sâu là KHÔNG BIẾT TRƯỚC.
    Với đệ quy:    visit(item):
                       nếu item là tập tin  -> xử lý nó          (BASE CASE)
                       nếu item là thư mục  -> visit từng con    (ĐỆ QUY)
```

---

## 4. Ngăn xếp cuộc gọi (Call Stack) — Cách các lờoi gọi hàm thực sự hoạt động

Trước khi hiểu đệ quy, ta phải hiểu cơ chế làm nó khả thi: **Ngăn xếp cuộc gọi (Call Stack)**.

### Call Stack là gì?

**Call Stack** là một vùng bộ nhớ theo dõi **hàm nào đang chạy** và **phải quay về đâu** khi hàm kết thúc. Nó hoạt động theo kiểu **LIFO — Vào sau, Ra trước (Last In, First Out)**:

* Khi một hàm được **gọi**, nó được **ĐẨY VÀO (PUSH)** lên đỉnh ngăn xếp.
* Khi một hàm **kết thúc (return)**, nó bị **LẤY RA (POP)** khỏi ngăn xếp.
* Hàm **nằm trên đỉnh** ngăn xếp là hàm đang thực thi.

### Code (từ `CallStack.py`):

```python
def funcThree():
    print('Three')

def funcTwo():
    funcThree()
    print('Two')

def funcOne():
    funcTwo()
    print('One')


funcOne()
```

### Kết quả in ra:

```
    Three
    Two
    One
```

Hãy chú ý thứ tự! `funcOne` được gọi **đầu tiên**, nhưng in ra **cuối cùng**. Tại sao? Vì call stack.

### Từng bước — Ngăn xếp lớn dần XUỐNG (Push):

```
    BƯỚC 1                BƯỚC 2                BƯỚC 3
    gọi funcOne()         funcOne gọi           funcTwo gọi
                          funcTwo()             funcThree()

    +---------------+     +---------------+     +---------------+
    |               |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |               |     |               |     |  funcThree()  | <== ĐỈNH
    +---------------+     +---------------+     +---------------+
    |               |     |   funcTwo()   |     |   funcTwo()   |
    +---------------+     +---------------+     +---------------+
    |   funcOne()   |     |   funcOne()   |     |   funcOne()   |
    +---------------+     +---------------+     +---------------+

    funcThree được đẩy vào CUỐI => nó nằm trên ĐỈNH => nó chạy ĐẦU TIÊN.
```

### Từng bước — Ngăn xếp thu dần LÊN (Pop):

```
    BƯỚC 4                BƯỚC 5                BƯỚC 6
    funcThree in 'Three'  funcTwo tiếp tục,     funcOne tiếp tục,
    & RETURN (bị pop)     in 'Two', RETURN      in 'One', RETURN
                          (bị pop)              (bị pop)

    +---------------+     +---------------+     +---------------+
    |               |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |               |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |   funcTwo()   |     |               |     |               |
    +---------------+     +---------------+     +---------------+
    |   funcOne()   |     |   funcOne()   |     |               |
    +---------------+     +---------------+     +---------------+

    Đã in ra:             Đã in ra:             Đã in ra:
    Three                 Three                 Three
                          Two                   Two
                                                One
```

### Quy tắc LIFO trong một hình:

```
        THỨ TỰ PUSH (đi xuống):         THỨ TỰ POP (đi lên):

            funcOne    (vào thứ 1)          funcThree  (ra thứ 1)
            funcTwo    (vào thứ 2)          funcTwo    (ra thứ 2)
            funcThree  (vào thứ 3, cuối)    funcOne    (ra thứ 3, cuối)

            VÀO SAU  ==================>  RA TRƯỚC
```

> **Ý chính:** Khi `funcOne` gọi `funcTwo`, `funcOne` không biến mất — nó bị **tạm dừng**, đóng băng giữa chừng, nằm chờ trên ngăn xếp. Chỉ khi mọi thứ phía trên nó đã được pop ra, nó mới chạy tiếp đúng chỗ đã dừng (ngay trước `print('One')`).

**Đệ quy dùng đúng cơ chế này** — chỉ khác là thay vì ba hàm *khác nhau*, đó là *cùng một* hàm được đẩy lên ngăn xếp lặp đi lặp lại, mỗi lần với đầu vào nhỏ hơn.

---

## 5. Giai thừa (Factorial) — Đệ quy thực hành

**Giai thừa (Factorial)** của một số `n` (viết là `n!`) là tích của mọi số nguyên dương từ 1 đến `n`:

```
    4!  =  4 * 3 * 2 * 1  =  24
```

Về mặt toán học, giai thừa được **định nghĩa một cách đệ quy**:

```
                    |  1                    nếu n = 1     (BASE CASE)
    factorial(n) =  |
                    |  n * factorial(n-1)   nếu n > 1     (RECURSIVE CASE)
```

### Code (từ `Factorial.py`):

```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)


print(factorial(4))
```

### Kết quả in ra:

```
    24
```

### Đọc code — Hai phần bắt buộc:

```
    def factorial(n):
        if n == 1:            <--+-- BASE CASE: dừng đệ quy
            return 1           --+   (không gọi nữa, trả lờ i trực tiếp)
        return n * factorial(n-1)
                          ^      ^
                          |      |
                          +------+-- RECURSIVE CASE: tự gọi chính nó
                                     với input NHỎ HƠN (n-1)
```

### Trace đầy đủ — Khoan xuống DƯỚI, rồi nổi ngược LÊN:

```
        CÁC LỜI GỌI ĐI XUỐNG (push lên stack)
        |                                CÁC GIÁ TRỊ TRẢ VỀ ĐI LÊN (pop)
        |                                |
        v                                |
    factorial(4)                         |
        = 4 * factorial(3)  ----------+  |
        |                             |  |
        v                             v  |
    factorial(3)                 6 * 4 = 24 -+----->  trả về 24
        = 3 * factorial(2)  ------+      ^
        |                         |      |
        v                         v      |
    factorial(2)             2 * 3 = 6 --+-------->  trả về 6
        = 2 * factorial(1)  --+      ^
        |                     |      |
        v                     v      |
    factorial(1)         1 * 2 = 2 --+----------->  trả về 2
        = 1  <== BASE CASE!       ^
            |                     |
            +---- trả về 1 -------+
```

### Cùng trace đó trên Call Stack:

```
    ĐỘ SÂU TỐI ĐA (4 khung):            THU NGƯỢC (kết quả nhân dần khi đi lên):

    +-----------------------+            factorial(1) trả về 1
    |    factorial(1)       | <== ĐỈNH   factorial(2) trả về 2 * 1 = 2
    |    n = 1, BASE CASE   |            factorial(3) trả về 3 * 2 = 6
    +-----------------------+            factorial(4) trả về 4 * 6 = 24
    |    factorial(2)       |
    |    n = 2, đang chờ... |                 ĐÁP ÁN CUỐI: 24
    +-----------------------+
    |    factorial(3)       |            Mỗi khung bị TẠM DỪNG tại:
    |    n = 3, đang chờ... |            "return n * factorial(n-1)"
    +-----------------------+            chờ lờoi gọi con trả kết quả về.
    |    factorial(4)       |
    |    n = 4, đang chờ... |
    +-----------------------+
```

### Chuyện gì xảy ra nếu KHÔNG có Base Case?

```
    def factorial(n):
        return n * factorial(n-1)    # quên mất base case!

    factorial(4) -> factorial(3) -> factorial(2) -> factorial(1)
                 -> factorial(0) -> factorial(-1) -> factorial(-2)
                 -> ... MÃI MÃI ...

    Ngăn xếp cứ lớn dần:
        |  factorial(-995)  |
        |  factorial(-994)  |
        |       ...         |
        |  factorial(2)     |
        |  factorial(3)     |
        |  factorial(4)     |
        +-------------------+
              |
              v
    RecursionError: maximum recursion depth exceeded
                    (còn gọi là STACK OVERFLOW - tràn ngăn xếp)
```

---

## 6. Phân tích Big O

Với `factorial(n)` đệ quy:

```
    Các lờoi gọi:  factorial(n) -> factorial(n-1) -> ... -> factorial(1)

    Đó là đúng n lờoi gọi. Mỗi lờoi gọi làm O(1) công việc (một phép nhân).

    Độ sâu ngăn xếp lúc đỉnh điểm:
        |  factorial(1)   |
        |      ...        |     <- sâu n khung
        |  factorial(n)   |
        +-----------------+
```

| Độ phức tạp | Giá trị | Lý do |
|:---|:---|:---|
| **Thờoi gian (Time)** | `O(n)` | Đúng `n` lờoi gọi đệ quy, mỗi lờoi làm `O(1)` công việc |
| **Không gian (Space)** | `O(n)` | Call stack lớn tới `n` khung trước khi thu lại |

> **Quan trọng:** Dù về mặt logic factorial chỉ *dùng* một con số tại một thờoi điểm, đệ quy vẫn *tốn* `O(n)` không gian bộ nhớ vì mỗi lờoi gọi bị tạm dừng đều giữ khung riêng của nó (bản sao riêng của `n`, địa chỉ trả về riêng) trên ngăn xếp.

---

## 7. Đệ quy vs Lặp (Iteration) — So sánh

Bất cứ thứ gì đệ quy làm được, vòng lặp cũng làm được (và ngược lại). Vậy khi nào dùng cái nào?

```
    +-----------------------+-----------------------+-----------------------+
    |                       |    ĐỆ QUY             |    VÒNG LẶP           |
    |                       |    (Recursion)        |    (Iteration)        |
    +-----------------------+-----------------------+-----------------------+
    | Khả năng đọc          | Tuyệt vờoi cho bài    | Tốt hơn cho bài toán  |
    |                       | toán tự giống chính nó| đơn giản, tuyến tính  |
    +-----------------------+-----------------------+-----------------------+
    | Độ dài code           | Rất ngắn              | Thường dài hơn với    |
    |                       | (phản ánh đúng toán)  | bài toán cây/lồng nhau|
    +-----------------------+-----------------------+-----------------------+
    | Bộ nhớ                | O(độ sâu) khung stack | O(1) không gian phụ   |
    |                       |                       | (chỉ biến vòng lặp)   |
    +-----------------------+-----------------------+-----------------------+
    | Rủi ro                | Tràn stack nếu thiếu  | Vòng lặp vô hạn nếu   |
    |                       | base case             | sai điều kiện         |
    +-----------------------+-----------------------+-----------------------+
    | Phù hợp nhất với      | Cây, đồ thị, chia để  | Đếm đơn giản,         |
    |                       | trị, dữ liệu lồng nhau| vòng lặp phẳng        |
    +-----------------------+-----------------------+-----------------------+
```

| Yếu tố | Đệ quy (Recursion) | Vòng lặp (Iteration) |
|:---|:---|:---|
| **Code factorial** | 4 dòng, phản ánh đúng định nghĩa | Cần vòng lặp + biến tích lũy rõ ràng |
| **Chi phí không gian** | `O(n)` khung stack | `O(1)` |
| **Giới hạn độ sâu Python** | ~1000 khung (`RecursionError`) | Không giới hạn |
| **Gỡ lỗi (Debug)** | Khó hơn (nhiều khung đang sống) | Dễ hơn (một trạng thái vòng lặp) |
| **Khi nào chọn** | Bài toán vốn mang tính đệ quy (cây!) | Bài toán lặp lại đơn thuần |

> **Kinh nghiệm:** Nếu bài toán có dạng *cây* hoặc *chia để trị*, hãy dùng đệ quy. Nếu là lặp phẳng, hãy dùng vòng lặp. Ở folder tiếp theo, bạn sẽ thấy cây tự quyết định điều này cho bạn.

---

## 8. Tóm tắt

```
    +----------------------------------------------------------+
    |  CHECKLIST ĐỆ QUY                                        |
    +----------------------------------------------------------+
    |  1. Hàm của tôi có TỰ GỌI CHÍNH NÓ không?                |
    |                                                          |
    |  2. Tôi có BASE CASE để dừng các lờoi gọi không?         |
    |     (Thiếu nó => tràn ngăn xếp!)                         |
    |                                                          |
    |  3. Mỗi lờoi gọi đệ quy có tiến GẦN HƠN tới              |
    |     base case không? (n-1, cây con nhỏ hơn, list ngắn...)|
    |                                                          |
    |  4. Tôi có chấp nhận trả O(độ sâu) không gian            |
    |     cho call stack không?                                |
    +----------------------------------------------------------+
```

```
    Mô hình tư duy cần nhớ mãi:

        LỜI GỌI KHOAN XUỐNG:    GIÁ TRỊ TRẢ VỀ NỔI LÊN:
        factorial(4)            factorial(1) = 1
            |                       |
        factorial(3)            2 * 1 = 2
            |                       |
        factorial(2)            3 * 2 = 6
            |                       |
        factorial(1)  ======>   4 * 6 = 24
        BASE CASE               ĐÁP ÁN
```

---

**Bước tiếp theo:** Bây giờ bạn đã hiểu đệ quy và call stack, hãy áp dụng nó vào một cấu trúc dữ liệu mà đệ quy thực sự tỏa sáng — viết lại các thao tác Cây tìm kiếm nhị phân (Binary Search Tree) một cách đệ quy (folder 12)!
