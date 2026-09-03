
---

# Cấu trúc Đồ thị và Cách cài đặt (Graph Structure Code Implementation)

## 1. Mục tiêu

Đồ thị (graph) là một sự mở rộng của cây N-ary. Cây có những quy tắc nghiêm
ngặt: một nút cha có thể trỏ đến các nút con, nhưng nút con không bao giờ trỏ
ngược về nút cha, và các nút anh em không bao giờ trỏ vào nhau. Đồ thị bỏ đi
tất cả những quy tắc đó, nên bất kỳ nút nào cũng có thể trỏ đến bất kỳ nút nào
khác, tạo thành những mạng lưới phong phú.

Bài viết này xây dựng hai cách lưu trữ đồ thị kinh điển trong code — **danh sách
kề** (adjacency list) và **ma trận kề** (adjacency matrix) — và trình bày cả bốn
tổ hợp của đồ thị có hướng/không hướng và có trọng số/không trọng số.

Nguồn tham khảo:
- https://labuladong.online/en/algo/data-structure-basic/graph-basic/

---

## 2. Vì sao Đồ thị ra đời

Cây ép buộc một mối quan hệ cha-con một chiều nghiêm ngặt. Nhiều vấn đề thực tế
không khớp với hình dạng đó:

```text
tree:                          graph:

      A                               A
     / \                            /   \
    B   C       B cannot           B <---> C
   /     \      point back,        | \   / |
  D       E     siblings           D---E---F
                cannot connect

  A social network, a road map, an electric circuit,
  or a web of dependencies is NOT a tree.
```

Đồ thị ra đời để mô hình hóa những thứ liên kết với nhau theo cách bất kỳ:

* mạng xã hội (bạn bè theo dõi lẫn nhau)
* mạng lưới đường bộ / hàng không (thành phố bất kỳ nối với thành phố khác)
* bảng mạch và hệ thống ống nước (linh kiện chạm vào nhiều lân cận)
* đồ thị phụ thuộc (một tác vụ có thể phụ thuộc vào nhiều tác vụ khác)

Một đồ thị đơn giản là một tập hợp các **nút** (vertices) và các **cạnh**
(edges) nối chúng lại với nhau.

---

## 3. Các khối cơ bản: Đỉnh và Cạnh

Một đỉnh chỉ là một điểm có nhãn. Một cạnh nối hai đỉnh và có thể mang một
**trọng số** (weight — một chi phí, khoảng cách, hoặc dung lượng).

```text
  a labelled vertex:              an edge with a weight:

        ( 0 )                     0 ------w=3------> 1
        (   )
```

Đồ thị được mô tả bằng bốn thuộc tính:

| Thuộc tính | Lựa chọn | Ý nghĩa |
|:---|:---|:---|
| Hướng | có hướng / không hướng | Cạnh có mũi tên không? |
| Trọng số | có trọng số / không trọng số | Cạnh có mang chi phí không? |
| Chu trình | có chu trình / không chu trình | Bạn có thể vòng lại một nút không? |
| Liên thông | liên thông / không liên thông | Mọi nút có chạm được mọi nút khác không? |

Code trong `GraphStructure.py` tập trung vào hai thuộc tính đầu tiên, vì chúng
làm thay đổi cách đồ thị được lưu trữ vật lý.

---

## 4. Hai Chiến lược Lưu trữ

Có hai cách chiếm ưu thế để lưu trữ một đồ thị, và mọi thư viện đồ thị đều được
xây trên một trong hai (hoặc cả hai).

### 4.1 Danh sách kề (Adjacency List)

Mỗi nút giữ một danh sách các nút mà nó có thể chạm tới.

```text
      1
     / \
    2   3
     \
      4

  adjacency list:
  1 -> [2, 3]
  2 -> [4]
  3 -> []
  4 -> []
```

### 4.2 Ma trận kề (Adjacency Matrix)

Một bảng `V x V` trong đó ô `[u][v]` cho biết liệu (và với chi phí nào) `u` có
thể chạm tới `v`.

```text
      1
     / \
    2   3
     \
      4

  adjacency matrix (1 = edge exists, 0 = no edge):

          1   2   3   4
    1  [  0   1   1   0 ]
    2  [  0   0   0   1 ]
    3  [  0   0   0   0 ]
    4  [  0   0   0   0 ]
```

### 4.3 Lựa chọn giữa hai cách

```text
              adjacency list          adjacency matrix
  memory       O(V + E)               O(V^2) always
  edge (u,v)?  walk u's list O(deg)   O(1) direct lookup
  iterate out  O(deg)                 O(V)
  best for     sparse (E << V^2)      dense (E ~ V^2)
  simple?      yes                    very simple
```

Quy tắc chung: dùng **danh sách kề** trừ khi đồ thị nhỏ và dày đặc. Đồ thị thực
tế gần như luôn thưa, nên danh sách kề thắng trong thực hành.

---

## 5. Bốn Tổ hợp

Module `GraphStructure.py` phơi bày một API thống nhất với nút được đánh số
(`0 .. n-1`). Mọi biểu diễn đều hỗ trợ ba thao tác giống nhau:

```python
graph.size()              # number of nodes
graph.neighbors(u)        # outgoing edges from node u
graph.add_edge(u, v, w)   # add an edge with weight w
```

Bốn tổ hợp lưu trữ là:

| Lưu trữ | Có hướng | Không hướng |
|:---|:---|:---|
| Danh sách kề | `Graph` | `UndirectedGraph` |
| Ma trận kề | `MatrixGraph` | `UndirectedMatrixGraph` |

---

## 6. Đồ thị Có hướng Có trọng số (Danh sách kề)

`Graph` lưu mỗi cạnh có hướng một lần, trong danh sách của nút nguồn.

```text
  edges:
    0 -> 1 (1)
    0 -> 2 (4)
    1 -> 2 (2)
    2 -> 3 (3)

  adjacency list:
    0: [1(w=1), 2(w=4)]
    1: [2(w=2)]
    2: [3(w=3)]
    3: []
```

```python
g = Graph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
g.neighbors(0)   # [Edge(0->1, w=1.0), Edge(0->2, w=4.0)]
```

Bởi vì cạnh có hướng, `0 -> 1` xuất hiện trong danh sách của nút `0` nhưng KHÔNG
xuất hiện trong danh sách của nút `1`.

---

## 7. Đồ thị Có hướng Có trọng số (Ma trận kề)

`MatrixGraph` lưu cùng một đồ thị trong một bảng `V x V`. `None` nghĩa là
"không có cạnh".

```text
          0    1    2    3
    0  [  .    1    4    . ]
    1  [  .    .    2    . ]
    2  [  .    .    .    3 ]
    3  [  .    .    .    . ]

  lookup weight(0,2) = 4    (direct O(1) read)
  lookup weight(0,3) = None (no edge)
```

```python
mg = MatrixGraph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
mg.weight(0, 2)   # 4.0
mg.weight(0, 3)   # None
```

---

## 8. Đồ thị Không hướng Có trọng số (Danh sách kề)

`UndirectedGraph` coi mỗi cạnh là một liên kết hai chiều. Một cạnh `u-v` được
lưu **hai lần**: một lần trong danh sách của `u` và một lần trong danh sách của
`v`.

```text
  edges:
    0 - 1 (1)
    0 - 2 (4)
    1 - 2 (2)
    2 - 3 (3)

  adjacency list (each edge appears twice):
    0: [1(w=1), 2(w=4)]
    1: [0(w=1), 2(w=2)]
    2: [0(w=4), 1(w=2), 3(w=3)]
    3: [2(w=3)]
```

```python
ug = UndirectedGraph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
ug.neighbors(1)   # [Edge(1->0, w=1.0), Edge(1->2, w=2.0)]
```

Nhân đôi bộ nhớ là cái giá để có thể đi bộ cạnh theo cả hai hướng.

---

## 9. Đồ thị Không hướng Có trọng số (Ma trận kề)

`UndirectedMatrixGraph` ghi mỗi cạnh không hướng vào **cả hai** ô `[u][v]` và
`[v][u]`, nên ma trận luôn đối xứng.

```text
          0    1    2    3
    0  [  .    1    4    . ]
    1  [  1    .    2    . ]
    2  [  4    2    .    3 ]
    3  [  .    .    3    . ]

  the matrix is symmetric: weight(u,v) == weight(v,u)
```

```python
umg = UndirectedMatrixGraph(4, [(0, 1, 1.0), (0, 2, 4.0), (1, 2, 2.0), (2, 3, 3.0)])
umg.weight(1, 2)   # 2.0
umg.weight(2, 1)   # 2.0   (symmetric)
```

---

## 10. Đồ thị Không trọng số như một Trường hợp Đặc biệt

Đồ thị không trọng số chỉ là đồ thị có trọng số với mọi cạnh có trọng số `1`.
Phần cài đặt tham chiếu mặc định `weight` là `1.0`, nên bạn có thể bỏ qua nó:

```python
# unweighted directed graph, every edge has weight 1
g = Graph(3)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 0)
```

Với đồ thị không trọng số, một ma trận boolean đơn giản hoặc một danh sách các
id lân cận là đủ — cột trọng số chỉ đơn giản bị bỏ đi.

```text
  unweighted adjacency list:      unweighted matrix:
    0: [1, 2]                          0   1   2
    1: [2]                       0  [  0   1   1 ]
    2: [0]                       1  [  0   0   1 ]
                                 2  [  1   0   0 ]
```

---

## 11. API Thống nhất là điều Quan trọng

Chú ý rằng mọi biểu diễn đều phơi bày đúng những phương thức giống nhau:

```python
graph.size()               # -> int
graph.neighbors(u)         # -> list of Edge
graph.add_edge(u, v, w)    # -> None
```

Đây là quyết định thiết kế quan trọng nhất trong module. Vì API thống nhất,
**các thuật toán đồ thị viết một lần theo giao diện này sẽ chạy không thay đổi
trên mọi biểu diễn**. Duyệt, đường đi ngắn nhất, và các thuật toán cây khung
nhỏ nhất (các bài viết sau trong chuỗi này) không bao giờ quan tâm tầng lưu trữ
phía sau là danh sách hay ma trận — chúng chỉ gọi `neighbors(u)`.

```text
                 uniform API
  algorithms <----------------- Graph / UndirectedGraph
      |                        MatrixGraph / UndirectedMatrixGraph
      |
      +--- call only: size(), neighbors(), add_edge()
```

---

## 12. Tóm tắt Độ phức tạp

| Lưu trữ | Bộ nhớ | Tra cứu cạnh `(u,v)` | Liệt kê lân cận của `u` |
|:---|:---:|:---:|:---:|
| Danh sách kề | `O(V + E)` | `O(deg(u))` | `O(deg(u))` |
| Ma trận kề | `O(V^2)` | `O(1)` | `O(V)` |

trong đó `V` là số nút và `E` là số cạnh.

* Ma trận kề tỏa sáng với đồ thị **dày đặc** khi `E ~ V^2`, vì tra cứu cạnh là
  `O(1)` và ma trận nhỏ so với kích thước của nó.
* Danh sách kề tỏa sáng với đồ thị **thưa** khi `E << V^2`, vì nó chỉ lưu
  những gì thực sự tồn tại.

---

## 13. Những Sai lầm Thường gặp

### Sai lầm 1: Quên lưu cạnh không hướng hai lần

Trong danh sách kề không hướng, `add_edge(u, v)` phải thêm vào CẢ HAI
`adj[u]` và `adj[v]`. Lưu một lần vô tình biến đồ thị thành có hướng.

### Sai lầm 2: Dùng sai biểu diễn cho độ dày của đồ thị

Dùng ma trận `V^2` cho đồ thị một triệu nút và một nghìn cạnh sẽ lãng phí
hàng gigabyte. Dùng danh sách kề cho đồ thị thưa.

### Sai lầm 3: Nhầm lẫn có hướng và không hướng

Trong đồ thị có hướng, `0 -> 1` không suy ra `1 -> 0`. Trong đồ thị không
hướng thì có. Hai loại có cấu trúc kề khác nhau (một bản sao so với hai).

### Sai lầm 4: Không chuẩn hóa nhãn nút

API mong đợi nhãn `0 .. n-1`. Nếu đầu vào của bạn dùng nhãn tùy ý (chuỗi,
hoặc id bắt đầu từ 1), bạn phải ánh xạ chúng về phạm vi này trước, nếu không
việc lập chỉ mục mảng/bảng sẽ hỏng.

---

## 14. Chạy Ví dụ

Chạy:

```text
python GraphStructure.py
```

Đầu ra ổn định mong đợi (hiển thị cho đồ thị 4 nút ở trên):

```text
=== Directed weighted graph, adjacency list ===
0: [1(w=1), 2(w=4)]
1: [2(w=2)]
2: [3(w=3)]
3: []

=== Same graph as adjacency matrix ===
      0     1     2     3
 0    .     1     4     .
 1    .     .     2     .
 2    .     .     .     3
 3    .     .     .     .

=== Undirected graph, adjacency list (edge stored twice) ===
0: [1(w=1), 2(w=4)]
1: [0(w=1), 2(w=2)]
2: [0(w=4), 1(w=2), 3(w=3)]
3: [2(w=3)]

=== Undirected graph, adjacency matrix (symmetric) ===
      0     1     2     3
 0    .     1     4     .
 1    1     .     2     .
 2    4     2     .     3
 3    .     .     3     .
```

Một dấu `.` trong ma trận nghĩa là "không có cạnh".

---

## 15. Bảng Tóm tắt Cuối cùng

```text
    1. A graph = vertices + edges, with no parent/child restriction.
    2. Adjacency list: each node owns a list of its outgoing edges.
    3. Adjacency matrix: a V x V table; cell [u][v] is the edge weight.
    4. Directed edge is stored once; undirected edge is stored twice.
    5. Unweighted is just weighted with every weight = 1.
    6. List -> O(V+E) space, good for sparse graphs.
    7. Matrix -> O(V^2) space, O(1) edge lookup, good for dense graphs.
    8. Expose a unified size()/neighbors()/add_edge() API.
    9. Algorithms written against the API work on any representation.
```

**Bước tiếp theo:** Hãy thử bài viết duyệt DFS/BFS tiếp theo, bài này đi bộ
đúng giao diện `neighbors(u)` này để thăm mọi nút.
