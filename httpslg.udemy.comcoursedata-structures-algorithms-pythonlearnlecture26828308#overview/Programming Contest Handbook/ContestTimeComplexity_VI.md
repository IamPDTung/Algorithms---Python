
---

# Cẩm Nang Lập Trình Thi Đấu: Độ Phức Tạp Thời Gian

Tài liệu này giải thích cách đọc đề thi lập trình, ước lượng khối lượng công việc của chương trình, chọn thuật toán phù hợp với giới hạn, và tránh nhầm lẫn giữa độ phức tạp tiệm cận với thời gian chạy chính xác.

Thói quen quan trọng nhất khi thi là:

> Đọc giới hạn dữ liệu trước khi chọn thuật toán.

```
    ĐỀ BÀI THI ĐẤU
           |
           v
    kích thước dữ liệu tối đa
           |
           v
    số phép tính cho phép
           |
           v
    độ phức tạp mục tiêu
           |
           v
    thuật toán + cấu trúc dữ liệu
           |
           v
    cài đặt và kiểm thử
```

---

## 1. `n` Có Nghĩa Là Gì?

Trong phân tích Big O, `n` thường đại diện cho kích thước dữ liệu đầu vào. Nó là một **biến**, không phải một hằng số.

Ví dụ:

```python
# n is the number of values in the list
numbers = [4, 2, 7, 1]
n = len(numbers)

# n is the number of characters in the string
text = "algorithm"
n = len(text)
```

Câu mô tả:

```text
1 <= n <= 2 * 10^5
```

không có nghĩa là `n` luôn bằng `200,000`. Nó có nghĩa là bộ kiểm tra có thể đưa vào bất kỳ dữ liệu hợp lệ nào có kích thước tối đa `200,000`, bao gồm cả trường hợp lớn nhất.

```
    các đầu vào có thể có:

    1, 2, 3, 4, ..., 199,999, 200,000
                                      ^
                              trường hợp xấu nhất quan trọng
```

### `n` Không Phải Là Hằng Số

Có hai khái niệm khác nhau:

```text
    n = kích thước đầu vào          biến; thay đổi theo test case
    c = hệ số cố định               hằng số; không phụ thuộc kích thước đầu vào
    2 * 10^5 = 200,000              giá trị giới hạn; n tối đa được phép
```

Ví dụ:

```text
5n + 20
```

có phần biến `n` và các hằng số cố định `5`, `20`. Trong ký hiệu tiệm cận:

```text
5n + 20 -> O(n)
```


---

## 2. Đọc Đề Thi Như Một Hợp Đồng


Hãy tìm:

| Thông tin trong đề | Điều nó cho biết |
|:---|:---|
| `n <= ...` | Kích thước của một đầu vào chính |
| `T <= ...` | Số lượng test case |
| `sum(n) <= ...` | Tổng kích thước dữ liệu của tất cả test case |
| `V, E` | Số đỉnh và cạnh của đồ thị |
| `a[i] <= ...` | Miền giá trị; có thể gợi ý dùng đếm hoặc mảng tần suất |
| `time limit` | Thời gian chạy tối đa trên máy chấm |
| `memory limit` | Bộ nhớ phụ tối đa được phép dùng |
| Dữ liệu đã được sắp xếp | Có thể dùng tìm kiếm nhị phân, hai con trỏ, hoặc greedy |
| Các giá trị khác nhau | Có thể không cần xử lý trùng lặp |

### Sơ Đồ Giới Hạn

```
    n <= 20              -> có thể dùng hàm mũ / bitmask
    n <= 500             -> có thể dùng O(n^2)
    n <= 2,000           -> thường dùng được O(n^2), cần xem time limit
    n <= 2 * 10^5        -> mục tiêu thường là O(n) hoặc O(n log n)
    n <= 10^6            -> thường cần O(n), chú ý hằng số và I/O
    n rất lớn            -> O(log n), O(1), hoặc suy luận toán học
```

Đây là **kinh nghiệm định hướng**, không phải luật tuyệt đối. Một chương trình C++ và một chương trình Python có thể có ngân sách thực tế khác nhau với cùng time limit. Hãy luôn xem time limit và cách cài đặt cụ thể.

### Giới Hạn Là Một Tín Hiệu


* Set hoặc dictionary để băm
* Sắp xếp rồi quét tuyến tính
* Hai con trỏ hoặc cửa sổ trượt
* Prefix sum
* Heap
* Duyệt đồ thị với độ phức tạp `O(V + E)`
* Quy hoạch động với số trạng thái tuyến tính hoặc gần tuyến tính

---

## 3. Big O Thực Sự Cho Biết Điều Gì?

Big O mô tả cách khối lượng công việc tăng khi dữ liệu tăng. Nó **không** trực tiếp cho biết số giây chạy.

```text
    Big O hỏi:

    Nếu kích thước đầu vào tăng gấp 2,
    khối lượng công việc thay đổi thế nào?
```

| Độ phức tạp | Khi `n` tăng gấp đôi | Ý nghĩa thường gặp |
|:---|:---|:---|
| `O(1)` | Gần như không đổi | Truy cập trực tiếp hoặc công việc cố định |
| `O(log n)` | Tăng nhẹ | Liên tục chia đôi không gian tìm kiếm |
| `O(n)` | Tăng khoảng 2 lần | Một lượt quét |
| `O(n log n)` | Hơn 2 lần một chút | Sắp xếp hiệu quả hoặc chia để trị |
| `O(n^2)` | Tăng khoảng 4 lần | So sánh mọi cặp |
| `O(2^n)` | Mỗi phần tử thêm làm công việc gần gấp đôi | Thử mọi tập con |

### Minh Họa Tốc Độ Tăng Trưởng

```text
    công việc
        ^
        |                                      O(2^n)
        |                                _____/
        |                         O(n^2) /
        |                    _____/     /
        |             O(n log n)       /
        |          __/                 /
        |       __/ O(n)              /
        |______/_____________________/____________> n
         O(1)   O(log n)
```

Sơ đồ không được vẽ theo đúng tỉ lệ. Nó cho thấy vì sao thuật toán bậc hai có thể ổn với `n = 1,000` nhưng không thể chạy với `n = 200,000`.

---

## 4. Chuyển Code Thành Số Phép Tính

Để ước lượng độ phức tạp từ code:

1. Xác định `n` đại diện cho điều gì.
2. Tìm phép toán được lặp lại.
3. Đếm số lần mỗi vòng lặp hoặc lời gọi đệ quy chạy.
4. Nhân các công việc lồng nhau và cộng các công việc tuần tự.
5. Giữ lại số hạng tăng nhanh nhất.
6. Thay giới hạn lớn nhất vào công thức.

### Công Việc Cố Định: `O(1)`

```python
    return numbers[0]
```

Có một lần truy cập mảng dù danh sách có 10 hay 200,000 phần tử.

```text
    1 lần truy cập -> O(1)
```

### Một Lượt Quét: `O(n)`

```python
    result = 0
    for number in numbers:
        result += number
    return result
```

Vòng lặp chạy một lần cho mỗi giá trị đầu vào:

```text
    n lần lặp -> O(n)
```

### Hai Vòng Lặp Tuần Tự: Vẫn Là `O(n)`

```python
    positive = 0
    even = 0

    for number in numbers:
        if number > 0:
            positive += 1

    for number in numbers:
        if number % 2 == 0:
            even += 1

    return positive, even
```

Công việc là:

```text
    n + n = 2n
    Bỏ hằng số cố định 2
    O(2n) = O(n)
```

```text
    lượt đầu:  [--------------------]  n
    lượt hai:  [--------------------]  n
                 tổng = 2n -> O(n)
```

### Vòng Lặp Lồng Nhau Độc Lập: `O(n^2)`

```python
    for first in numbers:
        for second in numbers:
            print(first, second)
```

Vòng ngoài chạy `n` lần. Với mỗi lần của vòng ngoài, vòng trong chạy `n` lần:

```text
    n * n = n^2
    O(n^2)
```

```text
                 chỉ số vòng trong
                0 1 2 3 ... n-1
             +-------------------+
    chỉ số   | x x x x ... x      | 0
    vòng     | x x x x ... x      | 1
    ngoài    | x x x x ... x      | 2
             |       ...         |
             | x x x x ... x      | n-1
             +-------------------+

             n hàng * n cột = n^2 phép tính
```

### Vòng Lặp Tam Giác: Vẫn Là `O(n^2)`

```python
    for i in range(len(numbers)):
        for j in range(i):
            compare(numbers[i], numbers[j])
```

Vòng trong thực hiện:

```text
    0 + 1 + 2 + ... + (n - 1)
    = n(n - 1) / 2
    = O(n^2)
```

Dù chỉ dùng một nửa lưới `n * n`, một nửa của `n^2` vẫn là bậc hai.

---

## 5. Các Mẫu Độ Phức Tạp Thường Gặp

### Liên Tục Chia Đôi Bài Toán: `O(log n)`

```python
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps
```

```text
    n -> n/2 -> n/4 -> n/8 -> ... -> 1

    số lần chia = log2(n)
    độ phức tạp = O(log n)
```

Đây là mẫu của tìm kiếm nhị phân.

### Chia Nhỏ Và Xử Lý Ở Mỗi Tầng: `O(n log n)`

Merge sort chia dữ liệu thành `log n` tầng. Mỗi tầng xử lý toàn bộ `n` phần tử khi trộn:

```text
    tầng 0:                  n công việc
    tầng 1:              n + n công việc
    tầng 2:          n/2 + n/2 + ... = n công việc
    ...
    số tầng:                 log n

    tổng = n * log n
    O(n log n)
```

### Vòng Lặp Lồng Nhau Với Con Trỏ Đơn Điệu: Thường Là `O(n)`

Cú pháp lồng nhau không tự động có nghĩa là `O(n^2)`.

```python
    left = 0
    current = 0

    for right in range(len(numbers)):
        current += numbers[right]

        while current > target and left <= right:
            current -= numbers[left]
            left += 1

        if current == target:
            return True

    return False
```

`right` tiến lên nhiều nhất `n` lần. `left` cũng tiến lên nhiều nhất `n` lần trong toàn bộ hàm:

```text
    right: 0 -> 1 -> 2 -> ... -> n-1       tối đa n bước
    left:  0 -> 1 -> 2 -> ... -> n-1       tối đa n bước tổng cộng

    n + n = 2n -> O(n)
```

Vòng `while` bên trong không quay lại từ 0 sau mỗi `right`. Đây gọi là **phân tích khấu hao (amortized analysis)**.

### Các Kích Thước Đầu Vào Khác Nhau

```python
    for value in first:
        use(value)

    for value in second:
        use(value)
```

Nếu hai danh sách có kích thước `a` và `b`, độ phức tạp là:

```text
    O(a + b)
```

Không nên viết `O(n)` nếu đề không đảm bảo cả hai kích thước đều được biểu diễn bằng cùng một `n`.

Với vòng lặp lồng nhau trên hai đầu vào khác nhau:

```python
for x in first:
    for y in second:
        use(x, y)
```

độ phức tạp là:

```text
    O(a * b)
```

---

## 6. Kích Thước Giới Hạn Và Thuật Toán Mục Tiêu

Bảng dưới đây là ước lượng thực tế ban đầu. Nó không thay thế cho việc phân tích chính xác.

| Kích thước tối đa | Thường cân nhắc | Thường tránh |
|:---|:---|:---|
| `n <= 20` | Backtracking, bitmask, `O(2^n)` | Không có gì bắt buộc phải tránh |
| `n <= 40` | Meet-in-the-middle, hàm mũ tối ưu | `O(2^n)` đầy đủ nếu có cách khác |
| `n <= 500` | `O(n^2)`, một số `O(n^3)` | Công việc hàm mũ lớn |
| `n <= 2,000` | `O(n^2)`, sort, prefix sum | `O(n^3)` nếu hằng số không rất nhỏ |
| `n <= 2 * 10^5` | `O(n)`, `O(n log n)`, hashing, heap, DP | `O(n^2)` thông thường |
| `n <= 10^6` | `O(n)`, I/O hiệu quả, bộ nhớ gọn | Hằng số lớn và quét lồng nhau |
| `n <= 10^9` | `O(log n)`, công thức, binary search, ma trận | Vòng lặp chạy đến `n` |

### Ví Dụ Khối Lượng Lớn Nhất

```text
    n = 2 * 10^5

    O(n)       = 200,000
    O(n log2n) = khoảng 3,600,000
    O(n sqrt n)= khoảng 89,000,000
    O(n^2)     = 40,000,000,000
```

```text
    vùng thường an toàn                 vùng nguy hiểm
    <--------------------------|---------------------------->
    O(n), O(n log n)            O(n sqrt n), O(n^2), O(2^n)
```

Thuật toán `O(n sqrt n)` có thể chạy được trong C++ tối ưu với time limit rộng nhưng thất bại trong Python với time limit chặt. Luôn xem giới hạn thực tế của đề.

---

## 7. Hằng Số: Big O Bỏ Qua, Thi Đấu Không Bỏ Qua

Trong ký hiệu tiệm cận:

```text
    O(5n)       -> O(n)
    O(100n)     -> O(n)
    O(2n + 50)  -> O(n)
```

Tại sao bỏ hằng số? Vì khi `n` tiến đến rất lớn, nhóm tăng trưởng vẫn là tuyến tính.

Nhưng cuộc thi có kích thước đầu vào hữu hạn và time limit hữu hạn. Ở kích thước đó, hằng số có thể quyết định code pass hay fail.

### Cùng Big O, Công Việc Thực Tế Khác Nhau

```text
    Thuật toán A:  n phép tính
    Thuật toán B:  100n phép tính

    Cả hai đều O(n), nhưng B thực hiện nhiều công việc hơn khoảng 100 lần.
```

Với `n = 200,000`:

```text
    n       = 200,000 phép tính
    100n     = 20,000,000 phép tính
```

Cả hai có thể pass, nhưng thuật toán thứ hai có ít khoảng an toàn hơn.

### So Sánh Các Nhóm Tăng Trưởng Khác Nhau

Với `n = 200,000`:

```text
    100n       = 20,000,000
    n log2 n   = khoảng 3,600,000
    n^2        = 40,000,000,000
```

```text
    100n       vẫn là tuyến tính
    n log n    tăng nhanh hơn về lâu dài, nhưng nhỏ hơn ở n này
    n^2        lớn hơn quá nhiều bậc
```

Quy trình đúng không phải là “hằng số không bao giờ quan trọng.” Quy trình đúng là:

1. Loại nhóm tăng trưởng sai trước.
2. So sánh hằng số giữa các thuật toán có nhóm tăng trưởng phù hợp.
3. Benchmark khi kết quả gần sát giới hạn.

### Hằng Số Đến Từ Nhiều Nguồn

Hệ số thực tế bao gồm:

* Số instruction trong vòng lặp trong
* Chi phí gọi hàm
* Chi phí băm
* Cấp phát bộ nhớ
* Cache
* Input/output
* Chi phí của trình thông dịch Python
* Các thao tác cấu trúc dữ liệu ẩn bên trong thư viện

```text
    phép cộng số nguyên đơn giản       hằng số nhỏ
    tra cứu dictionary                  hằng số lớn hơn, O(1) trung bình
    cắt một slice                       cấp phát + O(k log k) nếu sort tiếp
    print trong mỗi vòng lặp            chi phí thực tế rất lớn
```

---

## 8. Time Limit Và Ước Lượng Phép Tính

Big O không cung cấp công thức chính thức để đổi số phép tính thành số giây. Không có quy tắc toàn cầu như “đúng `10^8` phép tính luôn bằng một giây.”

Một kinh nghiệm thường được nhắc trong thi đấu là khoảng `10^7` đến `10^8` phép tính đơn giản mỗi giây có thể khả thi trên một số môi trường chấm, nhưng con số này thay đổi mạnh theo ngôn ngữ, thao tác, compiler, phần cứng và time limit.

Hãy coi đây là thang cảnh báo, không phải cam kết:

```text
    thời gian ước lượng ~= khối lượng công việc / tốc độ môi trường
```

### Vì Sao `O(n^2)` Nguy Hiểm Với `n = 200,000`?

```python
for i in range(n):
    for j in range(n):
        do_constant_work()
```

Thân vòng lặp chạy:

```text
    200,000 * 200,000
    = 40,000,000,000 lần
```

Ngay cả nếu môi trường xử lý được `10^8` vòng lặp đơn giản mỗi giây, thời gian sẽ xấp xỉ:

```text
    40,000,000,000 / 100,000,000
    = 400 giây
```

Hầu hết time limit của cuộc thi nhỏ hơn rất nhiều. Tốc độ chính xác không quan trọng ở đây vì khoảng cách đã quá lớn.

### Xem Time Limit Như Một Ngân Sách

```text
    time limit
        |
        v
    ngân sách thực tế
        |
        +--> đọc input
        +--> công việc thuật toán
        +--> output
        +--> khoảng an toàn
```

Nếu time limit là 2 giây, đừng thiết kế thuật toán cần dùng hết ngân sách lý thuyết. Hãy chừa chỗ cho đọc dữ liệu, cấp phát và overhead của ngôn ngữ.

---

## 9. Chi Phí Ẩn Trong Python

Vòng lặp nhìn thấy chưa chắc là độ phức tạp thật. Một dòng code có thể chứa một vòng lặp bên trong.

| Thao tác Python | Độ phức tạp thường gặp | Cảnh báo khi thi |
|:---|:---:|:---|
| `numbers[i]` | `O(1)` | Truy cập list trực tiếp |
| `numbers.append(x)` | Khấu hao `O(1)` | Đôi lúc phải resize |
| `numbers.pop()` | `O(1)` | Xóa phần tử cuối |
| `numbers.pop(0)` | `O(n)` | Dịch toàn bộ phần tử còn lại |
| `x in numbers` | `O(n)` | Quét list |
| `x in my_set` | Trung bình `O(1)` | Tra cứu hash |
| `x in my_dict` | Trung bình `O(1)` | Tra cứu hash |
| `numbers.sort()` | `O(n log n)` | Sort tại chỗ |
| `sorted(numbers)` | `O(n log n)` | Tạo list mới |
| `numbers[a:b]` | `O(b-a)` | Sao chép slice |
| Lặp `text += piece` | Có thể rất tốn | Dùng list và `join` |
| `print(...)` trong vòng lặp lớn | Phụ thuộc kích thước output | Nên gom output |

### Mẫu Quadratic Ẩn

Code này nhìn như hai thao tác đơn giản:

```python
for value in numbers:
    if value in numbers:
        print(value)
```

Nhưng `value in numbers` là `O(n)`:

```text
    vòng ngoài:          n
    kiểm tra membership: n cho mỗi vòng ngoài

    n * n = O(n^2)
```

Nếu bài cho phép, hãy dùng set:

```python
seen = set(numbers)

for value in numbers:
    if value in seen:
        print(value)
```

Phép kiểm tra membership trở thành trung bình `O(1)`, nên toàn bộ lượt quét là trung bình `O(n)`.

### `pop(0)` Trong Queue

```python
while items:
    current = items.pop(0)
```

Nếu list có `n` phần tử, chi phí dịch là:

```text
    (n - 1) + (n - 2) + ... + 1
    = O(n^2)
```

Dùng `collections.deque` cho queue hiệu quả:

```python
from collections import deque

items = deque(values)
while items:
    current = items.popleft()
```

---

## 10. Nhiều Test Case

Luôn nhân độ phức tạp của một test case với số test case, trừ khi đề cho giới hạn tổng kích thước.

### Mỗi Test Case Đều Có Giới Hạn Lớn Nhất

```text
    T <= 10
    n <= 200,000 cho mỗi test case
    thuật toán = O(n)

    tổng công việc <= 10 * 200,000
                      = 2,000,000
```

Với thuật toán `O(n^2)`:

```text
    10 * (200,000)^2
    = 400,000,000,000 phép tính
```

### Giới Hạn Tổng

Nhiều đề thay vào đó ghi:

```text
    T <= 200,000
    tổng n của tất cả test case <= 200,000
```

Khi đó tổng kích thước đầu vào bị giới hạn:

```text
    n1 + n2 + n3 + ... + nT <= 200,000
```

Thuật toán `O(n)` mỗi case vẫn là `O(sum(n))` cho toàn bộ input:

```text
    O(n1) + O(n2) + ... + O(nT)
    = O(sum(n))
    = O(200,000)
```

Nhưng thuật toán `O(n^2)` cho mỗi case không tự động an toàn. Tổng bình phương vẫn có thể rất lớn:

```text
    một case có 200,000:
    (200,000)^2 = 40,000,000,000
```

### Minh Họa Test Case

```text
    Case 1: [---------] n1
    Case 2: [---]     n2
    Case 3: [------]  n3
    ...
    tổng:   n1 + n2 + n3 + ... <= giới hạn
```

Hãy xem giới hạn áp dụng cho từng case hay cho tổng của tất cả case.

---

## 11. Trường Hợp Xấu Nhất Bao Phủ Mọi Đầu Vào Hợp Lệ

Khi đề yêu cầu chương trình chạy được với mọi input hợp lệ, hãy phân tích trường hợp xấu nhất.

```python
    for value in numbers:
        if value == target:
            return True
    return False
```

Trường hợp tốt nhất:

```text
    target ở đầu list -> O(1)
```

Trường hợp xấu nhất:

```text
    target không có hoặc ở cuối -> O(n)
```

Thuật toán được mô tả là `O(n)` vì máy chấm có thể đưa vào input xấu nhất hợp lệ.

### Early Exit Không Tự Động Đổi Big O

```python
for i in range(n):
    for j in range(n):
        if answer_found:
            return result
```

Nếu `answer_found` có thể vẫn false cho đến vòng lặp cuối, trường hợp xấu nhất vẫn là `O(n^2)`.

```text
    input may mắn:       dừng sớm
    input đối kháng:     đi qua toàn bộ không gian tìm kiếm
                          ^
                          độ phức tạp phải bao phủ trường hợp này
```

Early exit có thể cải thiện trường hợp trung bình, nhưng chỉ cải thiện Big O xấu nhất nếu code đảm bảo giới hạn nhỏ hơn với mọi input.

---

## 12. Độ Phức Tạp Không Gian Và Memory Limit

Thời gian không phải tài nguyên duy nhất. Hãy ước lượng bộ nhớ phụ theo kích thước input.

| Cấu trúc | Không gian phụ |
|:---|---:|
| Một vài biến | `O(1)` |
| Set chứa mọi giá trị | `O(n)` |
| Mảng prefix sum | `O(n)` |
| Adjacency list | `O(V + E)` |
| Adjacency matrix | `O(V^2)` |
| Bảng DP có `n` trạng thái | `O(n)` |
| Bảng DP hai chiều | `O(nm)` |
| Độ sâu đệ quy `n` | `O(n)` call stack |

### Minh Họa Bộ Nhớ

```text
    Mảng input:        [--------------------]  O(n) input
    Bản sao set:       {--------------------}  O(n) phụ
    Mảng prefix:       [--------------------]  O(n) phụ

    Tổng bộ nhớ phụ = hai cấu trúc bổ sung kích thước n
```

Với `n = 2 * 10^5`, một mảng `O(n)` thường hợp lý, nhưng kiểu phần tử và cách biểu diễn của ngôn ngữ rất quan trọng. Số nguyên và reference trong Python tốn nhiều bộ nhớ hơn số nguyên trong C++.

### Cảnh Báo Matrix

Nếu `V = 2 * 10^5`, adjacency matrix cần xấp xỉ:

```text
    V^2 = 40,000,000,000 ô
```

Điều này không thể chạy với memory limit thông thường. Hãy dùng adjacency list cho đồ thị thưa.

---

## 13. Ví Dụ Thi Đấu Có Phân Tích

### Ví Dụ A: Phát Hiện Phần Tử Trùng

Giới hạn:

```text
1 <= n <= 2 * 10^5
```

Cách ngây thơ:

```python
for i in range(n):
    for j in range(i + 1, n):
        if numbers[i] == numbers[j]:
            return True
```

Độ phức tạp:

```text
    O(n^2)
    công việc tối đa ~= 40,000,000,000 phép so sánh
    có khả năng quá chậm
```

Cách dùng hash set:

```python
seen = set()

for number in numbers:
    if number in seen:
        return True
    seen.add(number)

return False
```

Độ phức tạp:

```text
    thời gian trung bình: O(n)
    không gian phụ:        O(n)
```

Giới hạn gợi ý đổi bộ nhớ lấy thời gian.

### Ví Dụ B: Pair Sum Với Sort

Giới hạn:

```text
n <= 2 * 10^5
```

Sort trước, sau đó dùng hai con trỏ:

```python
numbers.sort()
left = 0
right = len(numbers) - 1

while left < right:
    current = numbers[left] + numbers[right]

    if current == target:
        return True
    if current < target:
        left += 1
    else:
        right -= 1

return False
```

```text
    sort:       O(n log n)
    quét:       O(n)
    tổng:       O(n log n)
    không gian: phụ thuộc sort và cách cài đặt
```

Hai con trỏ chỉ tiến vào trong:

```text
    left  -> -> ->
    [ 1  3  4  7  9  12 ]
                    <- <- right

    mỗi con trỏ di chuyển nhiều nhất n lần tổng cộng
```

### Ví Dụ C: Truy Vấn Tổng Đoạn

Giới hạn:

```text
n <= 2 * 10^5
q <= 2 * 10^5
```

Nếu mỗi query quét toàn bộ mảng:

```text
    O(nq) = khoảng 40,000,000,000 phép tính
```

Dùng prefix sum:

```python
prefix = [0]

for number in numbers:
    prefix.append(prefix[-1] + number)

def range_sum(left, right):
    return prefix[right + 1] - prefix[left]
```

Độ phức tạp:

```text
    tiền xử lý: O(n)
    mỗi query:  O(1)
    mọi query:  O(n + q)
```

### Ví Dụ D: Duyệt Đồ Thị

Giới hạn:

```text
V <= 2 * 10^5
E <= 2 * 10^5
```

DFS hoặc BFS với adjacency list:

```text
    O(V + E)
```

Adjacency matrix sẽ cần:

```text
    O(V^2)
```

vượt xa giới hạn khi `V = 200,000`.

---

## 14. Chọn Thuật Toán Từ Đề Bài

Hãy đi theo quy trình:

```text
    Đọc n, T, miền giá trị, time limit, memory limit
                         |
                         v
    Ước lượng công việc tối đa của cách làm trực tiếp
                         |
                 +-------+-------+
                 |               |
              đủ nhỏ?          quá lớn?
                 |               |
                 v               v
          cài đặt nó          tìm công việc lặp lại
                                  |
                                  v
       hash? sort? prefix sum? hai con trỏ? heap? DP?
                                  |
                                  v
                         tính lại độ phức tạp
```

### Các Mẫu Thay Thế

| Mẫu chậm | Cách thay thế thường dùng |
|:---|:---|
| Tìm membership lồng nhau | Set hoặc dictionary |
| Tính tổng đoạn nhiều lần | Prefix sum |
| So sánh mọi cặp trên dữ liệu đã sort | Hai con trỏ |
| Tìm min/max lặp lại | Heap |
| Tính lại trạng thái đệ quy | Memoization hoặc DP bottom-up |
| Tạo substring lặp lại | Dùng index, cấu trúc prefix, hoặc list và `join` |
| Queue dùng `pop(0)` | `collections.deque` |
| Quét đồ thị lặp lại | Adjacency list và traversal |
| So sánh mọi interval | Sort, sweep line, hoặc cấu trúc interval |

---

## 15. Benchmark: Hữu Ích Nhưng Không Phải Bằng Chứng

Benchmark tại máy cá nhân có thể cho thấy hằng số và lỗi cài đặt, nhưng không thay thế phân tích độ phức tạp.

```python
from time import perf_counter

start = perf_counter()
answer = solve(input_data)
elapsed = perf_counter() - start

print(f"elapsed: {elapsed:.3f}s")
```

### Vì Sao Đo Thời Gian Cục Bộ Có Thể Gây Nhầm?

```text
    máy cá nhân != máy chấm
    input cục bộ != input xấu nhất ẩn
    một lần chạy != tất cả test case
    cache nóng != cache lạnh
```

Dùng benchmark để so sánh hai cách đã có độ phức tạp phù hợp hoặc phát hiện hệ số quá lớn. Không dùng một input nhỏ chạy nhanh để biện minh cho thuật toán có nhóm tăng trưởng sai.

### Stress Test

Hãy tạo test gần giới hạn lớn nhất:

```text
    input nhỏ nhất       -> kiểm tra đúng/sai
    input ngẫu nhiên     -> hành vi thông thường
    input đã sort         -> bẫy pivot / trường hợp đặc biệt
    input đảo ngược       -> mẫu trường hợp xấu
    input lớn nhất        -> tốc độ và bộ nhớ
    input rỗng/tối thiểu  -> biên dữ liệu
```

---

## 16. Checklist Trước Khi Submit

Trước khi nộp bài, hãy hỏi:

```text
    [ ] n chính xác đại diện cho điều gì?
    [ ] Tôi đã đọc mọi giới hạn chưa?
    [ ] Có giới hạn số test case T không?
    [ ] Có giới hạn sum(n) không?
    [ ] Độ phức tạp thời gian xấu nhất là gì?
    [ ] Độ phức tạp không gian phụ là gì?
    [ ] Tôi đã tính chi phí ẩn như membership hoặc slicing chưa?
    [ ] Các vòng lặp lồng nhau có thật sự độc lập không?
    [ ] Các con trỏ chỉ tiến một lần theo một hướng không?
    [ ] Early exit cải thiện trường hợp xấu nhất hay chỉ trường hợp trung bình?
    [ ] Input có thể ép vòng lặp chạy tối đa không?
    [ ] Input/output có chiếm phần lớn công việc không?
    [ ] Tôi đã thử input lớn nhất có thể chưa?
```

### Ước Lượng Trong Năm Giây

Với một bài mới, hãy tính nhanh:

```text
    công việc tối đa = công thức độ phức tạp thay giới hạn lớn nhất
```

Ví dụ:

```text
    n <= 2 * 10^5
    vòng lặp lồng nhau -> n^2
    n^2 = 4 * 10^10
    loại cách làm này
```

Sau đó tìm công việc bị lặp lại và thay thế bằng cấu trúc dữ liệu hoặc thuật toán mạnh hơn.

---

## 17. Cheat Sheet Cuối Cùng

```text
    1. n là kích thước input, không phải một hằng số cố định.
    2. Giới hạn lớn nhất đại diện cho input hợp lệ khó nhất của máy chấm.
    3. Big O mô tả tăng trưởng, không mô tả số giây chính xác.
    4. Big O bỏ hằng số, nhưng hằng số có ý nghĩa trong thi đấu thực tế.
    5. Time limit và ngôn ngữ quyết định ngân sách thực tế.
    6. Tính cả công việc ẩn bên trong các thao tác thư viện.
    7. Phân tích trường hợp xấu nhất khi phải pass mọi input.
    8. Nhân với T trừ khi đề có giới hạn tổng kích thước.
    9. Kiểm tra cả thời gian và bộ nhớ.
   10. Benchmark gần giới hạn, nhưng không thay thế phân tích bằng input nhỏ.
```

### Mục Tiêu Thường Gặp Với `n <= 2 * 10^5`

```text
    ưu tiên:       O(n), O(n log n)
    đôi khi:       O(n sqrt n), tùy ngôn ngữ và time limit
    thường loại:   O(n^2), O(2^n)
```

Mục tiêu không phải là ghi nhớ một con số phép tính mỗi giây thần kỳ. Mục tiêu là liên kết giới hạn của đề với khối lượng công việc mà source code có thể thực hiện trong trường hợp xấu nhất.

---

**Bước tiếp theo:** Hãy luyện thói quen đọc giới hạn trước, dự đoán độ phức tạp mục tiêu, sau đó giải các mẫu thi đấu kinh điển như đếm tần suất, prefix sum, binary search, hai con trỏ, sliding window, duyệt đồ thị và quy hoạch động.
