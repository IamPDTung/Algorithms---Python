
---

# Khái niệm Cơ bản về Thuật toán Union-Find (Basic Concept of Union Find Algorithm)

## 1. Mục tiêu

Cấu trúc dữ liệu **Union-Find** (còn gọi là **Disjoint Set** — Tập rời nhau)
trả lời các câu hỏi về tính liên thông trong một đồ thị vô hướng trong thời
gian gần như hằng số:

```text
  union(p, q)      -> connect p and q into one group
  connected(p, q)  -> are p and q in the same group?
  count()          -> how many separate groups are there?
```

Nó là động cơ đằng sau thuật toán Kruskal (bài viết trước), các bài toán vòng
bạn bè, và tính liên thông động. Bài viết này giải thích khái niệm, vì sao nó
thắng việc duyệt đồ thị ngây thơ, và hai tối ưu hóa làm nó nhanh.

Nguồn tham khảo:
- https://labuladong.online/en/algo/data-structure-basic/union-find-basic/

---

## 2. Bài toán Tính liên thông Động

Xét 10 nút được đánh số `0..9` không có cạnh. Mỗi nút là một nhóm riêng — có 10
**thành phần liên thông**.

```text
  0  1  2  3  4  5  6  7  8  9     (10 isolated nodes, 10 components)
```

Bây giờ thực hiện một số **phép hợp (union)**: nối `0-1` và `1-2`.

```text
  after union(0,1) and union(1,2):

  0 -- 1 -- 2    3  4  5  6  7  8  9

  nodes 0,1,2 are now one component.
  components went from 10 down to 8.
```

**Bài toán tính liên thông động** hỏi: cho một chuỗi các phép hợp và truy vấn,
bạn có thể trả lời `connected(p, q)` và `count()` nhanh chóng khi đồ thị thay
đổi theo thời gian không?

Tính liên thông có ba tính chất hữu ích:

```text
  reflexivity:  p is connected to itself
  symmetry:     if p ~ q then q ~ p
  transitivity: if p ~ q and q ~ r then p ~ r
```

Tính chất bắc cầu là tính chất then chốt — nó chính là thứ khiến phép kiểm "có
cạnh trực tiếp không?" đơn giản thất bại, như ta thấy ngay sau đây.

---

## 3. Vì sao Duyệt Đồ thị Ngây thơ Quá Chậm

Một ý tưởng tự nhiên đầu tiên là lưu đồ thị bằng danh sách kề và chạy BFS/DFS
để trả lời `connected(p, q)`:

```python
# naive idea: BFS from p to see if q is reachable
def connected_via_dfs(adj, p, q):
    visited = [False] * len(adj)
    stack = [p]
    while stack:
        u = stack.pop()
        if u == q:
            return True
        if not visited[u]:
            visited[u] = True
            stack.extend(adj[u])
    return False
```

Nhưng đây là `O(V + E)` **cho mỗi truy vấn**. Và nó thất bại trong việc khai
thác tính bắc cầu:

```text
  0 -- 1 -- 2

  connected(0, 2)?
  there is no direct edge 0-2,
  but 0 connects to 1, and 1 connects to 2
  -> 0 and 2 ARE connected (transitively)

  a simple adjacency-matrix lookup "is there edge (0,2)?" would wrongly say no.
```

Vậy để xử lý tính bắc cầu bạn phải duyệt toàn bộ tập các nút chạm tới được —
chậm, và phải lặp lại cho mỗi truy vấn.

---

## 4. API của Union-Find

Union-Find giải quyết điều này chỉ với một mảng. Nó cung cấp:

```text
  class UF:
      init(n)        # O(n): n nodes, each its own component
      union(p,q)     # ~O(1): connect p and q
      connected(p,q) # ~O(1): are they in the same component?
      count()        # ~O(1): number of components
```

Điểm khéo léo: nó theo dõi tính liên thông bằng một **cây cho mỗi thành phần**,
nên `connected` chỉ cần so sánh gốc của hai cây — không cần duyệt.

---

## 5. Ý tưởng Cốt lõi: Một Cây cho Mỗi Thành phần

Biểu diễn mỗi thành phần như một cây. `parent[x]` trỏ tới cha của `x`; **gốc**
của một cây là nút có cha là chính nó.

```text
  array representation:

  index:   0  1  2  3  4  5
  parent: [0, 0, 0, 3, 3, 5]

  trees:
     0           3      5
    /|\         / \
   1 2 ...     4   ...

  connected(1,2)?  find(1)=0, find(2)=0 -> same root -> True
  connected(2,4)?  find(2)=0, find(4)=3 -> different roots -> False
```

`find(x)` đi lên các con trỏ cha để tới gốc:

```python
def find(self, x):
    while self._parent[x] != x:
        x = self._parent[x]
    return x
```

Rồi:

```python
def connected(self, p, q):
    return self.find(p) == self.find(q)

def union(self, p, q):
    rp, rq = self.find(p), self.find(q)
    if rp == rq:
        return False          # already connected
    self._parent[rp] = rq     # hang p's tree under q's tree
    self._count -= 1
    return True
```

`union` chỉ trỏ một gốc vào gốc kia — một phép ghi mảng duy nhất. `connected`
chỉ so sánh hai gốc. Cả hai đều rẻ. **Điều duy nhất** có thể sai là các cây mọc
quá cao.

---

## 6. Vấn đề: Cây có thể Suy biến thành Danh sách liên kết

Nếu không tối ưu, một chuỗi các phép union có thể làm một cây trở thành một
chuỗi dài. Xét `union(0,1), union(1,2), union(2,3), ...`:

```text
  0 -> 1 -> 2 -> 3 -> 4 -> 5

  find(5) must walk 5 steps up the chain
  -> O(V) per find, so O(V) per union/connected
  -> the whole thing is as slow as a linked list
```

```text
  naive parent array after 0..5 chained:
  [1, 2, 3, 4, 5, 5]

  0 -> 1 -> 2 -> 3 -> 4 -> 5   (a degenerate tree / linked list)
```

Đây là lý do tài liệu tham chiếu trình bày một Union-Find **chưa tối ưu** trước:
nó lộ ra vấn đề mà hai tối ưu hóa sẽ khắc phục.

---

## 7. Tối ưu hóa 1: Hợp theo Kích thước (Mảng Trọng số)

Cách khắc phục đầu tiên: khi trộn hai cây, luôn treo cây **nhỏ hơn** dưới cây
**lớn hơn**. Giữ một mảng `size[]` ghi mỗi gốc sở hữu bao nhiêu nút.

```python
def union(self, p, q):
    rp, rq = self.find(p), self.find(q)
    if rp == rq:
        return False
    if self._size[rp] < self._size[rq]:
        rp, rq = rq, rp            # rp is now the larger tree
    self._parent[rq] = rp          # hang the smaller under the larger
    self._size[rp] += self._size[rq]
    self._count -= 1
    return True
```

```text
  without size:               with union by size:
  0->1->2->3->4->5            every node points to one tall root
                              (the tree stays shallow)
  height ~ V                  height ~ log V
```

Vì cây nhỏ hơn (tối đa một nửa số nút) luôn được treo dưới cây lớn hơn, độ sâu
của một nút chỉ có thể tăng nhiều nhất `log V` lần. Vậy chiều cao là `O(log V)`
— không còn suy biến thành danh sách liên kết.

---

## 8. Tối ưu hóa 2: Nén Đường đi (Path Compression)

Cách khắc phục thứ hai làm phẳng các cây hơn nữa. Trong lúc `find`, mọi nút
trên đường đi đã bước qua đều được trỏ thẳng tới gốc.

```python
def find(self, x):
    root = x
    while self._parent[root] != root:
        root = self._parent[root]
    while self._parent[x] != x:     # second pass: flatten the path
        nxt = self._parent[x]
        self._parent[x] = root
        x = nxt
    return root
```

```text
  before find(5):            after find(5):

  0 -> 1 -> 2 -> 3 -> 4 -> 5      0
                                 /|\
                                1 2 3 4 5
  (long path)                  (all now point straight at the root)
```

Lần tới bạn gọi `find` trên bất kỳ nút nào trong số đó, nó chỉ còn một bước.
Điều này khiến chi phí khấu hao về cơ bản là hằng số.

```text
  naive chain:  [1, 2, 3, 4, 5, 5]        (linked list)
  compressed:   [0, 0, 0, 0, 0, 0]        (all point at root 0)
```

---

## 9. Kết quả Kết hợp

Với cả **hợp theo kích thước** và **nén đường đi**:

```text
  amortized time per operation:  O(alpha(V))

  alpha = the inverse Ackermann function
  for any practical V, alpha(V) <= 4   -> "basically O(1)"
```

```text
  version            union      connected      space
  naive              O(V)       O(V)           O(V)
  union by size      O(log V)   O(log V)       O(V)
  + path compress    ~O(1)      ~O(1)          O(V)
```

Đó là lý do Union-Find là công cụ được chọn cho tính liên thông động: nó biến
`O(V + E)` mỗi truy vấn thành `~O(1)`.

---

## 10. Ứng dụng: Đếm Vòng Bạn bè

Một ứng dụng kinh điển: cho một ma trận kề trong đó `M[i][j] == 1` nghĩa là
người `i` và `j` là bạn bè, đếm có bao nhiêu **vòng bạn bè** (những người được
nối qua một chuỗi tình bạn).

```text
  people: A B C D
  friends: A-B are friends; C and D have no friends

  matrix:
     A B C D
  A [1 1 0 0]
  B [1 1 0 0]
  C [0 0 1 0]
  D [0 0 0 1]

  union every friendship, then count()
  -> 3 circles: {A,B}, {C}, {D}
```

```python
def friend_circles(m):
    n = len(m)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(n):
            if m[i][j] == 1:
                uf.union(i, j)
    return uf.count()
```

Kết quả `count()` chính xác là số thành phần liên thông sau mọi phép hợp — một
lần đọc `O(1)` duy nhất.

---

## 11. Tóm tắt Độ phức tạp

| Thao tác | Ngây thơ | Hợp theo kích thước | + nén đường đi |
|:---|:---:|:---:|:---:|
| `union` | `O(V)` | `O(log V)` | `O(alpha(V))` ~ `O(1)` |
| `connected` | `O(V)` | `O(log V)` | `O(alpha(V))` ~ `O(1)` |
| `count` | `O(1)` | `O(1)` | `O(1)` |
| không gian | `O(V)` | `O(V)` | `O(V)` |

---

## 12. Những Sai lầm Thường gặp

### Sai lầm 1: Quên tính bắc cầu

`connected(p, q)` phải tìm **gốc** của mỗi cây và so sánh các gốc, không phải
kiểm tra một cạnh trực tiếp. Tra cứu cạnh trực tiếp bỏ lỡ các kết nối bắc cầu.

### Sai lầm 2: Không làm phẳng trong lúc find

Không nén đường đi, các lần gọi `find` lặp lại vẫn đi bộ các chuỗi dài. Luôn
trỏ lại đường đi về gốc khi bạn đi qua.

### Sai lầm 3: Treo cây tùy tiện

Union mà không hợp theo kích thước có thể dựng các cây cao `O(V)`. Luôn gắn cây
nhỏ hơn vào gốc lớn hơn để giữ chiều cao ở `O(log V)`.

### Sai lầm 4: Nhầm gốc với chính nút đó

Hai nút liên thông chỉ khi **gốc** của chúng khớp nhau. So sánh trực tiếp
`parent[p]` và `parent[q]` là sai — chúng có thể là các nút không phải gốc với
cha trực tiếp khác nhau nhưng cùng một gốc.

### Sai lầm 5: Sai số lệch một trong đếm thành phần

Mỗi `union` thành công (một phép thực sự trộn hai gốc khác nhau) phải giảm
`count`. Không theo dõi điều này sẽ cho `count()` sai.

---

## 13. Chạy Ví dụ

Chạy:

```text
python UnionFindBasics.py
```

Đầu ra ổn định mong đợi:

```text
=== Dynamic connectivity: 10 isolated nodes ===
initial components: 10 (each node is its own)

=== Union operations ===
  union(0,1) -> components now: 9
  union(1,2) -> components now: 8
  union(5,6) -> components now: 7

=== connected() queries ===
connected(0,2): True (0-1, 1-2 transitive)
connected(0,5): False (different circles)
connected(5,6): True

=== Why transitive connectivity matters ===
  0-1, 1-2  =>  0 and 2 are connected through 1
  connected(0,2) = True

=== Friend circles (LeetCode-style) ===
adjacency matrix:
   [1, 1, 0, 0]
   [1, 1, 0, 0]
   [0, 0, 1, 0]
   [0, 0, 0, 1]
number of friend circles: 3

=== Naive vs optimized tree shape ===
naive parent chain (0..5): [1, 2, 3, 4, 5, 5] (0->1->2->...->5 list)
opt   parent chain (0..5): [0, 0, 0, 0, 0, 0] (all point at one root)
```

Chú ý sự tương phản: mảng ngây thơ là một danh sách liên kết (`[1,2,3,4,5,5]`),
còn mảng tối ưu là phẳng (`[0,0,0,0,0,0]`).

---

## 14. Bảng Tóm tắt Cuối cùng

```text
    1. Union-Find tracks connected components of an undirected graph.
    2. Each component is a tree; parent[] stores one pointer per node.
    3. find(x) walks to the root of x's tree.
    4. connected(p,q) = (find(p) == find(q)).
    5. union(p,q) points one root at the other, count() decreases.
    6. Without care, trees degrade into O(V)-tall linked lists.
    7. Union by size keeps height at O(log V).
    8. Path compression flattens trees to ~O(1) amortized.
    9. Combined: O(alpha(V)) ~ constant per operation.
    10. Ideal for dynamic connectivity, Kruskal MST, friend circles.
```

**Bước tiếp theo:** Giờ bạn đã có bộ công cụ đồ thị đầy đủ — lưu trữ, duyệt,
đường Euler, đường đi ngắn nhất, MST và tính liên thông. Hãy thử áp dụng chúng
vào các bài toán thực để khóa chặt trực giác.
