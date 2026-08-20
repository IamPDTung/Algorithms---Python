
---

# Dùng Array để tăng cường Hash Table (ArrayHashMap)

## 1. Mục tiêu

Hash table cho lookup key với độ phức tạp kỳ vọng `O(1)`, nhưng mảng bucket có
slot rỗng và các chain va chạm. Chọn ngẫu nhiên một bucket vật lý vì vậy không
chọn được một key ngẫu nhiên đồng đều.

Cài đặt trong `ArrayHashMap.py` thêm một mảng entry dày đặc. Nó hỗ trợ:

- `put`, `get`, `remove` và `contains_key` với độ phức tạp kỳ vọng `O(1)`.
- `random_key()` đồng đều trong thời gian `O(1)`.
- Bucket hash để lookup và xử lý va chạm.
- Xóa bằng cách đổi với phần tử cuối để mảng dày đặc không có lỗ.

Tài liệu tham khảo:

- [Nguyên lý cốt lõi của Hash Table](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Dùng Array để tăng cường Hash Table](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-array/)

## 2. API `random_key` mới

API map thông thường gồm:

```python
map.get(key)
map.put(key, value)
map.remove(key)
map.contains_key(key)
map.keys()
```

Phần tăng cường thêm:

```python
key = map.random_key()
```

Yêu cầu là tính ngẫu nhiên đồng đều: nếu map có `N` key thì mỗi key phải được
chọn với xác suất `1 / N`. Method cũng phải có thời gian `O(1)`.

## 3. Vì sao chọn một slot hash table là sai

Xét một table open addressing có slot rỗng:

```text
table: [A, None, C, None, None, D]
```

Chọn một index vật lý ngẫu nhiên có thể trả về slot rỗng. Nếu thuật toán đi sang
phải sau khi gặp khoảng trống, những key ở phía phải khoảng trống sẽ có xác suất
cao hơn. Nếu thử lại index ngẫu nhiên nhiều lần, kết quả có thể đồng đều nhưng
thời gian phụ thuộc vào may rủi và không còn bảo đảm `O(1)`.

Với chaining, chọn bucket ngẫu nhiên còn có vấn đề khác. Bucket có thể chứa số
node khác nhau, vì vậy chọn bucket đồng đều rồi chọn node đồng đều sẽ ưu tiên
key trong chain ngắn hơn key trong chain dài.

Giải pháp là duy trì một mảng phụ dày đặc, chứa chính xác một entry cho mỗi key
đang sống.

## 4. Hai cấu trúc, một tập entry

`ArrayHashMap` duy trì:

```text
mảng bucket                          mảng entry dày đặc
---------------                     -------------------------
0 -> None                            index 0: [A, value A]
1 -> [C] -> [A]                      index 1: [B, value B]
2 -> [B]                             index 2: [C, value C]
```

Mảng bucket trả lời lookup key. Mảng dày đặc trả lời việc liệt kê và chọn ngẫu
nhiên. Mỗi `_ArrayEntry` lưu `array_index` của chính nó, vì vậy xóa có thể cập
nhật entry được di chuyển trong thời gian hằng số.

Map không dùng thêm một dictionary để theo dõi vị trí mảng. Object entry tự lưu
vị trí cần thiết cho thao tác swap.

## 5. Bố cục entry và bucket

Mỗi entry chứa:

```text
key, value
    Cặp mapping mà người dùng nhìn thấy.

array_index
    Vị trí hiện tại trong list `_entries` compact.

next_bucket
    Entry tiếp theo trong collision chain của bucket chứa key.
```

Bất biến chính là:

```text
0 <= entry.array_index < len(_entries)
_entries[entry.array_index] is entry
```

Mỗi entry đang sống xuất hiện đúng một lần trong bucket chain và đúng một lần
trong mảng dày đặc.

## 6. `put`: thêm hoặc cập nhật

`put(key, value)` trước hết tìm trong bucket tương ứng:

```text
1. Tính hash(key) % capacity.
2. Đi qua chain của bucket đó.
3. Nếu key đã có, chỉ thay value.
4. Nếu chưa có, tạo entry ở cuối `_entries`.
5. Nối entry vào bucket chain.
6. Resize nếu load factor quá cao.
```

Cập nhật key hiện có không thêm một entry mới vào mảng:

```python
array_map.put("a", 1)
array_map.put("b", 2)
array_map.put("a", 10)

assert array_map.keys() == ["a", "b"]
assert array_map["a"] == 10
```

Method trả về value cũ khi cập nhật và `None` khi thêm key mới.

## 7. `remove`: đổi với entry cuối

Xóa ở giữa Python list bằng cách dồn mọi phần tử phía sau sẽ tốn `O(N)`. Kỹ
thuật mảng dày đặc tránh dồn phần tử:

```text
trước: [A, B, C, D]
xóa B
đưa D vào slot của B
sau:   [A, D, C]
```

Các bước là:

```text
1. Tháo target khỏi bucket chain.
2. Lấy entry cuối của mảng dày đặc.
3. Nếu target chưa phải entry cuối, đặt last vào slot target.
4. Cập nhật last.array_index.
5. Pop vị trí cuối của list.
```

Vì vậy thứ tự của `keys()` không bảo đảm là thứ tự chèn. Nó là thứ tự hiện tại
của mảng compact, và một lần xóa có thể làm một key khác di chuyển. Sự thay đổi
này cần thiết để `remove` và các lần `random_key` sau đó vẫn là `O(1)`.

## 8. Chọn ngẫu nhiên đồng đều

Sau mỗi lần thêm hoặc xóa, `_entries` không có lỗ:

```python
index = rng.randrange(len(_entries))
return _entries[index].key
```

Mọi index hợp lệ có xác suất như nhau và mỗi index chứa một key đang sống. Do
đó mỗi key có xác suất `1 / len(_entries)`. Thuật toán không xem bucket rỗng,
không thử lại và không quét tìm phần tử lân cận.

Constructor nhận một object `random.Random` tùy chọn. Điều này hữu ích cho ví dụ
và test có thể lặp lại; bất biến của data structure không phụ thuộc generator.

Gọi `random_key()` trên map rỗng sẽ ném `KeyError` vì không có key nào có thể
được trả về.

## 9. Resize hash table

Mảng dày đặc và mảng bucket có nhiệm vụ khác nhau khi resize. Mảng entry đã
compact nên có thể giữ nguyên thứ tự hiện tại. Chỉ các liên kết bucket cần xây
dựng lại:

```text
index cũ = hash(key) % capacity cũ
index mới = hash(key) % capacity mới
```

Cài đặt đi qua `_entries`, tính index mới và nối entry vào bucket mới. Không có
entry nào được copy và không có `array_index` nào thay đổi.

## 10. Lookup, liệt kê và độ phức tạp

| Thao tác | Thời gian kỳ vọng | Lý do |
|:---|:---:|:---|
| `put` | `O(1)` | Tìm chain kỳ vọng ngắn và append |
| `get` | `O(1)` | Tìm trong một chain kỳ vọng ngắn |
| `contains_key` | `O(1)` | Cùng cách tìm bucket |
| `remove` | `O(1)` | Tháo liên kết và swap với entry cuối |
| `random_key` | `O(1)` | Một index ngẫu nhiên và một lần truy cập mảng |
| `keys` / `items` | `O(N)` | Đi qua mảng entry dày đặc |
| Resize | `O(N)` | Xây dựng lại liên kết mọi bucket |

Giống mọi hash table, hash phân bố kém có thể làm collision chain dài. Các cận
`O(1)` là cận kỳ vọng hoặc amortized trong điều kiện hash thông thường.

## 11. API Python công khai

```python
array_map = ArrayHashMap[str, int]()
array_map.put("language", 1)
array_map["version"] = 3

array_map.get("language")
array_map.contains_key("version")
array_map.random_key()
array_map.remove("language")
array_map.keys()
array_map.values()
array_map.items()
array_map.dense_array_snapshot()
array_map.bucket_snapshot()
array_map.clear()
```

Class cũng hỗ trợ `len(array_map)`, `key in array_map`, phép lặp và
`del array_map[key]`.

## 12. Ví dụ và minh họa xóa

Ví dụ thực thi tạo một random generator có seed, thêm bốn key, xóa một key ở
giữa mảng dày đặc rồi in cả mảng entry và các bucket chain. Kết quả làm rõ
thao tác swap với entry cuối.

Chạy bằng:

```text
python ArrayHashMap.py
```

Random key có thể khác khi truyền generator khác, nhưng mọi key đang sống vẫn
có xác suất được chọn như nhau.

## 13. Giới hạn thiết kế

Mảng dày đặc là index phụ, không phải mảng đã sắp xếp và cũng không phải danh
sách thứ tự chèn. Nếu ứng dụng cần thứ tự chèn ổn định, hãy dùng cài đặt
`LinkedHashMap`.

`random_key` trả về key, không trả về value. Có thể dùng key được chọn để gọi
`get`, nhưng việc chọn key/value vẫn bắt đầu từ một lần chọn đồng đều trên các
entry đang sống.

Key phải hash được và ổn định khi lưu. Tối ưu mảng không thể sửa một key có
hành vi hash hoặc equality thay đổi.

## 14. Tài liệu tham khảo

- [Dùng Array để tăng cường Hash Table (ArrayHashMap)](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-array/)
- [Khái niệm cơ bản của HashMap](https://labuladong.online/en/algo/data-structure-basic/hashmap-basic/)
- [Dùng Linked List để tăng cường Hash Table (LinkedHashMap)](https://labuladong.online/en/algo/data-structure-basic/hashtable-with-linked-list/)
