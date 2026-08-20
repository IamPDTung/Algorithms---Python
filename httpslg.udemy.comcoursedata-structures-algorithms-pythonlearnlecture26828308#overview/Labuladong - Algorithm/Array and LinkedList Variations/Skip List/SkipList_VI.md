
---

# Skip List

## 1. Skip List là gì?

**Skip list** là một cấu trúc linked list có thứ tự, được bổ sung các liên kết
forward. Tầng dưới cùng chứa mọi giá trị theo thứ tự tăng dần. Các tầng cao hơn
chứa một mẫu các giá trị và cho phép tìm kiếm bỏ qua nhiều node cùng lúc.

```text
    Level 3:  HEAD -------------------------------> 40 ----------> None
    Level 2:  HEAD -------------> 20 ------------> 40 ----------> None
    Level 1:  HEAD ------> 10 ---> 20 ---> 30 ---> 40 ---> 50 --> None
```

Cấu trúc này kết hợp:

* sự linh hoạt của linked list
* khả năng duyệt theo thứ tự
* search, insert và delete có độ phức tạp kỳ vọng `O(log n)`

Cài đặt trong `SkipList.py` lưu một ordered set gồm các giá trị có thể so sánh.
Nếu chèn trùng, phương thức trả về `False` và không tạo node mới.

---

## 2. Tại sao linked list cần các làn đường nhanh?

Một sorted linked list thông thường chỉ có một con trỏ next trong mỗi node:

```text
    HEAD -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> None
```

Tìm `50` buộc phải đi qua mọi node đứng trước nó. Search có độ phức tạp
`O(n)`.

Skip list thêm các liên kết nhảy xa hơn:

```text
    slow lane:  HEAD -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> None
    fast lane:  HEAD --------> 20 --------> 40 --------> 60 -> None
```

Search trước tiên di chuyển ở một tầng cao. Khi bước nhảy tiếp theo sẽ vượt qua
target, nó hạ xuống một tầng và tiếp tục. Cách này giống như đi tàu nhanh rồi
đổi sang tàu địa phương khi gần điểm đến.

---

## 3. Cấu tạo của Node

Khác với node của linked list thông thường, node của skip list sở hữu một mảng
các con trỏ forward.

```text
    node 30 với height 3:

    +------------------+
    | value = 30       |
    | forward[0] -----> node tiếp theo ở tầng dưới cùng
    | forward[1] -----> node tiếp theo ở level 1
    | forward[2] -----> node tiếp theo ở level 2
    +------------------+
```

**Height** của node là số con trỏ forward mà node sở hữu. Node có height `1`
chỉ xuất hiện ở tầng dưới cùng. Node có height `3` xuất hiện ở các level `0`,
`1` và `2`.

```text
    Height 1:  +-------+   chỉ có ở tầng dưới cùng
               |  10   |
               +-------+

    Height 3:  +-------+
               |  30   |   con trỏ level 2
               |       |   con trỏ level 1
               |       |   con trỏ level 0
               +-------+
```

List cũng có một node sentinel `head`. Sentinel không đại diện cho giá trị của
người dùng; nó tạo một điểm bắt đầu ổn định cho mọi level.

---

## 4. Height ngẫu nhiên và quy tắc xác suất

Khi chèn một giá trị, cài đặt tung một đồng xu ảo:

```text
    bắt đầu ở level 1
    trong khi random() < probability:
        đưa node lên level tiếp theo
```

Với `probability = 0.5`, trung bình khoảng một nửa số node lên level `1`, một
phần tư lên level `2`, v.v.:

```text
    số node kỳ vọng ở mỗi level:

    Level 3:  1/8 số node
    Level 2:  1/4 số node
    Level 1:  1/2 số node
    Level 0:  tất cả node
```

Các level không được cân bằng hoàn hảo; chúng được cân bằng theo xác suất. Vì
vậy độ phức tạp thông thường là **expected** `O(log n)`, không phải `O(log n)`
được đảm bảo tuyệt đối.

Constructor nhận `seed` để ví dụ và test có thể tạo ra các level lặp lại được:

```python
skip_list = SkipList[int](max_level=5, probability=0.5, seed=7)
```

Không dùng generator có seed cho randomness liên quan đến bảo mật. Seed chỉ có
mục đích làm ví dụ cấu trúc dữ liệu này có thể tái hiện.

---

## 5. Search từ trên xuống

Để tìm `37`, bắt đầu ở level đang hoạt động cao nhất:

```text
    Level 2:  HEAD ----------------------> 30 -----------------> 50
                                                ^
                                                | 50 quá lớn
                                                | hạ xuống
    Level 1:  HEAD ------> 10 -------> 30 --> 40 --> 50
                                                ^
                                                | 40 quá lớn
                                                | hạ xuống
    Level 0:  HEAD -> 10 -> 20 -> 30 -> 35 -> 40
                                       ^
                                       vùng ứng viên cho 37
```

Ở mỗi level:

1. Nhìn vào node tiếp theo.
2. Nếu giá trị của nó nhỏ hơn target, di chuyển tới đó.
3. Nếu không, hạ xuống một level.
4. Ở level `0`, kiểm tra node tiếp theo có bằng target không.

Thuật toán không bao giờ đi lùi. Mảng `update` ghi lại node cuối cùng đã đi qua
ở mỗi level; thông tin này cần cho insert và delete.

---

## 6. Bảng predecessor

Khi insert hoặc delete, search lưu các node predecessor:

```text
    target = 35

    update[2] = 30   -> node cuối cùng trước 35 ở level 2
    update[1] = 30   -> node cuối cùng trước 35 ở level 1
    update[0] = 30   -> node cuối cùng trước 35 ở level 0
```

Nếu node mới có height `2`, nó được nối sau `update[0]` và `update[1]`. Nếu một
node bị xóa, mỗi forward pointer tương ứng sẽ bỏ qua node đó.

```text
    trước insert(35):
    30 -------------------------------> 40
    30 ---------> 35? no -------------> 40

    sau insert(35), height 2:
    level 1: 30 -----------------------> 35 ----------> 40
    level 0: 30 ---------> 35 ---------> 40
```

Các pointer ở những level cao hơn height của node mới không thay đổi.

---

## 7. Các bước Insert

`insert(value)` thực hiện chuỗi bước sau:

```text
    1. Đi từ level đang hoạt động cao nhất xuống level 0.
    2. Lưu predecessor của mỗi level vào update[].
    3. Từ chối nếu candidate ở level 0 bằng value.
    4. Sinh height ngẫu nhiên cho node mới.
    5. Nối node mới vào mọi level mà nó đạt tới.
```

Nối pointer ở một level trông như sau:

```text
    TRƯỚC:

    previous ----------------------> next

    SAU:

    previous -------------> new -------------> next
```

Thứ tự gán rất quan trọng. Hãy lưu pointer `next` cũ trước khi thay thế
`previous.forward[level]`, nếu không phần còn lại của list có thể bị tách rời.

---

## 8. Các bước Delete

Để xóa `30`, trước tiên thu thập các predecessor:

```text
    TRƯỚC:

    Level 2: HEAD -----------------> 30 -----------------> 50
    Level 1: HEAD --------> 20 ----> 30 --------> 40 ----> 50
    Level 0: HEAD -> 10 -> 20 -> 30 -> 40 -> 50

    SAU:

    Level 2: HEAD ---------------------------------------> 50
    Level 1: HEAD --------> 20 ----------------> 40 ----> 50
    Level 0: HEAD -> 10 -> 20 -> 40 -> 50
```

Chỉ các level chứa node bị xóa mới được nối lại. Sau đó, các top level rỗng
được loại khỏi height đang hoạt động của list.

---

## 9. Interface của cài đặt

Toàn bộ cài đặt nằm trong `SkipList.py`:

```python
skip_list = SkipList[int](max_level=16, probability=0.5)

skip_list.insert(30)       # True nếu set thay đổi
skip_list.search(30)       # 30 hoặc None
skip_list.contains(30)     # True hoặc False
skip_list.delete(30)       # True nếu một node bị xóa
skip_list.to_list()        # các giá trị ở bottom level theo thứ tự
skip_list.levels()         # các giá trị ở mọi level đang hoạt động
```

Các giá trị phải hỗ trợ phép so sánh `<` và `==`. Cài đặt từ chối `None` vì
sentinel dùng `None` bên trong, còn giá trị thông thường cần có thể so sánh.

---

## 10. Độ phức tạp

| Thao tác | Kỳ vọng | Trường hợp xấu nhất | Lý do |
|:---|:---:|:---:|:---|
| Search | `O(log n)` | `O(n)` | Các level ngẫu nhiên có thể không thuận lợi |
| Insert | `O(log n)` | `O(n)` | Search cộng với nối pointer |
| Delete | `O(log n)` | `O(n)` | Search cộng với nối lại pointer |
| Duyệt có thứ tự | `O(n)` | `O(n)` | Đi theo level `0` |
| Bộ nhớ phụ | `O(n)` kỳ vọng | Giới hạn `O(n * max_level)` | Các forward pointer |

Bộ nhớ kỳ vọng là `O(n)` vì xác suất node lên level tiếp theo giảm theo cấp số
nhân. Balanced tree xác định cho bảo đảm trường hợp xấu nhất mạnh hơn; skip
list hấp dẫn khi muốn logic pointer đơn giản, duyệt có thứ tự và cài đặt dễ
hiểu.

---

## 11. Skip List so với các cấu trúc khác

| Cấu trúc | Search | Insert | Delete | Duyệt có thứ tự |
|:---|:---:|:---:|:---:|:---:|
| Linked list không sắp xếp | `O(n)` | `O(1)` tại vị trí đã biết | `O(n)` để tìm | `O(n)` |
| Linked list đã sắp xếp | `O(n)` | `O(n)` để tìm | `O(n)` để tìm | `O(n)` |
| Skip list, kỳ vọng | `O(log n)` | `O(log n)` | `O(log n)` | `O(n)` |
| Balanced search tree | `O(log n)` | `O(log n)` | `O(log n)` | `O(n)` |
| Hash table | `O(1)` trung bình | `O(1)` trung bình | `O(1)` trung bình | Không tự nhiên có thứ tự |

Skip list thường được dùng cho ordered index, database trong bộ nhớ và các hệ
thống chấp nhận một lựa chọn xác suất thay cho balanced tree.

---

## 12. Các lỗi thường gặp

### Lỗi 1: Chỉ search ở level `0`

Đó chỉ là sorted linked list và làm mất lợi thế tốc độ của skip list. Hãy search
từ level cao nhất đang hoạt động rồi hạ xuống khi bước nhảy tiếp theo quá lớn.

### Lỗi 2: Chỉ cập nhật một forward pointer

Node có height `3` phải được nối ở các level `0`, `1` và `2`. Bỏ sót một level
sẽ làm làn đường nhanh đó không nhất quán.

### Lỗi 3: Quên bảng predecessor

Delete cần node đứng trước target ở mọi level. Chỉ tìm được target là chưa đủ để
nối lại các forward pointer đơn hướng.

### Lỗi 4: Xem expected complexity như bảo đảm tuyệt đối

Các level ngẫu nhiên thường làm cấu trúc cân bằng, nhưng một chuỗi không may có
thể suy giảm về gần `O(n)`. Cài đặt này phục vụ học tập và không hứa hẹn cân bằng
xác định.

### Lỗi 5: Cho phép các giá trị không thể so sánh

Search dùng `<` để so sánh. Trộn string với integer hoặc chèn `None` sẽ gây lỗi
ordering.

---

## 13. Trực quan hóa các level

`levels()` trả về các giá trị ở mỗi level đang hoạt động, từ cao nhất xuống:

```text
    kết quả levels():

    [ [30], [10, 30, 50], [10, 20, 30, 40, 50] ]
      ^       ^                  ^
      |       |                  bottom level
      |       middle level
      highest active level
```

Hình dạng chính xác phụ thuộc vào random generator. Bottom list luôn được sắp
xếp và luôn chứa mọi giá trị đã insert.

---

## 14. Chạy ví dụ

Chạy:

```text
python SkipList.py
```

Output ổn định kỳ vọng cho ví dụ có seed:

```text
Ordered values: [10, 30, 40, 50]
Contains 40: True
Contains 25: False
Levels: [[30, 50], [10, 30, 40, 50], [10, 30, 40, 50]]
```

Dòng `Levels` chính xác phụ thuộc vào cách triển khai random và phiên bản
Python. Invariant quan trọng là mọi level đều được sắp xếp và bottom level chứa
`[10, 30, 40, 50]` sau khi xóa.

---

## 15. Cheat Sheet cuối cùng

```text
    1. Level 0 chứa mọi giá trị theo thứ tự tăng dần.
    2. Các level cao hơn là làn đường nhanh từ những node được lấy mẫu.
    3. Search từ level cao nhất rồi hạ xuống khi cần.
    4. Giữ update[level] cho insert và delete.
    5. Height của node quyết định node tham gia những level nào.
    6. Cài đặt này từ chối giá trị trùng.
    7. Search, insert và delete có expected O(log n).
    8. Trường hợp xấu nhất vẫn có thể là O(n).
    9. Các giá trị phải có thể so sánh với nhau.
```

**Bước tiếp theo:** Vẽ bảng predecessor cho một lần insert, sau đó tự nối lại
một node ở hai level khác nhau trước khi chạy `SkipList.py`.
