
---

# Cây Tìm Kiếm Nhị Phân (Binary Search Tree - BST)

## 1. Cây (Tree) là gì? — Thuật ngữ

**Cây (Tree)** là một cấu trúc dữ liệu phân cấp gồm các **nút (node)** được nối với nhau bằng các **cạnh (edge)**. Khác với Danh sách liên kết (Linked List) vốn **tuyến tính** (mỗi nút trỏ tới nút kế tiếp), cây **phân nhánh** — một nút có thể trỏ tới nhiều nút khác.

```
    LINKED LIST (tuyến tính):          TREE (phân nhánh):

    (head)                             (root / gốc)
       |                                  |
       v                                  v
     [4] -> [7] -> [2] -> null          (47)
                                       /    \
                                    (21)    (76)
```

### Thuật ngữ của Cây:

Mọi cây trong khóa học đều được mô tả bằng các từ vựng sau:

```
                        (47)  <------------------- ROOT (gốc)
                       /    \                      (nút duy nhất
                      /      \                      không có cha)
                   (21)      (76)  <------------- CHILDREN (con) của 47
                  /    \    /    \                 (47 là PARENT / cha)
                (18)  (27)(52)  (82)  <---------- LEAVES (lá)
                 ^      ^    ^      ^              (nút KHÔNG có con)
                 |      |
                 +--+---+
                    |
               18 và 27 là SIBLINGS (anh em)
               (cùng cha: 21)

    Mỗi đường nối "/ \" được gọi là một EDGE (cạnh).
    Một cây hoàn hảo (perfect tree) có mọi tầng đều được lấp đầy.
```

| Thuật ngữ | Định nghĩa |
|:---|:---|
| **Root (gốc)** | Nút trên cùng; nút duy nhất không có cha |
| **Parent (cha)** | Nút có cạnh trỏ xuống các nút khác |
| **Child (con)** | Nút được một nút cha trỏ tới |
| **Leaf (lá)** | Nút không có con |
| **Siblings (anh em)** | Các nút có cùng một cha |
| **Edge (cạnh)** | Đường kết nối (con trỏ) giữa cha và con |

---

## 2. Cây Tìm Kiếm Nhị Phân (Binary Search Tree) là gì?

**Cây nhị phân (Binary Tree)** là cây mà **mỗi nút có tối đa 2 con** — theo quy ước gọi là `left` (trái) và `right` (phải).

```
        CÂY NHỊ PHÂN:                  KHÔNG PHẢI CÂY NHỊ PHÂN:

            (47)                          (47)
           /    \                       /  |  \
        (21)    (76)                (21)(52)(76)   <- 3 con,
        /  \                          không hợp lệ!
     (18)  (27)
```

**Cây tìm kiếm nhị phân (BST)** là cây nhị phân có **thêm một quy tắc sắp xếp** phải đúng tại **MỌI nút**, không chỉ tại gốc:

> **QUY TẮC BST:** Với mọi nút, **mọi giá trị trong cây con TRÁI đều NHỎ HƠN** giá trị của nút, và **mọi giá trị trong cây con PHẢI đều LỚN HƠN**.

```
    QUY TẮC BST TẠI MỌI NÚT:

              (parent / cha)
              /          \
             /            \
      left child      right child
      (con trái)      (con phải)
      < cha           > cha

    VÍ DỤ — quy tắc đúng ở mọi nơi:

                (47)                21 < 47 < 76   OK tại gốc
               /    \
           (21)      (76)           18 < 21        OK tại 21
          /    \    /    \          52 < 76 < 82   OK tại 76
       (18)  (27)(52)    (82)

    Kiểm tra nút 47: TOÀN BỘ bên trái  {21,18,27} < 47  OK
                       TOÀN BỘ bên phải {76,52,82} > 47  OK
```

### BST hợp lệ vs không hợp lệ:

```
        BST HỢP LỆ:                   BST KHÔNG HỢP LỆ:

            (47)                          (47)
           /    \                        /    \
        (21)    (76)                 (21)    (76)
        /  \                         /  \
     (18)  (27)                  (18)  (55)   <-- 55 nằm trong cây con
                                                TRÁI của 47 nhưng
                                                55 > 47. VI PHẠM QUY TẮC!
```

---

## 3. Tại sao Cây Tìm Kiếm Nhị Phân được tạo ra?

Hai cấu trúc dữ liệu cơ bản ta đã biết đều thất bại ở một việc:

* **Danh sách liên kết (Linked List)** chèn ở đầu trong `O(1)`, nhưng **tìm kiếm (search)** một giá trị phải đi qua từng nút: **`O(n)`**.
* **Danh sách đã sắp xếp (sorted List / mảng)** tìm kiếm nhanh bằng tìm kiếm nhị phân: `O(log n)`, nhưng **chèn (insert)** một giá trị đòi hỏi dịch chuyển mọi phần tử phía sau: **`O(n)`**.

```
    LINKED LIST — tìm 82:               SORTED LIST — chèn 50:

    (head)                              +----+----+----+----+
      |                                 | 21 | 47 | 76 | 82 |
      v                                 +----+----+----+----+
    [21]->[47]->[76]->[82]                   |    |
      x     x     x    x                chèn 50 vào đây => 76 và 82
    xem   xem   xem   xem                 phải DỊCH sang phải => O(n)
    O(n) bước!

    BST — tìm kiếm VÀ chèn:

                (47)                    tìm 82: 47 -> 76 -> 82
               /    \                   chỉ 3 bước!
           (21)      (76)
          /    \    /    \              chèn 50: 47 -> 76 -> 52 -> gắn vào
       (18)  (27)(52)    (82)           chỉ đổi 1 con trỏ, không dịch chuyển!
```

### Ý tưởng cốt lõi của BST:
> Một BST **cân bằng (balanced)** sẽ **loại bỏ một nửa** dữ liệu còn lại sau mỗi phép so sánh — giống hệt tìm kiếm nhị phân — nhưng các nút được nối bằng con trỏ, nên chèn giá trị mới chỉ là **gắn thêm một nút**, không phải dịch chuyển mảng.

```
    Mỗi phép so sánh LOẠI BỎ một nửa cây:

    Tầng 0:  1 nút cần kiểm tra
    Tầng 1:  2 nút              => tìm trong 15 nút chỉ cần
    Tầng 2:  4 nút                  tối đa 4 phép so sánh
    Tầng 3:  8 nút                  (log2 của 15 ~ 4)
```

---

## 4. BST giải quyết những bài toán nào?

BST là cấu trúc được chọn khi bạn cần **dữ liệu có thứ tự** với **tìm kiếm nhanh VÀ chèn nhanh** cùng một lúc:

```
    +------------------------------------------------------+
    |              BST ĐƯỢC DÙNG Ở ĐÂU                     |
    +------------------------------------------------------+
    |  * Từ điển / map với khóa có thể sắp xếp             |
    |  * Chỉ mục cơ sở dữ liệu (B-tree là dạng mở rộng     |
    |    của BST)                                          |
    |  * Hệ thống tệp (thư mục sắp xếp theo tên)           |
    |  * Gợi ý tự động / truy vấn khoảng ("mọi tên A-M")   |
    |  * Lập lịch ưu tiên (phần tử nhỏ/lớn kế tiếp)        |
    +------------------------------------------------------+
```

### Các bài phỏng vấn kinh điển (xem thư mục `Leetcode`):

| Bài toán | Tệp | Ý tưởng chính |
|:---|:---|:---|
| **98. Validate Binary Search Tree** | `98. Validate Binary Search Tree.py` | Kiểm tra quy tắc BST đúng tại mọi nút |
| **450. Delete Node in a BST** | `450. Delete Node in a BST.py` | Xóa một nút mà vẫn giữ quy tắc BST |
| **226. Invert Binary Tree** | `226. Invert Binary Tree.py` | Hoán đổi con trái/phải bằng đệ quy |
| **109. Convert Sorted List to BST** | `109. Convert Sorted List to Binary Search Tree.py` | Xây BST cân bằng từ dữ liệu đã sắp xếp |

```
    Ví dụ — Validate BST (bài 98):

            (5)              Đây có phải BST hợp lệ?
           /   \
         (1)   (4)           Nút 4 có con phải là 3:
              /   \          3 < 4 nhưng nằm trong cây con
            (3)   (6)        PHẢI => KHÔNG HỢP LỆ!
```

---

## 5. Cách hoạt động — Constructor & Insert (chèn)

### Constructor (từ `SOLUTION-BST-Constructor.py`):

Mỗi nút lưu một `value` và hai con trỏ `left` và `right`. Bản thân cây khởi đầu **rỗng** (`root = None`):

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None
```

```
    Một nút mới:                  Một cây mới:

    +---------+                   root
    | value   |                    |
    | 47      |                    v
    | left: --+--> null          null     (cây rỗng)
    | right:--+--> null
    +---------+
```

### Thuật toán Insert (chèn):

> Bắt đầu từ gốc. Nếu giá trị mới **nhỏ hơn**, đi sang **trái**; nếu **lớn hơn**, đi sang **phải**. Lặp lại cho đến khi gặp **chỗ trống**, và gắn nút mới vào đó.

```python
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
```

### Từng bước — chèn `47, 21, 76, 18, 52, 82`:

```
    BƯỚC 1: insert(47)                     BƯỚC 2: insert(21)
    root là None -> gắn vào gốc            21 < 47 -> sang trái -> chỗ trống

        (47)                                     (47)
                                                /
                                             (21)

    BƯỚC 3: insert(76)                     BƯỚC 4: insert(18)
    76 > 47 -> sang phải -> chỗ trống      18 < 47 trái, 18 < 21 trái -> gắn

        (47)                                     (47)
        /    \                                  /
     (21)    (76)                            (21)
                                            /
                                         (18)

    BƯỚC 5: insert(52)                     BƯỚC 6: insert(82)
    52 > 47 phải, 52 < 76 trái -> gắn      82 > 47 phải, 82 > 76 phải -> gắn

        (47)                                     (47)
        /    \                                  /    \
     (21)    (76)                            (21)    (76)
    /        /                              /        /    \
 (18)     (52)                           (18)     (52)    (82)
```

### Cách `temp` đi xuống (chi tiết khi chèn 52):

```
    temp = 47:  52 > 47  -> temp = temp.right
    temp = 76:  52 < 76  -> temp.left là None -> GẮN tại đây, return True

                (47)
               /    \
           (21)      (76)
          /         /
       (18)      (52)   <== nút mới được gắn làm con TRÁI của 76
```

---

## 6. Cách hoạt động — Contains (tìm kiếm)

### Thuật toán Contains:

> Cùng quyết định trái/phải như insert — nhưng ta chỉ **đi**, không gắn gì. Nếu rơi khỏi cây (`temp` trở thành `None`), giá trị đó **không tồn tại**.

```python
    def contains(self, value):
        temp = self.root
        while (temp is not None):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
```

### Theo dấu — `contains(52)` trên cây của ta (TÌM THẤY):

```
    temp = [47]: 52 > 47 -> sang phải
    temp = [76]: 52 < 76 -> sang trái
    temp = [52]: 52 == 52 -> return True

                (47)  <== đã thăm 1
               /    \
           (21)      (76)  <== đã thăm 2
          /         /    \
       (18)      (52)    (82)
                  ^
                  đã thăm 3 -> TÌM THẤY!
```

### Theo dấu — `contains(30)` trên cây của ta (KHÔNG THẤY):

```
    temp = [47]: 30 < 47 -> sang trái
    temp = [21]: 30 > 21 -> sang phải
    temp = None  -> vòng lặp kết thúc -> return False

                (47)  <== đã thăm 1
               /    \
           (21)      (76)
          /  ^
       (18)  |
             đã thăm 2 -> con phải là None -> KHÔNG TÌM THẤY
```

### Chính sách trùng lặp (khóa học này):

```
    insert(47) hai lần:

        (47)                     (47)
           |          =>             |      lần chèn thứ hai trả về False
       gắn vào?                  KHÔNG ĐỔI   (KHÔNG chèn giá trị trùng)

    Dòng `if new_node.value == temp.value: return False`
    từ chối mọi giá trị đã có trong cây.
```

---

## 7. Phân tích Big O

### Cây cân bằng vs cây suy biến:

Số **tầng** mới là thứ quan trọng. Cây cân bằng (balanced) có `log n` tầng; cây được xây từ **dữ liệu đã sắp xếp sẵn** sẽ suy biến thành một **chuỗi** có `n` tầng:

```
    CÂY CÂN BẰNG — O(log n):            CÂY SUY BIẾN — O(n):
    (chèn 47,21,76,18,27,52,82)         (chèn 10,20,30,40,50 — đã sắp xếp!)

                (47)                    (10)
               /    \                     \
           (21)      (76)                 (20)
          /    \    /    \                  \
       (18)  (27)(52)    (82)               (30)
                                              \
    7 nút, 3 tầng.                            (40)
    Tìm 82: 3 phép so sánh.                     \
                                                (50)
                                     5 nút, 5 tầng.
                                     Tìm 50: 5 phép so sánh.
                                     Trông HỆT như một Linked List!
```

### Bảng Big O:

| Thao tác | BST cân bằng | Trường hợp xấu nhất (suy biến) |
|:---|:---|:---|
| **Tìm kiếm (`contains`)** | `O(log n)` | `O(n)` |
| **Chèn (insert)** | `O(log n)` | `O(n)` |
| **Bộ nhớ (space)** | `O(n)` | `O(n)` |

> **Điểm cần lưu ý:** BST thông thường **không** tự cân bằng lại. Nếu bạn chèn dữ liệu đã sắp xếp (`10, 20, 30, ...`), bạn sẽ nhận được chuỗi suy biến và mất lợi thế `O(log n)`. (Các biến thể tự cân bằng như cây AVL và cây Đỏ-Đen khắc phục điều này.)

### So sánh BST vs Linked List vs Sorted List:

| Thao tác | Linked List | Sorted List (mảng) | BST (cân bằng) |
|:---|:---|:---|:---|
| **Tìm kiếm** | `O(n)` | `O(log n)` (tìm kiếm nhị phân) | **`O(log n)`** |
| **Chèn** | `O(1)` ở đầu / `O(n)` nếu giữ thứ tự | `O(n)` (dịch chuyển) | **`O(log n)`** |
| **Xóa** | `O(n)` (phải tìm trước) | `O(n)` (dịch chuyển) | **`O(log n)`** |
| **Giữ thứ tự?** | Không | Có | Có (duyệt in-order) |

```
    ĐIỂM NGỌT CỦA BST:

    Tốc độ tìm:   Sorted List  =  BST  >  Linked List
    Tốc độ chèn:  Linked List  =  BST  >  Sorted List

    => BST kết hợp TRA CỨU NHANH (như mảng đã sắp xếp)
       với CHÈN NHANH (như linked list).
```

---

**Bước tiếp theo:** Bây giờ hãy áp dụng BST vào các bài phỏng vấn trong thư mục `Leetcode` — kiểm tra BST hợp lệ, xóa nút, đảo cây, và chuyển danh sách đã sắp xếp thành BST cân bằng!
