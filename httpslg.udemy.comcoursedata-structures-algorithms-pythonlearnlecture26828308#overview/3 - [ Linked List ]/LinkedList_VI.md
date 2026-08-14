
---

# Danh sách liên kết (Linked List)

## 1. Danh sách liên kết là gì?

**Danh sách liên kết (Linked List)** là một **cấu trúc dữ liệu tuyến tính (linear data structure)** gồm các **Nút (Node)**, trong đó mỗi nút lưu hai thứ:

* một **giá trị (value)** — dữ liệu mà nút đang giữ
* một **con trỏ `next`** — tham chiếu tới **nút tiếp theo** trong chuỗi

Bản thân danh sách theo dõi hai con trỏ đặc biệt cộng thêm một biến đếm:

* **head** — trỏ tới nút ĐẦU TIÊN
* **tail** — trỏ tới nút CUỐI CÙNG
* **length** — số nút trong danh sách

Con trỏ `next` của nút cuối cùng là **None**, đánh dấu điểm kết thúc của chuỗi.

### Ý tưởng cốt lõi:
> Danh sách liên kết giống như trò truy tìm kho báu: mỗi nút chứa một manh mối
> (con trỏ `next`) cho bạn biết nút tiếp theo nằm ở đâu trong bộ nhớ.

### Điểm khác biệt CHÍNH so với List của Python:
> List của Python có **chỉ số (index)** (0, 1, 2, ...). Danh sách liên kết **KHÔNG có index**.
> Cách duy nhất để chạm tới một nút là bắt đầu từ `head` và đi theo các con trỏ.

### Cấu tạo của một Nút và một Danh sách:

```
    MỘT NÚT (NODE):

        +---------+--------+
        |  value  |  next  | -----> trỏ tới nút tiếp theo (hoặc None)
        +---------+--------+


    MỘT LINKED LIST với các giá trị 1 -> 2 -> 3 -> 4:

       head                                                    tail
         |                                                       |
         v                                                       v
       +---+---+      +---+---+      +---+---+      +---+--------+
       | 1 | * | ---> | 2 | * | ---> | 3 | * | ---> | 4 | None |
       +---+---+      +---+---+      +---+---+      +---+--------+
         ^
         |
       KHÔNG CÓ INDEX! Muốn chạm tới nút 3, bạn phải đi bộ
       head -> 1 -> 2 -> 3, từng con trỏ một.
```

---

## 2. Tại sao Linked List được tạo ra?

List của Python (mảng động - dynamic array) lưu các phần tử trong **một khối bộ nhớ liền kề (contiguous memory)**. Thiết kế đó cho phép truy cập theo index rất nhanh, nhưng có một cái giá đau đớn: **chèn hoặc xóa ở đầu danh sách buộc mọi phần tử khác phải dịch chuyển một ô**.

```
    LIST CỦA PYTHON - một khối bộ nhớ liền kề:

       Index:     0        1        2        3
               +--------+--------+--------+--------+
     Giá trị: |   11   |   3    |   23   |   7    |
               +--------+--------+--------+--------+
     Địa chỉ:   100      104      108      112     <- một khối liền mạch


     insert(0, 99)  =>  MỌI phần tử phải dịch sang phải một ô:

               +--------+--------+--------+--------+--------+
               |   99   |   11   |   3    |   23   |   7    |
               +--------+--------+--------+--------+--------+
                          \__ TẤT CẢ ĐỀU DỊCH __/      =>  O(n)


    LINKED LIST - các nút nằm rải rác khắp bộ nhớ:

       +-------+        +-------+        +-------+
       | 11|*  | -----> | 3 |*  | -----> | 23|*  | -----> None
       +-------+        +-------+        +-------+
       đc 100           đc 372           đc 215


     prepend(99)  =>  tạo một nút, nối lại MỘT con trỏ:

       +-------+        +-------+        +-------+        +-------+
       | 99|*  | -----> | 11|*  | -----> | 3 |*  | -----> | 23|*  | -> None
       +-------+        +-------+        +-------+        +-------+
       đc 517           (không thứ gì khác phải dịch!)    =>  O(1)
```

### Tóm tắt:

| Thao tác ở ĐẦU danh sách | List của Python | Linked List |
|:---|:---|:---|
| Chèn vào đầu | `O(n)` — dịch toàn bộ | **`O(1)`** — nối lại một con trỏ |
| Xóa ở đầu | `O(n)` — dịch toàn bộ | **`O(1)`** — chỉ dỜI `head` |
| Cần bộ nhớ liền kề? | Có | **Không** — nút nằm đâu cũng được |

---

## 3. Linked List giải quyết những bài toán nào?

* **Kích thước động** — lớn lên và nhỏ đi theo từng nút; không cần resize, không cần copy.
* **Chèn/xóa ở đầu thường xuyên** — `O(1)` thay vì `O(n)`.
* **Không cần bộ nhớ liền kề** — các nút có thể rải rác khắp vùng heap.
* **Nền tảng cho các cấu trúc dữ liệu khác**:

```
    +-----------------------------------------------------------+
    |         LINKED LIST LÀ NỀN TẢNG CỦA:                      |
    +-----------------------------------------------------------+
    |   STACK       -> push/pop = prepend / pop_first   (O(1))  |
    |   QUEUE       -> enqueue = append, dequeue = pop_first    |
    |   GRAPH       -> danh sách kề lưu các đỉnh láng giềng     |
    |   HASH TABLE  -> chaining: mỗi bucket là một linked list  |
    |   DOUBLY LL   -> thêm con trỏ "prev" (bài tiếp theo)      |
    +-----------------------------------------------------------+
```

### Các bài phỏng vấn kinh điển (được giải trong thư mục `Leetcode/`):

```
    +------------------------------------------------+--------------+
    |  BÀI TOÁN                                      | KỸ THUẬT     |
    +------------------------------------------------+--------------+
    |  141. Linked List Cycle                        | Fast/slow ptr|
    |  206. Reverse Linked List                      | Lật 3 con trỏ|
    |  876. Middle of the Linked List                | Fast/slow ptr|
    |  19. Remove Nth Node From End of List          | Hai con trỏ  |
    |  24. Swap Nodes in Pairs                       | Nối lại ptr  |
    |  83. Remove Duplicates from Sorted List        | Duyệt 1 lần  |
    |  86. Partition List                            | Hai ds mới   |
    |  92. Reverse Linked List II                    | Lật đoạn con |
    |  1290. Convert Binary Number in a LL to Int    | Duyệt 1 lần  |
    +------------------------------------------------+--------------+
```

---

## 4. Xây dựng một Nút và Constructor

Mỗi **Nút (Node)** chỉ là một object với `value` và `next`. **Constructor** của LinkedList tạo nút đầu tiên và cho cả `head` lẫn `tail` cùng trỏ vào nó.

### Code (SOLUTION-LL-Constructor.py):

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1
```

### `LinkedList(4)` tạo ra gì trong bộ nhớ:

```
       head
         |
         v
       +---+--------+
       | 4 | None |      <- một nút: head và tail CÙNG trỏ vào nó
       +---+--------+
         ^
         |
       tail          length = 1
```

---

## 5. Append — O(1)

**Mục tiêu:** thêm một nút mới vào CUỐI danh sách. Nhờ con trỏ `tail`, đây là thao tác thờI gian hằng số.

```
    TRƯỚC append(2) với danh sách đang có [1]:

       head
         |
         v
       +---+--------+
       | 1 | None |
       +---+--------+
         ^
        tail

    BƯỚC 1: self.tail.next = new_node   -> nối tail cũ tới nút mới

       +---+---+      +---+--------+
       | 1 | * | ---> | 2 | None |
       +---+---+      +---+--------+
         ^               ^
       head           new_node     (tail vẫn đang trỏ vào 1!)

    BƯỚC 2: self.tail = new_node        -> dờI tail tới nút cuối mới

       +---+---+      +---+--------+
       | 1 | * | ---> | 2 | None |
       +---+---+      +---+--------+
         ^               ^
       head             tail         length = 2
```

**Trường hợp biên:** nếu danh sách rỗng, `head` và `tail` cùng trỏ vào nút mới.

### Code (SOLUTION-LL-Append.py):

```python
    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
```

---

## 6. Pop — O(n)

**Mục tiêu:** xóa nút CUỐI và trả về nó. Vấn đề: trong danh sách liên kết đơn (singly linked list) không có cách nào đi lùi, nên để tìm nút **đứng trước** `tail` ta phải đi bộ từ `head`.

```
    TRƯỚC pop() với [1 -> 2 -> 3]:

       head                              tail
         |                                 |
         v                                 v
       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]

    BƯỚC 1: cho temp đi tới nút CUỐI (pre luôn bám sau temp một bước)

       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]
                         ^              ^
                        pre            temp

    BƯỚC 2: self.tail = pre          -> nút đứng trước trở thành tail mới
    BƯỚC 3: self.tail.next = None    -> cắt nút cuối ra khỏi chuỗi

       [ 1 | * ] ---> [ 2 | None ]      [ 3 | None ]
                         ^                 ^
                        tail              temp -> ĐƯỢC TRẢ VỀ

                        length = 2
```

**Trường hợp biên:** danh sách rỗng -> trả về `None`; nếu sau khi pop danh sách trở nên rỗng, đặt lại `head = None` và `tail = None`.

### Code (SOLUTION-LL-Pop.py):

```python
    def pop(self):
        if self.length == 0:
            return None
        temp = self.head
        pre = self.head
        while(temp.next):
            pre = temp
            temp = temp.next
        self.tail = pre
        self.tail.next = None
        self.length -= 1
        if self.length == 0:
            self.head = None
            self.tail = None
        return temp
```

> Chính đoạn đi bộ từ `head` này khiến `pop()` là **O(n)** — và là lý do Doubly Linked List (bài tiếp theo) ra đờI.

---

## 7. Prepend — O(1)

**Mục tiêu:** thêm một nút mới vào ĐẦU danh sách. Đây là nơi linked list tỏa sáng — không dịch chuyển gì, chỉ hai lần nối lại con trỏ.

```
    TRƯỚC prepend(0) với [1 -> 2]:

       head
         |
         v
       [ 1 | * ] ---> [ 2 | None ]

    BƯỚC 1: new_node.next = self.head   -> nút mới trỏ vào head cũ

       [ 0 | * ] ---+
                    |
                    v
       head ---> [ 1 | * ] ---> [ 2 | None ]

    BƯỚC 2: self.head = new_node        -> head dờI tới nút mới

       head
         |
         v
       [ 0 | * ] ---> [ 1 | * ] ---> [ 2 | None ]
                                         ^
                                        tail     length = 3
```

### Code (SOLUTION-LL-Prepend.py):

```python
    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1
        return True
```

---

## 8. Pop First — O(1)

**Mục tiêu:** xóa nút ĐẦU và trả về nó. Chỉ cần dờI `head` sang phải một bước — ngược với `pop()`, và chỉ tốn **O(1)**.

```
    TRƯỚC pop_first() với [1 -> 2 -> 3]:

       head
         |
         v
       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]

    BƯỚC 1: temp = self.head             -> ghi nhớ nút sẽ bị xóa
    BƯỚC 2: self.head = self.head.next   -> head trượt sang phải một bước

       [ 1 | * ] ---> [ 2 | * ] ---> [ 3 | None ]
          ^              ^
         temp           head

    BƯỚC 3: temp.next = None             -> tách hẳn head cũ ra

       [ 1 | None ]     [ 2 | * ] ---> [ 3 | None ]
           ^               ^
       ĐƯỢC TRẢ VỀ       head          tail
```

**Trường hợp biên:** nếu danh sách trở nên rỗng, đặt luôn `tail = None`.

### Code (SOLUTION-LL-Pop_First.py):

```python
    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0:
            self.tail = None
        return temp
```

---

## 9. Get & Set — O(n)

**Mục tiêu:** đọc (hoặc cập nhật) nút tại một vị trí cho trước. Vì **không có index**, `get` phải bắt đầu từ `head` và đi theo `next` đúng `index` lần.

```
    get(2) với [11 -> 3 -> 23 -> 7]:

       head
         |
         v
       [ 11 | * ] ---> [ 3 | * ] ---> [ 23 | * ] ---> [ 7 | None ]
          ^                ^              ^
       bước 0          bước 1         bước 2  -> TRẢ VỀ nút này
      (temp = head)   (dịch lần 1)   (dịch lần 2)
```

### Code (SOLUTION-LL-Get.py):

```python
    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp
```

`set_value` đơn giản tái sử dụng `get`: nếu nút tồn tại, ghi đè `value` của nó.

### Code (SOLUTION-LL-Set.py):

```python
    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False
```

---

## 10. Insert — O(n)

**Mục tiêu:** chèn một nút mới tại index cho trước. Hai đầu được ủy quyền: index `0` -> `prepend`, index `length` -> `append`. Ở giữa, hai con trỏ được nối lại.

```
    insert(1, 99) với [1 -> 2 -> 3]:

    BƯỚC 1: temp = get(index - 1)   -> nút đứng TRƯỚC điểm chèn

       temp
         |
         v
       [1] ---> [2] ---> [3] ---> None

    BƯỚC 2: new_node.next = temp.next   -> [99] trỏ vào [2]
            (cả [1] và [99] bây giờ cùng trỏ vào [2])

       [1] ---> [2] ---> [3] ---> None
                 ^
                 |
               [99]  (new_node)

    BƯỚC 3: temp.next = new_node        -> [1] trỏ vào [99]

       [1] ---> [99] ---> [2] ---> [3] ---> None
```

### Code (SOLUTION-LL-Insert.py):

```python
    def insert(self, index, value):
        if index < 0 or index > self.length:
            return False
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)
        new_node = Node(value)
        temp = self.get(index - 1)
        new_node.next = temp.next
        temp.next = new_node
        self.length += 1   
        return True  
```

---

## 11. Remove — O(n)

**Mục tiêu:** xóa nút tại index cho trước và trả về nó. Hai đầu được ủy quyền: index `0` -> `pop_first`, index `length - 1` -> `pop`. Ở giữa, ta nhảy cóc qua nút mục tiêu.

```
    remove(1) với [1 -> 2 -> 3]:

    BƯỚC 1: pre  = get(index - 1)   -> nút trước mục tiêu
            temp = pre.next         -> chính nút mục tiêu

       [1] ---> [2] ---> [3] ---> None
        ^         ^
       pre       temp

    BƯỚC 2: pre.next = temp.next    -> mũi tên NHẢY CÓC qua mục tiêu

       [1] ---+         +---> [3] ---> None
              |         |
              +---------+      [2] bị bỏ qua

    BƯỚC 3: temp.next = None        -> tách ra và trả về

       [1] ---> [3] ---> None       [2 | None] -> ĐƯỢC TRẢ VỀ
```

### Code (SOLUTION-LL-Remove.py):

```python
    def remove(self, index):
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()
        pre = self.get(index - 1)
        temp = pre.next
        pre.next = temp.next
        temp.next = None
        self.length -= 1
        return temp
```

---

## 12. Reverse — O(n)

**Mục tiêu:** lật ngược toàn bộ danh sách ngay tại chỗ (in place). Câu trả lờI phỏng vấn kinh điển dùng **ba con trỏ**: `before`, `temp` (hiện tại), và `after`.

```
    reverse() với [1 -> 2 -> 3]:

    BƯỚC 0: đổi chỗ head và tail;  before = None;  temp = head cũ

       tail                              head
         |                                 |
         v                                 v
       [1] ---> [2] ---> [3] ---> None
        ^
      temp     before = None

    VÒNG LẶP (lặp length lần):
        after     = temp.next     # 1. ghi nhớ phần còn lại của chuỗi
        temp.next = before        # 2. LẬT con trỏ hiện tại
        before    = temp          # 3. before trượt sang phải một bước
        temp      = after         # 4. temp   trượt sang phải một bước

    LƯỢT 1:  None <--- [1]    [2] ---> [3] ---> None
                        ^       ^
                     before   temp

    LƯỢT 2:  None <--- [1] <--- [2]    [3] ---> None
                                 ^       ^
                              before   temp

    LƯỢT 3:  None <--- [1] <--- [2] <--- [3]
                                          ^
                                       before (temp = None, vòng lặp kết thúc)

    CUỐI:   head ---> [3] ---> [2] ---> [1] ---> None
            tail vẫn trỏ vào [1]. Xong!
```

### Code (SOLUTION-LL-Reverse.py):

```python
    def reverse(self):
        temp = self.head
        self.head = self.tail
        self.tail = temp
        after = temp.next
        before = None
        for _ in range(self.length):
            after = temp.next
            temp.next = before
            before = temp
            temp = after
```

---

## 13. Tổng kết Big O

| Phương thức | ThờI gian | Lý do |
|:---|:---|:---|
| `append(value)` | **`O(1)`** | `tail` cho truy cập trực tiếp — nối lại một con trỏ |
| `pop()` | **`O(n)`** | phải đi từ `head` để tìm nút TRƯỚC `tail` |
| `prepend(value)` | **`O(1)`** | chỉ `head` được nối lại |
| `pop_first()` | **`O(1)`** | chỉ `head` dịch chuyển |
| `get(index)` | **`O(n)`** | không có index — duyệt từ `head` |
| `set_value(index, value)` | **`O(n)`** | gọi `get` trước |
| `insert(index, value)` | **`O(n)`** | gọi `get(index - 1)` trước |
| `remove(index)` | **`O(n)`** | gọi `get(index - 1)` trước |
| `reverse()` | **`O(n)`** | một lượt; mỗi con trỏ lật đúng một lần |

| Tra cứu | ThờI gian |
|:---|:---|
| Theo giá trị | `O(n)` — quét tuyến tính |
| Theo index | `O(n)` — không có truy cập trực tiếp |

---

## 14. Linked List vs List của Python

```
    +---------------------------+------------------+-------------------+
    |  THAO TÁC                 |  LINKED LIST     |  LIST CỦA PYTHON  |
    +---------------------------+------------------+-------------------+
    |  Tra cứu theo index       |  O(n)            |  O(1)   <-- THẮNG |
    |  Append (cuối)            |  O(1)            |  O(1) amortized   |
    |  Pop (cuối)               |  O(n)            |  O(1)   <-- THẮNG |
    |  Prepend (đầu)            |  O(1) <-- THẮNG  |  O(n)             |
    |  Pop first (đầu)          |  O(1) <-- THẮNG  |  O(n)             |
    |  Chèn/Xóa ở giữa          |  O(n)            |  O(n)             |
    |  Bố cục bộ nhớ            |  Rải rác         |  Liền kề          |
    |  Bộ nhớ phụ mỗi phần tử   |  Một con trỏ next|  Không            |
    +---------------------------+------------------+-------------------+
```

### Quy tắc ngón tay cái:
> Cần **indexing** nhanh và thao tác ở **cuối**? Dùng **list của Python**.
> Cần chèn/xóa ở **đầu** nhanh và **kích thước động**? Dùng **linked list**.

| Tiêu chí | Linked List | List của Python |
|:---|:---|:---|
| Indexing | `O(n)` | `O(1)` |
| Append / Pop ở cuối | `O(1)` / `O(n)` | `O(1)` / `O(1)` |
| Chèn / Xóa ở đầu | `O(1)` / `O(1)` | `O(n)` / `O(n)` |
| Bộ nhớ | Rải rác + thêm con trỏ mỗi nút | Một khối liền kề |
| Thân thiện với cache | Kém | Xuất sắc |

---

**Bước tiếp theo:** Hãy nâng cấp Linked List với con trỏ thứ hai — **Danh sách liên kết đôi (Doubly Linked List)** — và biến `pop()` từ O(n) thành O(1)!
