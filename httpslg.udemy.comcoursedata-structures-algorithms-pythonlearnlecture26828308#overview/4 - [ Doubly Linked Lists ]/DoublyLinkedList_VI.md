---
# Danh sách liên kết đôi (Doubly Linked List)
## 1. Danh sách liên kết đôi là gì?
**Danh sách liên kết đôi (Doubly Linked List - DLL)** là một cấu trúc dữ liệu tuyến tính (linear data structure) được tạo từ các **nút (Node)** độc lập. Mỗi nút lưu một giá trị và hai liên kết (links): `next` trỏ về phía trước, còn `prev` trỏ về phía sau. Đối tượng danh sách lưu `head`, `tail` và `length`.
Khác với list của Python, danh sách liên kết (linked list) không có chỉ số (index) mảng trực tiếp. Muốn tới một vị trí, ta đi theo liên kết từ nút này sang nút khác. DLL có thể bắt đầu ở một trong hai đầu vì mỗi nút biết cả hai láng giềng.

```text
MỘT NÚT:
    +---------------------------+
    | prev | value | next        |
    +---------------------------+
      ^                  |
      |                  v
    nút trước         nút sau
DANH SÁCH [1, 2, 3]:
    head                                      tail
      |                                         |
      v                                         v
    [None | 1 | *] <--> [* | 2 | *] <--> [* | 3 | None]
    prev của head là None; next của tail là None.
```
Các liên kết là tham chiếu, không phải bản sao của giá trị. Các nút có thể nằm rải rác trong bộ nhớ; `next` và `prev` giữ nguyên thứ tự logic.
---
## 2. Vì sao cấu trúc này được tạo ra?
**Danh sách liên kết đơn (Singly Linked List - SLL)** chỉ có `next`. Khi đã lưu `tail`, ta dễ tìm nút cuối, nhưng xóa tail lại cần nút đứng trước nó. Không thể đi lùi để tìm nút đó, nên `pop()` của SLL phải đi từ `head` và tốn `O(n)`.
DLL thêm `prev` để giải quyết chính vấn đề duyệt ngược đó. Tail cũ đã trỏ sẵn tới nút trước nó, vì vậy `pop()` của DLL có thể dời `tail` sang trái trong `O(1)`. Con trỏ bổ sung làm tốn bộ nhớ, nhưng tránh các lượt duyệt toàn danh sách.

```text
Xóa tail của SLL: phải tìm từ phía đầu
    head                                      tail
      |                                         |
      v                                         v
    [1 | *] ----> [2 | *] ----> [3 | None]
       đi qua ---------------------------> nút trước tail

Xóa tail của DLL: nút trước đã có sẵn
    head                                      tail
      |                                         |
      v                                         v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
                                  ^
                                  | tail.prev
    +----> [2]
```
| Câu hỏi | SLL | DLL |
|:---|:---|:---|
| Duyệt xuôi | `O(n)` | `O(n)` |
| Duyệt ngược | Không hỗ trợ trực tiếp | `O(n)` từ `tail` |
| Xóa cuối khi có tail | `O(n)` | **`O(1)`** |
| Xóa đầu | `O(1)` | `O(1)` |
| Liên kết phụ mỗi nút | `next` | `next` và `prev` |
---
## 3. DLL giải quyết những bài toán nào?
DLL phù hợp khi một phần tử có nút trước (predecessor) và nút sau (successor) tự nhiên, đồng thời cần di chuyển theo cả hai hướng.

* **Lịch sử trình duyệt:** trang hiện tại đi tới `next` khi Forward và tới `prev` khi Back.
* **Undo/redo:** con trỏ chỉnh sửa đi lùi qua các trạng thái undo và đi tới qua các trạng thái redo.
* **Bộ nhớ đệm LRU (Least Recently Used):** bảng băm (hash map) tìm nút, còn DLL đưa nút lên đầu hoặc xóa nút ở giữa trong `O(1)` sau khi đã biết nút.
* **Deque (hàng đợi hai đầu):** thêm và xóa ở cả hai đầu mà không phải dịch chuyển mảng.
```text
                 +----------------------+
                 | nút hiện tại         |
                 +----------------------+
                    ^                |
       undo / Back  |                | redo / Forward
                    |                v
             [trạng thái cũ] <--> [trạng thái mới]

DEQUE:       pop_first / prepend       append / pop
             <--------------------->
```
DLL không tự biến mọi tra cứu thành thời gian hằng số. Nó làm cho thao tác ở hai đầu và việc nối lại một nút đã biết có `O(1)`. LRU cache vẫn cần map từ key tới node; map cung cấp tra cứu, còn DLL cung cấp thứ tự.
---
## 4. Node, head, tail và length
`Node` trong source của khóa học có đúng ba trường (fields):

* `value` là dữ liệu của nút.
* `next` tham chiếu tới nút sau, hoặc `None` ở tail.
* `prev` tham chiếu tới nút trước, hoặc `None` ở head.
Siêu dữ liệu (metadata) của danh sách có ba vai trò:

* `head` xác định nút đầu tiên.
* `tail` xác định nút cuối cùng.
* `length` ghi số nút và giúp các phương thức (methods) kiểm tra index.
```text
DLL KHÔNG RỖNG:
    head                                                        tail
      |                                                           |
      v                                                           v
    [prev=None | value=A | next=*] <--> [prev=* | value=B | next=None]
                    length = 2

TRẠNG THÁI RỖNG SAU KHI XÓA:
    head = None       tail = None       length = 0
```
Các file mã nguồn (source) khởi tạo node mới với cả hai liên kết là `None`. Hàm khởi tạo (constructor) nhận một value ban đầu, nên `DoublyLinkedList(value)` bắt đầu với một node; danh sách rỗng xuất hiện sau khi xóa node đó.
### Source khóa học: `SOLUTION-DLL-Constructor.py`
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
        

class DoublyLinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1
```
### Bất biến của con trỏ (pointer invariants)
1. Nếu `length == 0`, `head is None` và `tail is None`.
2. Nếu `length > 0`, cả `head` và `tail` đều khác `None`.
3. `head.prev is None` và `tail.next is None`.
4. Với mọi liên kết xuôi, `node.next.prev is node`.
5. Với mọi liên kết ngược, `node.prev.next is node`.
6. `head is tail` đúng chính xác khi `length == 1`.
7. Đếm node từ `head` theo chiều xuôi và từ `tail` theo chiều ngược đều cho `length`.
Sau khi xóa một node, node được trả về nên được tách rời: `next` và `prev` đều là `None`. Đây là cách nhanh nhất để phát hiện một phép gán con trỏ bị thiếu.
---
## 5. Khởi tạo
`DoublyLinkedList(value)` cấp phát một `Node`, gán cùng một object cho `head` và `tail`, rồi đặt `length` bằng `1`. Node này vừa là node đầu vừa là node cuối, nên `next` và `prev` giữ nguyên `None`.
```text
TRƯỚC KHI KHỞI TẠO:
    chưa có đối tượng danh sách

SAU DoublyLinkedList(7):
             head, tail
                |
                v
    None <--> [prev=None | value=7 | next=None] <--> None
                length = 1
```
| Công việc khởi tạo | Thời gian | Bộ nhớ phụ |
|:---|:---:|:---:|
| Cấp phát node đầu và metadata | `O(1)` | `O(1)` |
Implementation của khóa học không có constructor không tham số. Không được giả định `DoublyLinkedList()` tạo danh sách rỗng; đối số bắt buộc là value đầu tiên.
---
## 6. Append
`append(value)` thêm node sau `tail` hiện tại. Với danh sách không rỗng, `.next` của tail cũ trỏ tới node mới, `.prev` của node mới trỏ ngược về tail cũ, rồi `tail` được dời đi. `.next` của node mới đã là `None` từ `Node.__init__`.
```text
TRƯỚC append(4):
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
SAU append(4):
    head                                           tail
      |                                              |
      v                                              v
    [None|1|*] <--> [*|2|*] <--> [*|3|*] <--> [*|4|None]
```
Các cập nhật con trỏ theo đúng thứ tự trong source:

1. `self.tail.next = new_node`: tail cũ trỏ xuôi tới node mới.
2. `new_node.prev = self.tail`: node mới trỏ ngược về tail cũ.
3. `self.tail = new_node`: metadata nhận node cuối mới.
4. `self.length += 1`: số lượng tăng sau khi liên kết hợp lệ.
Ở trạng thái rỗng, source gán `self.head = new_node` và `self.tail = new_node`; không cần gán thêm `.next` hay `.prev`.
### Source khóa học: `SOLUTION-DLL-Append.py`
```python
    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1
        return True
```
Thời gian là `O(1)`, bộ nhớ phụ là `O(1)`. Method trả về `True`.
---
## 7. Pop
`pop()` xóa và trả về node cuối. DLL thay đổi thao tác vốn chậm ở SLL: `temp = self.tail`, sau đó `self.tail = self.tail.prev` lấy trực tiếp node trước.
```text
TRƯỚC pop() trên [1, 2, 3]:
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
                                     ^
                                     temp
SAU pop():
    head                       tail                 temp được trả về
      |                          |                         |
      v                          v                         v
    [None|1|*] <--> [*|2|None]  [None|3|None]
```
Cập nhật con trỏ và metadata với danh sách có nhiều hơn một node:

1. `temp = self.tail` lưu node sẽ trả về.
2. `self.tail = self.tail.prev` dời `tail` về node trước.
3. `self.tail.next = None` đánh dấu tail mới và cắt liên kết xuôi.
4. `temp.prev = None` tách node trả về ở phía sau.
5. `self.length -= 1` cập nhật số lượng.
Với một node, source đặt `self.head = None` và `self.tail = None`; không cần nối lại link vì hai link vốn đã là `None`. Với danh sách rỗng, method trả về `None` trước khi đọc `tail`.
### Source khóa học: `SOLUTION-DLL-Pop.py`
```python
    def pop(self):
        if self.length == 0:
            return None
        temp = self.tail
        if self.length == 1:
            self.head = None
            self.tail = None 
        else:       
            self.tail = self.tail.prev
            self.tail.next = None
            temp.prev = None
        self.length -= 1
        return temp
```
Thời gian là `O(1)`, bộ nhớ phụ là `O(1)`, và kết quả là `Node` đã tách rời hoặc `None`.
---
## 8. Prepend
`prepend(value)` chèn một node trước `head` hiện tại. Head cũ vẫn là node hiện có đầu tiên, nhưng node mới trở thành head mới.
```text
TRƯỚC prepend(0):
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|None]
SAU prepend(0):
    head                                           tail
      |                                              |
      v                                              v
    [None|0|*] <--> [*|1|*] <--> [*|2|None]
```
Cập nhật con trỏ theo thứ tự trong source:

1. `new_node.next = self.head`: node mới trỏ xuôi tới head cũ.
2. `self.head.prev = new_node`: head cũ trỏ ngược tới node mới.
3. `self.head = new_node`: metadata dời tới node đầu mới.
4. `self.length += 1`: số lượng tăng.
`new_node.prev` giữ `None` từ lúc khởi tạo. Trong nhánh rỗng, `head` và `tail` cùng trở thành `new_node`; node mới đã có hai liên kết null.
### Source khóa học: `SOLUTION-DLL-Prepend.py`
```python
    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1
        return True
```
Thời gian và bộ nhớ phụ đều là `O(1)`. Method trả về `True`.
---
## 9. Pop First
`pop_first()` xóa và trả về node đầu. Đây là ảnh đối xứng của `pop()`: dùng `head.next`, xóa `prev` của head mới, rồi tách `next` của head cũ.
```text
TRƯỚC pop_first() trên [1, 2, 3]:
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
      ^
     temp
SAU pop_first():
    temp trả về            head                       tail
          |                  |                          |
          v                  v                          v
    [None|1|None]  [None|2|*] <--> [*|3|None]
```
Cập nhật con trỏ và metadata:

1. `temp = self.head` lưu head cũ.
2. `self.head = self.head.next` dời tới node thứ hai.
3. `self.head.prev = None` xác định biên phía sau của head mới.
4. `temp.next = None` tách node trả về ở phía trước.
5. `self.length -= 1` cập nhật số lượng.
Với một node, source đặt cả `head` và `tail` thành `None`; nó không chạy các phép gán link của trường hợp nhiều node. Với danh sách rỗng, method trả về `None`.
### Source khóa học: `SOLUTION-DLL-Pop_First.py`
```python
    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
            temp.next = None      
        self.length -= 1
        return temp
```
Thời gian là `O(1)` và bộ nhớ phụ là `O(1)`.
---
## 10. Get và chọn hướng
`get(index)` trả về node ở index bắt đầu từ zero nếu index hợp lệ. Index không hợp lệ (`index < 0` hoặc `index >= length`) trả về `None`.
Source của khóa học chủ động chọn hướng. Nếu `index < self.length / 2`, nó bắt đầu ở `head` và đi theo `.next`. Ngược lại, nó bắt đầu ở `tail` và đi theo `.prev`. Vì điều kiện là so sánh chặt, index giữa của danh sách có kích thước lẻ thuộc nhánh bắt đầu từ tail.
```text
TRƯỚC get(1) hoặc get(3):
    head                                             tail
      |                                                |
      v                                                v
    [0] <--> [1] <--> [2] <--> [3] <--> [4]
      |------ đi xuôi với index nhỏ ------>|           |
      |<----- đi ngược với index lớn -----|           |

SAU get: `temp` là [1] qua next hoặc [3] qua prev; các link không đổi.
    [0] <--> [1] <--> [2] <--> [3] <--> [4]
```
`get` không sửa bất kỳ trường `.next` hay `.prev` nào. Nó chỉ di chuyển biến cục bộ `temp`, tức là duyệt chỉ đọc. Số bước là `O(min(index, length - 1 - index))` với chiến lược hai hướng, thời gian xấu nhất `O(n)` và bộ nhớ phụ `O(1)`.
### Source khóa học: `SOLUTION-DLL-Get.py`
```python
    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        if index < self.length/2:
            for _ in range(index):
                temp = temp.next
        else:
            temp = self.tail
            for _ in range(self.length - 1, index, -1):
                temp = temp.prev  
        return temp
```
---
## 11. Set Value
Method của khóa học có tên `set_value(index, value)`. Nó gọi `get(index)`, chỉ đổi `.value` của node được chọn và trả về Boolean. Index không hợp lệ trả `False`; index hợp lệ trả `True`.
```text
TRƯỚC set_value(1, 99):
    head                                      tail
      |                                         |
      v                                         v
    [None|10|*] <--> [*|20|*] <--> [*|30|None]
                             target

SAU set_value(1, 99):
    head                                      tail
      |                                         |
      v                                         v
    [None|10|*] <--> [*|99|*] <--> [*|30|None]
    Các link next và prev không đổi.
```
Cập nhật trường duy nhất là `temp.value = value`. `get` thực hiện duyệt theo hướng gần hơn, vì vậy `set_value` có thời gian xấu nhất `O(n)` và bộ nhớ phụ `O(1)`. Nó không tạo node, không đổi `head`, `tail` hay `length`.
### Source khóa học: `SOLUTION-DLL-Set.py`
```python
    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False
```
---
## 12. Insert
`insert(index, value)` nhận index từ `0` tới `length`, bao gồm cả hai đầu. Source chuyển `index == 0` cho `prepend` và `index == length` cho `append`. Chỉ chèn ở giữa mới thực hiện bốn phép gán link.
```text
TRƯỚC insert(2, 99):
    head                              tail
      |                                 |
      v                                 v
    [None|1|*] <--> [*|2|*] <--> [*|3|None]
                    before          after

SAU insert(2, 99):
    head                                           tail
      |                                              |
      v                                              v
    [None|1|*] <--> [*|2|*] <--> [*|99|*] <--> [*|3|None]
                                      new_node
```
Với chèn giữa, source cập nhật mọi link liên quan theo đúng thứ tự:

1. `new_node.prev = before` nối phía sau của node mới.
2. `new_node.next = after` nối phía trước của node mới.
3. `before.next = new_node` cho predecessor trỏ tới node mới.
4. `after.prev = new_node` cho successor trỏ ngược tới node mới.
5. `self.length += 1` ghi nhận thêm một node.
Source lấy `before` bằng `self.get(index - 1)` và đặt `after = before.next`. Index không hợp lệ trả `False`; chèn hợp lệ trả `True`. Ở danh sách rỗng, `insert(0, value)` đi qua `prepend`.
### Source khóa học: `SOLUTION-DLL-Insert.py`
```python
    def insert(self, index, value):
        if index < 0 or index > self.length:
            return False
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)

        new_node = Node(value)
        before = self.get(index - 1)
        after = before.next

        new_node.prev = before
        new_node.next = after
        before.next = new_node
        after.prev = new_node
        
        self.length += 1   
        return True  
```
Bản thân việc nối lại pointer là `O(1)`, nhưng tìm `before` có thời gian xấu nhất `O(n)`. Bộ nhớ phụ là `O(1)`.
---
## 13. Remove
`remove(index)` trả về và tách node ở index hợp lệ. Nó chuyển các biên cho method khác: index `0` gọi `pop_first`, còn index `length - 1` gọi `pop`. Xóa node giữa nối trực tiếp hai láng giềng.
```text
TRƯỚC remove(2) trên [1, 2, 3, 4]:
    head                                           tail
      |                                              |
      v                                              v
    [None|1|*] <--> [*|2|*] <--> [*|3|*] <--> [*|4|None]
                                    temp

SAU remove(2):
    head                              tail             temp trả về
      |                                 |                    |
      v                                 v                    v
    [None|1|*] <--> [*|2|*] <--> [*|4|None]       [None|3|None]
```
Với node giữa `temp`, source thực hiện chính xác các cập nhật sau:

1. `temp.next.prev = temp.prev`: successor trỏ ngược về predecessor.
2. `temp.prev.next = temp.next`: predecessor trỏ xuôi tới successor.
3. `temp.next = None`: tách node trả về ở phía trước.
4. `temp.prev = None`: tách node trả về ở phía sau.
5. `self.length -= 1`: giảm số lượng.
Index không hợp lệ trả về `None`. Với list một node, index `0` đi tới `pop_first`; với list rỗng, kiểm tra thất bại trước khi đọc con trỏ.
### Source khóa học: `SOLUTION-DLL-Remove.py`
```python
    def remove(self, index):
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()

        temp = self.get(index)
        
        temp.next.prev = temp.prev
        temp.prev.next = temp.next
        temp.next = None
        temp.prev = None

        self.length -= 1
        return temp
```
Source dùng `get` theo hướng gần hơn, nên toàn bộ method có thời gian xấu nhất `O(n)` và bộ nhớ phụ `O(1)`. Nếu đã có sẵn tham chiếu tới node, hai phép nối láng giềng là `O(1)`.
---
## 14. Bảng độ phức tạp đầy đủ
```text
THAO TÁC Ở HAI ĐẦU:
    prepend / pop_first  <==============================>  append / pop
             cả hai đầu đều truy cập trực tiếp qua head và tail

THAO TÁC THEO INDEX:
    head --next--> ... --next--> index
    tail --prev--> ... --prev--> index
    get chọn hướng ngắn hơn nhưng không có truy cập index trực tiếp.
```
| Method khóa học | Kết quả khi hợp lệ | Thời gian | Bộ nhớ phụ |
|:---|:---|:---:|:---:|
| Constructor | một node | `O(1)` | `O(1)` |
| `append(value)` | `True` | `O(1)` | `O(1)` |
| `pop()` | Node hoặc `None` | `O(1)` | `O(1)` |
| `prepend(value)` | `True` | `O(1)` | `O(1)` |
| `pop_first()` | Node hoặc `None` | `O(1)` | `O(1)` |
| `get(index)` | Node hoặc `None` | `O(n)` xấu nhất | `O(1)` |
| `set_value(index, value)` | `True` hoặc `False` | `O(n)` xấu nhất | `O(1)` |
| `insert(index, value)` | `True` hoặc `False` | `O(n)` xấu nhất | `O(1)` |
| `remove(index)` | Node hoặc `None` | `O(n)` xấu nhất | `O(1)` |
| `print_list()` | in toàn bộ value | `O(n)` | `O(1)` |
`get` có thể cần `O(min(index, n - 1 - index))` bước link khi `n` là length hiện tại. Bảng Big O dùng trường hợp xấu nhất vì vẫn có thể yêu cầu một index xa đầu trên một danh sách lớn.
---
## 15. So sánh SLL và DLL, chi phí bộ nhớ
```text
NODE SLL:                         NODE DLL:
    +-------------+               +----------------------+
    | value | next|               | prev | value | next  |
    +-------------+               +----------------------+
    một hướng                     hai hướng, thêm một tham chiếu
```
| Lựa chọn thiết kế | Singly linked list | Doubly linked list |
|:---|:---|:---|
| Liên kết của node | `value`, `next` | `value`, `next`, `prev` |
| Đi tới phía trước | Có | Có |
| Đi về phía sau | Không có link trực tiếp | Có |
| `append` khi có `tail` | `O(1)` | `O(1)` |
| Xóa tail | `O(n)` | **`O(1)`** |
| Xóa đầu | `O(1)` | `O(1)` |
| `get(index)` | `O(n)` từ head | `O(n)` xấu nhất, chọn một đầu |
| Xóa giữa theo index | `O(n)` để tìm và nối | `O(n)` để tìm, `O(1)` để nối |
| Bộ nhớ mỗi node | một link | hai link |
Với `n` node, DLL có bộ nhớ node `O(n)` cộng metadata `O(1)`. So với SLL, nó thêm một trường tham chiếu cho mỗi node, nên hằng số bộ nhớ lớn hơn dù bậc tăng trưởng vẫn là `O(n)`. Đổi lại, ta có duyệt ngược, xóa tail và xóa node đã biết nhanh hơn.
---
