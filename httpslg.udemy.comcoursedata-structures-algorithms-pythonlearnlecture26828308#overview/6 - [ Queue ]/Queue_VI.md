
---

# Queue (Hàng đợi)

**Queue (hàng đợi)** là một cấu trúc dữ liệu tuyến tính tuân theo **FIFO (First In, First Out - vào trước, ra trước)**. Phần tử đến trước là phần tử được xóa trước. Linked-list queue (queue dựa trên linked list) có hai tham chiếu hữu ích: **first (đầu)** trỏ đến phía trước, còn **last (cuối)** trỏ đến phía sau.

## 1. FIFO, First và Last

Hãy hình dung những người đang xếp hàng. Một người gia nhập ở phía sau và rời đi từ phía trước. Người đã chờ lâu nhất được phục vụ trước.

Các thuật ngữ chính là:

| Thuật ngữ | Ý nghĩa |
|:---|:---|
| **First (đầu)** | Tham chiếu đến node cũ nhất ở phía trước |
| **Last (cuối)** | Tham chiếu đến node mới nhất ở phía sau |
| **Enqueue (xếp vào)** | Thêm một phần tử ở phía sau |
| **Dequeue (lấy ra)** | Xóa và trả về một phần tử ở phía trước |
| **FIFO** | Phần tử vào trước là phần tử ra trước |
| **Length (độ dài)** | Số phần tử trong queue |

```text
     hướng dequeue (lấy ra)                 hướng enqueue (xếp vào)
            <---                                      --->

     first (đầu)                                      last (cuối)
          |                                                |
          v                                                v
     +-----+      +-----+      +-----+      +-----+
     |  A  | ---> |  B  | ---> |  C  | ---> |  D  |
     +-----+      +-----+      +-----+      +-----+
       cũ nhất                                  mới nhất
```

Nếu enqueue các giá trị `A`, `B`, rồi `C` theo thứ tự đó, thứ tự dequeue sẽ là `A`, `B`, `C`.

---

## 2. Biểu Diễn Dựa Trên Node

Phần cài đặt cốt lõi dùng một singly linked list (danh sách liên kết đơn). Mỗi **Node (nút)** lưu một giá trị và con trỏ `next`. Queue lưu `first`, `last`, và `length`, nên biết cả hai đầu mà không cần duyệt danh sách.

`first` là head của linked list và đại diện cho phần tử tiếp theo sẽ rời queue. `last` là tail và đại diện cho phần tử mới nhất. Node cuối luôn trỏ đến `None`.

```text
     queue.first (đầu)                             queue.last (cuối)
              |                                           |
              v                                           v
     +-----------+      +-----------+      +-----------+
     | value: 1  |      | value: 2  |      | value: 3  |
     | next:  o--+----->| next:  o--+----->| next: None|
     +-----------+      +-----------+      +-----------+
         cũ nhất                                  mới nhất

     queue.length = 3
```

Các bất biến quan trọng là:

| Bất biến | Vì sao quan trọng |
|:---|:---|
| `first` trỏ đến node cũ nhất | `dequeue` có thể xóa ngay |
| `last` trỏ đến node mới nhất | `enqueue` có thể nối ngay |
| `last.next is None` | Đánh dấu ranh giới phía sau |
| `length` bằng số node | Các trường hợp rỗng và một phần tử được biểu diễn rõ |
| Queue rỗng có `first is None` và `last is None` | Không endpoint nào trỏ đến node đã xóa |

Hai tham chiếu endpoint là yếu tố giúp linked-list queue hiệu quả ở cả hai đầu.

---

## 3. Enqueue Ở Last

`enqueue` dùng `last` để nối mà không duyệt: nối last cũ, di chuyển `last`, và tăng `length`.

```text
     Trạng thái 0: first -> [1] -> [2] -> None, last = [2], length = 2
     Trạng thái 1: new_node -> [3] -> None
     Trạng thái 2: first -> [1] -> [2] -> [3] -> None
     Trạng thái 3: last = [3], length = 3

     enqueue rỗng (9): first và last -> [9] -> None, length = 1
```

---

## 4. Dequeue Ở First

`dequeue` xóa node cũ nhất tại `first` trong thời gian hằng số.

```text
     Trạng thái 0: first -> [1] -> [2] -> [3] -> None, last = [3]
     Trạng thái 1: temp = [1], first -> [2] -> [3] -> None
     Trạng thái 2: temp trả về = [1] -> None, length = 2

     một phần tử: first = last = [1] -> None; sau pop cả hai là None
     rỗng: first = last = None, length = 0, result = None
```

Khi `length == 1`, phải reset cả `first` và `last` để tránh con trỏ phía sau cũ. Dequeue rỗng trả về `None` mà không dereference `first`.

---

## 5. Constructor (Hàm Khởi Tạo)

Constructor cốt lõi nhận một giá trị ban đầu, tạo một node, rồi cho cả `first` và `last` trỏ đến node đó. Nó đặt `length` bằng `1`. Queue rỗng được tạo ra sau khi dequeue phần tử cuối, hoặc được biểu diễn bằng `first = None`, `last = None`, và `length = 0` trong thiết kế constructor rỗng.

```text
     Queue(4)

     first --+
             +--> [4] ---> None
     last  --+
     length = 1
```

Lời giải trong repository được giữ nguyên code:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next




my_queue = Queue(4)

my_queue.print_queue()



"""
    EXPECTED OUTPUT:
    ----------------
    4

"""
```

Constructor có thời gian `O(1)` và dùng `O(1)` không gian phụ cho node mới.

---

## 6. Cài Đặt Enqueue

Lời giải `enqueue` có hai nhánh. Nếu `first is None`, queue rỗng, nên cả hai endpoint nhận node mới. Nếu không, `last.next` nhận node mới và `last` di chuyển đến đó. Trong cả hai nhánh, `length` tăng một.

```text
     Nhánh queue không rỗng:

     first ---> [first cũ] ---> ... ---> [last cũ] ---> None
                                                   |
                                                   +--> new_node
     last = new_node

     Nhánh queue rỗng:

     first ---> new_node <--- last
```

Lời giải trong repository được giữ nguyên:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next
        
    def enqueue(self, value):
        new_node = Node(value)
        if self.first is None:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1
        



my_queue = Queue(1)

print('Queue before enqueue(2):')
my_queue.print_queue()

my_queue.enqueue(2)

print('\nQueue after enqueue(2):')
my_queue.print_queue()



"""
    EXPECTED OUTPUT:
    ----------------
    Queue before enqueue(2):
    1

    Queue after enqueue(2):
    1
    2

"""
```

---

## 7. Cài Đặt Dequeue và Đặt Lại Last

Lời giải `dequeue` kiểm tra `length == 0` trước. Nó lưu `first` vào `temp`. Nếu có một phần tử, cả `first` và `last` trở thành `None`. Nếu không, `first` tiến đến node kế tiếp và `temp.next` được tách liên kết. Cuối cùng, `length` giảm và `temp` được trả về.

```text
     length > 1:                       length == 1:

     first -> [A] -> [B]               first -> [A] <- last
                |                       sau pop:
                +-- temp                first -> None
     first -> [B]                       last  -> None
     last không đổi
```

Việc đặt lại `last` là bắt buộc. Nếu thiếu, queue sẽ có `first is None` nhưng con trỏ phía sau cũ, và một lần enqueue sau đó có thể nối vào node không còn thuộc queue.

Lời giải trong repository được giữ nguyên:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class Queue:
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next
        
    def enqueue(self, value):
        new_node = Node(value)
        if self.first is None:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1
        return True

    def dequeue(self):
        if self.length == 0:
            return None
        temp = self.first
        if self.length == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            temp.next = None
        self.length -= 1
        return temp

 

 
my_queue = Queue(1)
my_queue.enqueue(2)

# (2) Items - Returns 2 Node
print(my_queue.dequeue().value)
# (1) Item -  Returns 1 Node
print(my_queue.dequeue().value)
# (0) Items - Returns None
print(my_queue.dequeue())



"""
    EXPECTED OUTPUT:
    ----------------
    1
    2
    None

"""
```

---

## 8. Độ Phức Tạp Của Thao Tác

Với cả hai tham chiếu endpoint, queue không bao giờ phải duyệt danh sách cho các thao tác chính.

```text
     first (đầu)                       last (cuối)
          |                                  |
          v                                  v
     [A] ---> [B] ---> [C] ---> [D] ---> None
       ^                                  ^
     dequeue                           enqueue
```

| Thao tác | Thời gian | Không gian phụ | Lý do |
|:---|:---:|:---:|:---|
| Constructor | `O(1)` | `O(1)` | Tạo một node và đặt hai endpoint |
| `enqueue` | `O(1)` | `O(1)` | Dùng `last.next`, rồi di chuyển `last` |
| `dequeue` | `O(1)` | `O(1)` | Xóa `first`, có reset khi một phần tử |
| `peek` tại first | `O(1)` | `O(1)` | Đọc `first.value` |
| `is_empty` | `O(1)` | `O(1)` | Kiểm tra `length` hoặc `first` |
| `print_queue` | `O(n)` | `O(1)` | Đi qua mọi node |

Bản thân queue chiếm `O(n)` bộ nhớ cho `n` node. Cột không gian của bảng chỉ tính bộ nhớ tạm khi chạy.

---

## 9. Hàng Đợi Máy In

Máy in nhận job nhanh hơn tốc độ in. Mỗi job được enqueue ở phía sau. Máy in dequeue job cũ nhất, nhờ đó job đến sau không chen trước job đến trước.

```text
     job đến: report, photo, invoice

     first (đầu)                            last (cuối)
          |                                      |
          v                                      v
     [report] ---> [photo] ---> [invoice] ---> None
         |
         +-- máy in dequeue job này trước
```

Queue cũng có thể lưu metadata như chủ sở hữu, số trang, nhóm ưu tiên, hoặc thời gian đến. Queue FIFO nghiêm ngặt xử lý mọi job theo thứ tự đến; priority queue (hàng đợi ưu tiên) là chính sách khác, chọn theo độ ưu tiên thay vì chỉ theo thời gian đến.

---

## 10. Scheduler và Work Queue

Hệ điều hành, web server, và background worker dùng queue để chứa các task đang chờ được phục vụ. Worker dequeue một task, thực hiện nó, rồi lấy task tiếp theo.

```text
     producer                            worker
     task A ---+                    +----------+
     task B ---+--> [A] -> [B] ---> | lấy A    |
     task C ---+                    +----------+

     sau khi A xong: [B] -> [C]
```

FIFO tạo ra tính công bằng dễ dự đoán. Scheduler có thể dùng nhiều queue khi cần ưu tiên, tách khách hàng, hoặc giới hạn tốc độ. Cơ chế con trỏ first/last vẫn giống nhau cho mỗi queue thông thường.

---

## 11. Breadth-First Search (Duyệt Theo Chiều Rộng)

**BFS (Breadth-First Search - duyệt theo chiều rộng)** duyệt graph (đồ thị) hoặc tree (cây) theo từng lớp. Nó enqueue đỉnh bắt đầu, liên tục dequeue đỉnh tiếp theo, rồi enqueue từng neighbor (đỉnh kề) chưa thăm. Thứ tự FIFO bảo đảm mọi đỉnh ở khoảng cách hiện tại được xử lý trước các đỉnh sâu hơn.

```text
     các lớp của graph:

             A                 khoảng cách 0
            / \
           B   C               khoảng cách 1
          / \   \
         D   E   F             khoảng cách 2

     thứ tự queue:
     [A] -> dequeue A -> [B, C]
     dequeue B         -> [C, D, E]
     dequeue C         -> [D, E, F]
```

Độ phức tạp BFS thông thường là `O(V + E)` với `V` đỉnh và `E` cạnh, khi dùng adjacency list (danh sách kề). Queue có thể chứa `O(V)` đỉnh ở lớp rộng nhất.

---

## 12. Queue Dùng Stack

Thư mục Queue `Interview` có `Queue Using Stacks - Enqueue.py` và `Queue Using Stacks - Dequeue.py`. Hai bài tập này cài đặt hành vi queue bằng hai Python list được dùng như stack: `stack1` và `stack2`.

Chiến lược enqueue trong repository giữ front ở `stack1[-1]`. Để thêm một giá trị vào phía sau, nó chuyển mọi giá trị từ `stack1` sang `stack2`, push giá trị mới vào `stack1`, rồi chuyển các giá trị cũ trở lại. Thứ tự được khôi phục để `peek` vẫn trả về giá trị cũ nhất.

```text
     enqueue 4 vào queue [1, 2, 3]

     stack1 top -> [3, 2, 1]       stack2 -> []
     chuyển     stack1 -> []       stack2 top -> [1, 2, 3]
     push 4     stack1 top -> [4]  stack2 -> [1, 2, 3]
     khôi phục  stack1 top -> [3, 2, 1, 4]  stack2 -> []
     front queue là stack1[-1] = 1
```

Bài dequeue xóa `stack1[-1]`. Nếu `stack1` rỗng, nó trả về `None`. Cách sắp xếp này cho enqueue `O(n)` và dequeue `O(1)` theo chiến lược đã nêu. Một queue hai stack khác thường đưa phần tử sang output stack chỉ khi output stack rỗng, nhờ đó mỗi thao tác có chi phí amortized `O(1)`.

Các file chứa prompt và scaffold quanh đúng các tên bài toán này; lời giải queue linked list là ba file `SOLUTION-Queue-*.py` dưới `Core`.

---

## 13. So Sánh Stack và Queue

Cả hai cấu trúc đều giới hạn việc truy cập ở một endpoint, nhưng áp dụng thứ tự xóa ngược nhau.

```text
     STACK: cùng một đầu cho cả hai thao tác

     push ---> [C] [B] [A] ---> pop
                         phần tử mới nhất ra trước

     QUEUE: hai đầu khác nhau

     dequeue <--- [A] [B] [C] <--- enqueue
                  phần tử cũ nhất ra trước
```

| Đặc điểm | Stack | Queue |
|:---|:---|:---|
| Quy tắc thứ tự | LIFO | FIFO |
| Thao tác thêm | `push` tại top | `enqueue` tại last |
| Thao tác xóa | `pop` tại top | `dequeue` tại first |
| Endpoint của linked list | `top` | `first` và `last` |
| Ứng dụng thường gặp | Undo, call stack, cú pháp lồng nhau | Máy in, scheduler, BFS |
| Thêm/xóa bằng linked list | `O(1)` / `O(1)` | `O(1)` / `O(1)` |
| Trạng thái rỗng quan trọng | `top is None` | `first is None` và `last is None` |

Hãy chọn dựa trên phần tử nào phải được phục vụ trước, không chỉ dựa vào tên method.

---

## 14. Checklist Cho Queue

Khi đề bài nói “người chờ đầu tiên,” “thứ tự đến,” “task tiếp theo,” hoặc “từng lớp,” hãy kiểm tra xem FIFO có phải hành vi cần thiết không.

```text
     Phần tử cũ nhất có rời đi trước không?
                          |
                       có v
                  +-------------+
                  | Dùng queue  |
                  +-------------+
                          |
             giữ cả hai endpoint nhất quán
                /                    \
           first = front           last = rear
           dequeue ở đây           enqueue ở đây
```

Trước khi cài đặt linked-list queue, hãy kiểm tra:

1. `first` luôn xác định node tiếp theo sẽ rời đi.
2. `last` luôn xác định node mới nhất.
3. `enqueue` xử lý queue rỗng bằng cách đặt cả hai endpoint.
4. `dequeue` reset cả hai endpoint khi xóa phần tử cuối.
5. `length` chỉ thay đổi sau một thao tác thành công.
6. Node bị xóa được tách liên kết trước khi trả về.

**Bước tiếp theo:** Thực hành cài đặt queue từ trạng thái rỗng, sau đó so sánh phiên bản linked list với thiết kế interview hai stack và đo nơi mỗi chiến lược thực hiện công việc.
