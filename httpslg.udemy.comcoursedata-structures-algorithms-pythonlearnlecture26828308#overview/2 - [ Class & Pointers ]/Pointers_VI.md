
---

# Pointers (Con trỏ và tham chiếu)

## 1. Tham chiếu trong Python

Trong các bài học về cấu trúc dữ liệu, từ **con trỏ (pointer)** thường chỉ một giá trị cho phép biến hoặc đối tượng truy cập đến một đối tượng khác. Python không cung cấp phép tính con trỏ kiểu C hay toán tử giải tham chiếu (dereference) rõ ràng. Thay vào đó, biến Python là **tên được liên kết với đối tượng (names bound to objects)**, và các liên kết đó hoạt động như tham chiếu.

Mô hình thực tế là:

1. Một đối tượng tồn tại ở đâu đó trong bộ nhớ.
2. Một tên tham chiếu đến đối tượng đó.
3. Phép gán thay đổi đối tượng mà một tên tham chiếu tới.
4. Phép biến đổi (mutation) thay đổi nội dung của chính một đối tượng có thể biến đổi.

Mô hình này giải thích vì sao `dict2 = dict1` khiến thay đổi được nhìn thấy qua cả hai tên, trong khi `num2 = 22` không làm đổi `num1`.

```
     tên                       đối tượng trong bộ nhớ
     +---------+              +----------------+
     | biến     | ------------> | giá trị/trạng thái|
     +---------+              +----------------+

     Hai tên có thể trỏ đến một đối tượng:

     tên_a --------------------+
                              v
                         +------------+
     tên_b ---------------->| đối tượng  |
                         +------------+
```

Ở đây “trỏ” mô tả khả năng truy cập; mã Python không thể cộng `1` vào địa chỉ, tự giải phóng đối tượng hoặc giải tham chiếu địa chỉ như số nguyên.

---

## 2. Vì sao tham chiếu dùng chung quan trọng?

Cấu trúc dữ liệu liên kết cần các đối tượng tham chiếu đến đối tượng khác. Linked list không chỉ là một hàng các giá trị độc lập; mỗi node phải biết node nào đứng sau. Node của tree phải truy cập các node con. Vertex của graph phải truy cập các đỉnh lân cận.

Nếu mỗi liên kết sao chép toàn bộ đối tượng đích, một cập nhật nhỏ có thể phải sao chép cả cấu trúc lớn và làm mất ý nghĩa của danh tính đối tượng. Thay vào đó, tham chiếu dùng chung lưu một quan hệ đến đối tượng đã tồn tại.

```
     Kết nối trong linked list

     head
      |
      v
     +---------+       +---------+       +---------+
     | value=10| next->| value=20| next->| value=30|
     +---------+       +---------+       +---------+
                                              next -> None

     Các mũi tên là tham chiếu được lưu trong node.
     Các node vẫn là những đối tượng riêng có danh tính ổn định.
```

Tham chiếu dùng chung cho phép đổi liên kết, biểu diễn cạnh đồ thị mà không sao chép đỉnh và để nhiều nơi quan sát một bản ghi có thể biến đổi. Trách nhiệm là mutation qua alias nào cũng được alias kia nhìn thấy.

---

## 3. Phép gán, liên kết và liên kết lại

Câu lệnh như `num2 = num1` tính vế phải rồi liên kết tên bên trái với cùng đối tượng. Nó không yêu cầu đối tượng tự sao chép.

Câu lệnh sau `num2 = 22` là **liên kết lại (rebinding)**. Nó khiến `num2` trỏ sang một đối tượng số nguyên khác. Nó không chỉnh sửa đối tượng số nguyên mà `num1` từng truy cập.

```
     Sau num1 = 11

     num1 ---------------------> [ số nguyên 11 ]

     Sau num2 = num1

     num1 ---------------------> [ số nguyên 11 ] <---------------- num2

     Sau num2 = 22

     num1 ---------------------> [ số nguyên 11 ]
     num2 ---------------------> [ số nguyên 22 ]
```

Một tên có thể được liên kết lại mà không đổi đối tượng; muốn đổi đối tượng phải dùng mutation mà kiểu đó hỗ trợ, như gán khóa dictionary hoặc thêm phần tử list. Python truyền tham chiếu đối tượng bằng phép gán, nên bên gọi thấy mutation nhưng không thấy việc liên kết lại tham số cục bộ.

---

## 4. Ví dụ số nguyên: đối tượng bất biến

Nửa đầu của `Pointers.py` dùng số nguyên. Số nguyên là **bất biến (immutable)**: sau khi đối tượng biểu diễn `11` được tạo, Python không biến nó thành `22`; `num2 = 22` liên kết `num2` với đối tượng số nguyên khác.

Trước khi cập nhật, trong mô hình khái niệm cả hai tên truy cập cùng một đối tượng số nguyên. Vì vậy, hai lệnh `id()` tại thời điểm đó in cùng một danh tính.

```
     TRƯỚC num2 = 22:  num1 ----+
                                  v
                              [ int: 11 ]
                                  ^
                          num2 ----+

     SAU num2 = 22:    num1 -> [ int: 11 ]
                        num2 -> [ int: 22 ]
     Phép gán đổi mũi tên num2, không đổi int:11.
```

Địa chỉ cụ thể phụ thuộc cách triển khai; điều ổn định cần nhớ là quan hệ danh tính ở từng giai đoạn.

---

## 5. `id()` chứng minh danh tính


Mã nguồn in danh tính trước và sau mỗi phép gán:

```
     TRƯỚC KHI LIÊN KẾT LẠI SỐ NGUYÊN
     num1 value = 11       num1 id = X
     num2 value = 11       num2 id = X
                                      ^ cùng đối tượng

     SAU KHI LIÊN KẾT LẠI SỐ NGUYÊN
     num1 value = 11       num1 id = X
     num2 value = 22       num2 id = Y
                                      ^ thường X != Y
```

`id()` chứng minh aliasing khi hai tên trả về cùng danh tính tại cùng thời điểm. Nó không chứng minh hai đối tượng có nội dung bằng nhau. Ngược lại, hai giá trị bất biến bằng nhau có thể là hai đối tượng khác nhau, dù Python có thể tái sử dụng hoặc intern một số giá trị.

Trong kiểm tra thông thường, dùng `is` cho câu hỏi cùng đối tượng và sentinel như `None`; dùng `==` cho nội dung bằng nhau. Hai giá trị bất biến bằng nhau vẫn có thể là hai đối tượng khác nhau.

---

## 6. Ví dụ dictionary: aliasing và mutation

Phần thứ hai tạo một dictionary rồi liên kết hai tên với nó. `dict1` và `dict2` là **bí danh (alias)**, tức hai tên của cùng đối tượng. Dictionary có thể biến đổi (mutable), nên `dict2['value'] = 22` thay đổi dictionary thay vì liên kết lại `dict2`.

```
     TRƯỚC: dict1 ---+
                      v
                 [ {'value': 11} ]
                      ^
              dict2 --+

     SAU:    dict1 ---+
                      v
                 [ {'value': 22} ]
                      ^
              dict2 --+
     id(dict1) == id(dict2); đối tượng bị biến đổi.
```

Hành vi này có chủ ý và hữu ích khi nhiều phần của chương trình cần chia sẻ một bản ghi có thể đổi. Nó cũng là nguồn lỗi phổ biến khi lập trình viên tưởng `dict2 = dict1` tạo ra bản sao độc lập.

---

## 7. Liên kết lại và biến đổi

Hai thao tác trông gần giống nhau trong mã nhưng có tác động khác nhau.

| Thao tác | Điều thay đổi? | Alias quan sát gì? |
|:---|:---|:---|
| `name = other` | Liên kết của tên | Chỉ tên bị liên kết lại trỏ nơi khác |
| `name[key] = value` | Nội dung đối tượng có thể biến đổi | Mọi alias thấy phép biến đổi |
| `name = name + [value]` | Thường tạo list mới rồi liên kết lại | Alias khác giữ list cũ |

So sánh hai nhóm thao tác trên list:

```python
items_a = [1, 2]
items_b = items_a
items_b.append(3)

items_c = [1, 2]
items_d = items_c
items_d = items_d + [3]
```

Trong cặp đầu, cả hai tên thấy `[1, 2, 3]`. Trong cặp sau, `items_d` trỏ đến list mới còn `items_c` vẫn trỏ đến `[1, 2]`.

```
     BIẾN ĐỔI: append                  LIÊN KẾT LẠI: + tạo list
     a ----+                            c -----> [1, 2]
           v                            d -----> [1, 2, 3]
       [1, 2, 3]                        (đối tượng cũ và mới khác nhau)
     b ----+
```

Khi gỡ lỗi vấn đề tham chiếu, trước hết hãy hỏi: “Câu lệnh đã sửa đối tượng hay chỉ đổi tên đang liên kết?” Câu hỏi này thường chỉ ra ngay vì sao biến khác có hoặc không đổi.

---

## 8. Sơ đồ bộ nhớ trước và sau khi đổi dictionary

Sơ đồ từng bước giúp dự đoán kết quả của `Pointers.py`. Trạng thái trước là alias do `dict2 = dict1` tạo; trạng thái sau đến từ `dict2['value'] = 22`.

```
     TRƯỚC KHI BIẾN ĐỔI                SAU KHI BIẾN ĐỔI
     dict1 ---+                         dict1 ---+
              v                                  v
         +-------------+                    +-------------+
         | D: value=11 |                    | D: value=22 |
         +-------------+                    +-------------+
              ^                                  ^
     dict2 ---+                         dict2 ---+

     id(dict1) == id(dict2) ở cả hai trạng thái; chỉ nội dung D đổi.
```

Danh tính của dictionary giữ nguyên trong khi nội dung đổi. Đây chính là mẫu được dùng khi một node lưu tham chiếu đến đối tượng lân cận có thể biến đổi: liên kết giữ nguyên, còn trạng thái của đối tượng được truy cập có thể đổi.

---

## 9. Nối các node bằng `next`

Linked list dùng cùng hành vi tham chiếu với các thể hiện của lớp. `next` là thuộc tính có giá trị là một đối tượng `Node` khác hoặc `None`.

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


first = Node(10)
second = Node(20)
first.next = second
```

Phép gán `first.next = second` không sao chép `second`. Nó lưu một tham chiếu đến đối tượng đã tồn tại bên trong `first`.

```
     first ------------------+
                              v
     +----------------+   +----------------+
     | Node A          |   | Node B          |
     | value: 10       |   | value: 20       |
     | next -----------|-->| next: None      |
     +----------------+   +----------------+
                              ^
     second ------------------+
```

Bây giờ `first.next` và `second` truy cập cùng một node. Nếu đổi `second.value`, phép duyệt từ `first` cũng thấy giá trị đó vì nó đi đến cùng đối tượng.

Đây là cầu nối cốt lõi từ biến và dictionary đến linked list, tree và graph. Một kết nối là một thuộc tính chứa tham chiếu.

---

## 10. Mã `Pointers.py` thực tế

Đoạn dưới đây là toàn bộ tệp nguồn dùng trong bài học. Nó minh họa liên kết lại số nguyên trước, sau đó minh họa aliasing và mutation của dictionary.

```python
num1 = 11

num2 = num1

print("Before num2 value is updated:")
print("num1 =", num1)
print("num2 =", num2)

print("\nnum1 points to:", id(num1))
print("num2 points to:", id(num2)) 

num2 = 22 

print("\nAfter num2 value is updated:")
print("num1 =", num1)
print("num2 =", num2) 

print("\nnum1 points to:", id(num1))
print("num2 points to:", id(num2))


#####################################


dict1 = {
         'value': 11
        }

dict2 = dict1 

print("\n\nBefore value is updated:")
print("dict1 =", dict1)
print("dict2 =", dict2)

print("\ndict1 points to:", id(dict1))
print("dict2 points to:", id(dict2)) 

dict2['value'] = 22

print("\nAfter value is updated:")
print("dict1 =", dict1)
print("dict2 =", dict2) 

print("\ndict1 points to:", id(dict1))
print("dict2 points to:", id(dict2))

```

### Mã chương trình thể hiện điều gì?

Giai đoạn số nguyên in `11` và `22` sau khi chỉ liên kết lại `num2`. Giai đoạn dictionary tạo alias, biến đổi một đối tượng dùng chung và in `{'value': 22}` qua cả hai tên.

```
     integer:    num1 -> 11       num2 -> 22  (sau rebinding)
     dictionary: dict1 --+        dict2 --+   (sau mutation)
                           v                v
                          {'value': 22}
```

Các danh tính số do `id()` in ra có thể khác giữa các lần chạy. Điều cần quan sát là chúng bằng hay khác nhau trong từng giai đoạn.

---

## 11. Các lỗi tham chiếu thường gặp

### Alias ngoài ý muốn

Viết `backup = current` không tạo bản sao của đối tượng có thể biến đổi. Nó tạo thêm một tên cho cùng đối tượng.

```
     backup = current       # hai tên, một đối tượng có thể đổi
     backup['x'] = 9         # current cũng thấy thay đổi
```

Khi cần trạng thái độc lập, hãy shallow copy hoặc deep copy có chủ đích; shallow copy vẫn có thể chia sẻ giá trị lồng nhau. Giá trị mặc định mutable cũng dùng chung giữa các lần gọi, nên dùng `None` làm sentinel và tạo đối tượng mới trong hàm.

### Làm mất head của list

Liên kết lại biến duy nhất truy cập head của linked list có thể làm phần còn lại không thể truy cập. Giữ một tham chiếu `head` ổn định khi di chuyển con trỏ tạm.

```
     duyệt an toàn:
     head -> Node(10) -> Node(20) -> None
     current ---------> Node(10)
     current = current.next      # head vẫn truy cập được list
```

### Chu trình và duyệt vô hạn

Nếu tham chiếu `next` trỏ ngược lại, phép duyệt không có kiểm tra chu trình hoặc tập visited có thể không bao giờ tới `None`.

```
     Node A -> Node B -> Node C
        ^                   |
        +-------------------+
     Chu trình: không có điểm kết thúc None tự nhiên
```

### Bằng nhau và tham số cục bộ

Hai dictionary có thể có nội dung bằng nhau nhưng danh tính khác nhau: dùng `==` cho nội dung và `is` cho danh tính. Hàm có thể mutate list nhận vào, nhưng rebinding tham số cục bộ không rebinding tên của bên gọi.

---

## 12. Các trường hợp sử dụng thực tế

Tham chiếu xuất hiện trong gần như mọi cấu trúc dữ liệu không tầm thường và nhiều thiết kế ứng dụng.

| Trường hợp | Quan hệ tham chiếu | Thao tác thường gặp |
|:---|:---|:---|
| Linked list | Node -> Node kế tiếp | Chèn, xóa, duyệt |
| Binary tree | Node -> con trái/phải | Tìm kiếm, chèn, đệ quy |
| Graph | Vertex -> các vertex lân cận | BFS, DFS, đường đi ngắn |
| Cache dùng chung | Nhiều tên -> một dictionary | Đọc hoặc cập nhật cache |
| Ghép đối tượng | Order -> Customer, items | Điều phối trạng thái liên quan |

```
     CÁC ĐỐI TƯỢNG ỨNG DỤNG
     +---------+       +---------+       +---------+
     | Order   |------>| Customer|       | Product |
     +----+----+       +---------+       +----^----+
          |                                  |
          +----------------------------------+
                    tham chiếu biểu diễn quan hệ
```

Khi một quan hệ có danh tính và có thể đổi độc lập, tham chiếu thường là mô hình tốt hơn sao chép toàn bộ giá trị. Khi cần các snapshot độc lập, hãy chủ động sao chép.

---

## 13. Phân tích Big O của thao tác tham chiếu

Gán tham chiếu thường chỉ đổi một liên kết tên hoặc một trường giống con trỏ, nên có thời gian `O(1)` và bộ nhớ phụ `O(1)`. Phép gán đó không duyệt hoặc sao chép cấu trúc được tham chiếu.

| Thao tác | Thời gian | Bộ nhớ phụ | Giải thích |
|:---|:---:|:---:|:---|
| `name = other` | `O(1)` | `O(1)` | Liên kết lại một tên |
| `node.next = other` | `O(1)` | `O(1)` | Lưu một tham chiếu |
| `dict2 = dict1` | `O(1)` | `O(1)` | Tạo alias, không sao chép |
| `dict2['value'] = 22` | Trung bình `O(1)` | `O(1)` | Cập nhật khóa hash table |
| `id(object)` | `O(1)` | `O(1)` | Hỏi siêu dữ liệu danh tính |
| Duyệt `n` node liên kết | `O(n)` | `O(1)` | Theo một tham chiếu mỗi node |
| Sao chép cấu trúc có `n` phần tử | Ít nhất `O(n)` | `O(n)` | Phải thăm từng phần tử/tham chiếu |

Chi phí hằng số khi nối hai node giải thích vì sao chèn vào linked list có thể hiệu quả khi đã biết vị trí chèn. Việc tìm vị trí đó vẫn có thể tốn `O(n)`.

```
     nối hai node đã biết:          O(1)
     first -> second

     tìm node thứ k trước:          O(n)
     rồi nối tại vị trí đó:         O(1)
     tổng:                          O(n)
```

---

## 14. Bảng tóm tắt và danh sách kiểm tra

### Số nguyên và dictionary

| Đặc điểm | Số nguyên `11` | Dictionary `{'value': 11}` |
|:---|:---|:---|
| Có thể biến đổi? | Không, immutable | Có, mutable |
| `b = a` | Ban đầu hai tên cùng chia sẻ đối tượng | Hai tên alias dictionary |
| `b = new_value` | Liên kết lại `b`; `a` không đổi | Liên kết lại `b` nếu là phép gán |
| `b['value'] = new_value` | Không áp dụng | Biến đổi đối tượng dùng chung |
| Alias khác thấy mutation? | Không có mutation số nguyên | Có |

### Câu hỏi khi gỡ lỗi

1. Có bao nhiêu đối tượng tồn tại?
2. Tên hoặc thuộc tính nào truy cập từng đối tượng?
3. Kiểu đó mutable hay immutable?
4. Câu lệnh liên kết lại tên hay biến đổi đối tượng?
5. Quan hệ này nên dùng chung hay nên sao chép?
6. Duyệt có tới `None` không, hay có thể tạo chu trình?
7. Chi phí thời gian và bộ nhớ khi theo các tham chiếu là bao nhiêu?

```
     vòng gỡ lỗi tham chiếu
     [tên] --> [đối tượng] --> [trạng thái có thể đổi]
        |             |                  |
        |             |                  +-- nội dung có đổi không?
        |             +--------------------- cùng id / cùng đối tượng?
        +----------------------------------- tên có bị liên kết lại không?
```

Quy tắc trung tâm rất đơn giản:

> Phép gán đổi liên kết. Phép biến đổi đổi đối tượng có thể biến đổi. Alias cùng quan sát một mutation.

Quy tắc này giải thích toàn bộ ví dụ `Pointers.py` và chuẩn bị cho việc cài đặt cấu trúc dữ liệu liên kết an toàn.

---

**Bước tiếp theo:** Định nghĩa lớp `Node` với tham chiếu `next`, sau đó cài đặt chèn và xóa trong linked list, đồng thời vẽ các mũi tên trước và sau mỗi phép biến đổi.
