
---

# Dùng Linked List để tăng cường Hash Table (LinkedHashMap)

## 1. Mục tiêu

Hash table thông thường được tối ưu cho việc tìm kiếm, thêm, cập nhật và xóa.
Mảng bucket của nó không cung cấp một thứ tự có ý nghĩa khi duyệt các key. Cài
đặt này thêm một cấu trúc thứ hai để map có thể duyệt key theo thứ tự chèn.

Cài đặt trong `LinkedHashMap.py` hỗ trợ:

- `put`, `get`, `remove` và `contains_key` với độ phức tạp kỳ vọng `O(1)`.
- Duyệt `keys`, `items` và `values` theo thứ tự chèn.
- Resize nhưng vẫn giữ nguyên thứ tự logic.
- Cú pháp map quen thuộc như `map[key]` và `map[key] = value`.


- [Nguyên lý cốt lõi của Hash Table](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Dùng Linked List để tăng cường Hash Table](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-linked-list/)

## 2. Ý tưởng cốt lõi

Cấu trúc dữ liệu kết hợp hai góc nhìn độc lập trên cùng các entry:

```text
                         danh sách theo thứ tự chèn
                         đầu                    cuối
                          |                      |
                          v                      v
                       [A] <-> [B] <-> [C] <-> [D]
                        |             |          |
                        +-------------+----------+
                              các entry cũng ở trong bucket
```

Liên kết bucket trả lời các câu hỏi của hash table. Danh sách liên kết đôi toàn
cục trả lời các câu hỏi về thứ tự. Một entry tham gia cả hai cấu trúc; map không
lưu thêm một bản sao của cặp key/value.

## 3. Vì sao Hash Map thông thường không bảo đảm thứ tự

Hash map trước hết tính một chỉ số mảng:

```python
index = hash(key) % capacity
```

Khi duyệt thông thường, ta quét mảng bucket từ index `0` đến cuối. Thứ tự đó
phụ thuộc vào hash và các chain va chạm, không phải thứ tự chèn. Khi map resize,
phép modulo thay đổi và các entry được hash lại vào vị trí mới. Vì vậy thứ tự
duyệt có thể thay đổi dù không xóa phần tử nào.

Quy tắc quan trọng là thứ tự bucket của hash table chỉ là chi tiết cài đặt. Nếu
code cần thứ tự chèn ổn định, ta phải lưu thứ tự đó một cách tường minh.

## 4. Hai loại liên kết, hai trách nhiệm

`_LinkedEntry` có ba nhóm field:

```text
key, value
    Cặp mapping mà người dùng nhìn thấy.

next_bucket
    Entry kế tiếp trong bucket được chọn bởi hash(key).

previous_order, next_order
    Entry trước và sau trong danh sách theo thứ tự chèn.
```

Không được nhầm hai hệ thống liên kết này. Xóa một entry phải tháo nó khỏi cả
bucket chain và danh sách thứ tự. Resize chỉ xây dựng lại liên kết bucket; các
liên kết thứ tự phải được giữ nguyên.

## 5. Tìm trong bucket và xử lý va chạm

Mỗi bucket lưu entry đầu của một chain va chạm đơn:

```text
bucket 1 ---> [beta] ---> [alpha] ---> None
```

Lookup tính một bucket rồi so sánh key trong chain đó. Hai key khác nhau có thể
cùng index hash, nên sau bước hash vẫn cần so sánh bằng. Key phải hash được và
không được thay đổi dữ liệu dùng trong `__hash__` hoặc `__eq__` khi đang được
lưu trong map.

Trong Python, phép modulo với số dương vẫn cho index hợp lệ ngay cả khi
`hash(key)` là số âm.

## 6. `put`: thêm hoặc cập nhật

`put(key, value)` thực hiện các bước:

```text
1. Tìm key trong bucket chain.
2. Nếu đã có, chỉ thay value.
3. Nếu chưa có, tạo một entry.
4. Nối entry vào bucket chain.
5. Nối chính entry đó vào cuối danh sách thứ tự.
6. Resize nếu load factor quá cao.
```

Cập nhật key hiện có không đưa key đó xuống cuối. Đây là hành vi theo thứ tự
chèn: vị trí chèn ban đầu được giữ nguyên. Nếu xóa key rồi chèn lại, entry mới
sẽ được nối vào cuối.

```python
linked_map.put("a", 1)
linked_map.put("b", 2)
linked_map.put("a", 10)

assert linked_map.keys() == ["a", "b"]
assert linked_map["a"] == 10
```

Method trả về value cũ khi cập nhật và `None` khi thêm key mới.

## 7. `get` và `contains_key`

Cả hai thao tác dùng bucket chain, không dùng danh sách thứ tự:

```python
value = linked_map.get("missing", 0)
exists = linked_map.contains_key("a")

assert value == 0
assert exists
```

`get` trả về `default` khi không tìm thấy key. Truy cập bằng ngoặc vuông,
`linked_map[key]`, ném `KeyError` nếu key không tồn tại, giống mapping thông
thường của Python.

## 8. `remove`: sửa cả hai cấu trúc

Trong bucket chain, xóa entry bằng cách bỏ qua entry đích:

```text
previous ---> target ---> next

previous ----------------> next
```

Target cũng phải được xóa khỏi danh sách liên kết đôi:

```text
trước:  A <-> target <-> B
sau:    A <-----------> B
```

Cài đặt xử lý mọi vị trí trong danh sách:

- Xóa đầu danh sách thì `_head` chuyển sang entry kế tiếp.
- Xóa cuối danh sách thì `_tail` chuyển về entry trước đó.
- Xóa entry duy nhất thì xóa cả hai endpoint.
- Xóa entry ở giữa thì nối hai hàng xóm lại với nhau.

`remove` trả về value và ném `KeyError` nếu key không tồn tại.

## 9. Resize nhưng không mất thứ tự

Load factor được tính như sau:

```text
load factor = số entry / số bucket
```

Khi vượt ngưỡng cấu hình, table tăng kích thước. Vì bucket index phụ thuộc vào
capacity nên mọi entry phải được hash lại:

```text
index cũ = hash(key) % capacity cũ
index mới = hash(key) % capacity mới
```

`_resize` đi qua danh sách thứ tự toàn cục và chỉ xây dựng lại liên kết bucket.
Các liên kết thứ tự cùng `_head` và `_tail` không đổi, nên resize không làm đổi
thứ tự của `keys()`.

## 10. Duyệt và độ phức tạp

| Thao tác | Thời gian kỳ vọng | Lý do |
|:---|:---:|:---|
| `put` | `O(1)` | Hash một bucket và nối vào cuối list |
| `get` | `O(1)` | Tìm trong một chain kỳ vọng ngắn |
| `contains_key` | `O(1)` | Cùng cách tìm bucket như `get` |
| `remove` | `O(1)` | Tháo khỏi bucket và list liên kết đôi |
| `keys` / `items` | `O(N)` | Đi qua mọi entry trong order list |
| Resize | `O(N)` | Hash lại mọi entry |

Các cận trên giả sử hash phân bố tốt. Một hash function cố tình tệ có thể làm
một chain rất dài và khiến thao tác trên bucket chậm hơn.

## 11. API Python công khai

Class cung cấp các method chính:

```python
linked_map = LinkedHashMap[str, int]()
linked_map.put("language", 1)
linked_map["version"] = 3

linked_map.get("language")
linked_map.contains_key("version")
linked_map.remove("language")
linked_map.keys()
linked_map.values()
linked_map.items()
linked_map.clear()
```

Ngoài ra còn hỗ trợ `len(linked_map)`, `key in linked_map`, phép lặp và
`del linked_map[key]`.

## 12. Ví dụ và minh họa va chạm

Ví dụ thực thi định nghĩa `CollisionKey`, trong đó mỗi object có thể được gán
cùng một giá trị hash. Chương trình thêm các key va chạm, cập nhật một key,
trigger resize, xóa đầu danh sách và in thứ tự cuối cùng.

Chạy bằng:

```text
python LinkedHashMap.py
```

Thứ tự được in ra đến từ linked list, không đến từ mảng bucket vật lý. Đây là
phần tăng cường cốt lõi so với hash map cơ bản.

## 13. Giới hạn thiết kế

Class này cài đặt duyệt theo thứ tự chèn, không phải thứ tự truy cập. Gọi `get`
không đưa key xuống cuối. Một cache theo access order cần tháo rồi nối entry vào
cuối sau mỗi lần truy cập thành công, thường đi kèm chính sách loại bỏ theo
capacity.

Map vẫn yêu cầu key hash được và ổn định. Linked list giữ thứ tự nhưng không thể
sửa một hash key không hợp lệ hoặc có thể thay đổi.

## 14. Tài liệu tham khảo

- [Dùng Linked List để tăng cường Hash Table (LinkedHashMap)](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-linked-list/)
- [Khái niệm cơ bản của HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Cài đặt HashMap bằng Separate Chaining](https://labuladong.online/en/algo/data-structure-basic/hashtable-chaining/)
