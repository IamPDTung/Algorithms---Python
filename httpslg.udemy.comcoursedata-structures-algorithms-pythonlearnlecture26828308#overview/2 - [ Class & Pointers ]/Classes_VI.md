
---

# Classes (Lớp)

## 1. Tại sao mô hình hóa sự vật bằng lớp?

**Lớp (class)** là một kiểu dữ liệu do lập trình viên định nghĩa, mô tả cả dữ liệu mà một đối tượng lưu giữ và các thao tác có thể thực hiện trên dữ liệu đó. Thay vì xem mọi giá trị là những phần tử nguyên thủy không liên quan, ta có thể mô hình hóa một sự vật thành một đơn vị thống nhất.

Một đối tượng được tạo từ lớp được gọi là **thể hiện (instance)**. Lớp là bản thiết kế; thể hiện là một giá trị cụ thể được tạo theo bản thiết kế đó. Chương trình có thể tạo nhiều thể hiện từ một lớp, và mỗi thể hiện có thể giữ trạng thái khác nhau.

Đây là ý tưởng quan trọng đầu tiên của lập trình hướng đối tượng:

1. Định nghĩa một thiết kế có thể tái sử dụng một lần.
2. Tạo bao nhiêu đối tượng độc lập tùy theo nhu cầu của bài toán.
3. Để mỗi đối tượng cung cấp hành vi qua các phương thức (method).

Ví dụ, hệ thống giao hàng có thể cần hàng nghìn đối tượng `Package`. Mỗi gói có mã theo dõi và nơi nhận khác nhau, trong khi mọi gói đều có thể dùng phương thức `mark_delivered()`.

```
                    LỚP: thiết kế có thể tái sử dụng
                 +---------------------------+
                 | Package                   |
                 | dữ liệu: tracking_id      |
                 | dữ liệu: destination      |
                 | hành vi: mark_delivered   |
                 +-------------+-------------+
                               |
                 +-------------+-------------+
                 |                             |
                 v                             v
        +------------------+          +------------------+
        | đối tượng/thể hiện|         | đối tượng/thể hiện|
        | tracking_id=101  |          | tracking_id=102  |
        | destination=NY   |          | destination=LA   |
        +------------------+          +------------------+
```

---

## 2. Vì sao cần tạo kiểu dữ liệu tùy chỉnh?

Python đã có các kiểu dựng sẵn như `int`, `str`, `list`, `dict`, và `set`. Các kiểu này dùng được cho nhiều mục đích, nhưng một bài toán thực tế thường có khái niệm cụ thể hơn bất kỳ kiểu dựng sẵn nào.

Ví dụ, chương trình lưu một chiếc bánh bằng chuỗi màu. Chuỗi chứa được màu, nhưng không cho biết đó là màu của bánh và cũng không cung cấp thao tác riêng cho bánh. Một kiểu tùy chỉnh (custom type) có thể gom trạng thái và hành vi liên quan:

* **Ý nghĩa:** `Cookie('green')` truyền đạt nhiều hơn một chuỗi không có nhãn.
* **Tổ chức:** thuộc tính và phương thức của một khái niệm được đặt cùng nhau.
* **Tái sử dụng:** một định nghĩa tạo được nhiều đối tượng.
* **Đóng gói (encapsulation):** bên gọi dùng giao diện nhỏ thay vì phải biết mọi chi tiết lưu trữ.
* **Bất biến:** phương thức có thể bảo đảm những chuyển đổi hợp lệ, chẳng hạn từ chối màu không hợp lệ.
* **Kết hợp:** đối tượng có thể chứa hoặc tham chiếu đến đối tượng khác, điều rất cần cho cấu trúc dữ liệu.

Không có kiểu tùy chỉnh, chương trình thường truyền nhiều biến song song. Các biến song song dễ bị ghép nhầm:

```
     KHÔNG CÓ KIỂU TÙY CHỈNH               CÓ KIỂU TÙY CHỈNH
     ----------------------               -----------------
     cookie_color = 'green'              cookie = Cookie('green')
     cookie_size = 8                      cookie.color
     cookie_batch = 3                     cookie.get_color()
     # Biến nào thuộc về nhau?            # Một đối tượng sở hữu trạng thái

     Dữ liệu song song có thể lệch nhau.  Trạng thái và hành vi đi cùng nhau.
```

---

## 3. Lớp, đối tượng, thuộc tính và phương thức

Bốn thuật ngữ này tạo thành vốn từ được dùng trong các cấu trúc dữ liệu.

1. **Lớp (class):** định nghĩa hoặc khuôn mẫu. `Cookie` là một lớp.
2. **Đối tượng (object):** giá trị cụ thể được tạo từ lớp. `cookie_one` tham chiếu đến một đối tượng `Cookie`.
3. **Thể hiện (instance):** tên gọi khác của đối tượng được tạo từ một lớp cụ thể.
4. **Thuộc tính (attribute):** dữ liệu lưu trên đối tượng, truy cập bằng dấu chấm. `cookie_one.color` là một thuộc tính.
5. **Phương thức (method):** hàm được định nghĩa trong lớp. `cookie_one.get_color()` là một lần gọi phương thức.
6. **Trạng thái (state):** các giá trị hiện tại của thuộc tính trên đối tượng.
7. **Hành vi (behavior):** công việc mà phương thức cung cấp.

Dấu chấm phân tách đối tượng với thành viên được truy cập. Một lần gọi phương thức cũng ngầm truyền đối tượng làm đối số đầu tiên; vì vậy phương thức được viết với `self`.

```
     cookie_one = Cookie('green')
     |             |       |
     |             |       +-- đối số của hàm khởi tạo
     |             +---------- lớp được tạo thể hiện
     +------------------------ tên biến liên kết với đối tượng

     cookie_one.color          -> thuộc tính/trạng thái
     cookie_one.get_color()    -> phương thức/hành vi
     Cookie                    -> lớp/kiểu
     cookie_one                 -> đối tượng/thể hiện
```

---

## 4. Phép so sánh với khuôn cắt bánh

Ví dụ `Cookie` dùng khuôn cắt bánh vật lý làm phép so sánh cho một lớp.

* Khuôn mô tả hình dạng nhưng không phải là chiếc bánh có thể ăn.
* Ấn khuôn vào bột tạo ra một chiếc bánh mới.
* Mọi chiếc bánh có cùng hình dạng chung, nhưng màu hoặc trang trí có thể khác.
* Đổi một chiếc bánh đã nướng không làm đổi các chiếc bánh khác.

Lớp là khuôn. Gọi `Cookie(...)` tạo một thể hiện. Đối số của hàm khởi tạo chọn trạng thái ban đầu của đúng thể hiện đó.

```
       LỚP COOKIE / KHUÔN
       +-------------------+
       | hình dạng + quy tắc|
       | __init__           |
       | get_color          |
       | set_color          |
       +---------+---------+
                 |
       tạo       |    tạo
                 v
       +----------------+       +----------------+
       | cookie_one     |       | cookie_two     |
       | color=green    |       | color=blue     |
       +----------------+       +----------------+
          thể hiện độc lập        thể hiện độc lập
```

---

## 5. Hàm khởi tạo và `self`

Phương thức tên `__init__` là **hàm khởi tạo (initializer/constructor)** thường được gọi là constructor trong các bài học Python nhập môn. Nó tự động chạy khi một thể hiện được tạo.

Trong mã nguồn, `__init__(self, color)` nhận hai phần thông tin về mặt khái niệm:

* `self` là thể hiện vừa được tạo.
* `color` là giá trị do bên gọi cung cấp.

Câu lệnh `self.color = color` tạo hoặc cập nhật thuộc tính trên đúng thể hiện đó. Tên bên trái thuộc về đối tượng; tên bên phải là tham số cục bộ.

```
     Cookie('green')
          |
          | Python tạo đối tượng và gọi __init__
          v
     __init__(self=<đối tượng mới>, color='green')
          |
          | self.color = color
          v
     +-------------------+
     | đối tượng Cookie mới|
     | color: 'green'     |
     +-------------------+
```

Khi viết `cookie_one.get_color()`, Python truyền `cookie_one` làm `self`. Khi viết `cookie_one.set_color('yellow')`, phương thức nhận cùng thể hiện đó làm `self` và `'yellow'` làm `color`.

---

## 6. Tạo nhiều thể hiện độc lập

Mã nguồn tạo hai đối tượng từ cùng một lớp:

```python
cookie_one = Cookie('green')
cookie_two = Cookie('blue')
```

Cả hai đối tượng có cùng các phương thức, nhưng thuộc tính `color` được khởi tạo riêng. Tên biến cũng là các tham chiếu riêng.

```
     cookie_one --------------------+
                                    v
                            +----------------+
                            | Đối tượng Cookie A|
                            | color='green'  |
                            +----------------+

     cookie_two --------------------+
                                    v
                            +----------------+
                            | Đối tượng Cookie B|
                            | color='blue'   |
                            +----------------+

     Cùng định nghĩa lớp, hai đối tượng khác nhau, hai trạng thái khác nhau.
```

Hai lệnh in đọc các giá trị khác nhau vì mỗi lần gọi constructor khởi tạo trạng thái độc lập. Mẫu này mở rộng cho hàng đợi, cây và đồ thị có nhiều đối tượng.

---

## 7. Đổi thuộc tính qua phương thức

`get_color` đọc trạng thái hiện tại và trả về nó. `set_color` đổi trạng thái bằng cách gán giá trị mới cho `self.color`.

Câu lệnh sau chỉ đổi `cookie_one`:

```python
cookie_one.set_color('yellow')
```

Đối tượng được tham chiếu bởi `cookie_two` không được truyền vào lời gọi đó, nên trạng thái của nó vẫn là `'blue'`.

```
     TRƯỚC LỜI GỌI SETTER
     cookie_one -> [ Cookie | color='green' ]
     cookie_two -> [ Cookie | color='blue'  ]

     cookie_one.set_color('yellow')
                  |
                  | chỉ cập nhật self.color trên đối tượng một
                  v

     SAU LỜI GỌI SETTER
     cookie_one -> [ Cookie | color='yellow' ]
     cookie_two -> [ Cookie | color='blue'   ]
```

Phương thức là một thao tác có kiểm soát trên trạng thái đối tượng. Ví dụ nhỏ này chưa kiểm tra dữ liệu, nhưng lớp phong phú hơn có thể xác nhận màu hợp lệ hoặc ghi lịch sử thay đổi.

---

## 8. Sơ đồ đối tượng và bộ nhớ

Một sơ đồ hữu ích tách **tên**, **đối tượng** và định nghĩa lớp. Tên trỏ đến đối tượng; đối tượng lưu thuộc tính của thể hiện. Lớp cung cấp cấu trúc và định nghĩa phương thức dùng chung.

Sơ đồ này là mô hình khái niệm. CPython có các chi tiết triển khai khác, nhưng mô hình giải thích đúng hành vi trong bài học.

```
     ĐỐI TƯỢNG LỚP
     +--------------------------------+
     | Cookie                         |
     | định nghĩa phương thức         |
     | __init__, get_color,           |
     | set_color                      |
     +----------------+---------------+
                      | các thể hiện theo lớp này
          +-----------+-----------+
          |                       |
          v                       v
     +-------------+         +-------------+
     | đối tượng A |         | đối tượng B |
     | color=green |         | color=blue  |
     +-------------+         +-------------+
          ^                       ^
          |                       |
     cookie_one               cookie_two
```

Khi `cookie_one` đổi, chỉ vùng thuộc tính của đối tượng A đổi. Tra cứu phương thức có thể dùng định nghĩa lớp, còn `self` khiến phương thức tác động lên thể hiện đã gọi nó. Mã nguồn dùng thuộc tính thể hiện được tạo bằng `self.color`.

---

## 9. Mã `Cookie.py` thực tế

Đoạn dưới đây là toàn bộ tệp nguồn dùng trong bài học. Nó cố ý ngắn để cơ chế lớp hiện rõ mà không bị che bởi mã ứng dụng không liên quan.

```python
class Cookie:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


cookie_one = Cookie('green')
cookie_two = Cookie('blue')

print('Cookie one is', cookie_one.get_color())
print('Cookie two is', cookie_two.get_color())

cookie_one.set_color('yellow')

print('\nCookie one is now', cookie_one.get_color())
print('Cookie two is still', cookie_two.get_color())
```

### Hành vi

Định nghĩa lớp khởi tạo thể hiện, `get_color` đọc nó, còn `set_color` thay thế nó. Hai lần gọi constructor tạo thể hiện độc lập, nên kết quả cuối là `yellow` cho bánh thứ nhất và vẫn `blue` cho bánh thứ hai.

```
     Cookie('green') -> get_color() -> green
     Cookie('blue')  -> get_color() -> blue
     set_color trên đối tượng đầu -> yellow
     đối tượng đầu đọc yellow; đối tượng hai vẫn blue
```

Dòng trống trong hai lệnh in cuối đến từ `\n` trong chuỗi. Kết quả quan trọng là trạng thái của hai đối tượng độc lập.

---

## 10. Lớp là nền tảng của cấu trúc dữ liệu

### Node (nút)

Một **Node (nút)** thường lưu một giá trị và một hoặc nhiều tham chiếu đến nút khác. Tham chiếu biến các đối tượng tách rời thành chuỗi hoặc cấu trúc phân nhánh.

```
     +-----------+      +-----------+      +-----------+
     | Node      |      | Node      |      | Node      |
     | value: 10 | next|-> value:20 | next|-> value:30 |
     +-----------+      +-----------+      +-----------+
                                              next -> None
```

### LinkedList (danh sách liên kết)

Lớp **LinkedList (danh sách liên kết)** thường lưu `head`, có thể có `tail`, và `length`. Các phương thức append, prepend, tìm kiếm và xóa sẽ thay đổi tham chiếu nút.

```
     Đối tượng LinkedList
     +---------------------------+
     | head ---------------------|----> Node(10) -> Node(20) -> None
     | tail ---------------------|--------------------^        |
     | length: 2                 |                             |
     +---------------------------+                             +-- cuối
```

### Tree (cây)

Nút cây có thể giữ tham chiếu `left` và `right`. Lớp `Tree` có thể giữ root và cung cấp phương thức chèn hoặc duyệt.

```
                         Tree.root
                             |
                         +---v---+
                         |   8   |
                         +---+---+
                       trái     phải
                        /          \
                   +---v---+    +---v---+
                   |   3   |    |  10   |
                   +-------+    +-------+
```

### Graph (đồ thị)

Đồ thị có thể dùng các đối tượng đỉnh với tập hợp tham chiếu hàng xóm, hoặc lớp đồ thị ánh xạ một giá trị đến danh sách giá trị kề. Lớp tạo nơi lưu quan hệ và định nghĩa các phương thức duyệt BFS, DFS.

```
     Graph.vertices
       A --------> B
       |           |
       v           v
       C --------> D

     Mũi tên là tham chiếu/cạnh được graph hoặc vertex sở hữu.
```

---

## 11. Những vấn đề thực tế được giải quyết bằng lớp

| Vấn đề | Giải pháp dùng lớp | Lợi ích |
|:---|:---|:---|
| Nhiều bản ghi có cùng hình dạng | Định nghĩa một lớp và tạo các thể hiện | Tái sử dụng, trường nhất quán |
| Trạng thái và thao tác bị rải rác | Đặt thuộc tính và phương thức cùng nhau | Sở hữu rõ ràng |
| Giá trị có chuyển đổi hợp lệ | Kiểm tra cập nhật trong phương thức | Bảo vệ bất biến |
| Các phần tử cần nối với nhau | Lưu tham chiếu đối tượng như `next` | Cấu trúc liên kết tự nhiên |
| Cần mô hình hóa thực thể thật | Dùng kiểu theo miền bài toán | Mã phản ánh bài toán |

```
     VẤN ĐỀ THỰC TẾ                TRÁCH NHIỆM CỦA LỚP
     --------------------------    --------------------------
     gói có nơi nhận               Package.destination
     gói có thể được giao          Package.mark_delivered()
     nút có nút kế tiếp            Node.next
     danh sách có nút đầu          LinkedList.head
     cây có thể tìm kiếm           Tree.search()
```

---

## 12. Phân tích Big O cho lớp Cookie

Các phương thức trong `Cookie` đọc hoặc gán một thuộc tính. Nếu xem truy cập và gán thuộc tính là thao tác thời gian hằng số, mỗi thao tác riêng lẻ là `O(1)`.

| Thao tác | Thời gian | Bộ nhớ phụ | Lý do |
|:---|:---:|:---:|:---|
| Định nghĩa lớp | `O(1)` về mặt khái niệm | `O(1)` cho thiết lập mã | Định nghĩa được viết một lần |
| Tạo một `Cookie` | `O(1)` | `O(1)` trạng thái thể hiện | Gán một thuộc tính cố định |
| `get_color()` | `O(1)` | `O(1)` | Một lần tra cứu và trả thuộc tính |
| `set_color(color)` | `O(1)` | `O(1)` | Một lần gán thuộc tính |
| Tạo `n` cookie | `O(n)` | `O(n)` | Mỗi cookie có kích thước hằng số |
| Đọc hoặc đổi cả `n` cookie | `O(n)` | `O(1)` phụ trợ | Duyệt mỗi thể hiện một lần |

```
     MỘT THỂ HIỆN:                  n THỂ HIỆN:
     tạo       -> O(1)             tạo từng cái -> n * O(1) = O(n)
     đọc màu   -> O(1)             lưu trữ      -> n * O(1) = O(n)
     cập nhật  -> O(1)
```

---

## 13. Tóm tắt và danh sách kiểm tra

Các mối quan hệ cốt lõi là:

1. **Lớp (class)** định nghĩa một kiểu tùy chỉnh.
2. Gọi lớp tạo một **đối tượng/thể hiện (object/instance)**.
3. **Thuộc tính (attribute)** lưu trạng thái đối tượng.
4. **Phương thức (method)** cài đặt hành vi đối tượng.
5. `self` xác định thể hiện nhận lời gọi phương thức.
6. `__init__` khởi tạo từng thể hiện mới.
7. Các lần gọi constructor riêng tạo trạng thái thể hiện độc lập.
8. Lớp cho phép cấu trúc dữ liệu lưu liên kết giữa các đối tượng có ý nghĩa.

```
     LỚP
       |
       | gọi với các đối số
       v
     THỂ HIỆN
       |
       +--> thuộc tính = trạng thái
       +--> phương thức = hành vi
       +--> tham chiếu  = kết nối đến đối tượng khác
       |
       v
     cấu trúc lớn hơn: LinkedList, Tree, Graph
```

Trước khi viết một lớp, hãy hỏi:

| Câu hỏi | Cần xác định |
|:---|:---|
| Một đối tượng là gì? | Đơn vị cần có danh tính riêng |
| Trạng thái nào thuộc về nó? | Thuộc tính khởi tạo trong `__init__` |
| Nó có thể làm gì? | Phương thức và đầu vào/đầu ra |
| Điều gì luôn phải đúng? | Bất biến được bảo vệ bởi giao diện |
| Nó có nối với đối tượng khác không? | Tham chiếu như `next`, `left`, hàng xóm |
| Chi phí là bao nhiêu? | Thời gian và bộ nhớ của từng thao tác |

---

**Bước tiếp theo:** Dùng mô hình lớp và thể hiện để học tham chiếu và con trỏ trong Python, sau đó nối các đối tượng `Node` thành linked list, tree và graph.
