
---

# Duyệt theo Chiều Rộng (Breadth-First Search — BFS)

## 1. Duyệt theo Chiều Rộng là gì?

**Duyệt theo chiều rộng (Breadth-First Search — BFS)** là một thuật toán duyệt cây/đồ thị, thăm các nút **THEO TỪNG MỨC (LEVEL)**, từ **trái sang phải**, trước khi đi sâu xuống mức tiếp theo.

Thay vì lao xuống một nhánh cho đến tận nút lá (như DFS), BFS mở rộng **ra ngoài** từ gốc — nó duyệt xong toàn bộ một mức rồi mới chuyển sang mức kế tiếp.

### Ý tưởng chính:
> "Thăm tất cả mọi ngưởi ở mức của bạn trước khi gặp con cái của họ."
> BFS hoạt động giống gợn sóng trên mặt hồ — lan ra từ điểm bắt đầu, từng vòng một.

### Cấu trúc dữ liệu đứng sau BFS: HÀNG ĐỢI (QUEUE)
BFS được vận hành bởi một **Hàng đợi (Queue — FIFO: First In, First Out / Vào trước, Ra trước)** — chính là cấu trúc ta đã xây dựng ở **phần Queues (thư mục 6)**:
* Các nút được **enqueue** (thêm vào cuối hàng đợi) khi vừa được phát hiện.
* Các nút được **dequeue** (lấy ra từ đầu hàng đợi) để được thăm.
* Vì hàng đợi là FIFO, nút nào được phát hiện **sớm hơn** sẽ được thăm **sớm hơn** — đây chính là điều tạo ra thứ tự duyệt theo từng mức.

```
        +--------------------------------------------------+
        |           DUYỆT THEO CHIỀU RỘNG (BFS)            |
        +--------------------------------------------------+
        |                                                  |
        |   Thứ tự thăm:  TỪNG MỨC MỘT, trái sang phải     |
        |                                                  |
        |        Mức 0:     [ 47 ]                         |
        |                   /    \                         |
        |        Mức 1:   [21]  [76]                       |
        |                  / \    / \                      |
        |        Mức 2:  [18][27][52][82]                  |
        |                                                  |
        |   Vận hành bởi:  HÀNG ĐỢI (FIFO)                 |
        |   enqueue -> cuối  |  dequeue <- đầu             |
        +--------------------------------------------------+
```

---

## 2. Tại sao BFS được tạo ra?

Một số bài toán không hỏi "cái gì nằm ở đáy cây" — chúng hỏi về **độ gần với gốc** (hoặc với một nút xuất phát).

DFS (Duyệt theo chiều sâu — Depth-First Search) lao xuống một nhánh đến tận lá **trước khi** nó thăm các anh em (siblings) của nút đó. Nếu câu trả lởi bạn cần là "nút GẦN NHẤT với điểm xuất phát", DFS sẽ lãng phí thởi gian đi qua các nút sâu và xa trước.

BFS trả lởi hoàn hảo đúng một câu hỏi:

> **"Cái gì gần với điểm xuất phát nhất?"**

Vì BFS thăm các nút theo thứ tự **khoảng cách (số cạnh) tính từ gốc**, nên lần đầu tiên BFS chạm tới một nút, nó đã đi theo **đường ngắn nhất có thể** (trong đồ thị không trọng số).

```
        CÂU HỎI MÀ MỖI THUẬT TOÁN TRẢ LỜI:

        DFS:   "Cái gì ở CUỐI nhánh này?"
                        |
                        v   (lao xuống sâu trước)

        BFS:   "Cái gì GẦN gốc nhất?"
                        o   (lan ra xung quanh trước)
                      / | \
                     o  o  o
```

### Trực giác thực tế:
Nếu bạn muốn tìm ngưởi trong mạng xã hội có **ít mức độ xa cách (degrees of separation) nhất** với bạn mà làm việc tại Google, bạn sẽ kiểm tra:
1. Tất cả bạn bè trực tiếp (khoảng cách 1)
2. Tất cả bạn của bạn bè (khoảng cách 2)
3. Tất cả bạn của bạn của bạn bè (khoảng cách 3)

Đó **chính là** BFS. Bạn sẽ không bao giờ kiểm tra "bạn của bạn của bạn bè" trước khi kiểm tra HẾT bạn bè trực tiếp — làm vậy là DFS, và nó sẽ đưa cho bạn một câu trả lởi ở rất xa trước.

---

## 3. BFS giải quyết những bài toán nào?

* **Đường đi ngắn nhất (shortest path) trong đồ thị không trọng số** — BFS bảo đảm đường đi đầu tiên tìm thấy tới một nút là đường ngắn nhất (ít cạnh nhất). Đây là nền tảng của các thuật toán như Dijkstra (cho đồ thị có trọng số).
* **In cây theo mức (level-order printing)** — in cây, mỗi mức một dòng.
* **Mạng xã hội — mức độ xa cách** — tính năng "những ngưởi bạn có thể biết" là BFS đến độ sâu 2 hoặc 3.
* **Web crawler theo độ sâu** — thu thập tất cả các trang được liên kết từ trang chủ trước khi đi sâu hơn, để crawler luôn "ở gần" trang gốc.
* **Tìm các nút gần gốc nhất** — ví dụ: "trạm xăng gần nhất" trên bản đồ không trọng số.
* **Bài toán phỏng vấn** — xem thư mục `Interview` trong phần này: `BST-Kth Smallest Node.py` và `BST-Validate BST.py` đều được giải bằng các kỹ thuật duyệt cây giống như trong thư mục này.

```
        +----------------------------------------------------------+
        |  BFS XUẤT HIỆN Ở ĐÂU TRONG THỰC TẾ                       |
        +----------------------------------------------------------+
        |                                                          |
        |   Google Maps (đường không trọng số) -> đường ngắn nhất  |
        |   LinkedIn "kết nối bậc 2"         -> BFS đến độ sâu 2   |
        |   Web crawler "ở gần trang gốc"    -> BFS theo độ sâu    |
        |   In cây từng mức một              -> BFS tự nhiên       |
        |                                                          |
        +----------------------------------------------------------+
```

---

## 4. Cây chúng ta sẽ dùng

Đây là **chính xác cái cây** được xây dựng bởi đoạn code kiểm thử ở cuối file `SOLUTION-BFS.py` (insert lần lượt: 47, 21, 76, 18, 27, 52, 82):

```
                    47
                  /    \
                21      76
               /  \    /  \
             18   27  52   82
```

### Các mức của nó:

```
        Mức 0:                            47
                                       /      \
        Mức 1:                       21        76
                                    /  \      /  \
        Mức 2:                    18    27  52    82

        Độ rộng Mức 0 = 1
        Độ rộng Mức 1 = 2
        Độ rộng Mức 2 = 4   <== độ rộng lớn nhất của cây (w = 4)
```

### Thứ tự thăm của BFS trên cây này (1..7):

```
                 [1] 47
                 /      \
                /        \
           [2] 21        [3] 76
           /    \        /    \
      [4] 18  [5] 27 [6] 52 [7] 82

      Danh sách kết quả mong đợi:  [47, 21, 76, 18, 27, 52, 82]
```

---

## 5. BFS hoạt động như thế nào — Từng bước một

Thuật toán diễn giải bằng lởi:

```
    1. Cho nút GỐC (root) vào hàng đợi.
    2. Trong khi hàng đợi CHƯA rỗng:
         a. DEQUEUE nút ở đầu      -> nút này được THĂM.
         b. APPEND giá trị của nó vào danh sách kết quả.
         c. ENQUEUE con TRÁI của nó  (nếu có).
         d. ENQUEUE con PHẢI của nó (nếu có).
    3. Trả về danh sách kết quả.
```

### Cơ chế hàng đợi (FIFO — Vào trước, Ra trước):

```
        cuối                                              đầu
          |                                                 |
          v                                                 v
        +-----+-----+-----+-----+-----+-----+-----+
        |  82 |  52 |  27 |  18 |  76 |  21 |  47 |
        +-----+-----+-----+-----+-----+-----+-----+
          ^                                                 ^
          |                                                 |
    con cái mới đi vào đây              các nút rồi đây để được thăm
```

### Bảng truy vết đầy đủ từng bước (hàng đợi, dequeue, enqueue, kết quả):

| Bước | Hàng đợi (đầu -> cuối) | Dequeue / Được thăm | Con được Enqueue | Kết quả hiện tại |
|:---|:---|:---|:---|:---|
| 0 | `[47]` | — | — | `[]` |
| 1 | `[21, 76]` | `47` | `21, 76` | `[47]` |
| 2 | `[76, 18, 27]` | `21` | `18, 27` | `[47, 21]` |
| 3 | `[18, 27, 52, 82]` | `76` | `52, 82` | `[47, 21, 76]` |
| 4 | `[27, 52, 82]` | `18` | (không có — lá) | `[47, 21, 76, 18]` |
| 5 | `[52, 82]` | `27` | (không có — lá) | `[47, 21, 76, 18, 27]` |
| 6 | `[82]` | `52` | (không có — lá) | `[47, 21, 76, 18, 27, 52]` |
| 7 | `[]` | `82` | (không có — lá) | `[47, 21, 76, 18, 27, 52, 82]` |

Hàng đợi giờ đã **rỗng** — vòng lặp kết thúc và danh sách kết quả được trả về.

### Cùng quá trình đó, vẽ theo từng bước:

```
    BƯỚC 1:  dequeue 47, enqueue 21 & 76
             queue = [21, 76]          results = [47]

    BƯỚC 2:  dequeue 21, enqueue 18 & 27
             queue = [76, 18, 27]      results = [47, 21]

    BƯỚC 3:  dequeue 76, enqueue 52 & 82
             queue = [18, 27, 52, 82]  results = [47, 21, 76]
                         ^
             hàng đợi rộng nhất lúc này = 4 = độ rộng mức dưới cùng

    BƯỚC 4:  dequeue 18 (lá, không có gì để enqueue)
             queue = [27, 52, 82]      results = [47, 21, 76, 18]

    BƯỚC 5:  dequeue 27 (lá)
             queue = [52, 82]          results = [47, 21, 76, 18, 27]

    BƯỚC 6:  dequeue 52 (lá)
             queue = [82]              results = [47, 21, 76, 18, 27, 52]

    BƯỚC 7:  dequeue 82 (lá)
             queue = []                results = [47, 21, 76, 18, 27, 52, 82]

    HÀNG ĐỢI RỖNG  =>  XONG. Lưu ý: kích thước TỐI ĐA của hàng đợi
    chính là độ rộng lớn nhất của cây.
```

### Thứ tự thăm theo từng mức với các mũi tên:

```
                          47  <------ thăm lần #1
                 -------- Mức 0 ----------------------
                         /    \
                       21      76  <-- thăm lần #2, #3
                 -------- Mức 1 ----------------------
                      /  \    /  \
                    18   27  52   82  <- thăm lần #4, #5, #6, #7
                 -------- Mức 2 ----------------------

        Hướng di chuyển:  ===============================>

        Một mức LUÔN được duyệt xong hoàn toàn trước khi
        mức tiếp theo bắt đầu — đó chính là HÀNG ĐỢI đang
        làm việc của nó.
```

---

## 6. Code

Đây là code **thực tế, nguyên bản (verbatim)** từ file `SOLUTION-BFS.py` trong thư mục này. Chú ý comment ở trên — viết BFS bằng một lớp `Queue` thật (như cái ta đã làm ở thư mục 6) về mặt kỹ thuật là giải pháp tốt hơn; phiên bản dùng list bên dưới là bản đơn giản hóa được dùng trong khóa học:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return True
        temp = self.root
        while (True):
            if new_node.value == temp.value:
                return False
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            else: 
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right

    def contains(self, value):
        if self.root is None:
            return False
        temp = self.root
        while (temp):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
    
   
    # YOU CAN ALSO WRITE BFS WITH A QUEUE INSTEAD OF LIST
    # (TECHNICALLY THIS IS A BETTER SOLUTION)
    #
    # def BFS(self):
    #     current_node = self.root
    #     queue = Queue()
    #     results = []
    #     queue.put(current_node)

    #     while not queue.empty():
    #         current_node = queue.get()
    #         results.append(current_node.value)
    #         if current_node.left is not None:
    #             queue.put(current_node.left)
    #         if current_node.right is not None:
    #             queue.put(current_node.right)
    #     return results
                
    
    def BFS(self):
        current_node = self.root
        queue = []
        results = []
        queue.append(current_node)

        while len(queue) > 0:
            current_node = queue.pop(0)
            results.append(current_node.value)
            if current_node.left is not None:
                queue.append(current_node.left)
            if current_node.right is not None:
                queue.append(current_node.right)
        return results




my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.BFS())



"""
    EXPECTED OUTPUT:
    ----------------
    [47, 21, 76, 18, 27, 52, 82]

 """
```

### Giải thích từng dòng của `BFS()`:

```
    queue.append(current_node)      <- gốc đi vào hàng đợi (ở cuối)

    while len(queue) > 0:           <- tiếp tục đến khi không còn gì để thăm
        current_node = queue.pop(0) <- DEQUEUE từ ĐẦU hàng (FIFO!)
        results.append(...)         <- THĂM: ghi lại giá trị
        nếu có con trái: enqueue nó <- con cái xếp hàng chở ở cuối
        nếu có con phải: enqueue nó
```

> **Chỉ một dòng tạo nên toàn bộ phép màu:** `queue.pop(0)` lấy ra từ **đầu** trong khi `append` thêm vào **cuối**. Chính quyết định FIFO duy nhất này biến "lao xuống sâu" thành "từng mức một".

---

## 7. Phân tích Big O

| Độ phức tạp | Giá trị | Lý do |
|:---|:---|:---|
| **Thởi gian (Time)** | `O(n)` | Mỗi nút được enqueue một lần, dequeue một lần và thăm một lần |
| **Không gian (Space)** | `O(w)` | Hàng đợi chứa tối đa **một mức đầy đủ** của cây tại một thởi điểm, với `w` = **độ rộng lớn nhất** của cây |

### Tại sao không gian là `O(w)` — và tại sao điều đó có thể tệ:

```
        MỘT CÂY NHỊ PHÂN HOÀN HẢO — mỗi mức NHÂN ĐÔI:

        Mức 0:                          o                    rộng 1
        Mức 1:                  o               o            rộng 2
        Mức 2:              o       o       o       o        rộng 4
        Mức 3:            o   o   o   o   o   o   o   o      rộng 8
                              \______________________/
                                riêng mức DƯỚI CÙNG đã
                                chứa khoảng  n / 2  nút!
```

Với một cây **hoàn hảo/đầy đủ**, mức dưới cùng chứa khoảng **một nửa tổng số nút** (`≈ n/2`). Vì BFS phải giữ toàn bộ mức đó trong hàng đợi trước khi đi tiếp, **không gian xấu nhất thực tế là `O(n)`** cho một cây rộng.

```
        +-----------------------+---------------------------+
        |                       |  KHÔNG GIAN CẦN DÙNG      |
        +-----------------------+---------------------------+
        |  BFS (hàng đợi)       |  O(w) — lên tới ~n/2      |
        |                       |  (TỆ với cây rộng)        |
        +-----------------------+---------------------------+
        |  DFS (call stack)     |  O(h) — chỉ là chiều cao  |
        |                       |  (TỆ với cây sâu)         |
        +-----------------------+---------------------------+

        BFS đánh đổi bộ nhớ lấy độ rộng; DFS đánh đổi lấy độ sâu.
```

---

## 8. BFS vs DFS — So sánh nhanh

| | **BFS** | **DFS** |
|:---|:---|:---|
| **Thứ tự thăm** | Từng mức một, trái sang phải | Xuống một nhánh đến lá, rồi quay lui (backtrack) |
| **Cấu trúc dữ liệu** | Hàng đợi — Queue (FIFO) | Ngăn xếp gọi hàm — Call stack (đệ quy, LIFO) |
| **Thởi gian** | `O(n)` | `O(n)` |
| **Không gian** | `O(w)` — độ rộng tối đa | `O(h)` — chiều cao cây |
| **Tốt nhất khi cây...** | Sâu và hẹp | Rộng và thấp |
| **Ứng dụng kinh điển** | Đường đi ngắn nhất, in theo mức, "gần gốc nhất" | Xuất BST đã sắp xếp (In-Order), tuần tự hóa (Pre-Order), xóa cây (Post-Order) |

---

**Bước tiếp theo:** Bây giờ hãy xem mặt còn lại của duyệt cây — Duyệt theo chiều sâu (DFS) với ba biến thể: Tiền thứ tự (Pre-Order), Trung thứ tự (In-Order) và Hậu thứ tự (Post-Order)!
