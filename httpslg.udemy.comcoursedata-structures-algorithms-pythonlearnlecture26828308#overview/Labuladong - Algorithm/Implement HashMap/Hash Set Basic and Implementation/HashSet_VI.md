
---

# Hash Set: Cơ bản và Cài đặt

## 1. Hash Set là gì?

**Set** lưu các value mà không có value đi kèm. Dictionary hoặc hash map lưu cặp:


```text
    key -> value
```

Hash set chỉ lưu các value như những key duy nhất:

```text
    value A
    value B
    value C
```

Quy tắc trung tâm là **tính duy nhất**. Thêm một value đã có không tạo bản sao
thứ hai. Implementation trong `HashSet.py` dùng cùng ý tưởng hash table như
separate chaining, nhưng mỗi node chỉ chứa một value và một con trỏ `next`.

Tài liệu tham khảo:

- [Core Principles of HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Hash Set Basic and Implementation](https://labuladong.online/en/algo/data-structure-basic/hash-set/)

---

## 2. Set là hash map chỉ có key

Cách hình dung đơn giản nhất là hash map mà value bị bỏ qua:

```text
    HashMap                         HashSet

    "alice" -> 100                  "alice"
    "bob"   -> 200                  "bob"
    "carol" -> 300                  "carol"
```

Để cài set bằng map, có thể lưu mọi value làm key và dùng một placeholder value
chung. `HashSet.py` lưu trực tiếp key node, tránh tạo và cập nhật placeholder
không cần thiết nhưng vẫn giữ nguyên logic bucket và collision.

---

## 3. Cấu trúc bucket

Set băm mỗi value thành bucket index:

```text
    value                 hash(value)                bucket

    12              --->  hash(12)             --->    2
    17              --->  hash(17)             --->    2   collision
    20              --->  hash(20)             --->    0
```

Mỗi bucket lưu một chain các value:

```text
    index       bucket

      0         [20] ---> None
      1         None
      2         [17] ---> [12] ---> None
      3         None
```

Implementation chèn value mới vào đầu chain. Thứ tự bucket và thứ tự duyệt không
phải sorted order hoặc insertion-order guarantee.

---

## 4. Hash và yêu cầu đối với key

Bucket index được tính bằng:

```python
index = hash(value) % capacity
```

Python yêu cầu set value phải hashable. Value cũng phải ổn định trong thời gian
được lưu. Object mutable có hành vi hash hoặc equality thay đổi có thể trở nên
không thể tìm thấy bên trong table.

Các value phù hợp:

```python
HashSet([1, 2, 3])
HashSet(["red", "green", "blue"])
HashSet([(1, 2), (3, 4)])
```

List và dictionary không hashable nên không thể insert trực tiếp. Hãy đổi chúng
sang biểu diễn immutable nếu phù hợp với bài toán, chẳng hạn tuple hoặc frozen
set.

---

## 5. `add`: Bảo đảm tính duy nhất

`add(value)` thực hiện:

```text
    1. Tính bucket index của value.
    2. Quét chain của bucket.
    3. Trả về False nếu value tương đương đã tồn tại.
    4. Nếu chưa có, thêm node vào đầu chain.
    5. Tăng size và resize nếu cần.
```

Kiểm tra duplicate là khác biệt cốt lõi giữa set và bag:

```text
    add("A") -> True
    add("A") -> False

    contents cuoi: {"A"}
```

Method trả về set có thay đổi hay không. Điều này giúp test hành vi duplicate dù
`set.add` dựng sẵn của Python trả về `None`.

---

## 6. Kiểm tra membership

Membership chỉ đi qua một bucket chain:

```text
    contains value B:

    hash(B) -> bucket 2
                      |
                      v
    [A] ---> [B] ---> [C] ---> None
              ^
              +-- equality match -> True
```

Class hỗ trợ cả method rõ ràng và cú pháp tự nhiên:

```python
members.contains("B")
"B" in members
```

Nếu value không có trong chain, kết quả là `False`. Thao tác không cần kiểm tra
những bucket không liên quan.

---

## 7. `discard` và `remove`

Xóa node khỏi chain dùng việc sửa link predecessor giống chained hash map:

```text
    truoc:

    previous ------> target ------> next

    sau:

    previous ---------------------> next
```

Implementation cung cấp cả hai semantics phổ biến:

```python
members.discard("missing")  # False, khong exception
members.remove("present")   # xoa value
members.remove("missing")   # raise KeyError
```

Dùng `discard` khi value thiếu là bình thường và không cần lỗi. Dùng `remove`
khi dữ liệu thiếu thể hiện lỗi logic cần nhìn thấy.

---

## 8. Resize và load factor

Load factor là:

```text
    load factor = so value dang luu / so bucket
```

Separate chaining về lý thuyết hỗ trợ load factor lớn hơn `1` vì một bucket có
thể giữ chain dài. Chain dài làm membership chậm, nên implementation mở rộng
table khi load factor vượt `0.75`.

```text
    capacity = 4, size = 3
    load factor = 0.75

    add them mot value:
    size = 4, load factor = 1.0
    resize thanh capacity 8
```

Mọi value phải được rehash sau resize vì capacity là một phần của phép tính
bucket index:

```text
    old index = hash(value) % old_capacity
    new index = hash(value) % new_capacity
```

Logical contents và size của set không đổi trong resize.

---

## 9. Set algebra

Với hai set `A` và `B`:

```text
    A = {1, 2, 3}
    B = {3, 4, 5}

    union:        A U B = {1, 2, 3, 4, 5}
    intersection: A n B = {3}
    difference:   A - B = {1, 2}
```

`HashSet.py` cài các phép toán này mà không dựa vào Python built-in set cho dữ
liệu được lưu:

```python
left = HashSet([1, 2, 3])
right = HashSet([3, 4, 5])

left.union(right)
left.intersection(right)
left.difference(right)
left.is_subset(right)

left | right
left & right
left - right
```

Với iterable bất kỳ, implementation tạo một `HashSet` tạm khi cần membership
check với collection còn lại. Nhờ đó thao tác có expected `O(n + m)` thay vì
quét collection kia cho từng value.

---

## 10. Public Interface

```python
members = HashSet(["red", "blue"], capacity=5)

members.add("green")
members.update(["blue", "yellow"])

"red" in members
members.contains("green")
members.discard("yellow")
members.remove("blue")

len(members)
list(members)
members.bucket_snapshot()
members.clear()
```

Constructor nhận một iterable tùy chọn. Value được yield theo physical bucket
order, vì vậy nên sort kết quả khi cần output xác định:

```python
sorted(members)
```

Set không cam kết insertion order.

---

## 11. Độ phức tạp

Gọi `n` là số value và `k` là độ dài chain được chọn.

| Thao tác | Trung bình | Xấu nhất | Không gian phụ | Lý do |
|:---|:---:|:---:|:---:|:---|
| `add` | `O(1)` | `O(n)` | `O(1)` | Hash cộng quét một chain |
| `contains` | `O(1)` | `O(n)` | `O(1)` | Quét một bucket chain |
| `discard` / `remove` | `O(1)` | `O(n)` | `O(1)` | Tìm và unlink một node |
| `union` | `O(n + m)` expected | `O(nm)` | `O(n + m)` | Add value từ hai set |
| `intersection` | `O(n + m)` expected | `O(nm)` | `O(n + m)` | Membership check trong set kia |
| `difference` | `O(n + m)` expected | `O(nm)` | `O(n + m)` | Loại value trong set kia |
| Iteration | `O(capacity + n)` | `O(capacity + n)` | `O(1)` | Duyệt bucket và node |
| Resize | `O(n)` | `O(n)` | `O(n)` tạm thời | Rehash mọi value |
| Set đang lưu | - | - | `O(n + capacity)` | Node cộng bucket head |

Các bound trung bình yêu cầu hàm băm phân bố hợp lý và value hashable ổn định.

---

## 12. Use case của hash set

Hash set hữu ích khi câu hỏi là “value này đã thấy chưa?” thay vì “value nào
thuộc key này?”

```text
    +-------------------------------------------------------------+
    | USE CASE PHO BIEN CUA HASH SET                             |
    +-------------------------------------------------------------+
    | Loai duplicate khoi mot sequence                            |
    | Theo doi vertex da tham trong graph                        |
    | Kiem tra hai collection co chung item                       |
    | Membership trong collection lon                             |
    | Dem so value khac nhau                                      |
    | Tao ket qua union, intersection, difference                 |
    +-------------------------------------------------------------+
```

Ví dụ, visited set ngăn graph traversal xử lý cùng một vertex nhiều lần. Bài
duplicate detector add từng item và kiểm tra boolean trả về từ `add`.

---

## 13. Invariant quan trọng

```text
    1. Moi value duoc luu reachable tu dung mot bucket head.
    2. Mot value xuat hien toi da mot lan.
    3. Bucket cua value la hash(value) % capacity.
    4. Size counter bang so value dang luu.
    5. Xoa chain head phai cap nhat bucket head.
    6. Resize phai rehash moi value theo capacity moi.
    7. Set khong expose bucket order nhu sorted/insertion order.
```

Các invariant này giải thích mọi method chính. Nếu một invariant bị phá vỡ,
membership có thể fail, duplicate có thể xuất hiện, hoặc resize làm value biến
mất.

---

## 14. Chạy ví dụ

Chạy:

```text
python HashSet.py
```

Demo cho thấy duplicate bị từ chối, membership, remove và ba phép toán set
chính. Demo chỉ sort value khi in để output dễ đọc; bản thân set không duy trì
sorted order.

---

## 15. So sánh Hash Set với HashMap

| Đặc điểm | HashSet | HashMap |
|:---|:---|:---|
| Dữ liệu lưu | Value duy nhất | Key duy nhất cùng value |
| Truy vấn chính | Value có tồn tại? | Value nào thuộc key? |
| Quy tắc duplicate | Từ chối value trùng | Key trùng update value |
| Xử lý collision | Bucket chain | Bucket chain hoặc probe |
| Use case | Membership và distinctness | Association và lookup |

Set không phải sorted collection. Nếu cần duyệt có thứ tự, dùng cấu trúc khác
hoặc sort kết quả sau iteration.

---

## 16. Checklist cuối cùng

```text
    1. Set luu key/value ma khong co mapped value rieng.
    2. Moi value dang luu phai duy nhat.
    3. Hash value de chon mot bucket.
    4. So sanh value bang nhau trong bucket do.
    5. Add tra False khi duplicate.
    6. Discard im lang; remove raise khi value thieu.
    7. Resize rehash moi value vi capacity doi index.
    8. Membership trung binh O(1); xau nhat O(n).
    9. Set algebra xay tu membership va insert.
```

**Bước tiếp theo:** Dùng `HashSet` để tìm duplicate đầu tiên trong một list, sau
đó viết lại bằng map và so sánh dữ liệu mỗi cấu trúc lưu.
