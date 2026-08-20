
---

# Kỹ thuật Circular Array và Cài đặt

## 1. Circular Array là gì?

**Circular array (mảng vòng)** lưu các giá trị trong một mảng có kích thước
thông thường, nhưng xem ô vật lý cuối cùng như được nối với ô vật lý đầu tiên.
Phần tử đầu theo thứ tự logic không bắt buộc phải nằm ở index vật lý `0`.

Cấu trúc theo dõi ba trạng thái:

* `head` — ô vật lý chứa index logic `0`
* `size` — số giá trị hiện đang được lưu
* `capacity` — số ô vật lý đang tồn tại

Công thức ánh xạ quan trọng là:

```text
    physical_index = (head + logical_index) % capacity
```

Cài đặt trong `CircularArray.py` dùng kỹ thuật này để hỗ trợ `append`,
`appendleft`, `pop` và `popleft` mà không phải dịch chuyển mọi giá trị.

---

## 2. Nó giải quyết vấn đề gì?

List thông thường của Python rất tốt cho việc truy cập theo index, nhưng chèn
vào đầu yêu cầu các giá trị hiện có phải dịch sang phải.

```text
    MẢNG THÔNG THƯỜNG: appendleft(5)

    trước:      [ 10 ][ 20 ][ 30 ][ 40 ]
    sau:        [  5 ][ 10 ][ 20 ][ 30 ][ 40 ]
                     <---- mọi giá trị cũ đều dịch ---->
```

Nếu dùng cấu trúc như một queue, việc liên tục xóa ở index `0` cũng có thể
đắt:

```text
    popleft() trên list thông thường:

    [ 10 ][ 20 ][ 30 ][ 40 ][ 50 ]
       X    [ 20 ][ 30 ][ 40 ][ 50 ]  <- các giá trị dịch sang trái
```

Circular array chỉ di chuyển ranh giới logic:

```text
    popleft() trên circular array:

    trước:  head -> [ 10 ][ 20 ][ 30 ][ 40 ][    ]
    sau:            [    ][ 20 ][ 30 ][ 40 ][    ]
                             head ->
```

Các giá trị vẫn nằm trong những ô vật lý của chúng. Chỉ `head` và `size` thay
đổi.

---

## 3. Thứ tự logic và vùng lưu trữ vật lý

Thứ tự logic là thứ tự mà caller nhìn thấy. Thứ tự vật lý là thứ tự của các ô
trong mảng nền. Hai thứ tự này có thể khác nhau sau khi `head` wrap.

```text
    capacity = 8
    head = 6
    size = 5

    các ô vật lý:
    index       0       1       2       3       4       5       6       7
             +-------+-------+-------+-------+-------+-------+-------+-------+
    storage  |  30   |  40   |  50   |       |       |       |  10   |  20   |
             +-------+-------+-------+-------+-------+-------+-------+-------+
                 ^       ^       ^                               ^       ^
                 |       |       |                               |       |
              logic    logic    logic                           logic   logic
                2       3       4                                0       1

    các giá trị logic: [10, 20, 30, 40, 50]
```

Các index logic được ánh xạ như sau:

```text
    logical 0 -> (6 + 0) % 8 = 6
    logical 1 -> (6 + 1) % 8 = 7
    logical 2 -> (6 + 2) % 8 = 0
    logical 3 -> (6 + 3) % 8 = 1
    logical 4 -> (6 + 4) % 8 = 2
```

Đây là lý do phép modulo là thao tác trung tâm của circular array.

---

## 4. Ba invariant

Cài đặt đúng khi các điều kiện sau luôn được giữ:

1. `0 <= size <= capacity`
2. Index logic `i` được lưu tại `(head + i) % capacity` với
   `0 <= i < size`.
3. Mọi ô nằm ngoài phạm vi logic đều rỗng hoặc không ảnh hưởng đến chuỗi công
   khai.

```text
    phạm vi logic hợp lệ:

        head                                      tail
          |                                         |
          v                                         v
    [ value ][ value ][ value ][ empty ][ empty ]
       0         1         2
```

Khi phạm vi đi qua ranh giới vật lý, nó trở thành hai phần:

```text
    [ value ][ value ][ empty ][ empty ][ value ][ value ]
       ^       ^                              ^       ^
      head    next                           ...     tail
```

Chuỗi logic vẫn là một chuỗi, dù vùng lưu trữ đã bị tách thành hai đoạn.

---

## 5. Thêm vào đầu bên phải

Với `append(value)`, ô vật lý tiếp theo là:

```text
    tail_slot = (head + size) % capacity
```

Ví dụ:

```text
    head = 6, size = 3, capacity = 8

    tail_slot = (6 + 3) % 8 = 1

    index:    0       1       2       3       4       5       6       7
            +-------+-------+-------+-------+-------+-------+-------+-------+
            |  30   | empty | empty |       |       |       |  10   |  20   |
            +-------+-------+-------+-------+-------+-------+-------+-------+
                              ghi giá trị mới vào ô 1
```

Không cần di chuyển giá trị nào. Nếu mảng đầy, cài đặt sẽ cấp phát vùng lưu
trữ lớn hơn trước rồi sao chép các giá trị theo thứ tự logic.

---

## 6. Thêm vào đầu bên trái

Với `appendleft(value)`, lùi `head` một ô:

```text
    new_head = (head - 1) % capacity
```

Phép modulo xử lý việc wrap từ ô `0` sang ô cuối cùng:

```text
    head = 0, capacity = 8
    new_head = (0 - 1) % 8 = 7

    index:    0       1       2       3       4       5       6       7
            +-------+-------+-------+-------+-------+-------+-------+-------+
            |  10   |  20   |  30   |       |       |       |       |  new  |
            +-------+-------+-------+-------+-------+-------+-------+-------+
                                                                        ^
                                                                      head
```

Đây là phiên bản circular-array của thao tác prepend trong deque.

---

## 7. Resize mà không làm mất thứ tự logic

Khi circular array động đầy, nó tăng gấp đôi capacity. Các giá trị được sao
chép từ index logic `0` trở đi vào vùng lưu trữ mới:

```text
    vùng lưu trữ cũ, đã wrap:

        head -> [ 40 ][ 50 ][    ][    ][ 10 ][ 20 ][ 30 ]
                  3     4                 0     1     2

    vùng lưu trữ mới, đã chuẩn hóa:

        head -> [ 10 ][ 20 ][ 30 ][ 40 ][ 50 ][    ][    ][    ]
                  0     1     2     3     4
```

Sau khi resize, `head` trở thành `0`. Các giá trị không bị sắp xếp hoặc thay
đổi; chỉ bố cục vật lý của chúng được chuẩn hóa.

Cài đặt cũng thu nhỏ vùng lưu trữ khi phần lớn capacity không còn được dùng,
nhưng không bao giờ nhỏ hơn capacity ban đầu truyền cho constructor.

---

## 8. Các ý tưởng cốt lõi trong cài đặt

### Constructor

```python
numbers = CircularArray[int](capacity=4)
```

Constructor tạo bốn ô vật lý, đặt `head = 0` và bắt đầu với `size = 0`.

### Truy cập theo index logic

```python
value = numbers[index]
numbers[index] = replacement
```

Cả hai thao tác đều kiểm tra index logic trước, sau đó dịch nó bằng công thức
`(head + index) % capacity`.

### Các thao tác Queue và Deque

```python
numbers.append(value)       # đầu bên phải
numbers.appendleft(value)    # đầu bên trái
numbers.pop()                # xóa đầu bên phải
numbers.popleft()            # xóa đầu bên trái
```

Các thao tác ở đầu trái cập nhật `head`; các thao tác ở đầu phải tính ô tail
từ `head` và `size`.

---

## 9. Tham chiếu Python đầy đủ

Toàn bộ cài đặt nằm trong `CircularArray.py`. Giao diện công khai có dạng:

```python
class CircularArray(Generic[T]):
    def append(self, value: T) -> None: ...
    def appendleft(self, value: T) -> None: ...
    def pop(self) -> T: ...
    def popleft(self) -> T: ...
    def clear(self) -> None: ...
    def to_list(self) -> List[T]: ...
```

Class cũng hỗ trợ `len(array)`, `array[index]`, index âm, iteration,
`capacity`, `size`, `head_index` và `debug_slots()`.

---

## 10. Độ phức tạp

| Thao tác | Độ phức tạp thường gặp | Lý do |
|:---|:---:|:---|
| Tra cứu index | `O(1)` | Một phép tính modulo |
| Cập nhật index | `O(1)` | Ghi một ô vật lý |
| `append` | `O(1)` amortized | Ghi một ô; resize chỉ xảy ra định kỳ |
| `appendleft` | `O(1)` amortized | Di chuyển `head` một ô |
| `pop` | `O(1)` amortized | Xóa ô tail |
| `popleft` | `O(1)` amortized | Xóa ô head |
| Resize | `O(n)` | Sao chép các giá trị theo thứ tự logic |
| Tìm theo giá trị | `O(n)` | Không có đảm bảo tìm kiếm có thứ tự |
| Bộ nhớ phụ | `O(capacity)` | Mảng nền và metadata |

Từ **amortized** rất quan trọng. Một lần `append` gây resize có thể là
`O(n)`, nhưng vì capacity tăng gấp đôi nên resize xảy ra không thường xuyên.
Do đó, một chuỗi dài các lần append có chi phí trung bình `O(1)` mỗi lần.

---

## 11. Trace ví dụ: Wrap ở ranh giới

Bắt đầu với capacity `4`:

```text
    append(10), append(20), append(30)

    head = 0, size = 3
    slots = [ 10 ][ 20 ][ 30 ][    ]
```

Xóa giá trị ở đầu:

```text
    popleft()

    returned = 10
    head = 1, size = 2
    slots = [    ][ 20 ][ 30 ][    ]
```

Thêm giá trị ở bên phải. Tail wrap về ô `0`:

```text
    append(40), append(50)

    head = 1, size = 4
    slots = [ 50 ][ 20 ][ 30 ][ 40 ]
                ^                 ^
              logical 1        logical 3

    logical values = [20, 30, 40, 50]
```

Mảng đã đầy, nhưng chuỗi không liên tục về mặt vật lý nếu bắt đầu từ index
`0`. Đây là hành vi chính mà kỹ thuật này cung cấp.

---

## 12. Các lỗi thường gặp

### Lỗi 1: Dùng `size` như một index vật lý

`size` cho biết có bao nhiêu giá trị tồn tại. Nó không nhất thiết là ô tail vật
lý. Luôn dùng `(head + size) % capacity` cho vị trí tiếp theo ở đầu phải.

### Lỗi 2: Quên modulo khi cập nhật `head`

```python
self._head = self._head - 1       # có thể trở thành -1
self._head = (self._head - 1) % capacity  # wrap chính xác
```

### Lỗi 3: Sao chép thứ tự vật lý khi resize

Sao chép trực tiếp `data[0:]` có thể làm thay đổi thứ tự logic. Hãy lặp từ
index logic `0` đến `size - 1`.

### Lỗi 4: Nhầm trạng thái rỗng và đầy

Chỉ với `head` và `tail`, buffer rỗng và buffer đầy có thể trông giống nhau.
Theo dõi `size` sẽ loại bỏ sự mơ hồ này.

### Lỗi 5: Nghĩ rằng circular có nghĩa là đã sắp xếp

Circular array giữ nguyên thứ tự chèn. Nó không tự động cung cấp binary search
hoặc truy cập theo thứ tự tăng dần.

---

## 13. Nó hữu ích ở đâu?

```text
    +---------------------------------------------------------------+
    | CÁC USE CASE CỦA CIRCULAR ARRAY                              |
    +---------------------------------------------------------------+
    | Queue / deque             -> thêm, xóa ở cả hai đầu          |
    | Ring buffer               -> giữ lịch sử mới nhất             |
    | Sliding window            -> hết hạn hoặc ghi đè giá trị cũ   |
    | Producer / consumer       -> buffer stream có giới hạn       |
    | Round-robin scheduling    -> lặp qua các ô theo vòng          |
    +---------------------------------------------------------------+
```

Nếu queue có kích thước tối đa đã biết, circular array cố định có thể tránh
hoàn toàn việc resize động. Cài đặt hiện tại là dynamic để dễ tái sử dụng
trong các chương trình Python tổng quát.

---

## 14. Chạy ví dụ

Chạy:

```text
python CircularArray.py
```

Output kỳ vọng:

```text
Logical values: [20, 30, 40, 50]
Physical slots: [50, 20, 30, 40]
Head index: 1
After both-end operations: [20, 30, 40]
Capacity: 8
```

Các ô vật lý hiển thị `[50, 20, 30, 40]`, trong khi chuỗi logic bắt đầu tại
`head index = 1`. Sự khác biệt này chính là biểu diễn circular.

---

## 15. Cheat Sheet cuối cùng

```text
    1. Theo dõi head, size và capacity.
    2. Ánh xạ i logic bằng (head + i) % capacity.
    3. Append bên phải tại (head + size) % capacity.
    4. Append bên trái bằng cách lùi head theo modulo capacity.
    5. Resize bằng cách sao chép thứ tự logic, không phải thứ tự vật lý thô.
    6. Theo dõi size để phân biệt rõ trạng thái rỗng và đầy.
    7. Thao tác ở hai đầu là O(1) amortized; resize là O(n).
```

**Bước tiếp theo:** Tự trace một queue sau nhiều thao tác `popleft` và
`append`, sau đó xem `debug_slots()` để liên hệ index logic với vùng lưu trữ
vật lý.
