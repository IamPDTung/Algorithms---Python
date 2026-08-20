
---

# HashMap với Linear Probing

## 1. Ý tưởng cốt lõi

**Linear probing** là chiến lược open addressing để xử lý hash collision. Table
tự lưu trực tiếp các entry. Khi home slot đã bị chiếm, map kiểm tra slot kế
tiếp, rồi slot sau nữa, cho đến khi tìm thấy key hoặc gặp ô trống.

```text
    home index cua key A = 3
    home index cua key B = 3

    index:      0       1       2       3       4       5
             +-------+-------+-------+-------+-------+-------+
    values:  |       |       |       |   A   |   B   |       |
             +-------+-------+-------+-------+-------+-------+
                                     home    probe + 1
```

`LinearProbingHashMap.py` chứa cả hai chiến lược xóa được mô tả trong tài liệu
tham khảo:

- `LinearProbingHashMap`: đánh dấu slot đã xóa bằng tombstone.
- `RehashingLinearProbingHashMap`: xóa slot rồi sửa cluster phía sau.

Cả hai class có cùng interface map, nên có thể so sánh trực tiếp cách xóa.

Tài liệu tham khảo:

- [Core Principles of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Key Points to Implement Linear Probing](https://labuladong.online/en/algo/data-structure-basic/linear-probing-key-point/)
- [Two Implementations of Linear Probing](https://labuladong.online/en/algo/data-structure-basic/linear-probing-code/)

---

## 2. Home index và probe sequence

Vị trí đầu tiên được tính từ key:

```python
home = hash(key) % capacity
```

Nếu slot đó không dùng được, linear probing kiểm tra các vị trí liên tiếp:

```text
    probe 0: home
    probe 1: (home + 1) % capacity
    probe 2: (home + 2) % capacity
    probe 3: (home + 3) % capacity
    ...
```

Modulo là bắt buộc. Nó biến array thành vòng tròn thay vì dừng ở index cuối:

```text
    capacity = 7, home = 5

    5 -> 6 -> 0 -> 1 -> 2 -> 3 -> 4
```

Nếu thiếu modulo, key có probe sequence đi đến cuối có thể thất bại dù đầu
array vẫn còn slot trống.

---

## 3. Collision cluster

Các key chiếm những slot liên tiếp tạo thành một **cluster**:

```text
    index:      0       1       2       3       4       5       6
             +-------+-------+-------+-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |       |       |       |
             +-------+-------+-------+-------+-------+-------+-------+
                         <----------- cluster ----------->
```

Nếu `B` và `C` đều bắt đầu từ index `1`, vị trí lưu của chúng không làm thay đổi
home index. Search `C` phải bắt đầu tại `1`, đi qua `A`, `B`, rồi tiếp tục đến
`C` hoặc một slot chứng minh `C` không tồn tại.

Đây là lý do linear probing có locality tốt: entry nằm trong cùng một array.
Nhưng đây cũng là lý do xóa phức tạp: slot trống thông thường có thể là tín
hiệu để search dừng lại.

---

## 4. `put`: Tìm hoặc cập nhật slot

Insert thực hiện:

```text
    1. Tính home index của key.
    2. Probe về phía trước và wrap quanh array.
    3. Nếu tìm thấy key, thay value.
    4. Nếu không, chèn vào slot dùng được đầu tiên.
    5. Resize trước khi table quá đầy.
```

Update phải giữ một entry cho mỗi key:

```text
    truoc put("A", 99):

    index:      0       1       2       3
             +-------+-------+-------+-------+
             |       | "A":10|       |       |
             +-------+-------+-------+-------+

    sau put("A", 99):

             |       | "A":99|       |       |
```

Method `put` trả về value cũ nếu key đã tồn tại và `None` nếu key mới. Cú pháp
quen thuộc cũng được hỗ trợ:

```python
table["A"] = 10
table["A"] = 99
```

---

## 5. Search phải đi theo probe sequence

Search bắt đầu tại đúng home index dùng khi insert:

```text
    tim C, home = 1

    index:      0       1       2       3       4
             +-------+-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |       |
             +-------+-------+-------+-------+-------+
                         ^       ^       ^
                         |       |       tim thay C
                       probe   probe
```

Quy tắc search:

```text
    slot có key khác       -> tiếp tục
    tombstone              -> tiếp tục
    slot trống             -> key không tồn tại
    key khớp               -> trả về value
```

Quy tắc dừng ở slot trống chỉ đúng khi thao tác xóa bảo toàn probe invariant.
Đó là lý do linear-probing map không thể chỉ gán mọi slot bị xóa thành `None`.

---

## 6. Vì sao xóa đơn giản bằng `None` làm hỏng search?

Xét ba key collision:

```text
    truoc khi xoa B:

    index:      0       1       2       3
             +-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |
             +-------+-------+-------+-------+

    sau khi dat slot cua B thanh None:

    index:      0       1       2       3
             +-------+-------+-------+-------+
    values:  |       |   A   | None  |   C   |
             +-------+-------+-------+-------+
```

Search `C` bắt đầu tại index `1`, thấy `A`, rồi thấy `None` tại index `2` và kết
luận sai rằng `C` chưa từng được insert. Slot trống trở thành một lỗ trong
cluster.

Hai cách sửa chuẩn là:

```text
    Cach 1: di chuyen/reinsert entry phia sau lo.
    Cach 2: de lai mot deleted marker dac biet trong lo.
```

---

## 7. Cách 1: Rehash cluster phía sau

`RehashingLinearProbingHashMap` dùng cách thứ nhất. Sau khi xóa `B`, nó tạm thời
xóa rồi insert lại các entry phía sau lỗ cho đến khi cluster kết thúc:

```text
    truoc:
    index:      0       1       2       3       4
             +-------+-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |   D   |
             +-------+-------+-------+-------+-------+

    xoa B, sau do sua C va D:

    index:      0       1       2       3       4
             +-------+-------+-------+-------+-------+
    values:  |       |   A   |   C   |   D   |       |
             +-------+-------+-------+-------+-------+
```

Thuật toán:

```text
    1. Đặt slot bị xóa thành None.
    2. Di chuyển đến slot tròn kế tiếp.
    3. Trong khi slot đang có entry:
       a. Lưu entry.
       b. Xóa vị trí cũ.
       c. Insert lại bằng hash ban đầu.
       d. Di chuyển đến slot tiếp theo.
    4. Dừng ở slot trống đầu tiên.
```

Reinsert có thể đưa entry gần home index hơn. Search khi đó có thể dừng tại slot
trống thông thường mà không cần marker.

Chi phí một lần xóa là expected `O(1)` khi cluster ngắn, nhưng có thể là `O(n)`
khi phải xây lại cluster lớn.

---

## 8. Cách 2: Tombstone marker

`LinearProbingHashMap` dùng object nội bộ `_DELETED`. Slot bị xóa không phải slot
trống thông thường và cũng không phải live entry:

```text
    truoc:

    index:      0       1       2       3
             +-------+-------+-------+-------+
    values:  |       |   A   |   B   |   C   |
             +-------+-------+-------+-------+

    sau remove(B):

    values:  |       |   A   | DELETED |  C   |
             +-------+-------+-------+-------+
```

Search bỏ qua tombstone và tới được `C`. Insert ghi nhớ tombstone đầu tiên gặp
nhưng vẫn tiếp tục probe cho đến khi tìm thấy key hoặc gặp slot trống thật. Điều
này ngăn tạo key trùng ở phía sau cùng probe sequence.

```text
    insert D:

    slot co the tai su dung dau tien = tombstone
    tiep tuc search de kiem tra D chua ton tai
    luu D vao slot tombstone
```

Tombstone làm xóa từng phần tử đơn giản, nhưng quá nhiều marker làm probe dài
hơn. Implementation định kỳ rebuild table ở cùng capacity khi tombstone nhiều
hơn live entry và chiếm phần lớn table.

---

## 9. Circular probing bắt buộc cho mọi thao tác

Table là vòng tròn về mặt logic cho `put`, `get` và `remove`:

```text
    physical array:  [0] [1] [2] [3] [4]
                              ^       |
                              |       v
                              +-------+

    probe order tu 3: 3 -> 4 -> 0 -> 1 -> 2
```

Implementation giới hạn mỗi lần search tối đa `capacity` probe. Giới hạn này
ngăn vòng lặp vô hạn nếu table đầy hoặc invariant bị hỏng.

Linear probing cũng phải giữ load factor nhỏ hơn `1`. Threshold mặc định là
`0.7`, để lại slot trống cho search dừng và giảm primary clustering.

---

## 10. Resize và rehash

Khi insert tiếp theo sẽ vượt threshold, table mở rộng và mọi live entry được
insert lại:

```text
    old index = hash(key) % old_capacity
    new index = hash(key) % new_capacity
```

Không thể chỉ copy entry vào cùng physical position vì probe sequence phụ thuộc
capacity mới. Resize cũng xóa mọi tombstone.

```text
    truoc resize:  [A] [DELETED] [B] [ ] [C]
    sau resize:    [ ] [ ] [A] [ ] [B] [ ] [C] [ ] [ ]
```

Rehash mất `O(n)` và chỉ diễn ra định kỳ. Chi phí được amortize qua các lần
insert làm table tăng trưởng.

---

## 11. Public Interface

Cả hai class cung cấp cùng các thao tác:

```python
table = LinearProbingHashMap[str, int]()
# Hoac:
table = RehashingLinearProbingHashMap[str, int]()

table.put("red", 1)
table["blue"] = 2

table.get("red")             # 1
table.get("missing", -1)    # -1
table["blue"]                # 2
"red" in table               # True
table.contains_key("blue")   # True
table.remove("red")
len(table)
list(table.items())
table.keys()
table.values()
table.slot_snapshot()         # xem slot rong, live va deleted
```

Map nhận key hashable và value bất kỳ. Thứ tự physical slot không phải cam kết
sorted order hoặc insertion order.

---

## 12. Độ phức tạp

Gọi `n` là số entry và `alpha` là load factor.

| Thao tác | Trung bình | Xấu nhất | Không gian phụ | Ghi chú |
|:---|:---:|:---:|:---:|:---|
| `put` | `O(1)` | `O(n)` | `O(1)` | Probe đến key hoặc slot dùng được |
| `get` | `O(1)` | `O(n)` | `O(1)` | Probe một cluster |
| `remove`, tombstone | `O(1)` | `O(n)` | `O(1)` | Ghi marker, có thể cleanup |
| `remove`, sửa cluster | `O(1)` | `O(n)` | `O(1)` | Reinsert cluster phía sau |
| `keys` / `items` | `O(capacity)` | `O(capacity)` | `O(n)` cho result | Quét physical slot |
| Resize | `O(n)` | `O(n)` | `O(n)` tạm thời | Insert lại live entry |
| Map đang lưu | - | - | `O(capacity)` | Một slot cho mỗi vị trí |

Expected performance phụ thuộc vào phân bố hash tốt và load factor thấp hơn `1`
một khoảng an toàn. Linear probing có thể gặp primary clustering: các slot gần
nhau bị chiếm làm probe sequence gần đó dài hơn.

---

## 13. Invariant và trường hợp biên

```text
    1. Mọi live key nằm tại hoặc sau home slot theo probe order.
    2. Search không bỏ qua live entry hoặc tombstone.
    3. Slot trống thông thường kết thúc search.
    4. Probe wrap từ capacity - 1 về 0.
    5. Một key xuất hiện nhiều nhất một lần.
    6. Linear probing resize trước khi table đầy.
    7. Tombstone không được trả về như live entry.
```

Các trường hợp biên quan trọng:

- Collision cluster đi qua cuối physical array.
- Key bị xóa nằm giữa home slot và một live key khác.
- Update key cũ không được tăng `len(table)`.
- Table có nhiều tombstone dù số live entry thấp vẫn cần cleanup.
- Không dùng key unhashable hoặc mutable làm map key.

---

## 14. Chạy ví dụ

Chạy:

```text
python LinearProbingHashMap.py
```

Demo tạo ba custom key có cùng hash value, xóa key ở giữa, kiểm tra key cuối
vẫn tìm được, rồi insert một key thay thế. Cùng scenario được chạy với cả hai
chiến lược và in items cùng physical slot layout.

Tombstone implementation có thể hiện `"<DELETED>"` ngay sau khi xóa; cluster
repair implementation không cần marker đó.

---

## 15. So sánh chaining với linear probing

| Đặc điểm | Separate chaining | Linear probing |
|:---|:---|:---|
| Hướng collision | Linked chain theo chiều dọc | Probe array theo chiều ngang |
| Load factor | Có thể lớn hơn `1` | Phải nhỏ hơn `1` |
| Độ phức tạp xóa | Unlink một node | Tombstone hoặc sửa cluster |
| Locality lưu trữ | Node có thể ở object riêng | Entry nằm trong một array |
| Ý nghĩa slot trống | Bucket đó không có head | Có thể chứng minh key không có |

Khác biệt khi xóa là bài học chính. Trong chained map, xóa một node không che
giấu các node sau nó. Trong open-addressed map, probe path phải tiếp tục tìm
được sau khi xóa.

---

## 16. Checklist cuối cùng

```text
    1. Mọi thao tác bắt đầu tại hash(key) % capacity.
    2. Probe bằng (index + 1) % capacity.
    3. Không dừng tại tombstone khi search.
    4. Không dùng None làm deleted marker.
    5. Sửa cluster hoặc giữ tombstone sau khi xóa.
    6. Update key cũ thay vì thêm duplicate.
    7. Resize trước khi load factor chạm 1.
    8. Rehash sau khi capacity thay đổi.
    9. Kỳ vọng O(1) trung bình, không phải bảo đảm tuyệt đối.
```

**Bước tiếp theo:** Vẽ một cluster wrap chiếm hai slot cuối và hai slot đầu,
sau đó xóa một entry rồi trace cả hai chiến lược.
