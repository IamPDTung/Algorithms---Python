
---

# Stack (Ngăn xếp)

**Stack (ngăn xếp)** là một cấu trúc dữ liệu tuyến tính tuân theo **LIFO (Last In, First Out - vào sau, ra trước)**. Phần tử mới nhất là phần tử được lấy ra đầu tiên. Stack có một đầu đang hoạt động gọi là **top (đỉnh)**. Cả thao tác thêm và xóa đều diễn ra ở đầu này.

## 1. LIFO và Top (Đỉnh)

Hãy hình dung chồng đĩa: đĩa trên cùng được thêm và lấy ra trước.

| Thuật ngữ | Ý nghĩa |
|:---|:---|
| **Top (đỉnh)** | Tham chiếu đến node được thêm gần đây nhất |
| **Push (đẩy vào)** | Thêm một phần tử vào top |
| **Pop (lấy ra)** | Xóa và trả về phần tử ở top |
| **Height (chiều cao)** | Số phần tử trong stack |
| **LIFO** | Phần tử vào sau là phần tử ra trước |

```text
                 TOP (ĐỈNH)
                      |
             [mới nhất]  <- ra trước
             [cũ hơn]
             [cũ nhất]   <- ra sau cùng
                      |
                BOTTOM (ĐÁY)
```

Nếu đẩy `A`, `B`, rồi `C` theo thứ tự đó, thứ tự lấy ra sẽ là `C`, `B`, `A`.

---

## 2. Biểu diễn Dựa trên Node (Node-Based)

Phần cài đặt cốt lõi dùng singly linked list (danh sách liên kết đơn). Mỗi **Node (nút)** lưu giá trị và `next`; stack lưu `top` và `height`. Node đầu tiên là top, còn `None` đánh dấu đáy.

```text
       stack.top (đỉnh)
              |
     [3] ---> [2] ---> [1] ---> None
      mới nhất   cũ hơn    cũ nhất
     height = 3
```

| Bất biến | Vì sao quan trọng |
|:---|:---|
| `top` trỏ đến node mới nhất | `push` và `pop` có thể bắt đầu ngay lập tức |
| Node cuối có `next == None` | Đánh dấu đáy của danh sách |
| `height` bằng số node | Kiểm tra rỗng và theo dõi kích thước trong thời gian hằng số |
| Stack rỗng có `top == None` | Không có node để xóa |

Chỉ `top` và nhiều nhất một con trỏ `next` thay đổi; không cần dịch chuyển phần tử.

---

## 3. Vì sao Head của Linked List Là Top

Head của singly linked list truy cập ngay được. Thêm/xóa ở head đổi một con trỏ; dùng tail cho `pop` phải tìm node trước nó, nên là `O(n)`.

```text
     HEAD LÀ TOP: top ---> [mới] ---> [cũ] ---> None
     TAIL LÀ TOP: head ---> [1] ---> [2] ---> [3] ---> None
                         duyệt đến node trước: O(n)
```

Quy tắc con trỏ vì vậy rất đơn giản: **head của linked list là top của stack**.

Push nối node mới vào top cũ, di chuyển `top`, rồi tăng `height`. Pop lưu top, tiến `top`, tách node đã lưu, rồi giảm `height`.

```text
     push: top -> [2] -> [1]       top -> [4] -> [2] -> [1]
     pop:  temp=[4] -> [2] -> [1]   top -> [2] -> [1]
```

---

## 4. Constructor (Hàm Khởi Tạo)

Constructor cốt lõi tạo một `Node`, gán nó cho `top`, và đặt `height` bằng `1`; `Stack(4)` không rỗng.

```text
     Stack(4): top ---> [4] ---> None
     height = 1
```

Lời giải trong repository, không thay đổi code:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Stack:
    def __init__(self, value):
        new_node = Node(value)
        self.top = new_node
        self.height = 1



my_stack = Stack(4)

print('Top:', my_stack.top.value)
print('Height:', my_stack.height)


"""
    EXPECTED OUTPUT:
    ----------------
    Top: 4
    Height: 1

"""
```

Constructor có độ phức tạp thời gian `O(1)` và dùng `O(1)` không gian phụ cho node mới.

---

## 5. Push (Đẩy Vào)

`push` nối node mới vào top cũ trước khi di chuyển `top`, nhờ đó giữ lại mọi node cũ hơn.

```text
     Trạng thái 0: top -> [2] -> [1] -> None, height = 2
     Trạng thái 1: new_node -> [3] -> None
     Trạng thái 2: new_node -> [3] -> [2] -> [1] -> None
     Trạng thái 3: top -> [3] -> [2] -> [1] -> None, height = 3

     push rỗng (9): top -> [9] -> None, height 0 -> 1
```

Lời giải trong repository được giữ nguyên:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Stack:
    def __init__(self, value):
        new_node = Node(value)
        self.top = new_node
        self.height = 1

    def print_stack(self):
        temp = self.top
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def push(self, value):
        new_node = Node(value)
        if self.height == 0:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node
        self.height += 1
 



my_stack = Stack(2)

print('Stack before push(1):')
my_stack.print_stack()

my_stack.push(1)

print('\nStack after push(1):')
my_stack.print_stack()



"""
    EXPECTED OUTPUT:
    ----------------
    Stack before push(1):
    2

    Stack after push(1):
    1
    2   

"""
```

---

## 6. Pop (Lấy Ra) và Trường Hợp Rỗng

`pop` lưu top, tiến `top`, tách node đã lưu, và giảm `height`. Nó kiểm tra rỗng trước, trả về `None` mà không dereference.

```text
     Trạng thái 0: top -> [1] -> [2] -> [3] -> None, temp = [1]
     Trạng thái 1: top -> [2] -> [3] -> None
     Trạng thái 2: temp trả về = [1] -> None, height = 2

     pop rỗng: top -> None, height = 0, result = None
```

Lời giải trong repository được giữ nguyên:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Stack:
    def __init__(self, value):
        new_node = Node(value)
        self.top = new_node
        self.height = 1

    def print_stack(self):
        temp = self.top
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def push(self, value):
        new_node = Node(value)
        if self.height == 0:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node
        self.height += 1
        return True

    def pop(self):
        if self.height == 0:
            return None
        temp = self.top
        self.top = self.top.next
        temp.next = None
        self.height -= 1
        return temp
    

    

my_stack = Stack(4)
my_stack.push(3)
my_stack.push(2)
my_stack.push(1)

print('Stack before pop():')
my_stack.print_stack()

print('\nPopped node:')
print(my_stack.pop().value)

print('\nStack after pop():')
my_stack.print_stack()



"""
    EXPECTED OUTPUT:
    ----------------
    Stack before pop():
    1
    2
    3
    4

    Popped node:
    1

    Stack after pop():
    2
    3
    4

"""
```

---

## 7. Độ Phức Tạp Của Thao Tác

Vì `top` là head của linked list, thao tác tại top không cần duyệt.

```text
     top ---> [A] ---> [B] ---> [C] ---> None
              ^ push/pop ở đầu này
```

| Thao tác | Thời gian | Không gian phụ | Lý do |
|:---|:---:|:---:|:---|
| Constructor | `O(1)` | `O(1)` | Tạo một node và hai tham chiếu |
| `push` | `O(1)` | `O(1)` | Đổi một liên kết `next` và `top` |
| `pop` | `O(1)` | `O(1)` | Tiến `top` và tách một node |
| `peek` | `O(1)` | `O(1)` | Đọc `top.value` |
| `is_empty` | `O(1)` | `O(1)` | Kiểm tra `height` hoặc `top` |
| `print_stack` | `O(n)` | `O(1)` | Đi qua mọi node |

Stack dùng `O(n)` bộ nhớ cho `n` node; cột không gian chỉ tính bộ nhớ tạm.

---

## 8. Call Stack, Undo và Back Của Trình Duyệt

**Call stack (ngăn xếp lời gọi)** lưu các frame của hàm đang hoạt động: một lời gọi sẽ push frame và một lần return sẽ pop frame. Đệ quy thêm frame cho đến case cơ sở. Đệ quy quá sâu có thể làm tràn stack hữu hạn này.

Trình soạn thảo push mỗi trạng thái hoàn tất, nên undo pop chỉnh sửa mới nhất. Stack thứ hai có thể giữ trạng thái redo. Back của trình duyệt cũng tương tự: điều hướng push trang, Back pop trang hiện tại, và forward stack có thể giữ trang đó.

```text
     call stack:       undo stack:       lịch sử trình duyệt:
     TOP               TOP              TOP
      |                 |                |
     [first()]         [delete C]       [docs]
     [main()]          [type B]         [search]
                       [type A]         [home]
     return pop        undo pop         Back pop docs
```

Mở trang mới sau khi Back thường xóa lịch sử forward vì trang mới tạo ra một nhánh tương lai khác.

---

## 9. Thuật Toán Interview

### Dấu Ngoặc Cân Bằng

`Parentheses Balanced.py` quét từ trái sang phải: push dấu mở, pop khi gặp dấu đóng, từ chối dấu đóng không có dấu mở tương ứng, và yêu cầu stack rỗng ở cuối.

```text
     input: (()())
     stack: ( -> (( -> ( -> (( -> ( -> []
     stack rỗng cuối cùng => cân bằng
```

Chuỗi rỗng cân bằng; `(()`, `())`, và `)(` thì không. Cài đặt tham khảo là:

```python
def is_balanced_parentheses(parentheses):
    stack = []
    for character in parentheses:
        if character == '(':
            stack.append(character)
        elif not stack:
            return False
        else:
            stack.pop()
    return len(stack) == 0
```

Độ phức tạp: thời gian `O(n)` và không gian xấu nhất `O(n)`.

### Đảo Một Chuỗi

`Reverse String.py` push từng ký tự đầu vào, rồi pop vào kết quả; lần pop đầu tiên là ký tự cuối ban đầu.

```text
     push: h e l l o       top -> [o] -> [l] -> [l] -> [e] -> [h]
     pop:  o l l e h       output = "olleh"
```

```python
def reverse_string(string):
    stack = []
    for character in string:
        stack.append(character)

    reversed_string = ''
    while stack:
        reversed_string += stack.pop()
    return reversed_string
```

Độ phức tạp: thời gian `O(n)` và không gian phụ `O(n)`; stack thể hiện trực tiếp LIFO.

### Sắp Xếp Stack

`Sort Stack.py` yêu cầu thứ tự tăng dần với giá trị nhỏ nhất ở top, dùng một stack bổ sung. Nó hoạt động như insertion sort.

```text
     pop temp; chuyển giá trị lớn hơn về input; push temp
     sorted top: [1] -> [2] -> [3] -> [4] -> [5]
     chuyển sorted_stack trở lại input stack
```

Chuyển giá trị lớn hơn về input trước khi push `temp`, rồi chuyển kết quả trở lại. Độ phức tạp: thời gian `O(n^2)` và không gian phụ `O(n)`.

```python
def sort_stack(stack):
    sorted_stack = Stack()
    while not stack.is_empty():
        temp = stack.pop()
        while (not sorted_stack.is_empty()
               and sorted_stack.peek() > temp):
            stack.push(sorted_stack.pop())
        sorted_stack.push(temp)

    while not sorted_stack.is_empty():
        stack.push(sorted_stack.pop())
```

File trong repository là scaffold; hàm trên diễn đạt thuật toán mà không sửa nguồn đó.

---

## 10. File Interview và So Sánh

Thư mục Stack `Interview` có các tên bài toán sau:

| File | Ý tưởng chính |
|:---|:---|
| `Implement Stack Using a List.py` | Lưu giá trị trong một Python list rỗng |
| `Parentheses Balanced.py` | Dùng thứ tự LIFO để kiểm tra dấu ngoặc |
| `Reverse String.py` | Dùng push và pop để đảo ký tự |
| `Sort Stack.py` | Sắp xếp bằng một stack bổ sung |

File đầu tiên là bài tập constructor; ba file còn lại có scaffold và test. Code linked list hoàn chỉnh nằm trong ba file `SOLUTION-Stack-*.py` dưới `Core`.

### Stack Linked List So Với Stack Python List

Cả hai đều cung cấp LIFO. Linked list thay đổi head; Python list dùng `append` và `pop` ở cuối, amortized `O(1)`.

```text
     Stack linked list                  Stack Python list

     top -> [C] -> [B] -> [A]           list: [A, B, C]
             head là top                       cuối là top
```

| Tiêu chí | Stack linked list | Stack Python list |
|:---|:---|:---|
| Vị trí top | Con trỏ head | Cuối list |
| `push` | `O(1)` trong trường hợp xấu nhất | `O(1)` amortized |
| `pop` | `O(1)` trong trường hợp xấu nhất | `O(1)` amortized |
| Truy cập ngẫu nhiên | Không tự nhiên | `O(1)` theo index, nhưng không phải hành vi stack |
| Chi phí mỗi phần tử | Object node và con trỏ | Chi phí lưu trữ của list |
| Biểu diễn rỗng | `top is None`, `height == 0` | `len(stack_list) == 0` |
| Giá trị học tập | Thao tác con trỏ | Code sản phẩm đơn giản |

Các file interview dùng `stack_list[-1]` làm top; file core minh họa cơ chế con trỏ của linked-list stack.

### Checklist Cho Stack

Nếu đề bài nói “hành động cuối,” “mới nhất,” “lồng nhau,” hoặc “undo,” hãy kiểm tra LIFO.

Trước khi cài đặt linked-list stack, hãy kiểm tra:

1. `top` trỏ node mới nhất và node mới nối trước khi top di chuyển.
2. `pop` kiểm tra rỗng trước khi dereference.
3. `height` đổi một lần cho mỗi thao tác thành công.
4. Node trả về được tách liên kết.

**Bước tiếp theo:** Chuyển sang queue để học thứ tự FIFO, các con trỏ `first` và `last`, và cách enqueue cùng dequeue vẫn đạt `O(1)` trong linked-list implementation.
