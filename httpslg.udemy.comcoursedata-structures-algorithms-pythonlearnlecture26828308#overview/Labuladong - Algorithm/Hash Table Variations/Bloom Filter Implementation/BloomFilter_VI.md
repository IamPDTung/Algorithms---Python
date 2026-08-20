
---

# Cài đặt Bloom Filter

## 1. Bloom Filter là gì?

**Bloom filter** là một cấu trúc dữ liệu xác suất, nhỏ gọn, dùng để kiểm tra
membership. Nó không lưu các value ban đầu. Thay vào đó, nó lưu một số vị trí
bit được suy ra từ fingerprint hash của mỗi value.

Câu trả lời của nó có tính bất đối xứng có chủ đích:

- `False` nghĩa là value chắc chắn không có.
- `True` nghĩa là value có thể có.

Cài đặt trong `BloomFilter.py` dùng `bytearray` làm mảng bit và double hashing để
sinh nhiều vị trí. Đây là filter chỉ thêm, có thao tác `clear`; nó không cung
cấp thao tác xóa từng value không an toàn.

Tài liệu tham khảo:

- [Khái niệm và cài đặt Hash Set](https://labuladong.online/en/algo/data-structure-basic/hash-set/)
- [Nguyên lý và cài đặt Bloom Filter](https://labuladong.online/en/algo/data-structure-basic/bloom-filter/)
- [Nguyên lý và cài đặt Bitmap](https://labuladong.online/en/algo/data-structure-basic/bitmap/)

## 2. Vì sao Hash Set đôi khi chưa đủ

Hash set cho membership chính xác và thêm, lookup kỳ vọng `O(1)`. Tuy nhiên nó
lưu value thật, object entry, reference và metadata của hash table. Với dataset
rất lớn, chi phí bộ nhớ này có thể quá cao.

Bloom filter hữu ích như một phép kiểm tra sơ bộ nhỏ:

```text
query
  |
  v
Bloom filter trả False? ---- có ---> chắc chắn không có
  |
  không
  v
Kiểm tra hash set, database hoặc file đĩa tốn kém
```

Nó có thể tránh công việc đắt khi một item chắc chắn không thuộc data source
lớn. Nó không thể thay thế exact set khi false positive gây hậu quả nghiêm
trọng.

## 3. Mảng bit

Filter sở hữu `m` bit, ban đầu đều bằng zero:

```text
bits: 0 0 0 0 0 0 0 0 0 0 0 0 ...
       ^       ^       ^
       các vị trí được set bởi một value
```

Cài đặt Python đóng gói tám bit logic vào mỗi byte của `bytearray`:

```python
byte_index = bit_position >> 3
bit_mask = 1 << (bit_position & 7)
bits[byte_index] |= bit_mask       # set
bool(bits[byte_index] & bit_mask)  # kiểm tra
```

Filter không lưu danh sách value đã thêm. Bộ nhớ cho fingerprint là `ceil(m / 8)`
byte, cộng thêm metadata nhỏ của object.

## 4. Nhiều vị trí hash

Một vị trí hash tạo ra quá nhiều va chạm. Bloom filter vì vậy dùng `k` vị trí
cho mỗi value:

```text
value -> h1, h2
          |
          +--> (h1 + 0 * h2) % m
          +--> (h1 + 1 * h2) % m
          +--> (h1 + 2 * h2) % m
          +--> ...
```

Đây là double hashing. Nó suy ra nhiều vị trí từ hai hash value thay vì phải
viết `k` hash function độc lập. Các vị trí được set khi add và được kiểm tra lại
khi query.

`BloomFilter` yêu cầu value hash được, giống hash set. Kết quả `hash` của Python
có thể âm; modulo với số bit dương đưa nó về một bit index hợp lệ.

## 5. Thêm một value

Để thêm `x`, tính tất cả `k` vị trí rồi set các bit tương ứng:

```text
trước: các bit được chọn có thể là 0
add x: set vị trí 4, vị trí 19, vị trí 37, ... thành 1
sau:   các vị trí đó giữ giá trị 1
```

Thêm lại cùng một value là an toàn. Nó set lại các bit cũ và không thay đổi câu
trả lời logic của filter. Property `insertions` đếm số lần gọi `add`, không phải
số value duy nhất, vì Bloom filter chuẩn không thể khôi phục cardinality từ các
bit.

`expected_items` là mục tiêu dùng để tính kích thước, không phải giới hạn cứng.
Có thể thêm nhiều item hơn, nhưng false-positive rate sẽ tăng vượt ước lượng
mục tiêu.

## 6. Kiểm tra membership

Để kiểm tra `x`, tính lại các vị trí tương tự:

```text
nếu bất kỳ bit bắt buộc nào là 0:
    x chắc chắn không có
ngược lại:
    x có thể có
```

API Python làm rõ sự không chắc chắn:

```python
if not bloom.might_contain(url):
    skip_expensive_lookup(url)
else:
    perform_exact_check(url)
```

Toán tử `in` cũng được hỗ trợ, nên `url in bloom` nghĩa là “filter nói value có
thể có”, không phải “value chắc chắn có”.

## 7. Vì sao có false positive

Các value khác nhau có thể set trùng bit. Giả sử `x` set các vị trí `2`, `5`,
và `9`. Một value `y` chưa từng được thêm vẫn có thể thấy cả ba vị trí đã được
các value khác set:

```text
query y -> bit 2, 5, 9 đều là 1 -> có thể có
```

Đây là false positive. Nó là sự đánh đổi bình thường, không phải bug. Filter
không được trả `False` cho value đã add miễn là các bit chưa bị xóa hoặc hỏng.

## 8. Công thức chọn kích thước

Gọi:

- `n` là số item dự kiến được thêm.
- `p` là false-positive rate mục tiêu.
- `m` là số bit.
- `k` là số vị trí hash trên mỗi item.

Công thức chuẩn:

```text
m = -n * ln(p) / (ln(2) ^ 2)
k = (m / n) * ln(2)
```

Cài đặt làm tròn `m` lên thành số bit nguyên và làm tròn `k` nhưng luôn có ít
nhất một vị trí hash. Với `n = 1000` và `p = 0.01`, kết quả xấp xỉ `9586` bit
và `7` vị trí hash.

False-positive rate gần đúng sau khi thêm `n` item là:

```text
p_actual ~= (1 - exp(-k * n / m)) ^ k
```

`estimated_false_positive_rate()` áp dụng công thức này cho số lần add để thấy
tác động của việc vượt mục tiêu kích thước.

## 9. Cấu hình `BloomFilter`

Constructor:

```python
bloom = BloomFilter[str](
    expected_items=100_000,
    false_positive_rate=0.01,
)
```

Nó kiểm tra số item dự kiến phải dương và rate mục tiêu phải nằm giữa zero và
one. Nó tính và lưu:

- `bit_count`: tổng số bit logic.
- `hash_count`: số vị trí set cho mỗi value.
- `byte_count`: kích thước storage đóng gói theo byte.

Các property này giúp quan sát sự đánh đổi bộ nhớ/độ chính xác thay vì giấu nó
trong các magic constant.

## 10. Không xóa từng value an toàn

Bloom filter chuẩn không thể cài đặt `remove(value)` an toàn. Nếu hai value dùng
chung một bit, xóa bit đó cho một value có thể khiến value còn lại bị coi là
không có, tạo ra false negative:

```text
x set bit 4
y cũng set bit 4
remove x -> xóa bit 4 làm hỏng y
```

Cài đặt cố ý cung cấp `clear()` để reset toàn filter nhưng không có xóa từng
value. Nếu cần delete, dùng counting Bloom filter với counter cho mỗi vị trí
hoặc xây dựng lại filter từ source data còn lại. Counting filter tốn bộ nhớ hơn
và vẫn cần xử lý cẩn thận các va chạm.

## 11. Độ phức tạp và bộ nhớ

Gọi `k` là số hash đã cấu hình:

| Thao tác | Thời gian | Dữ liệu lưu thêm |
|:---|:---:|:---|
| `add` | `O(k)` | Chỉ mảng bit đã cấu hình |
| `might_contain` | `O(k)` | Không lưu value |
| `clear` | `O(m / 8)` | Giữ nguyên kích thước |
| `estimated_false_positive_rate` | `O(1)` | Không quét value |

Với accuracy mục tiêu cố định, `k` là một hằng số nhỏ. Chi phí bộ nhớ chính là
mảng bit, không phải số lượng hay kích thước của value ban đầu.

## 12. API Python công khai

```python
bloom = BloomFilter[str](expected_items=1000, false_positive_rate=0.01)
bloom.add("/blocked")
bloom.add_many(["/admin", "/private"])

bloom.might_contain("/blocked")
"/private" in bloom

bloom.bit_count
bloom.hash_count
bloom.byte_count
bloom.insertions
bloom.estimated_false_positive_rate()
bloom.to_bytes()
```

`contains` và `__contains__` cố ý giữ nghĩa “có thể tồn tại”. Muốn có kết quả
chính xác cần kiểm tra nguồn thứ hai như hash set.

## 13. Ví dụ

Ví dụ thực thi lưu fingerprint của một số URL, kiểm tra một URL đã biết và một
URL chưa biết, rồi in số bit cùng rate ước lượng. Nó cũng tìm một false positive
có thể có để làm rõ hành vi xác suất khi gặp trường hợp đó.

Chạy bằng:

```text
python BloomFilter.py
```

Output cụ thể có thể thay đổi vì Python randomize hash giữa các process và vì
false positive là hiện tượng xác suất.

## 14. Ứng dụng thực tế và giới hạn riêng tư

Một số ứng dụng:

- Kiểm tra URL có thể nằm trong blacklist rất lớn hay không.
- Tránh đọc đĩa cho các file chắc chắn không chứa key.
- Lọc identifier trùng hoặc đã thấy trước một bước xử lý tốn kém.

Filter không giữ value ban đầu, giúp giảm lộ trực tiếp và giảm bộ nhớ. Nó không
phải ranh giới privacy hoặc security hoàn chỉnh: attacker vẫn có thể suy luận
qua query, và input hash vẫn tồn tại trong lúc thao tác. Hệ thống nhạy cảm nên
kết hợp filter với access control và bước xác thực chính xác.

## 15. Bloom Filter so với Hash Set

| Thuộc tính | Bloom filter | Hash set |
|:---|:---|:---|
| Lưu value ban đầu | Không | Có |
| False positive | Có thể xảy ra | Không |
| False negative sau add bình thường | Không | Không |
| Xóa từng value an toàn | Không với loại chuẩn | Có |
| Bộ nhớ | Mảng bit compact | Entry/object và table |
| Vai trò phù hợp | Pre-check nhanh | Nguồn membership chính xác |

Thiết kế production thường dùng cả hai: hỏi Bloom filter trước, rồi chỉ gọi
exact set hoặc database khi câu trả lời là positive.

## 16. Tài liệu tham khảo

- [Cài đặt Bloom Filter](https://labuladong.online/en/algo/data-structure-basic/bloom-filter/)
- [Khái niệm và cài đặt Hash Set](https://labuladong.online/en/algo/data-structure-basic/hash-set/)
- [Nguyên lý và cài đặt Bitmap](https://labuladong.online/en/algo/data-structure-basic/bitmap/)
