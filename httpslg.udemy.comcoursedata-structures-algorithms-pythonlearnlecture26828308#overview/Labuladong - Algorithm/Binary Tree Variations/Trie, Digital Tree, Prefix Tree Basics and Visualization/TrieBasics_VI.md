# Trie, Digital Tree, Prefix Tree Basics and Visualization (tiếng Việt)

## 1. Mục tiêu

Trie — còn gọi là digital tree, prefix tree, hay dictionary tree — là một
cây N-ary trong đó mỗi cạnh được gắn nhãn đúng một ký tự và mỗi nút lưu
một giá trị tùy chọn. Một nút có giá trị khác None đánh dấu điểm kết thúc
của một khóa đã lưu, và đường đi từ gốc xuống nút đó viết ra chính khóa.
Việc tra cứu, chèn, và xóa một khóa có độ dài L đều đi qua đúng L cạnh,
nên mỗi thao tác là O(L) bất kể cây đang chứa bao nhiêu khóa.

Trie ra đời vì các cấu trúc kinh điển thất bại với những chuỗi dùng chung
tiền tố. HashMap lưu trọn từng khóa: với "apple", "app" và "appl", tiền tố
"app" được giữ ba lần, lãng phí bộ nhớ. Và cả HashMap lẫn TreeMap đều không
trả lời được các câu hỏi tiền tố như "liệt kê mọi khóa bắt đầu bằng th"
hay mẫu wildcard như "t.e" — cả hai đều phải quét từng khóa một. Trie giải
quyết đồng thời cả hai vấn đề: tiền tố dùng chung nằm trong các nút dùng
chung, và chính hình dạng của cây có thể được bước đi để liệt kê hoặc khớp
khóa theo tiền tố.

Nguồn tham khảo:

- [Trie, Digital Tree, Prefix Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/trie-map-basic/)

Cài đặt trong `TrieBasics.py` cung cấp:

- Lớp `TrieNode` chứa một dict `children` và một `val` tùy chọn.
- Một `TrieMap` tổng quát với `put`, `get`, `remove`, `contains_key`,
  `keys`, `shortest_prefix_of`, `longest_prefix_of`, `has_key_with_prefix`,
  `keys_with_prefix`, `has_key_with_pattern` và `keys_with_pattern`.
- Một `TrieSet` bọc quanh một `TrieMap`, phơi bày các API tiền tố và
  wildcard tương tự như một tập hợp.
- Một helper `node_count` cho việc so sánh bộ nhớ và một trình vẽ ASCII
  theo từng độ sâu dùng trong demo.

Ba khóa "apple", "app" và "appl" dùng chung đường đi `a -> p -> p`, và các
nút tại "app", "appl", "apple" mỗi nút mang một dấu đặc biệt báo "một khóa
kết thúc tại đây":

```text
   (root)
     |
     a
     |
     p
     |
     p@           end of key "app"
     |
     l@           end of key "appl"
     |
     e@           end of key "apple"

   @ = this node's val is not None (a stored key ends here)
   every edge is one character, so the path to any node spells a word
```

## 2. Ứng dụng: tiết kiệm bộ nhớ

HashMap lưu trọn chuỗi khóa tại mỗi mục. Ba khóa "apple", "app" và "appl"
mang tổng cộng 12 ký tự, và tiền tố "app" được viết ba lần:

```text
   HashMap with three keys:

   "apple" -> a p p l e         5 characters
   "app"   -> a p p             3 characters
   "appl"  -> a p p l           4 characters
                                 ---------
                                 12 characters stored, "app" repeated 3x

   Trie with the same three keys:

   (root) --a--> --p--> --p--> --l--> --e-->    end of "apple"
                              |      |
                        end of "app"  end of "appl"

   only 5 character nodes exist: a, p, p, l, e
   the prefix "app" is written once and shared by all three keys
```

Một cây chứa hàng nghìn số điện thoại, tên miền, hay từ tiếng Anh giữ được
sự dùng chung này cho mọi tiền tố chung, nên tổng bộ nhớ tỷ lệ với tổng độ
dài các khóa trừ đi phần dùng chung — thường là một khoản tiết kiệm lớn.
Trong demo, `node_count()` trả về 6 cho ba khóa này (gốc cộng `a p p l e`):
5 nút ký tự trong khi HashMap cần 12 ký tự.

## 3. Ứng dụng: thao tác tiền tố

Bốn API tiền tố là lý do trie mạnh hơn một tập chuỗi đơn thuần. Tất cả đều
hoạt động bằng cách đi xuống một nút rồi khảo sát cây con bên dưới nó. Giả
sử trie đang chứa "that", "the", "them" và "apple".

`shortest_prefix_of(s)` trả về khóa đã lưu ngắn nhất mà là tiền tố của `s`.
Đi `s` từng ký tự một và dừng ở nút đầu tiên có giá trị khác None:

```text
   shortest_prefix_of("themxyz")

   walk s = t h e m x y z
             | | | |
   (root) --t--> --h--> --e--> --m--> --x--> (no child, stop)

   "the"  ends at the 3rd node  -> value found, return "the"
   "them" ends at the 4th node  -> not reached, we already stopped
   result: "the"
```

`longest_prefix_of(s)` trả về tiền tố dài nhất như vậy. Cùng một đường đi
nhưng giữ một ứng viên chạy và cập nhật nó mỗi khi đi qua một nút có giá
trị:

```text
   longest_prefix_of("themxyz")

   (root) --t--> --h--> --e--> --m--> --x--> (no child, stop)
                        |        |
                      "the"    "them"
                      found    found, longer -> overwrite

   result: "them"
```

`has_key_with_prefix(prefix)` chỉ hỏi nút đi tới được bởi `prefix` có tồn
tại hay không:

```text
   has_key_with_prefix("tha")        has_key_with_prefix("thz")

   (root) --t--> --h--> --a-->      (root) --t--> --h--> --z--> ???
                          |                                  |
                     "that" exists               no "z" child
                     result: True                result: False
```

`keys_with_prefix(prefix)` gom mọi khóa trong cây con đó — đúng thứ một
danh sách gợi ý tự hoàn thành (autocomplete) hiển thị trong lúc người dùng
gõ:

```text
   autocomplete: the user has typed "th"

        keyboard:  t h
                     |
                     v
   (root) --t--> --h--> subtree
                         |-- "that"     (suggestion 1)
                         |-- "the"      (suggestion 2)
                         |-- "them"     (suggestion 3)

   answer: keys_with_prefix("th") -> ["that", "the", "them"]
   cost: O(L) to reach the "th" node plus O(K) to collect the K matches
```

## 4. Ứng dụng: hỗ trợ wildcard

Một chuỗi mẫu có thể chứa '.', khớp với bất kỳ ký tự đơn nào. Việc tìm
kiếm vẫn là cùng một đường đi trong trie, nhưng tại một dấu '.' đường đi
rẽ nhánh sang mọi con thay vì theo đúng một ký tự cố định:

```text
   pattern "t.e"   (t, any, e)

   (root) --t--> --h--> --e-->    "the"  matched, value found -> True
                     \--a--> ...  dead end, no "e" child below

   pattern "t.x"   (t, any, x)

   (root) --t--> --h--> --x--> ???     no "x" child under "h"
                   \--a--> --x--> ???  no "x" child under "a"
   result: False
```

`keys_with_pattern` gom mọi khóa khớp theo thứ tự từ điển:

```text
   pattern "t..t"   (t, any, any, t)

   (root) --t--> --h--> --a--> --t-->    "that"  matched
                   \--e--> --m--> ???    "them" fails at the last char

   pattern ".pp."   (any, p, p, any)

   (root) --a--> --p--> --p--> --l-->    "appl"  matched
   result: ["appl"]
```

Một tìm kiếm wildcard chỉ tốn chi phí bằng số nút nó thực sự ghé: dấu '.'
tại một nút rộng sẽ rẽ nhánh nhiều, nhưng những nhánh không khớp một ký tự
cố định sẽ chết ngay lập tức.

## 5. Ứng dụng: duyệt khóa theo thứ tự

Các con của mỗi nút sống trong một dict khóa theo ký tự. Nếu các con được
duyệt theo thứ tự ký tự đã sắp xếp, các khóa được phát ra theo thứ tự từ
điển — trie cư xử như một map đã sắp xếp, chứ không như HashMap với thứ tự
duyệt tùy ý:

```text
   trie holding "app", "appl", "apple", "that", "the", "them"

   (root)
     |-- a -- p -- p -- l -- e         end of "apple"
                        |    |
                     "app"  "appl"
     |-- t -- h -- a -- t              end of "that"
                   |
                   e -- m
             end of "the"  end of "them"

   visit children in sorted order (a before t):

   "app" < "appl" < "apple" < "that" < "the" < "them"
```

Một đường đi đã sắp xếp giúp các báo cáo có thứ tự và autocomplete trở nên
dễ dàng: HashMap kinh điển cần cả một lượt sắp xếp toàn bộ khóa, còn trie
phát ra chúng vốn đã sắp xếp.

## 6. Cấu trúc cơ bản

Một nút trie chỉ là một dictionary các con cộng một giá trị tùy chọn:

```python
class TrieNode(Generic[V]):
    def __init__(self) -> None:
        self.children: Dict[str, TrieNode[V]] = {}
        self.val: Optional[V] = None
```

Nhãn cạnh chính là khóa của dict, và `val` là None trừ khi nút này là điểm
kết thúc của một khóa đã lưu:

```text
   TrieNode at the path "app"            TrieNode at the path "appl"
   +---------------------------------+   +---------------------------------+
   | children: Dict[str, TrieNode]   |   | children: Dict[str, TrieNode]   |
   |   "l" -> TrieNode("appl")       |   |   "e" -> TrieNode("apple")      |
   | val: 2  <- not None: key "app"  |   | val: 3  <- not None: key "appl" |
   +---------------------------------+   +---------------------------------+
```

`TrieMap` giữ một nút gốc cộng một bộ đếm kích thước. Các con của gốc là
những ký tự đầu tiên của mọi khóa đã lưu, nên hệ số rẽ nhánh của một nút
nhiều nhất bằng kích thước bảng chữ cái:

```text
   TrieMap
   +-------------------------------------+
   | root: TrieNode                      |
   |   children: { "a": node_a,          |   first letters of keys
   |                "t": node_t }        |
   |   val: None                         |   root never ends a key
   | size: 6                             |   number of stored keys
   +-------------------------------------+
```

`TrieSet` là một lớp bọc mỏng lưu một sentinel khác None làm giá trị của
mỗi khóa — None vốn đã mang nghĩa "không phải điểm kết thúc của khóa" bên
trong một nút:

```text
   TrieMap (values of any type)          TrieSet (values are the sentinel)

   +----------------------------+        +----------------------------+
   | "app"  -> 2                |        | "cat" -> True (sentinel)   |
   | "the"  -> 2                |        | "car" -> True (sentinel)   |
   | "them" -> 3                |        | "dog" -> True (sentinel)   |
   +----------------------------+        +----------------------------+
   put / get / remove / keys             add / remove / contains
   prefix + wildcard APIs                prefix + wildcard APIs
```

## 7. API TrieMap

Mọi thao tác đều mất O(L) thời gian, trong đó L là độ dài của khóa, tiền
tố, hay mẫu liên quan, cộng thời gian gom kết quả:

```python
class TrieMap(Generic[V]):
    def put(self, key: str, value: V) -> Optional[V]       # O(L), returns previous value
    def get(self, key: str) -> Optional[V]                 # O(L), None if absent
    def remove(self, key: str) -> Optional[V]              # O(L), prunes dead nodes
    def contains_key(self, key: str) -> bool               # O(L)
    def keys(self) -> List[str]                            # O(N), lexicographic
    def is_empty(self) -> bool                             # O(1)
    def node_count(self) -> int                            # O(N), memory demos
    def shortest_prefix_of(self, s: str) -> Optional[str]  # O(L)
    def longest_prefix_of(self, s: str) -> Optional[str]   # O(L)
    def has_key_with_prefix(self, prefix: str) -> bool     # O(L)
    def keys_with_prefix(self, prefix: str) -> List[str]   # O(L + K)
    def has_key_with_pattern(self, pattern: str) -> bool   # O(visited nodes)
    def keys_with_pattern(self, pattern: str) -> List[str] # O(visited nodes + K)
```

`keys_with_prefix` và `keys_with_pattern` trả thêm `K` cho số khóa chúng
gom; cặp wildcard còn trả chi phí cho mọi nút đường đi ghé qua, bị chặn
trên bởi kích thước cây con.

Ba hợp đồng mà demo dựa vào, nêu rõ ràng:

```text
   keys()                 -> sorted, shorter keys first ("app" < "appl")
   keys_with_prefix(p)    -> sorted, only keys starting with p
   remove(k)              -> prunes nodes with no val and no children
```

## 8. Thuật toán chèn và xóa

Chèn đi từng ký tự của khóa, tạo bất kỳ nút nào còn thiếu, và cuối cùng đặt
giá trị lên nút cuối:

```text
   put("apple", 1), starting from an empty trie

   step 1   (root) --a-->                        create "a"
   step 2   (root) --a--> --p-->                 create "p"
   step 3   (root) --a--> --p--> --p-->          create "p"
   step 4   (root) --a--> --p--> --p--> --l-->   create "l"
   step 5   (root) --a--> --p--> --p--> --l--> --e-->   create "e"
   step 6   val of the final node := 1           "apple" is now a key

   inserting "appl" next reuses the nodes a, p, p and l;
   only the value of node "l" needs to be set
```

Xóa hoạt động từ dưới lên: xóa giá trị của nút cuối, rồi tỉa những nút trở
nên vô dụng. Một nút chỉ bị gỡ khi nó không còn giá trị và không còn con
nào:

```text
   remove("apple") from a trie holding "appl" (val 3) and "apple" (val 1)

   before:
   (root) --a--> --p--> --p--> --l--> --e-->   val = 1  ("apple")
                                |
                              val = 3          ("appl")

   step 1   clear val at node "e", remember 1 (the returned value)
   step 2   node "e" has no children and no val  -> prune "e"
   step 3   node "l" still holds val = 3         -> keep "l"
   step 4   nodes "a", "p", "p" lead to a live key -> keep them

   after:
   (root) --a--> --p--> --p--> --l-->   val = 3  ("appl")

   "appl" survived because its own node still carries a value;
   the shared prefix nodes were kept because they lead to it
```

## 9. Độ phức tạp

Gọi L là độ dài của khóa hay tiền tố, K là số khóa một thao tác gom về, và
N là tổng số nút của trie.

| Thao tác | Thời gian | Ghi chú |
|:---|:---:|:---|
| put / get / contains_key | `O(L)` | một nút mỗi ký tự |
| remove | `O(L)` | cộng phần tỉa trên đường quay lui |
| shortest / longest_prefix_of | `O(L)` | một đường đi đơn, không rẽ nhánh |
| has_key_with_prefix | `O(L)` | chỉ cần chạm tới nút |
| keys_with_prefix | `O(L + K)` | đi bộ cộng gom cây con |
| has_key_with_pattern | `O(visited)` | wildcard rẽ nhánh tại '.', bị chặn bởi cây con |
| keys_with_pattern | `O(visited + K)` | cùng đường đi, gom các khớp |
| keys | `O(N)` | duyệt toàn bộ, kết quả vốn đã sắp xếp |
| Không gian | `O(N)` | một nút mỗi tiền tố phân biệt |

`N` bám sát số ký tự thực sự được lưu vì tiền tố dùng chung dùng chung nút:
ba khóa mà các bản sao trong HashMap tổng cộng 12 ký tự chỉ cần 5 nút ký tự
cộng gốc. Cái giá phải trả là một đối tượng dictionary mỗi nút, khiến trie
nặng hơn một danh sách phẳng với những tập khóa nhỏ.

## 10. Trình diễn demo

Chạy:

```text
python TrieBasics.py
```

Demo dựng một `TrieMap` và chạy năm phần xác định:

```text
   Part A   put "apple", "app", "appl"
            -> 3 keys, node_count = 6 (root + a p p l e)
            -> HashMap would store 12 characters, trie stores 5
   Part B   put "that", "the", "them", "apple"
            -> shortest_prefix_of("themxyz") = "the"
            -> longest_prefix_of("themxyz")  = "them"
            -> has_key_with_prefix("tha") = True, ("thz") = False
            -> keys_with_prefix("th") = ["that", "the", "them"]
   Part C   wildcard checks on the same trie
            -> has_key_with_pattern("t.e") = True, ("t.x") = False
            -> keys_with_pattern("t..t") = ["that"]
            -> keys_with_pattern(".pp.") = ["appl"]
   Part D   remove("app"), then remove("apple")
            -> "appl" survives, keys stay sorted, missing key returns None
   Part E   a TrieSet with "cat", "car", "dog"
            -> contains("cat") = True, contains("cow") = False
            -> keys() = ["car", "cat", "dog"]
            -> keys_with_prefix("ca") = ["car", "cat"]
```

Dòng in cuối cùng vẽ trie nhỏ thuộc họ "apple" mỗi độ sâu một dòng, với dấu
`#` trên những nút kết thúc một khóa:

```text
   depth 0: (root)
   depth 1: a
   depth 2: p
   depth 3: p#
   depth 4: l#
   depth 5: e#
   lexicographic keys: ['app', 'appl', 'apple']
```

Mọi kỳ vọng đều được ép buộc bằng `assert`, nên một lần chạy qua cũng chính
là một bài kiểm tra qua.

## 11. Hạn chế và tóm tắt

Điều trie không làm được, và những điểm cần ghi nhớ:

- Khóa phải là chuỗi. Một `TrieMap` không thể trực tiếp lưu khóa nguyên như
  TreeMap; số phải được tuần tự hóa thành chuỗi trước.
- Hỗ trợ wildcard giới hạn ở ký tự đơn '.'. Không có neo (anchor), lặp
  (repetition), hay hoặc (alternation) — một engine regex đầy đủ vượt xa
  tầm một trie.
- Mỗi nút sở hữu một dict. Chi phí trên mỗi nút là thật, nên trie có thể
  lớn hơn một mảng đóng gói khi khóa ngắn và không liên quan nhau.
- Các phương thức tiền tố chỉ trả lời câu hỏi tiền tố. Truy vấn hậu tố cần
  một trie đảo ngược; truy vấn chuỗi con cần suffix tree hoặc tương tự.

Tóm tắt toàn cảnh:

```text
   problem                      HashMap / TreeMap          Trie
   store "app"+"appl"+"apple"   12 characters              5 nodes, shared "app"
   all keys starting with "th"  scan every key             O(L + K) subtree walk
   pattern "t.e"                regex over all keys        trie walk with '.'
   keys in sorted order         sort all keys              already sorted walk
```

Trie là hình dạng tự nhiên đằng sau autocomplete, trình kiểm tra chính tả,
bảng định tuyến IP, và tìm kiếm gõ nhanh trong các từ điển lớn — bất cứ khi
nào khóa là chuỗi, công việc xoay quanh tiền tố, và tiền tố dùng chung
không nên tốn chi phí.

Nguồn:

- [Trie, Digital Tree, Prefix Tree Basics and Visualization](https://labuladong.online/en/algo/data-structure-basic/trie-map-basic/)
- [208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)
- [211. Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)