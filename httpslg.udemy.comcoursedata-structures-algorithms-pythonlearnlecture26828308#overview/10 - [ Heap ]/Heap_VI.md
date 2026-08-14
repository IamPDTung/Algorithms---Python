
---

# Đống (Heap)

## 1. Cây hoàn chỉnh và đống cực đại

**Đống (heap)** là cấu trúc dạng cây giúp một giá trị cực trị quan trọng luôn dễ truy cập. Ghi chú này dùng **đống nhị phân cực đại (binary max-heap)**: mỗi nút có nhiều nhất hai nút con, cây hoàn chỉnh, và mọi nút cha lớn hơn hoặc bằng các nút con.

**Cây nhị phân hoàn chỉnh (complete binary tree)** lấp đầy từng tầng từ trái sang phải. Chỉ tầng cuối có thể chưa đầy và tầng đó không được có khoảng trống trước một nút khác. Đống cực đại thêm quy tắc thứ tự cha-con; nó không sắp xếp các nút anh em hay toàn bộ các nhánh.

```
    CÂY HOÀN CHỈNH                         TÍNH CHẤT ĐỐNG CỰC ĐẠI

             95                                  95
           /    \                              /    \
         75      80                           75      80
        /  \    /  \                         /  \    /  \
      55   60  50   65                      55  60  50  65

    Tầng cuối lấp từ trái sang phải.          95 >= 75,80; 75 >= 55,60;
                                               80 >= 50,65.

    giá trị lớn nhất = gốc = heap[0]         không phải cây sắp xếp toàn bộ
```

Nếu có con phải trong khi vị trí con trái trước đó trống, cây không hoàn chỉnh. Tính hoàn chỉnh là lý do phần cài đặt có thể dùng list gọn thay vì con trỏ nút.

---

## 2. Đống cực đại, đống cực tiểu và lý do tồn tại

**Đống cực đại (max-heap)** giữ phần tử lớn nhất ở gốc. **Đống cực tiểu (min-heap)** đảo phép so sánh và giữ phần tử nhỏ nhất ở gốc; hình dạng và công thức chỉ số vẫn giữ nguyên.

```
    ĐỐNG CỰC ĐẠI (cha lớn hơn)              ĐỐNG CỰC TIỂU (cha nhỏ hơn)

             95                                  10
           /    \                              /    \
         75      80                            20     15
        /  \    /  \                           / \    / \
      55   60  50   65                        40 30  25 35

    gốc = cực đại                           gốc = cực tiểu
    bọt nếu con > cha                       bọt nếu con < cha
```

List chưa sắp xếp phải quét mọi giá trị để tìm cực đại. List đã sắp xếp cho cực trị nhanh nhưng có thể tốn `O(n)` để duy trì sau khi chèn. Heap chỉ giữ thứ tự cần thiết tại gốc, nên `peek` là `O(1)` và cập nhật là `O(log n)`.

```
    CHƯA SẮP XẾP: [55, 95, 50, 80, 65, 75] -> quét tất cả -> O(n)
    ĐỐNG CỰC ĐẠI:             95           -> đọc heap[0] -> O(1)
                              /  \
                            75    80
```

Heap hỗ trợ **hàng đợi ưu tiên (priority queue)**, **sắp xếp bằng heap (heap sort)**, truy vấn phần tử thứ k, giá trị lớn nhất trong luồng, lập lịch và thuật toán đồ thị. Hàng đợi ưu tiên liên tục xóa gốc thay vì giữ mọi phần tử theo thứ tự toàn cục.

```
    công việc đến -> heap theo độ ưu tiên -> công việc kế tiếp
    [thấp, cao, vừa] -> [cao, thấp, vừa]  -> cao (gốc)
```

---

## 3. Biểu diễn cây, mảng và công thức chỉ số

Cây logic được lưu trong Python list `self.heap`. Cách đặt theo thứ tự từng tầng giúp xác định địa chỉ cha và con bằng số học; không cần con trỏ `left` hoặc `right`.

```
    CÂY                                  MẢNG (theo thứ tự tầng)

             95                           chỉ số:  0  1  2  3  4  5  6
           /    \                         giá trị: [95,75,80,55,60,50,65]
         75      80
        /  \    /  \                      0=95, 1=75, 2=80, 3=55,
      55   60  50   65                    4=60, 5=50, 6=65
```

Với chỉ số bắt đầu từ 0 là `i`:

```text
left child  = 2 * i + 1
right child = 2 * i + 2
parent      = (i - 1) // 2
```

```
    i = 1 (75): left=3 (55), right=4 (60), parent=0 (95)

                 95 (0)
                /
             75 (1)
             /   \
          55 (3) 60 (4)
```

Phải kiểm tra giới hạn của nút con: lá không có con và nút cuối có thể chỉ có con trái.

---

## 4. Chèn: thêm vào cuối rồi bọt lên

Chèn thêm giá trị tại vị trí list trống tiếp theo để giữ hình dạng hoàn chỉnh, sau đó đổi chỗ với cha khi nó lớn hơn. Việc sửa đi lên này gọi là **bọt lên (bubble-up)** hoặc sift-up và nhiều nhất chỉ đi theo một đường đến gốc.

Truy vết cụ thể: bắt đầu với `[99, 72, 61, 58]`, chèn `100` tại chỉ số `4`; cha của nó là `72` tại chỉ số `1`.

```
    thêm: [99,72,61,58,100]       100 > 72

          99                 đổi chỉ số 4 <-> 1       99
         /  \              --------------------->    /  \
       72    61                                      100  61
      /  \                                            / \
    58  100                                          58  72

    mảng sau lần đổi 1: [99,100,61,58,72]
    100 > gốc 99, nên đổi chỉ số 1 <-> 0:

          100
         /   \
       99     61       mảng: [100,99,61,58,72]
      /  \
    58   72            chỉ số 0 không có cha: dừng
```

Thêm `75` vào `[100,99,61,58,72]` tạo `[100,99,61,58,72,75]`; so sánh với cha `61`, đổi một lần thành `[100,99,75,58,72,61]`, rồi dừng vì `75 < 99`.

---

## 5. Xóa gốc: đưa phần tử cuối lên rồi chìm xuống

Để xóa cực đại, lưu `heap[0]`, đưa giá trị cuối lên chỉ số `0`, `pop` ô cuối, rồi **chìm xuống (sink-down)**. Ở mỗi tầng, so sánh các con hợp lệ và đổi với con lớn hơn nếu nó lớn hơn phần tử thay thế.

### Truy vết mọi so sánh của ví dụ source

Bắt đầu với `[95,75,80,55,60,50,65]`. Lưu `95`; đưa `65` lên gốc: `[65,75,80,55,60,50]`.

```
    trước:                   95                 sau khi đưa 65 lên:
                             /  \                         65
                           75    80                      /  \
                          / \   / \                    75    80
                        55  60 50 65                    / \   /
                                                       55 60 50

    chỉ số 0: so sánh trái 75 và phải 80; chọn 80 vì lớn hơn.
    80 > 65: ĐỔI CHỖ 1 -> [80,75,65,55,60,50].
    chỉ số 2: con trái chỉ số 5 là 50; con phải chỉ số 6 vượt giới hạn.
    so sánh 50 với 65: không đổi chỗ. Trả về 95.
```

Lần xóa thứ hai cho thấy đường đi nhiều tầng: đưa `50` vào `[50,75,65,55,60]`; so sánh `75` với `65`, đổi thành `[75,50,65,55,60]`; tại chỉ số `1` so sánh `55` với `60`, đổi với `60` thành `[75,60,65,55,50]`; chỉ số `4` không có con, trả về `80`.

```
    [80,75,65,55,60,50] -> đưa 50 -> [50,75,65,55,60]
    so sánh 75,65 -> đổi -> [75,50,65,55,60]
    so sánh 55,60 -> đổi -> [75,60,65,55,50]
```

### Trường hợp biên

```
    []       remove() -> None       [42]       remove() -> 42, rồi []
    chèn [] -> [value]               [42,17]    remove -> [17]
```

Solution kiểm tra heap rỗng trước `heap[0]`, dùng `pop()` cho một phần tử, bỏ qua con phải bị thiếu và dùng `>` chặt nên các giá trị bằng nhau không cần đổi chỗ.

---

## 6. Solution thực tế: Insert

Đây là toàn bộ nội dung của `Core/SOLUTION-Heap-Insert.py`, được chép nguyên văn.

```
    thêm -> so sánh cha -> đổi chỗ đi lên -> dừng tại gốc hoặc cha hợp lệ
```

```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _parent(self, index):
        return (index - 1) // 2

    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and self.heap[current] > self.heap[self._parent(current)]:
            self._swap(current, self._parent(current))
            current = self._parent(current)



myheap = MaxHeap()
myheap.insert(99)
myheap.insert(72)
myheap.insert(61)
myheap.insert(58)

print(myheap.heap)  


myheap.insert(100)

print(myheap.heap)  


myheap.insert(75)

print(myheap.heap)


"""
    EXPECTED OUTPUT:
    ----------------
    [99, 72, 61, 58]
    [100, 99, 61, 58, 72]
    [100, 99, 75, 58, 72, 61]

"""

```

---

## 7. Solution thực tế: Remove và Sink-Down

Cả hai tệp core còn lại đều có class và phần minh họa đầy đủ bên dưới. Chúng là hai tệp riêng nhưng cùng một implementation, nên cả hai được chép nguyên văn.

```
    xóa gốc -> đưa phần tử cuối lên -> chọn con lớn hơn -> lặp lại
```

### `SOLUTION-Heap-Remove.py`

```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _parent(self, index):
        return (index - 1) // 2

    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and self.heap[current] > self.heap[self._parent(current)]:
            self._swap(current, self._parent(current))
            current = self._parent(current)


    def _sink_down(self, index):
        max_index = index
        while True:
            left_index = self._left_child(index)
            right_index = self._right_child(index)

            if (left_index < len(self.heap) and 
                    self.heap[left_index] > self.heap[max_index]):
                max_index = left_index

            if (right_index < len(self.heap) and 
                    self.heap[right_index] > self.heap[max_index]):
                max_index = right_index

            if max_index != index:
                self._swap(index, max_index)
                index = max_index
            else:
                return
                       
    def remove(self):
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)

        return max_value



myheap = MaxHeap()
myheap.insert(95)
myheap.insert(75)
myheap.insert(80)
myheap.insert(55)
myheap.insert(60)
myheap.insert(50)
myheap.insert(65)

print(myheap.heap)


myheap.remove()

print(myheap.heap)


myheap.remove()

print(myheap.heap)


"""
    EXPECTED OUTPUT:
    ----------------
    [95, 75, 80, 55, 60, 50, 65]
    [80, 75, 65, 55, 60, 50]
    [75, 60, 65, 55, 50]

"""

```

### `SOLUTION-Heap-Sink_Down.py`

```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _parent(self, index):
        return (index - 1) // 2

    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and self.heap[current] > self.heap[self._parent(current)]:
            self._swap(current, self._parent(current))
            current = self._parent(current)


    def _sink_down(self, index):
        max_index = index
        while True:
            left_index = self._left_child(index)
            right_index = self._right_child(index)

            if (left_index < len(self.heap) and 
                    self.heap[left_index] > self.heap[max_index]):
                max_index = left_index

            if (right_index < len(self.heap) and 
                    self.heap[right_index] > self.heap[max_index]):
                max_index = right_index

            if max_index != index:
                self._swap(index, max_index)
                index = max_index
            else:
                return
                       
    def remove(self):
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)

        return max_value



myheap = MaxHeap()
myheap.insert(95)
myheap.insert(75)
myheap.insert(80)
myheap.insert(55)
myheap.insert(60)
myheap.insert(50)
myheap.insert(65)

print(myheap.heap)


myheap.remove()

print(myheap.heap)


myheap.remove()

print(myheap.heap)


"""
    EXPECTED OUTPUT:
    ----------------
    [95, 75, 80, 55, 60, 50, 65]
    [80, 75, 65, 55, 60, 50]
    [75, 60, 65, 55, 50]

"""

```

---

## 8. Tệp phỏng vấn và ứng dụng

Thư mục `Interview` có `Heap-Maximum Element in a Stream.py` và `Heap-Kth Smallest Element in an Array.py`. Mỗi tệp cung cấp `MaxHeap` và để trống một hàm cấp cao bên ngoài class.

```
    MAX TRONG LUỒNG: chèn từng giá trị, đọc gốc
    1 -> 3 -> 2 -> 5 -> 4       gốc: 1 -> 3 -> 3 -> 5 -> 5
    kết quả: [1, 3, 3, 5, 5]
```

Với bài toán luồng, chèn từng `nums[i]` và thêm `heap.heap[0]`. Các test gồm đầu vào rỗng, một phần tử, tăng dần, trùng lặp và số âm; đầu vào rỗng trả về `[]`.

```
    PHẦN TỬ NHỎ THỨ K, k=2: chỉ giữ hai giá trị trong max-heap
    [3,2,1,5,6,4] -> thêm/xóa khi cần -> [2,1] -> gốc 2
```

Với bài toán phần tử nhỏ thứ k, chèn từng số và xóa gốc lớn nhất khi heap vượt quá `k`. Gốc còn lại là phần tử nhỏ thứ k; các phần tử trùng nhau được tính ở các vị trí riêng. Hai tệp phỏng vấn là đề bài, không phải các tệp solution core bổ sung.

---

## 9. Big O và so sánh với list

Chiều cao của cây hoàn chỉnh là `O(log n)`, vì vậy bọt lên và chìm xuống đi qua nhiều nhất một đường logarit.

| Thao tác | Heap | List chưa sắp xếp | List đã sắp xếp |
|:---|:---:|:---:|:---:|
| Peek cực đại | **`O(1)`** | `O(n)` | `O(1)` |
| Insert | **`O(log n)`** | `O(1)` ở cuối | `O(n)` |
| Xóa cực đại | **`O(log n)`** | `O(n)` | `O(1)` |
| Tìm giá trị bất kỳ | `O(n)` | `O(n)` | `O(log n)` |
| Không gian | `O(n)` | `O(n)` | `O(n)` |

```
    XÂY DỰNG VÀ TRUY VẤN ĐẶC BIỆT

    n lần insert: O(n log n)             heapify từ dưới lên: O(n)
    heap sort: O(n log n)                nhỏ thứ k, heap k: O(n log k)
    stream max bằng heap này: O(n log n), không gian heap O(n)
```

Dùng list đã sắp xếp khi cần thứ tự đầy đủ hoặc tìm kiếm nhị phân. Dùng heap khi thường xuyên cần phần tử lớn nhất hoặc nhỏ nhất tiếp theo mà không muốn trả giá duy trì toàn bộ thứ tự.

---

## 10. Danh sách kiểm tra

```
    HÌNH DẠNG: lấp từ trái sang phải     THỨ TỰ: cha cực đại >= con
    INSERT: thêm, bọt lên                REMOVE: đưa cuối, chìm xuống
    BIÊN: kiểm tra con                   GỐC: heap[0] là cực đại
```

Kiểm tra heap rỗng và một phần tử trước khi truy cập con, chọn con lớn hơn khi chìm trong max-heap, và nhớ rằng heap chỉ có thứ tự từng phần chứ không phải list đã sắp xếp. Mẫu cốt lõi là **thêm vào cuối rồi bọt lên; thay gốc rồi chìm xuống**.
