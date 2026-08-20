
---

# HashMap với Separate Chaining

## 1. Ý tưởng cốt lõi

**Hash map** lưu các key duy nhất cùng value tương ứng. Hàm băm biến một key
thành chỉ số của mảng:

```text
    key                 ham bam                    chi so bucket

    "alpha"       --->  hash("alpha")       --->       1
    "beta"        --->  hash("beta")        --->       1   dung do
    "gamma"       --->  hash("gamma")       --->       3
```

Mảng cho phép truy cập `O(1)` khi đã biết chỉ số. Hash map dùng key để tính chỉ
số đó, rồi lưu hoặc tìm cặp key/value tại vị trí tương ứng. Các thao tác chính
có expected `O(1)` khi hàm băm phân bố key tốt.

Implementation trong `SeparateChainingHashMap.py` dùng **separate chaining**:
mỗi vị trí mảng lưu node đầu của một linked list. Mọi cặp có key băm đến vị trí
đó được lưu trong cùng một chain.

Tài liệu tham khảo:

- [Core Principles of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Implement HashMap with Separate Chaining](https://labuladong.online/en/algo/data-structure-basic/hashtable-chaining/)

---

## 2. Vì sao collision không thể tránh?

Tập key có thể có thường lớn hơn nhiều so với số vị trí của mảng. Vì vậy, hai
key khác nhau có thể tạo cùng một chỉ số:

```text
    rat nhieu key co the co
             |
             v
        hash(key)
             |
             v
    chi co mot so bucket co dinh

    key A ---> bucket 1
    key B ---> bucket 1
```

Đây là **hash collision**. Collision không nhất thiết là lỗi. Cấu trúc dữ liệu
phải giữ được cả hai cặp và vẫn phân biệt chúng bằng cách so sánh key.

Separate chaining giải quyết collision bằng cách mở rộng bucket theo chiều dọc:

```text
    bucket 1
       |
       v
    +---------+      +---------+
    | key A   | ---> | key B   | ---> None
    | value A |      | value B |
    +---------+      +---------+
```

Linked list này là chain. Search chọn bucket trước, rồi chỉ duyệt chain đó thay
vì duyệt toàn bộ table.

---

## 3. Cấu trúc Entry và Bucket

Mỗi `_Entry` lưu ba thông tin:

```text
    +-------------------+
    | key               |
    | value             |
    | next entry ------ |----> entry tiếp theo hoặc None
    +-------------------+
```

Table là một list chứa các bucket head:

```text
    index       bucket head

      0         None
      1         [beta] ---> [alpha] ---> None
      2         None
      3         [gamma] ---> None
      4         None
```

`SeparateChainingHashMap` chèn entry mới vào đầu chain. Sau khi đã biết bucket,
việc này có thời gian hằng số. Vì thế thứ tự trong chain và thứ tự duyệt toàn
bộ map là chi tiết implementation, không phải cam kết theo thứ tự chèn.

---

## 4. Băm một key

Implementation dùng `hash(key)` của Python, rồi đưa kết quả vào capacity hiện tại
bằng phép modulo:

```python
def _bucket_index(self, key, capacity=None):
    bucket_count = self._capacity if capacity is None else capacity
    return hash(key) % bucket_count
```

Kết quả modulo của Python là không âm khi số chia dương, nên hash âm vẫn tạo ra
chỉ số hợp lệ.

Key phải hashable và ổn định trong thời gian được lưu:

```text
    cung key + cung capacity cua table -> cung bucket index
```

Mutable key rất nguy hiểm. Nếu key thay đổi dữ liệu dùng bởi `__hash__` hoặc
`__eq__`, cặp key/value có thể vẫn còn trong chain nhưng không thể tìm thấy bằng
key đã thay đổi. Hãy dùng key immutable như string, number, hoặc tuple chỉ chứa
giá trị immutable.

---

## 5. `put`: Chèn hoặc cập nhật

`put(key, value)` thực hiện các bước:

```text
    1. Tính bucket index.
    2. Duyệt chain của bucket đó.
    3. Nếu key đã tồn tại, thay value.
    4. Nếu chưa có, tạo entry ở đầu chain.
    5. Tăng size và resize nếu load factor quá cao.
```

Cập nhật không được tạo key trùng:

```text
    truoc put("A", 99):

    bucket 2: ["A", 10] ---> ["B", 20] ---> None

    sau put("A", 99):

    bucket 2: ["A", 99] ---> ["B", 20] ---> None
```

Method trả về value cũ nếu key đã tồn tại, ngược lại trả về `None`. Quy ước này
hữu ích khi quan sát update, còn `__setitem__` cung cấp cú pháp map quen thuộc:

```python
hash_map["language"] = "Python"
hash_map["language"] = "Python 3"
```

---

## 6. `get`: Tìm trong chain

`get(key, default)` tính một bucket rồi so sánh key dọc theo chain:

```text
    tim key B:

    hash(B) -> bucket 1
                     |
                     v
    [key A] -> [key B] -> [key C] -> None
                ^
                | khop equality -> tra ve value B
```

Nếu bucket rỗng hoặc key không có trong chain, default được trả về. Default là
`None` nếu không truyền:

```python
value = hash_map.get("missing")
value = hash_map.get("missing", 0)
```

`hash_map[key]` cũng search như vậy nhưng raise `KeyError` khi key không tồn tại,
giống dictionary dựng sẵn của Python.

---

## 7. `remove`: Bỏ một entry khỏi chain

Để xóa entry khỏi singly linked chain, cần giữ entry hiện tại và predecessor:

```text
    truoc:

    previous ------> target ------> next

    sau:

    previous ---------------------> next
```

Nếu target là head, bucket head chuyển thành `target.next`. Nếu không,
`next` của predecessor bỏ qua target.

```python
removed_value = hash_map.remove("language")
del hash_map["other-key"]
```

`remove` raise `KeyError` nếu key không tồn tại. Điều này giúp phát hiện việc
xóa nhầm key thay vì âm thầm không làm gì.

---

## 8. Load factor và resize

Load factor đo mức độ đầy của các bucket:

```text
    load factor = so entry / so bucket
```

Với separate chaining, load factor có thể lớn hơn `1` vì chain có thể dài không
giới hạn. Tuy nhiên chain dài làm search chậm, nên implementation resize khi
load factor vượt `0.75` theo mặc định.

```text
    capacity = 4, size = 3
    load factor = 3 / 4 = 0.75

    chen them mot item:
    size = 4, load factor = 1.0
    mo rong table thanh capacity 8
```

Resize không chỉ là copy vị trí bucket cũ. Index phụ thuộc vào capacity, nên mọi
entry phải được băm lại:

```text
    old index = hash(key) % old_capacity
    new index = hash(key) % new_capacity
```

Method `_resize` chuyển mọi entry vào bucket array mới. Logical size của map
không thay đổi trong quá trình này.

---

## 9. Public Interface

Class cung cấp cả method mô tả rõ ràng và cú pháp mapping quen thuộc:

```python
table = SeparateChainingHashMap[str, int]()

table.put("red", 1)
table["blue"] = 2

table.get("red")             # 1
table.get("missing", -1)    # -1
table["blue"]                # 2
"red" in table               # True
table.contains_key("blue")   # True
table.remove("red")
len(table)                    # 1
list(table.items())
table.keys()
table.values()
table.bucket_snapshot()       # dùng để xem các chain
```

Map nhận mọi key hashable và không yêu cầu key phải là string. Value có thể lặp
lại và có thể thuộc bất kỳ kiểu nào.

---

## 10. Độ phức tạp

Gọi `n` là số entry và `k` là độ dài chain được chọn.

| Thao tác | Trung bình | Xấu nhất | Không gian phụ | Lý do |
|:---|:---:|:---:|:---:|:---|
| `put` key mới | `O(1)` | `O(n)` | `O(1)` | Băm, duyệt chain, có thể resize |
| `put` key cũ | `O(1)` | `O(n)` | `O(1)` | Tìm key trong chain |
| `get` | `O(1)` | `O(n)` | `O(1)` | Chỉ duyệt tối đa một chain |
| `remove` | `O(1)` | `O(n)` | `O(1)` | Tìm rồi unlink một entry |
| `keys` / `values` | `O(n)` | `O(n)` | `O(n)` cho result | Thăm mọi entry |
| Resize | `O(n)` | `O(n)` | `O(n)` | Băm lại mọi entry |
| Map đang lưu | - | - | `O(n + capacity)` | Entry cộng bucket head |

Expected `O(1)` giả định hàm băm phân bố tốt và load factor được kiểm soát. Nếu
mọi key cùng băm vào một bucket, cấu trúc trở thành một linked list và các thao
tác giảm xuống `O(n)`.

---

## 11. Invariant quan trọng

Implementation đúng khi các mệnh đề sau luôn đúng:

```text
    1. Mọi entry reachable từ đúng một bucket head.
    2. Mỗi chain chứa key duy nhất.
    3. Bucket của entry là hash(entry.key) % capacity.
    4. Size counter bằng số entry đang lưu.
    5. Update key chỉ đổi value, không đổi số entry.
    6. Xóa chain head phải cập nhật bucket head.
    7. Resize phải băm lại mọi entry theo capacity mới.
```

Đây là checklist quan trọng hơn việc chọn cú pháp linked node nào. Hãy dùng nó
khi debug lỗi collision hoặc resize.

---

## 12. Chạy ví dụ

Chạy file từ thư mục này:

```text
python SeparateChainingHashMap.py
```

Demo dùng custom key có cùng giá trị `__hash__`, nên collision luôn xảy ra mà
không phụ thuộc random seed hash string của Python. Demo minh họa:

```text
    chen alpha va beta vao mot chain
    chen gamma vao bucket khac
    update alpha ma khong tao key trung
    xoa beta khoi chain
```

Bucket snapshot sau resize không nhất thiết giữ thứ tự toàn cục ổn định. Không
nên dùng thứ tự duyệt hash table như cam kết sorted order hoặc insertion order.

---

## 13. So sánh chaining với linear probing

| Đặc điểm | Separate chaining | Linear probing |
|:---|:---|:---|
| Hướng xử lý collision | Mở rộng bucket thành chain | Tìm các ô tiếp theo trong array |
| Lưu trữ | Entry cộng linked pointer | Một entry trên mỗi array slot |
| Load factor | Có thể lớn hơn `1` | Phải nhỏ hơn `1` |
| Xóa | Unlink một entry | Cần tombstone hoặc sửa cluster |
| Locality chính | Duyệt chain bằng pointer | Probe trên array |

Cả hai đều bắt đầu bằng cùng một bước: băm key để lấy index ban đầu. Khác biệt
là cách chúng giữ mọi entry khi index đó đã bị chiếm.

---

## 14. Checklist cuối cùng

```text
    1. Key là duy nhất; value có thể lặp.
    2. Key khác nhau có thể map vào một bucket.
    3. Chain lưu mọi cặp collision tại bucket đó.
    4. Search phải so sánh key, không chỉ so sánh hash index.
    5. Update key cũ không được tăng size.
    6. Resize phải rehash vì capacity làm thay đổi index.
    7. Key immutable và hashable là lựa chọn an toàn.
    8. Thao tác trung bình O(1); xấu nhất O(n).
```

**Bước tiếp theo:** Tạo hai key có cùng giá trị `__hash__`, rồi trace `put`,
`get`, update và `remove` của chúng qua cùng một chain.
