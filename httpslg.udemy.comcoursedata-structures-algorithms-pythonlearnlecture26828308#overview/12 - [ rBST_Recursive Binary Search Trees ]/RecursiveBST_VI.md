
---

# Cây tìm kiếm nhị phân đệ quy (recursive Binary Search Tree, rBST)
Các ghi chú mở rộng cây tìm kiếm nhị phân (Binary Search Tree, BST) ở thư mục 7: bất biến giữ nguyên, nhưng thao tác đi bằng đệ quy.
## 1. BST và rBST
Thư mục 7 dùng `while` và `temp`; thư mục này dùng lớp bao (wrapper) và helper riêng tư (private helper).
`ASCII: LẶP root -> temp -> child     ĐỆ QUY root -> helper(root) -> helper(child) -> trả nút`
Quy tắc vẫn là `left < node < right`; giá trị bằng nhau bị từ chối như ở thư mục 7.
---
## 2. Vì sao cây tự nhiên có tính đệ quy?
Mỗi con là gốc của một BST nhỏ hơn, nên một thao tác có cùng hình dạng ở mọi tầng.
`ASCII: (47) /\ (21) (76)   giải quyết(47) -> giải quyết(21 hoặc 76) -> giải quyết(con hoặc None)`
| Trạng thái | `current_node` là gốc cây con hiện tại |
| Điểm dừng | `None`, hoặc đã tìm thấy giá trị |
| Tiến triển | Gọi đúng một cây con nhỏ hơn |
---
## 3. Mẫu wrapper và helper private
Các phương thức công khai (public methods) `r_contains`, `r_insert` và `delete_node` che giấu `root`; helper nhận `current_node`.
`ASCII: public(value) -> private(current_node, value) -> private(left/right, value)`
Helper trả gốc cây con đã xử lý để cha nối lại `.left` hoặc `.right`.
---
## 4. Dấu vết contains đệ quy
Với `27`: `47` đi trái, `21` đi phải, `27` khớp; với `17`, `47 -> 21 -> 18 -> None` trả `False`.
`ASCII: [47] 27<47 -> [21] 27>21 -> [27] bằng -> True; đường thiếu -> None -> False`
Case cơ sở `None` và phép so sánh bằng dừng đệ quy trước khi truy cập con.
---
## 5. Chèn đệ quy và gắn nút trả về
`__r_insert(None, value)` là trường hợp cơ sở (base case) và trả `Node(value)`; lời gọi đang chờ gán kết quả vào con trỏ con.
`ASCII: (2).right -> None; helper(None,3) trả (3); bên gọi (caller) đặt (2).right = (3)`
Khi bằng nhau không có nhánh; nút cũ được trả lại. `r_insert` tạo root rỗng nhưng, khác `insert` lặp, không trả Boolean.
---
## 6. Lần đi `min_value`
Method được cung cấp là lặp: đi trái đến khi không còn con trái; nó giả định `current_node` không phải `None`.
`ASCII: (76) -> trái (52) -> trái None; trả 52; dùng làm nút kế tiếp (successor) từ cây con phải`
Giá trị ngoài cùng bên trái là giá trị nhỏ nhất lớn hơn đích khi xóa nút có hai con.
---
## 7. Xóa và ba trường hợp
`__delete_node` tìm đệ quy rồi trả cây con thay thế cho cha; các liên kết trước/sau cho thấy kết quả từng case.
`ASCII LÁ: TRƯỚC (21).left=(18) -> SAU (21).left=None`
`ASCII MỘT CON: TRƯỚC (47).left=(21).right=(27) -> SAU (47).left=(27)`
`ASCII HAI CON: TRƯỚC (47) có (21) và (76.left=52) -> chép successor 52 -> SAU root=(52), rồi xóa 52 cũ`
Lá trả `None`; một con trả chính con đó; hai con chép `min_value(current_node.right)` rồi xóa đệ quy successor trùng.
---
## 8. Biên và ngăn xếp lời gọi (call stack)
Cây rỗng contains là `False`, insert đầu tạo `root`, delete thiếu giữ nguyên cây, xóa nút duy nhất đặt `root=None`, chèn trùng không đổi.
`ASCII STACK: __r_contains(47) chờ -> (76) chờ -> (52) trả True -> True quay về root`
Stack sâu tối đa bằng chiều cao `h`; chuỗi đã sắp xếp có `h=n` và có thể chạm giới hạn đệ quy Python.
---
## 9. Độ phức tạp và so sánh với lặp
Mỗi thao tác đi một đường từ gốc tới lá: cân bằng `h=O(log n)`, suy biến `h=O(n)`, stack phụ đệ quy `O(h)`.
`ASCII CÂN BẰNG: (47)/\(21)(76)     SUY BIẾN: (10) -> (20) -> ... -> (n)`
| Thao tác | Cân bằng | Suy biến | Stack đệ quy |
|:---|:---:|:---:|:---:|
| contains / insert / delete | `O(log n)` | `O(n)` | `O(h)` |
| min walk | `O(log n)` | `O(n)` | `O(1)` |
| lưu trữ | `O(n)` | `O(n)` | - |
| BST lặp | loop, `O(1)` phụ | cùng worst case `O(n)` | không có call stack |
| BST đệ quy | giống định nghĩa cây; gắn nút trả về | cùng worst case `O(n)` | có rủi ro stack |
Đệ quy đổi luồng điều khiển, không đổi Big O; chỉ cây tự cân bằng mới kiểm soát chiều cao với mọi thứ tự chèn.
---
## 10. Code nguồn thực tế
Bốn khối mã (code blocks) sau được chép nguyên văn từ bốn file `Core/SOLUTION-*.py`, gồm cả ví dụ và comment.
### 10.1 `SOLUTION-BST-R_Insert.py`
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
        temp = self.root
        while (temp is not None):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False 


    def __r_contains(self, current_node, value):
        if current_node == None: 
            return False      
        if value == current_node.value:
            return True 
        if value < current_node.value:
            return self.__r_contains(current_node.left, value) 
        if value > current_node.value:
            return self.__r_contains(current_node.right, value)

    def r_contains(self, value):
        return self.__r_contains(self.root, value)

                  
    def __r_insert(self, current_node, value):
        if current_node == None: 
            return Node(value)   
        if value < current_node.value:
            current_node.left = self.__r_insert(current_node.left, value)
        if value > current_node.value:
            current_node.right = self.__r_insert(current_node.right, value) 
        return current_node    

    def r_insert(self, value):
        if self.root == None: 
            self.root = Node(value)
        self.__r_insert(self.root, value)  




my_tree = BinarySearchTree()
my_tree.r_insert(2)
my_tree.r_insert(1)
my_tree.r_insert(3)

"""
    THE LINES ABOVE CREATE THIS TREE:
                 2
                / \
               1   3
"""


print('Root:', my_tree.root.value)            
print('Root -> Left:', my_tree.root.left.value)        
print('Root -> Right:', my_tree.root.right.value)    



"""
    EXPECTED OUTPUT:
    ----------------
	Root: 2
	Root -> Left: 1
	Root -> Right: 3

"""




```
### 10.2 `SOLUTION-BST-R_Contains.py`
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
        temp = self.root
        while (temp is not None):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
        
    def __r_contains(self, current_node, value):
        if current_node == None: 
            return False      
        if value == current_node.value:
            return True 
        if value < current_node.value:
            return self.__r_contains(current_node.left, value) 
        if value > current_node.value:
            return self.__r_contains(current_node.right, value)


    def r_contains(self, value):
        return self.__r_contains(self.root, value)
        



my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print('BST Contains 27:')
print(my_tree.r_contains(27))

print('\nBST Contains 17:')
print(my_tree.r_contains(17))
                


"""
    EXPECTED OUTPUT:
    ----------------
    BST Contains 27:
    True

    BST Contains 17:
    False

"""
```
### 10.3 `SOLUTION-BST-Min_Value.py`
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
        temp = self.root
        while temp is not None:
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
    
    
    def min_value(self, current_node):
        while current_node.left is not None:
            current_node = current_node.left
        return current_node.value
        

        

my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)


print( my_tree.min_value(my_tree.root) )

print( my_tree.min_value(my_tree.root.right) )

            

"""
    EXPECTED OUTPUT:
    ----------------
	18
	52

"""
```
### 10.4 `SOLUTION-BST-Delete.py`
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
        temp = self.root
        while (temp is not None):
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
 

    def __r_contains(self, current_node, value):
        if current_node == None: 
            return False      
        if value == current_node.value:
            return True 
        if value < current_node.value:
            return self.__r_contains(current_node.left, value) 
        if value > current_node.value:
            return self.__r_contains(current_node.right, value)

    def r_contains(self, value):
        return self.__r_contains(self.root, value)

 
          
    def __r_insert(self, current_node, value):
        if current_node == None: 
            return Node(value)   
        if value < current_node.value:
            current_node.left = self.__r_insert(current_node.left, value)
        if value > current_node.value:
            current_node.right = self.__r_insert(current_node.right, value) 
        return current_node    

    def r_insert(self, value):
        if self.root == None: 
            self.root = Node(value)
        self.__r_insert(self.root, value)  


    def min_value(self, current_node):
        while (current_node.left is not None):
            current_node = current_node.left
        return current_node.value 

    def __delete_node(self, current_node, value):
	    if current_node == None: 
		    return None
	    if value < current_node.value:
		    current_node.left = self.__delete_node(current_node.left, value)
	    elif value > current_node.value: 
		    current_node.right = self.__delete_node(current_node.right, value)
	    else:
		    if current_node.left == None and current_node.right == None:
			    return None
		    elif current_node.left == None:
			    current_node = current_node.right
		    elif current_node.right == None:
			    current_node = current_node.left
		    else:
			    sub_tree_min = self.min_value(current_node.right)
			    current_node.value = sub_tree_min
			    current_node.right = self.__delete_node(current_node.right, sub_tree_min)
	    return current_node
    
    def delete_node(self, value):
        self.root = self.__delete_node(self.root, value)




my_tree = BinarySearchTree()
my_tree.r_insert(2)
my_tree.r_insert(1)
my_tree.r_insert(3)

"""
       2
      / \
     1   3
"""

print("root:", my_tree.root.value)
print("root.left =", my_tree.root.left.value)
print("root.right =", my_tree.root.right.value)


my_tree.delete_node(2)

"""
       3
      / \
     1   None
"""


print("\nroot:", my_tree.root.value)
print("root.left =", my_tree.root.left.value)
print("root.right =", my_tree.root.right)



"""
    EXPECTED OUTPUT:
    ----------------
	root: 2
	root.left = 1
	root.right = 3

	root: 3
	root.left = 1
	root.right = None

"""
```
