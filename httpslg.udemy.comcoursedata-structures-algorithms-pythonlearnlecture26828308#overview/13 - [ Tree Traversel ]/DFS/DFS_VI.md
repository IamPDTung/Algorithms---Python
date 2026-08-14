---

# Duyệt theo Chiều Sâu (Depth-First Search — DFS)
## 1. DFS là gì?
**Duyệt theo chiều sâu (Depth-First Search — DFS)** là thuật toán duyệt cây/đồ thị: thăm một nút, đi theo một nhánh sâu nhất có thể, rồi quay lui để sang nhánh khác. Mỗi nút có thể tới được được thăm một lần; điều quan trọng là thứ tự ghi lại từng nút.
```
    DFS: bắt đầu -> nhánh -> lá -> quay lui -> nhánh khác
    cơ chế: đệ quy + ngăn xếp gọi hàm
```
---

## 2. Tại sao DFS được tạo ra?
Dữ liệu phân cấp có nhánh: thư mục, cây cú pháp và cây tìm kiếm đều cần cách khám phá trọn một nhánh mà không mất vị trí cha. DFS cung cấp chiến lược đi sâu đó.
```
    Gốc -> A -> C -> D -> B -> E -> F
    /  \     quay lui về cha rồi chọn nhánh khác
```
---

## 3. Cây mẫu
Cả ba lời giải (solution) đều chèn `47, 21, 76, 18, 27, 52, 82` vào cùng một **Cây tìm kiếm nhị phân (Binary Search Tree — BST)**; cây được đánh lại cho từng thứ tự bên dưới.
```
    [1]47
     / \
[2]21 [5]76 -> [3]18 [4]27 [6]52 [7]82
```
---

## 4. Đệ quy và ngăn xếp gọi hàm (Call Stack)
Hàm trợ giúp giải **duyệt cây con của nút này**. Nút lá trả về cha; lời gọi mới nhất tiếp tục trước: **LIFO (Last In, First Out — vào sau, ra trước)**. Mỗi khung (frame) nhớ nút và vị trí tiếp tục.
```
    traverse(47) [node=47]
       | traverse(21) [node=21]
       +-- traverse(18) -> lá -> trả về phía trên
```
---

## 5. Vị trí thăm
```
    PRE: gốc -> trái -> phải | IN: trái -> gốc -> phải
    POST: trái -> phải -> gốc
```
---

## 6. Tiền thứ tự (Pre-Order): Gốc-Trái-Phải
Tiền thứ tự append (thêm vào) ngay khi đi vào một nút, trước cả hai lời gọi con.
```
                         [1] 47
                       /          \
                 [2] 21            [5] 76
                 /    \            /    \
            [3] 18  [4] 27    [6] 52  [7] 82
```
```
    gọi traverse(47): append47; gọi traverse(21): append21
    gọi traverse(18): append18 -> trả về; gọi traverse(27): append27 -> trả về21
    xong trái 47; gọi traverse(76): append76; gọi traverse(52): append52 -> trả về
    gọi traverse(82): append82 -> trả về76 -> trả về47
```
```text
[47, 21, 18, 27, 76, 52, 82]
```
Tiền thứ tự hữu ích cho **sao chép và tuần tự hóa**: ghi cha trước con; cây tổng quát cũng cần dấu rỗng.
### `SOLUTION-DFS_Pre_Order.py` nguyên bản

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
    
    def dfs_pre_order(self):
        results = []
        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
        traverse(self.root)
        return results





my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.dfs_pre_order())



"""
    EXPECTED OUTPUT:
    ----------------
    [47, 21, 18, 27, 76, 52, 82]

 """

                

```
---

## 7. Trung thứ tự (In-Order): Trái-Gốc-Phải
Trung thứ tự append giữa lời gọi cây con trái và cây con phải.

```
                         [4] 47
                       /          \
                 [2] 21            [6] 76
                 /    \            /    \
            [1] 18  [3] 27    [5] 52  [7] 82
vị trí append: TRÁI, rồi GỐC, rồi PHẢI
```
```
    traverse(47) -> trái -> traverse(21) -> trái -> 18 append -> trả về
      append 21; traverse(27) append -> trả về; append 47
    traverse(76) -> 52 append -> trả về; append 76; 82 append -> trả về 47
```
```text
[18, 21, 27, 47, 52, 76, 82]
```
Với BST hợp lệ, giá trị trái nhỏ hơn và giá trị phải lớn hơn nên kết quả trung thứ tự được sắp xếp. `BST-Kth Smallest Node.py` đếm dòng này để tìm phần tử nhỏ thứ k; `BST-Validate BST.py` kiểm tra `dfs_in_order()` tăng nghiêm ngặt.
### `SOLUTION-DFS_In_Order.py` nguyên bản

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
    

    def dfs_pre_order(self):
        results = []

        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)

        traverse(self.root)
        return results

    def dfs_post_order(self):
        results = []
        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
            results.append(current_node.value)
        traverse(self.root)
        return results

    def dfs_in_order(self):
        results = []
        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            results.append(current_node.value) 
            if current_node.right is not None:
                traverse(current_node.right)          
        traverse(self.root)
        return results
        




my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.dfs_in_order())



"""
    EXPECTED OUTPUT:
    ----------------
    [18, 21, 27, 47, 52, 76, 82]

 """

                



 
```

---

## 8. Hậu thứ tự (Post-Order): Trái-Phải-Gốc
Hậu thứ tự chỉ append sau khi cả hai lời gọi con hoàn tất.

```
                         [7] 47
                       /          \
                 [3] 21            [6] 76
                 /    \            /    \
            [1] 18  [2] 27    [4] 52  [5] 82
vị trí append: TRÁI, rồi PHẢI, rồi GỐC
```
```
    traverse(47) -> trái -> traverse(21) -> trái -> 18 append -> [18]
      phải 27 append -> [18,27]; xong hai con, append 21
    phải traverse(76) -> trái 52 append -> [...,52]; phải 82 append -> [...,82]
      xong hai con, append 76; xong hai con của 47, append 47
```
```text
[18, 27, 21, 52, 82, 76, 47]
```
Hậu thứ tự tự nhiên cho **xóa** (con trước cha) và **tính giá trị biểu thức** (toán hạng trước toán tử).
```
        +       hậu thứ tự: 2 -> 3 -> * -> 5 -> +
       / \
    *(2,3) 5    (2 * 3) + 5 = 11
```
### `SOLUTION-DFS_Post_Order.py` nguyên bản

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
    
    def dfs_pre_order(self):
        results = []
        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
        traverse(self.root)
        return results

    def dfs_post_order(self):
        results = []
        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
            results.append(current_node.value)
        traverse(self.root)
        return results





my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.dfs_post_order())



"""
    EXPECTED OUTPUT:
    ----------------
    [18, 27, 21, 52, 82, 76, 47]

 """
```

---

## 9. So sánh và độ phức tạp
Với `n` nút và chiều cao `h`, mọi thứ tự mất `O(n)` thời gian, `O(h)` call stack và `O(n)` cho kết quả. Cây cân bằng: `h = O(log n)`; cây lệch: `h = O(n)`; gồm kết quả: `O(n + h)`.

| Phép đo | Độ phức tạp |
|:---|:---|:---|
| **Thời gian** | `O(n)` |
| **Call stack** | `O(h)` |
| **Độ sâu tối đa** | `O(log n)` cân bằng, `O(n)` lệch |
```
    cân bằng: o        lệch: o -> o -> o -> ... -> o
              / \       một frame hoạt động cho mỗi mức
```

---

## 10. BFS so với DFS
**Duyệt theo chiều rộng (Breadth-First Search — BFS)** dùng hàng đợi FIFO và thăm theo mức; DFS dùng đệ quy hoặc ngăn xếp LIFO và đi theo nhánh.
| Đặc điểm | BFS | DFS |
|:---|:---|:---|
| Thứ tự thăm | theo từng mức | nhánh sâu rồi quay lui |
| Lưu trữ | hàng đợi/FIFO | call stack/ngăn xếp LIFO |
| Thời gian | `O(n)` | `O(n)` |
| Không gian | `O(w)`, độ rộng tối đa | `O(h)`, chiều cao |
| Câu hỏi phù hợp | gần gốc nhất? | có gì dưới nhánh này? |
| Ứng dụng | theo mức/đường ngắn nhất không trọng số | kết quả có thứ tự/xử lý cây con |
```
    BFS theo độ rộng: o o o o       DFS theo chiều cao: o
                          hàng đợi                       |
                                                        o
```

---

## 11. File phỏng vấn và checklist
| Tên file | Mục đích |
|:---|:---|
| `BST-Kth Smallest Node.py` | đếm trung thứ tự để tìm giá trị BST nhỏ thứ k |
| `BST-Validate BST.py` | kết quả trung thứ tự phải tăng nghiêm ngặt khi BST hợp lệ |
```
    Dòng trung thứ tự BST: 18 -> 21 -> 27 -> 47 -> 52 -> 76 -> 82
                            ^ giá trị thứ k       ^ bất biến thứ tự
```
**Tóm tắt:** DFS khám phá sâu, quay lui qua call stack, chạy trong `O(n)` và dùng `O(h)` không gian ngăn xếp duyệt. Vị trí thăm tạo ra ý nghĩa khác nhau cho tiền thứ tự, trung thứ tự và hậu thứ tự.
