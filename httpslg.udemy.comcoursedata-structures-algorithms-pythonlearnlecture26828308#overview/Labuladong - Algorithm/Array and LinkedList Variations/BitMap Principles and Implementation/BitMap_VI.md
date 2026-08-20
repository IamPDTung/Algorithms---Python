
---

# Nguyên lý và Cài đặt BitMap

## 1. Bitmap là gì?

**Bitmap** biểu diễn một tập hợp các trạng thái boolean bằng từng bit riêng lẻ.
Với một tập số nguyên, vị trí bit `x` trả lời câu hỏi:

```text
    x có đang tồn tại không?
```

Cài đặt trong `BitMap.py` lưu một universe cố định gồm các giá trị từ `0` đến
`size - 1` bên trong một `bytearray`.

```text
    value 0 -> bit 0
    value 1 -> bit 1
    value 2 -> bit 2
    ...
    value 7 -> bit 7
    value 8 -> bit 0 của byte tiếp theo
```

Một bit lưu một câu trả lời có/không. Cách này gọn hơn rất nhiều so với việc
lưu một Python boolean object hoặc một Python integer object cho mỗi giá trị có
thể xuất hiện.

---

## 2. Nó giải quyết vấn đề gì?

Giả sử bài toán hỏi những ID từ `0` đến `15` đã xuất hiện chưa:

```text
    biểu diễn bằng Python set:

    {1, 3, 8, 13}
```

Set linh hoạt và có membership trung bình nhanh, nhưng phải lưu metadata của
hash table và các object reference. Nếu universe dày và đã biết trước, bitmap
có thể biểu diễn cùng câu trả lời chỉ bằng hai byte:

```text
    các giá trị tồn tại: 1, 3, 8, 13

    value:     15 14 13 12 11 10  9  8 |  7  6  5  4  3  2  1  0
    bit:        0  0  1  0  0  0  0  1 |  0  0  0  0  1  0  1  0
    byte:                          32 + 1 = 33 |     8 + 2 = 10
```

Bitmap dùng chính xác `ceil(size / 8)` byte cho phần lưu bit, chưa tính Python
object nhỏ và metadata.

---

## 3. Bit, byte và mask

Tám bit tạo thành một byte:

```text
    bit offset:   7   6   5   4   3   2   1   0
                 +---+---+---+---+---+---+---+---+
    byte value:  |   |   |   |   |   |   |   |   |
                 +---+---+---+---+---+---+---+---+
```

Với một giá trị nguyên `x`, tính:

```text
    byte_index = x >> 3       # giống x // 8
    bit_offset = x & 7        # giống x % 8
    bit_mask   = 1 << bit_offset
```

Ví dụ với `x = 13`:

```text
    byte_index = 13 >> 3 = 1
    bit_offset = 13 & 7  = 5
    bit_mask   = 1 << 5  = 00100000
```

Mask chỉ chọn đúng bit cần thao tác:

```text
    byte hiện tại:  00001011
    mask cho 13:    00100000
                     -------- OR
    thêm 13:        00101011
```

---

## 4. Set một bit

Dùng phép OR bitwise để bật bit:

```python
bits[byte_index] |= bit_mask
```

OR giữ nguyên mọi bit hiện tại và bảo đảm bit được chọn trở thành `1`:

```text
    hiện tại:  01000001
    mask:      00000100
               -------- OR
    kết quả:   01000101
```

Thêm một giá trị đã tồn tại không làm thay đổi gì. `BitMap.add()` trả về
`False` trong trường hợp đó và cardinality vẫn giữ nguyên.

---

## 5. Xóa một bit

Dùng mask đảo với phép AND bitwise:

```python
bits[byte_index] &= ~bit_mask
```

Bit được chọn bị ép về `0`, còn các bit khác giữ nguyên:

```text
    hiện tại:  01000101
    ~mask:      11111011
                -------- AND
    kết quả:    01000001
```

Integer của Python có độ chính xác không giới hạn, nhưng gán kết quả trở lại
`bytearray` giữ giá trị đã lưu trong phạm vi một byte.

---

## 6. Kiểm tra một bit

Dùng AND bitwise rồi chuyển kết quả thành boolean:

```python
present = bool(bits[byte_index] & bit_mask)
```

Kết quả khác không chính xác khi bit được chọn đang bật:

```text
    byte:       01000101
    mask:       00000100
                -------- AND
    result:     00000100  -> có mặt
```

`value in bitmap` được cài đặt như một membership check an toàn. Giá trị không
hợp lệ hoặc nằm ngoài range trả về `False` qua toán tử membership, còn các
phương thức `add`, `remove`, `toggle` và `contains` rõ ràng sẽ từ chối giá trị
không hợp lệ bằng exception.

---

## 7. Toggle một bit

Exclusive OR lật chính xác một bit:

```python
bits[byte_index] ^= bit_mask
```

```text
    hiện tại:  01000101
    mask:      00000100
               -------- XOR
    kết quả:   01000001

    áp dụng lại XOR một lần nữa:

    hiện tại:  01000001
    mask:      00000100
               -------- XOR
    kết quả:   01000101
```

`BitMap.toggle()` trả về trạng thái boolean mới sau khi lật bit.

---

## 8. Ánh xạ giá trị vào byte

Với bitmap size `20`, cần ba byte vì:

```text
    ceil(20 / 8) = 3 bytes
```

Công thức chính xác là `(size + 7) // 8`, nên `20` cần `3` byte. Các giá trị hợp
lệ chiếm bốn bit đầu tiên của byte cuối:

```text
    byte 0: các giá trị  0 -  7
    byte 1: các giá trị  8 - 15
    byte 2: các giá trị 16 - 19, các bit còn lại không dùng

    values:       0  1  2  3  4  5  6  7 |  8 ... 15 | 16 17 18 19
    byte index:   0  0  0  0  0  0  0  0 |  1 ...  1 |  2  2  2  2
```

Các bit nằm ngoài universe được khai báo sẽ bị từ chối khi load raw bytes, vì
vậy `BitMap(20)` không thể vô tình chứa giá trị `23`.

---

## 9. Bitmap so với Boolean Array và Set

| Biểu diễn | Membership | Ý tưởng lưu trữ | Phù hợp khi |
|:---|:---:|:---|:---|
| Python `set` | `O(1)` trung bình | Hash table và object | Giá trị thưa hoặc tùy ý |
| Boolean list | `O(1)` | Một object/reference Python cho mỗi ô | Ưu tiên sự đơn giản |
| `BitMap` | `O(1)` | Một bit cho mỗi giá trị có thể có | Universe integer bị giới hạn và dày |
| Sorted list | `O(log n)` với binary search | Một object cho mỗi giá trị | Cần lưu theo thứ tự |

Bitmap không phải lúc nào cũng tốt hơn. Nếu universe cực lớn nhưng chỉ có vài
giá trị xuất hiện, set có thể ít tốn bộ nhớ hơn vì không cần biểu diễn mọi giá
trị bị thiếu.

---

## 10. Interface của cài đặt

Toàn bộ cài đặt nằm trong `BitMap.py`:

```python
bitmap = BitMap(16)

bitmap.add(13)              # set value 13; True nếu mới
bitmap.remove(13)           # clear value 13; True nếu đang tồn tại
bitmap.toggle(13)           # lật value 13; trả về trạng thái mới
bitmap.contains(13)         # membership có kiểm tra rõ ràng
13 in bitmap                # cú pháp membership an toàn
list(bitmap)                # các value đang set theo thứ tự tăng dần
len(bitmap)                 # số value đang set
bitmap.to_bytes()           # các byte đã đóng gói
```

Class cũng cung cấp `union()` và `intersection()` để thực hiện phép toán set
theo bit giữa các bitmap có cùng kích thước universe.

---

## 11. Union và Intersection

Hai bitmap cùng universe có thể được kết hợp theo từng byte.

```text
    A:       01001100
    B:       00010110

    A union B:
             01011110       bitwise OR

    A intersect B:
             00000100       bitwise AND
```

Kết quả có cùng `size` với hai đầu vào. Cài đặt tính lại số bit đang set sau
phép toán.

---

## 12. Duyệt các giá trị đang set

Để duyệt hiệu quả, cài đặt quét từng byte và liên tục xóa bit thấp nhất đang
set:

```text
    remaining = byte
    while remaining != 0:
        lowest_bit = remaining & -remaining
        process lowest_bit
        remaining ^= lowest_bit
```

Ví dụ:

```text
    remaining:       10110100
    lowest bit:      00000100
    after removing:  10110000

    lowest bit:      00010000
    after removing:  10100000
```

Cách này thăm các bit đang set thay vì kiểm tra mọi giá trị có thể bên trong
một byte. Các value được yield vẫn theo thứ tự tăng dần vì byte và bit offset
được quét từ thấp lên cao.

---

## 13. Serialization

`to_bytes()` trả về biểu diễn đã đóng gói. `size` được lưu riêng vì byte cuối có
thể chứa các bit không dùng:

```python
payload = bitmap.to_bytes()
restored = BitMap.from_bytes(bitmap.size, payload)
```

Các byte serialize không chứa metadata của Python object. Chúng hữu ích cho
việc lưu trữ hoặc truyền dữ liệu gọn nhẹ khi bên nhận cũng biết universe size.

---

## 14. Độ phức tạp

| Thao tác | Thời gian | Bộ nhớ phụ | Lý do |
|:---|:---:|:---:|:---|
| `add` | `O(1)` | `O(1)` | Tìm một byte và set một bit |
| `remove` | `O(1)` | `O(1)` | Tìm một byte và clear một bit |
| `toggle` | `O(1)` | `O(1)` | Một lần cập nhật kiểu XOR |
| `contains` | `O(1)` | `O(1)` | Tra cứu một byte |
| `len` | `O(1)` | `O(1)` | Counter được duy trì sẵn |
| Iteration | `O(số bit đang set + số byte)` | `O(1)` | Quét storage đã đóng gói |
| `union` | `O(size / 8)` | `O(size / 8)` | Kết hợp mọi byte |
| `intersection` | `O(size / 8)` | `O(size / 8)` | Kết hợp mọi byte |
| Bộ nhớ lưu trữ | - | `O(size / 8)` byte | Một bit cho mỗi giá trị có thể có |

Kích thước universe đầu vào quyết định bộ nhớ bitmap, ngay cả khi chỉ có một
giá trị được set.

---

## 15. Nó hữu ích ở đâu?

```text
    +---------------------------------------------------------------+
    | CÁC USE CASE CỦA BITMAP                                      |
    +---------------------------------------------------------------+
    | Presence flags       -> ID đã thấy, state đã thăm             |
    | Sieve of Eratosthenes-> đánh dấu số hợp thành                 |
    | Permission masks     -> feature flag gọn nhẹ                   |
    | Deduplication        -> giá trị integer bị giới hạn            |
    | Bloom-filter bits    -> membership xác suất gọn nhẹ            |
    | Calendar occupancy   -> một bit cho mỗi ngày hoặc time slot    |
    +---------------------------------------------------------------+
```

Bitmap đặc biệt hữu ích trong bài contest có constraint như `0 <= value <=
10^7` và cần kiểm tra presence nhanh. Luôn so sánh chi phí bộ nhớ `size / 8`
với memory limit của đề.

---

## 16. Các trường hợp biên

### Universe rỗng

`BitMap(0)` hợp lệ nhưng không có giá trị hợp lệ nào. Thêm bất kỳ giá trị nào
đều gây lỗi.

### Add trùng

Thêm một value hai lần không làm `len(bitmap)` tăng hai lần.

### Giá trị không hợp lệ

Các phương thức thay đổi và truy vấn rõ ràng từ chối giá trị âm, giá trị lớn hơn
hoặc bằng `size`, non-integer và boolean.

### Bit cuối không dùng

Nếu `size` không chia hết cho `8`, byte cuối có các bit cao không dùng. Loader
serialization từ chối các bit đó thay vì âm thầm tạo ra giá trị nằm ngoài
universe đã khai báo.

### Universe thưa

Nếu `size` là `10^9` và chỉ có ba giá trị tồn tại, bitmap cần khoảng
`125,000,000` byte trước Python object overhead. Khi đó set có thể phù hợp hơn.

---

## 17. Chạy ví dụ

Chạy:

```text
python BitMap.py
```

Output kỳ vọng:

```text
Members: [1, 3, 8, 13]
Count: 4
Contains 13: True
After remove/toggle: [1, 5, 8, 13]
Union: [1, 5, 8, 12, 13]
Intersection: [5]
```

---

## 18. Cheat Sheet cuối cùng

```text
    1. Bitmap lưu một trạng thái boolean cho mỗi bit.
    2. byte_index = value >> 3.
    3. bit_mask = 1 << (value & 7).
    4. OR dùng để set một bit.
    5. AND với mask đảo dùng để clear một bit.
    6. AND dùng để kiểm tra một bit.
    7. XOR dùng để toggle một bit.
    8. Membership có độ phức tạp O(1).
    9. Bộ nhớ là một bit cho mỗi giá trị trong universe.
   10. Dùng set khi universe lớn và thưa.
```

**Bước tiếp theo:** Tự viết byte và mask cho các giá trị `0`, `7`, `8` và `15`,
sau đó đối chiếu với cách suy luận `_location` trong `BitMap.py`.
