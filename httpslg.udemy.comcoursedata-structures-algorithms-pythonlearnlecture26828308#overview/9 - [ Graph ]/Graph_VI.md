
---

# Đồ thị (Graph)

## 1. Đồ thị là gì?

**Đồ thị (Graph)** là một cấu trúc dữ liệu gồm một tập hợp các **Đỉnh (Vertex)** — còn gọi là nút (node) — được nối với nhau bởi các **Cạnh (Edge)**. Đây là cấu trúc **tổng quát nhất** trong tất cả các cấu trúc ta đã học — **Danh sách liên kết (Linked List) là một Cây (Tree) bị ràng buộc**, và **Cây là một Đồ thị bị ràng buộc**.

Cây là một đồ thị với các quy tắc nghiêm ngặt: một gốc duy nhất, không có chu trình, đúng một đường đi giữa hai nút bất kỳ. Đồ thị bỏ hết các quy tắc đó — **bất kỳ đỉnh nào cũng có thể nối với bất kỳ đỉnh nào**, chu trình được phép tồn tại, và không hề có "gốc".

### Thuật ngữ chính:

* **Đỉnh (Vertex)** — một nút trong đồ thị (số nhiều: vertices).
* **Cạnh (Edge)** — một kết nối giữa hai đỉnh.
* **Kề nhau / Láng giềng (Adjacent / Neighbor)** — hai đỉnh được nối bởi một cạnh thì kề nhau.

### Các loại đồ thị:

* **Có hướng vs Vô hướng (Directed vs Undirected)** — cạnh có chiều (đường một chiều) hay không (đường hai chiều)?
* **Có trọng số vs Không trọng số (Weighted vs Unweighted)** — cạnh có mang chi phí/khoảng cách/giá trị hay tất cả đều ngang nhau?

> **Khóa học này xây dựng một đồ thị VÔ HƯỚNG, không trọng số, lưu bằng Danh sách kề (Adjacency List)** — một dictionary trong Python ánh xạ mỗi đỉnh tới một danh sách các láng giềng của nó.

### Minh họa — Cây vs Đồ thị:

```
        CÂY (đồ thị bị ràng buộc):            ĐỒ THỊ (tổng quát):

               A  <- một gốc                      A ------- B
              / \                                / \       /
             B   C                              /   \     /
            / \   \                            D ----- C
           D   E   F                            \     /
            ^   ^   ^                            \   /
            |   |   |                             E
       cấm chu trình                         chu trình ĐƯỢC phép
       một đường giữa 2 nút                  nhiều đường giữa 2 nút
```

### Các loại đồ thị — Minh họa:

```
        VÔ HƯỚNG (cạnh hai chiều):          CÓ HƯỚNG (cạnh một chiều):

            A --------- B                        A --------> B
            |           |                        |           |
            |           |                        v           v
            C --------- D                        C --------> D

        "A và B là bạn bè"                    "A theo dõi B"
            (Facebook)                           (Twitter/X)


        KHÔNG TRỌNG SỐ:                       CÓ TRỌNG SỐ:

            A --------- B                        A ---- 5 ---- B
            |           |                        |             |
            |           |                        2             7
            C --------- D                        |             |
                                                 C ---- 1 ---- D

        các cạnh ngang nhau                   cạnh có CHI PHÍ
                                              (khoảng cách, thờ gian, tiền)
```

---

## 2. Tại sao Đồ thị được tạo ra?

Tất cả các cấu trúc ta đã học đến giờ đều là **phân cấp hoặc đường thẳng**: danh sách liên kết là một đường thẳng, cây phân nhánh đi xuống từ một gốc duy nhất, và mỗi nút chỉ có **một cha**.

Nhưng thế giới thực đầy những **mạng lưới (network)**, chứ không phải phân cấp:

* **Thành phố và chuyến bay** — bạn có thể bay Thành phố A -> Thành phố B -> Thành phố C -> quay lại Thành phố A (một **chu trình**!). Cây không thể biểu diễn điều đó.
* **Mạng xã hội** — Alice kết bạn với Bob, Bob kết bạn với Carol, và Carol kết bạn với Alice. Quan hệ **nhiều-nhiều**.
* **World Wide Web** — các trang web liên kết lẫn nhau theo mọi hướng.

### Hạn chế của Cây:

```
    CÂY CÓ THỂ MÔ HÌNH:                    CHỈ ĐỒ THỊ MỚI MÔ HÌNH ĐƯỢC:

        Sơ đồ tổ chức công ty                   Đường bay
            CEO                                  NYC --------> LA
           /   \                                ^  \          ^
          VP   VP                               |    \        |
         /  \  /  \                             |     v       |
       ... ... ... ...                         CHI <--- DAL <---
           |                                       ^          |
       không chu trình, mỗi ngườ một sếp           |          |
                                                   SEA <------+
                                              (bay vòng tròn —
                                               cây CẤM điều này!)
```

### Tư tưởng cốt lõi của Đồ thị:

> Khi bài toán xoay quanh **mối quan hệ giữa các đối tượng** — và các mối quan hệ đó có thể vòng, chéo, nối theo bất kỳ mẫu nào — bạn cần một **Đồ thị**. Đây chính là cấu trúc nằm bên dưới bản đồ, mạng lưới, và chính Internet.

---

## 3. Các bài toán mà Đồ thị giải quyết

Đồ thị vận hành một số phần mềm quan trọng nhất thế giới:

```
    +---------------------------+----------------------------------------+
    |      ỨNG DỤNG             |      ĐỈNH / CẠNH                       |
    +---------------------------+----------------------------------------+
    | Mạng xã hội               | Ngườ dùng / kết bạn (vô hướng),       |
    | (Facebook, LinkedIn)      | theo dõi (có hướng)                    |
    +---------------------------+----------------------------------------+
    | Dẫn đường Google Maps     | Ngã tư / con đường (có trọng số       |
    |                           | theo khoảng cách hoặc thờ gian)       |
    +---------------------------+----------------------------------------+
    | Web crawling & PageRank   | Trang web / siêu liên kết (có hướng)  |
    +---------------------------+----------------------------------------+
    | Tô pô mạng                | Router, máy tính / dây cáp             |
    +---------------------------+----------------------------------------+
    | Giải quyết phụ thuộc      | Gói phần mềm, tác vụ / cạnh           |
    | (pip, npm, build systems) | "phụ thuộc vào" (có hướng)            |
    +---------------------------+----------------------------------------+
```

* **Mạng xã hội** — "gợi ý kết bạn" chính là các đỉnh cách bạn 2 cạnh.
* **Google Maps** — bài toán đường đi ngắn nhất: lộ trình nào có tổng trọng số nhỏ nhất?
* **Web crawling (PageRank)** — thuật toán gốc của Google xếp hạng trang web bằng cách phân tích đồ thị liên kết.
* **Tô pô mạng** — tìm cách nối tất cả máy tính rẻ nhất (cây khung nhỏ nhất).
* **Giải quyết phụ thuộc** — một gói chỉ được cài sau khi mọi thứ nó trỏ tới đã được cài.

### Những gì sắp tới:

Các phép **duyệt BFS và DFS** ở thư mục 13 được viết cho cây, nhưng chúng mở rộng **trực tiếp** sang đồ thị (chỉ cần theo dõi các đỉnh "đã thăm" để chu trình không lặp vô hạn). Sau đó là các thuật toán đồ thị nổi tiếng:

```
    BFS / DFS trên đồ thị  -->  Đường đi ngắn nhất (Dijkstra, Bellman-Ford)
                           -->  Cây khung nhỏ nhất (Prim, Kruskal)
                           -->  Sắp xếp Tô pô (thứ tự phụ thuộc)
```

---

## 4. Lưu trữ Đồ thị: Danh sách kề vs Ma trận kề

Có hai cách kinh điển để lưu đồ thị trong bộ nhớ. Ta dùng cùng một đồ thị ví dụ cho cả hai:

```
            A --------- B
            |           |
            |           |
            C --------- D

        Các cạnh: A-B, A-C, B-D, C-D
```

### Cách 1 — Ma trận kề (Adjacency Matrix, lưới 2 chiều):

Một lưới `V x V` gồm các số 0 và 1. `matrix[A][B] = 1` nghĩa là "cạnh A-B tồn tại".

```
              A   B   C   D
           +---+---+---+---+
        A  | 0 | 1 | 1 | 0 |
           +---+---+---+---+
        B  | 1 | 0 | 0 | 1 |
           +---+---+---+---+
        C  | 1 | 0 | 0 | 1 |
           +---+---+---+---+
        D  | 0 | 1 | 1 | 0 |
           +---+---+---+---+

        Hàng A nói: "A chạm tớ B và C"
```

### Cách 2 — Danh sách kề (Adjacency List, dictionary của các danh sách) — **cách khóa học dùng**:

Mỗi đỉnh ánh xạ tới **danh sách chỉ gồm các láng giềng của nó**:

```
        {
            'A' : ['B', 'C'],
            'B' : ['A', 'D'],
            'C' : ['A', 'D'],
            'D' : ['B', 'C']
        }

        Khóa 'A' nói: "A chạm tớ B và C"
```

### Tại sao Danh sách kề thắng (với đa số đồ thị thực tế):

```
    +----------------------+--------------------+--------------------+
    |                      |  DANH SÁCH KỀ     |  MA TRẬN KỀ        |
    +----------------------+--------------------+--------------------+
    | Bộ nhớ               | O(V + E)           | O(V^2)             |
    |                      | (chỉ cạnh thật)    | (mọi ô, kể cả ô   |
    |                      |                    |  trống)            |
    +----------------------+--------------------+--------------------+
    | Kiểm tra "A-B có     | O(bậc)             | O(1)               |
    | phải cạnh không?"    | quét ds láng giềng | một phép tra lưới  |
    +----------------------+--------------------+--------------------+
    | Phù hợp nhất vớ     | đồ thị THƯA        | đồ thị DÀY ĐẶC    |
    |                      | (ít cạnh — đa số   | (gần như mọi cặp   |
    |                      |  mạng thực tế)     |  đều nối nhau)     |
    +----------------------+--------------------+--------------------+

    Facebook: ~3 tỷ ngườ dùng, mỗi ngườ ~300 bạn.
        Ma trận: 3 tỷ x 3 tỷ ô = 9 TRIỆU TỶ ô   <- không thể!
        Danh sách: 3 tỷ x 300 mục               <- hoàn toàn ổn
```

---

## 5. Đồ thị hoạt động thế nào — Từng bước

Lớp này lưu mọi thứ trong `self.adj_list`, một dictionary trong đó:

```
        khóa  = một đỉnh
        giá trị = DANH SÁCH các láng giềng của đỉnh đó
```

### 5.1 `add_vertex` — Thêm khóa với danh sách rỗng

Một đỉnh mới tinh **chưa có cạnh nào**, nên nó nhận một danh sách láng giềng rỗng:

```
    TRƯỚC:  adj_list = {}

    add_vertex('A'):

    SAU:    adj_list = { 'A' : [] }

                 A      <- tồn tại, nhưng chưa nối vớ ai
```

Nếu đỉnh **đã tồn tại**, phương thức trả về `False` và không thay đổi gì.

### 5.2 `add_edge` — Thêm mỗi đỉnh vào danh sách của đỉnh kia

Vì đồ thị là **vô hướng**, mỗi cạnh được lưu **hai lần** — một lần ở mỗi phía:

```
    TRƯỚC:  { 1: [], 2: [] }

        1       2          <- chưa có cạnh

    add_edge(1, 2):
        thêm 2 vào adj_list[1]      -->  1: [2]
        thêm 1 vào adj_list[2]      -->  2: [1]   <- CẢ HAI chiều!

    SAU:    { 1: [2], 2: [1] }

        1 ------- 2        <- một cạnh vô hướng
```

**Trường hợp biên từ code:** nếu một trong hai đỉnh **không có** trong dictionary, trả về `False` — bạn không thể nối các đỉnh không tồn tại.

### 5.3 `remove_edge` — Xóa cả hai chiều

Phép ngược của `add_edge` — xóa mỗi đỉnh khỏi danh sách của đỉnh **kia**:

```
    TRƯỚC:  A : ['B', 'C']
            B : ['A', 'C']
            C : ['B', 'A']

            A ----- B
             \     /
              \   /
                C

    remove_edge('A', 'C'):
        xóa 'C' khỏi adj_list['A']  -->  A : ['B']
        xóa 'A' khỏi adj_list['C']  -->  C : ['B']

    SAU:    A : ['B']
            B : ['A', 'C']
            C : ['B']

            A ----- B
                   /
                  /
                C          <- cạnh A-C đã biến mất
```

Code bọc thao tác xóa trong `try/except ValueError` để xóa một cạnh **không tồn tại** thì không làm gì cả (vẫn trả về `True`). Nếu một trong hai đỉnh **hoàn toàn vắng mặt**, trả về `False`.

### 5.4 `remove_vertex` — Xóa đỉnh VÀ mọi cạnh trỏ tới nó

Đây là phép khó nhất. Bạn không thể chỉ xóa khóa — mọi láng giềng vẫn còn **tham chiếu lủng lẳng** tới nó. Trước tiên bạn phải duyệt danh sách láng giềng của đỉnh đó và xóa nó khỏi danh sách của **từng** láng giềng:

```
    TRƯỚC:  A : ['B', 'C', 'D']
            B : ['A', 'D']
            C : ['A', 'D']
            D : ['A', 'B', 'C']

                 A
               / | \
              B--D--C        <- D nối vớ A, B, C

    remove_vertex('D'):

        Bước 1: duyệt adj_list['D'] = ['A', 'B', 'C']

            other_vertex = 'A':  xóa 'D' khỏi ds của A
                                 A : ['B', 'C', 'D'] -> ['B', 'C']
            other_vertex = 'B':  xóa 'D' khỏi ds của B
                                 B : ['A', 'D']      -> ['A']
            other_vertex = 'C':  xóa 'D' khỏi ds của C
                                 C : ['A', 'D']      -> ['A']

        Bước 2: BÂY GIỜ mớ xóa chính khóa đó:
                del adj_list['D']

    SAU:    A : ['B', 'C']
            B : ['A']
            C : ['A']

                 A
                / \
               B   C         <- D và MỌI cạnh của nó đều biến mất
```

**Trường hợp biên từ code:** nếu đỉnh **không có trong dictionary**, trả về `False`.

---

## 6. Code đầy đủ

Đây là lớp `Graph` hoàn chỉnh (từ `SOLUTION-GR-Remove_Vertex.py`, chứa tất cả các phương thức):

```python
class Graph:
    def __init__(self):
        self.adj_list = {}

    def print_graph(self):
        for vertex in self.adj_list:
            print(vertex, ':', self.adj_list[vertex])

    def add_vertex(self, vertex):
        if vertex not in self.adj_list.keys():
            self.adj_list[vertex] = []
            return True
        return False

    def add_edge(self, v1, v2):
        if v1 in self.adj_list.keys() and v2 in self.adj_list.keys():
            self.adj_list[v1].append(v2)
            self.adj_list[v2].append(v1)
            return True
        return False

    def remove_edge(self, v1, v2):
        if v1 in self.adj_list.keys() and v2 in self.adj_list.keys(): 
            try:
                self.adj_list[v1].remove(v2)
                self.adj_list[v2].remove(v1)
            except ValueError:
                pass
            return True
        return False

    def remove_vertex(self, vertex):
        if vertex in self.adj_list.keys():
            for other_vertex in self.adj_list[vertex]:
                self.adj_list[other_vertex].remove(vertex)
            del self.adj_list[vertex]
            return True
        return False        
```

### Chạy thử (từ file SOLUTION):

```python
my_graph = Graph()
my_graph.add_vertex('A')
my_graph.add_vertex('B')
my_graph.add_vertex('C')
my_graph.add_vertex('D')

my_graph.add_edge('A','B')
my_graph.add_edge('A','C')
my_graph.add_edge('A','D')
my_graph.add_edge('B','D')
my_graph.add_edge('C','D')

my_graph.remove_vertex('D')
```

### Kết quả:

```
    Đồ thị trước remove_vertex():
    A : ['B', 'C', 'D']
    B : ['A', 'D']
    C : ['A', 'D']
    D : ['A', 'B', 'C']

    Đồ thị sau remove_vertex():
    A : ['B', 'C']
    B : ['A']
    C : ['A']
```

---

## 7. Phân tích Big O

### Các phép toán trên Đồ thị (Danh sách kề):

| Phép toán | Độ phức tạp thờ gian | Lý do |
|:---|:---|:---|
| **Thêm Đỉnh (Add Vertex)** | `O(1)` | Một phép chèn vào dictionary |
| **Thêm Cạnh (Add Edge)** | `O(1)` | Hai phép append vào list |
| **Xóa Cạnh (Remove Edge)** | `O(V)` | Phải quét danh sách láng giềng của một đỉnh để tìm giá trị (trường hợp xấu nhất: một đỉnh nối tới tất cả `V-1` đỉnh còn lại) |
| **Xóa Đỉnh (Remove Vertex)** | `O(V + E)` | Duyệt các láng giềng của đỉnh (`O(V)` xấu nhất) và xóa nó khỏi danh sách của từng láng giềng; mỗi cạnh bị ảnh hưởng được chạm đúng một lần |
| **Bộ nhớ (Space)** | `O(V + E)` | Một khóa cho mỗi đỉnh + một mục danh sách cho mỗi đầu cạnh (mỗi cạnh lưu hai lần) |

> `V` = số đỉnh, `E` = số cạnh. Một cạnh giữa hai đỉnh xuất hiện **hai lần** trong danh sách kề vô hướng, nên bộ nhớ là `O(V + E)` chứ không chỉ `O(V)`.

### Danh sách kề vs Ma trận kề — So sánh cuối cùng:

| | **Danh sách kề** | **Ma trận kề** |
|:---|:---|:---|
| **Bộ nhớ** | `O(V + E)` | `O(V^2)` |
| **Thêm Đỉnh** | `O(1)` | `O(V^2)` (dựng lại lưới) hoặc `O(V)` (thêm hàng/cột) |
| **Thêm Cạnh** | `O(1)` | `O(1)` |
| **Kiểm tra Cạnh tồn tại** | `O(bậc)` — quét danh sách láng giềng | `O(1)` — tra lưới trực tiếp |
| **Xóa Đỉnh** | `O(V + E)` | `O(V^2)` |
| **Phù hợp nhất với** | Đồ thị **thưa** (ít cạnh mỗi đỉnh — mạng xã hội, bản đồ) | Đồ thị **dày đặc** (gần như mọi cặp đều nối) |

---

## 8. Tóm tắt

```
    +----------------------------------------------------------+
    |  ĐỒ THỊ = Đỉnh + Cạnh                                    |
    +----------------------------------------------------------+
    |  - Tổng quát hóa cây (cây cấm chu trình & nhiều đường)  |
    |  - Có hướng hoặc vô hướng, có trọng số hoặc không       |
    |  - Lưu bằng DANH SÁCH KỀ: dict các ds láng giềng        |
    |                                                          |
    |  add_vertex    ->  khóa mớ, ds rỗng             O(1)     |
    |  add_edge      ->  thêm CẢ HAI chiều            O(1)     |
    |  remove_edge   ->  xóa CẢ HAI chiều             O(V)     |
    |  remove_vertex ->  dọn láng giềng TRƯỚC,        O(V+E)   |
    |                    rồ mớ xóa khóa                        |
    +----------------------------------------------------------+
```

---

**Bước tiếp theo:** Giờ hãy duyệt đồ thị này — lấy các phép duyệt BFS và DFS từ thư mục 13 và xem chúng đi qua một đồ thị có chu trình thế nào, rồi chinh phục các bài toán đường đi ngắn nhất kinh điển!
