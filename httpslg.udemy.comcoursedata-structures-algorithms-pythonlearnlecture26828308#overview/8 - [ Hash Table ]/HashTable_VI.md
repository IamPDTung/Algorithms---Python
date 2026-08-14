
---

# Bảng băm (Hash Table)

## 1. Bảng băm là gì?

**Bảng băm (Hash Table)** là một **kho lưu trữ khóa/giá trị (key/value store)**. Bạn đưa vào một **khóa (key)**, chẳng hạn như một từ hoặc một tên, và nhận lại **giá trị (value)** tương ứng với tốc độ cực nhanh.

Thành phần kỳ diệu là **hàm băm (hash function)**: nó nhận khóa và chuyển khóa thành một **địa chỉ (address, hay chỉ số/index)** trong một mảng nền. Cặp khóa/giá trị sau đó được lưu tại địa chỉ đó.

```
    KHÓA                    HÀM BĂM                    ĐỊA CHỈ

    "bolts"     --->   [  __hash("bolts")  ]   --->       4
    "washers"   --->   [  __hash("washers")]   --->       4   (đụng độ!)
    "lumber"    --->   [  __hash("lumber") ]   --->       6

    MẢNG NỀN (data_map, kích thước 7):

    Chỉ số:   0        1        2        3        4          5        6
             +-------+-------+-------+-------+----------+-------+----------+
             | rỗng  | rỗng  | rỗng  | rỗng  | bolts    | rỗng  | lumber   |
             |       |       |       |       | washers  |       |          |
             +-------+-------+-------+-------+----------+-------+----------+
```

### Ý tưởng cốt lõi:
> Mảng nhanh **khi truy cập bằng chỉ số** (`O(1)`). Bảng băm chuyển mọi **khóa** thành một **chỉ số**, vì vậy tra cứu bằng khóa cũng nhanh như truy cập bằng chỉ số.

---

## 2. Hàm băm (Hash Function)

Hàm băm của khóa học (từ `SOLUTION-HT-Constructor.py`) lặp qua từng chữ cái của khóa, trộn `ord(letter) * 23`, rồi giữ kết quả trong mảng bằng phép modulo `%`:

```python
    def __hash(self, key):
        my_hash = 0
        for letter in key:
            my_hash = (my_hash + ord(letter) * 23) % len(self.data_map)
        return my_hash  
```

### Đặc điểm của một hàm băm tốt:

```
    +---------------------------------------------------------------+
    |                 ĐẶC ĐIỂM CỦA HÀM BĂM                        |
    +---------------------------------------------------------------+
    |  1. XÁC ĐỊNH:                                                 |
    |     cùng một khóa ==> cùng một địa chỉ, MỌI lần              |
    |     hash("bolts") là 4 hôm nay, ngày mai, luôn luôn         |
    |                                                               |
    |  2. PHÂN BỐ ĐỀU:                                              |
    |     các khóa được trải ra trên mọi địa chỉ                    |
    |     (ít đụng độ => tra cứu nhanh)                             |
    |                                                               |
    |  3. MỘT CHIỀU:                                                |
    |     khóa -> địa chỉ là dễ                                     |
    |     địa chỉ -> khóa ban đầu gần như không thể                 |
    +---------------------------------------------------------------+
```

### Truy vết - băm từng bước cho `"bolts"` (kích thước = 7):

```
    my_hash bắt đầu bằng 0. Với mỗi chữ cái: my_hash = (my_hash + ord(letter)*23) % 7

    'b':  (0 + 98*23)  % 7 = 2254 % 7 = 0
    'o':  (0 + 111*23) % 7 = 2553 % 7 = 5
    'l':  (5 + 108*23) % 7 = 2489 % 7 = 4
    't':  (4 + 116*23) % 7 = 2672 % 7 = 5
    's':  (5 + 115*23) % 7 = 2650 % 7 = 4

    ĐỊA CHỈ CUỐI CÙNG của "bolts"  ==>  4
```

---

## 3. Vì sao bảng băm được tạo ra?

Một **mảng/danh sách (array/list)** có hai đặc điểm trái ngược:

* Truy cập **THEO CHỈ SỐ** là tức thời - `my_list[4]` có độ phức tạp `O(1)`.
* Tìm kiếm **THEO GIÁ TRỊ** chậm - để biết "82 có trong danh sách không?" phải kiểm tra từng phần tử: `O(n)`.

```
    DANH SÁCH - truy cập bằng chỉ số:       DANH SÁCH - tìm giá trị (82?):

    +----+----+----+----+                   +----+----+----+----+
    | 21 | 47 | 76 | 82 |                   | 21 | 47 | 76 | 82 |
    +----+----+----+----+                   +----+----+----+----+
              ^                              x    x    x    x
              |                              kiểm tra cả 4 => O(n)
    my_list[3] => O(1), tức thời

    BẢNG BĂM - tra cứu theo KHÓA "washers":

    "washers" --> băm --> 4 --> nhảy thẳng đến chỉ số 4 => O(1) trung bình
```

### Nhận xét then chốt về bảng băm:
> **Băm khóa để lấy chỉ số, sau đó dùng truy cập chỉ số `O(1)` của mảng.** Trung bình, tra cứu, chèn và xóa theo khóa đều trở thành `~O(1)` - không cần quét toàn bộ.

---

## 4. Bảng băm giải quyết những bài toán nào?

Bảng băm xuất hiện ở mọi nơi ta cần **ghi nhớ theo tên** và lấy lại ngay lập tức:

```
    +----------------------------------------------------------+
    |                 NƠI DÙNG BẢNG BĂM                       |
    +----------------------------------------------------------+
    |  * Từ điển / map (Python dict LÀ một bảng băm)           |
    |  * Bộ nhớ đệm (URL -> trang đã kết xuất)                 |
    |  * Đếm tần suất (đếm từ, kiểm phiếu)                      |
    |  * Phát hiện trùng lặp (giá trị này đã thấy chưa?)        |
    |  * Lập chỉ mục dòng cơ sở dữ liệu theo ID                 |
    +----------------------------------------------------------+
```

### Các bài phỏng vấn kinh điển (xem thư mục `Interview`):

| Bài toán | Tệp | Ý tưởng cốt lõi |
|:---|:---|:---|
| **Two Sum** | `HT-Two Sum.py` | Lưu các giá trị bù, tìm cặp trong một lượt duyệt |
| **Group Anagrams** | `HT-Group Anagrams.py` | Dùng từ đã sắp xếp làm khóa, danh sách anagram làm giá trị |
| **First Non-Repeating Character** | `HT-First Non-Repeating Character.py` | Đếm tần suất ký tự, trả về ký tự đầu tiên có số đếm bằng 1 |
| **Find Duplicates** | `HT-Find Duplicates.py` | Dùng giá trị làm khóa; đã thấy trước đó thì là trùng lặp |
| **Subarray Sum** | `HT-Subarray Sum.py` | Lưu tổng tiền tố để tìm đoạn có tổng mục tiêu |
| **Item In Common** | `HT-ItemInCommon1.py` / `HT-ItemInCommon2.py` | Vòng lặp lồng nhau so với bảng băm |

### Đối chiếu kinh điển - Item In Common:

```
    VÒNG LẶP LỒNG O(n^2) (ItemInCommon1):    BẢNG BĂM O(n) (ItemInCommon2):

    list1 = [1, 3, 5]                         đưa list1 vào bảng băm:
    list2 = [2, 4, 5]                         {1:T, 3:T, 5:T}

    for i in list1:                           for j in list2:
        for j in list2:                           if j in table: return True
            if i == j: ...                    một lượt, tra cứu O(1) => O(n)

    mỗi i gặp mọi j
    => 3 x 3 = 9 phép so sánh => O(n^2)
```

---

## 5. Đụng độ (Collision) và phương pháp nối chuỗi (Chaining)

Một **đụng độ (collision)** xảy ra khi **hai khóa khác nhau băm đến cùng một địa chỉ**. Điều này không thể tránh - có vô hạn khóa khả dĩ nhưng chỉ có 7 địa chỉ.

```
    ĐỤNG ĐỘ: "bolts" và "washers" ĐỀU băm đến địa chỉ 4

    "bolts"   ---> [băm] ---+
                             +--->  4  ???
    "washers" ---> [băm] ---+
```

### Giải pháp 1 - Chaining (cách khóa học dùng):

Mỗi địa chỉ chứa một **danh sách (chain)** các cặp `[key, value]`. Những cặp bị đụng độ chỉ cần được **nối thêm** vào cùng chuỗi:

```
    Chuỗi tại chỉ số 4 sau khi chèn "bolts" rồi "washers":

    4 :  [ ['bolts', 1400], ['washers', 50] ]
           \_______________/  \________________/
              cặp đầu tiên       nối thêm sau đụng độ
```

### Giải pháp 2 - Open Addressing (địa chỉ mở, phương án thay thế):

Nếu địa chỉ đã bị chiếm, ta **thăm dò (probe)** ô trống tiếp theo ngay trong mảng (linear probing, quadratic probing, ...):

```
    "washers" muốn địa chỉ 4, nhưng địa chỉ đã bị chiếm:

    Chỉ số:   4          5          6
             +---------+---------+---------+
             | bolts   | washers |         |   <- washers chuyển đến ô trống kế tiếp
             +---------+---------+---------+
```

| Chiến lược | Ý tưởng | Được dùng bởi |
|:---|:---|:---|
| **Chaining** | Mỗi địa chỉ lưu một danh sách các cặp | Khóa học này |
| **Open Addressing** | Tìm địa chỉ trống tiếp theo | Nhiều `dict` dựng sẵn |

---

## 6. Cách hoạt động - Constructor và `set_item`

### Constructor (từ `SOLUTION-HT-Constructor.py`):

Bộ nhớ nền là một list đơn giản có kích thước 7, mọi ô ban đầu là `None`:

```python
class HashTable:
    def __init__(self, size = 7):
        self.data_map = [None] * size
```

```
    data_map ngay sau khi khởi tạo:

    Chỉ số:   0      1      2      3      4      5      6
             +------+------+------+------+------+------+------+
             | None | None | None | None | None | None | None |
             +------+------+------+------+------+------+------+
```

### Phương thức `set_item` (từ `SOLUTION-HT-Set.py`):

```python
    def set_item(self, key, value):
        index = self.__hash(key)
        if self.data_map[index] == None:
            self.data_map[index] = []
        self.data_map[index].append([key, value])
```

### Truy vết từng bước - `set_item('bolts', 1400)`, rồi `'washers'`, rồi `'lumber'`:

```
    BƯỚC 1: set_item('bolts', 1400)
    hash('bolts') = 4 -> ô 4 là None -> tạo [] -> nối ['bolts', 1400]

    4 :  [ ['bolts', 1400] ]

    BƯỚC 2: set_item('washers', 50)          <== ĐỤNG ĐỘ tại địa chỉ 4!
    hash('washers') = 4 -> ô 4 đã tồn tại -> nối ['washers', 50]

    4 :  [ ['bolts', 1400], ['washers', 50] ]

    BƯỚC 3: set_item('lumber', 70)
    hash('lumber') = 6 -> ô 6 là None -> tạo [] -> nối ['lumber', 70]

    6 :  [ ['lumber', 70] ]

    TRẠNG THÁI CUỐI (khớp với kết quả của print_table()):

    0 :  None
    1 :  None
    2 :  None
    3 :  None
    4 :  [['bolts', 1400], ['washers', 50]]
    5 :  None
    6 :  [['lumber', 70]]
```

---

## 7. Cách hoạt động - `get_item`

### Phương thức `get_item` (từ `SOLUTION-HT-Get.py`):

```python
    def get_item(self, key):
        index = self.__hash(key)
        if self.data_map[index] is not None:
            for i in range(len(self.data_map[index])):
                if self.data_map[index][i][0] == key:
                    return self.data_map[index][i][1]
        return None
```

### Truy vết - `get_item('washers')` (TÌM THẤY trong một chain):

```
    hash('washers') = 4  -> nhảy đến địa chỉ 4

    Chuỗi tại 4:  [ ['bolts', 1400], ['washers', 50] ]
                         ^                 ^
                      i = 0:            i = 1:
                   'bolts' !=        'washers' ==
                   'washers'         'washers' -> trả về 50
```

### Truy vết - `get_item('lumber')` khi lumber chưa từng được chèn (KHÔNG TÌM THẤY):

```
    hash('lumber') = 6  -> địa chỉ 6 là None -> trả về None

    OUTPUT:   Bolts: 1400     Washers: 50     Lumber: None
```

---

## 8. Cách hoạt động - `keys`

### Phương thức `keys` (từ `SOLUTION-HT-Keys.py`):

Duyệt **mọi địa chỉ**; tại nơi có chain, duyệt **mọi cặp** trong chain và lấy key (phần tử `[0]` của mỗi cặp):

```python
    def keys(self):
        all_keys = []
        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for j in range(len(self.data_map[i])):
                    all_keys.append(self.data_map[i][j][0])
        return all_keys
```

### Truy vết - thu thập toàn bộ khóa:

```
    i = 0..3:  None          -> bỏ qua
    i = 4:     chain có 2    -> nối 'bolts', nối 'washers'
    i = 5:     None          -> bỏ qua
    i = 6:     chain có 1    -> nối 'lumber'

    all_keys = ['bolts', 'washers', 'lumber']
```

---

## 9. Phân tích Big O

### Trường hợp trung bình và xấu nhất:

```
    TRƯỜNG HỢP TRUNG BÌNH (hàm băm tốt):        TRƯỜNG HỢP XẤU NHẤT (mọi khóa đụng độ):

    khóa trải trên cả 7 địa chỉ                mọi khóa rơi vào địa chỉ 0

    0 : [k1]                                   0 : [k1,k2,k3,k4,k5,k6,k7]
    1 : [k2]                                   1 : None
    2 : [k3]                                   2 : None
    ...                                        ...
    6 : [k7]                                   6 : None

    độ dài chain ~ 1 => O(1) mỗi lần tra cứu    độ dài chain = n => O(n) mỗi lần tra cứu
    (một lần băm + nhảy thẳng đến đó)          (băm + duyệt một linked list!)
```

### Bảng Big O:

| Thao tác | Trung bình | Xấu nhất (mọi khóa đụng độ) |
|:---|:---|:---|
| **`set_item`** | `O(1)` | `O(n)` |
| **`get_item`** | `O(1)` | `O(n)` |
| **`keys`** | `O(n)` - phải thăm mọi cặp | `O(n)` |
| **Không gian** | `O(n)` | `O(n)` |

> **Giả định:** `O(1)` trung bình hoàn toàn phụ thuộc vào một **hàm băm tốt** phân bố khóa đều. Phép modulo theo kích thước bảng (cộng với một hệ số nguyên tố như 23) giúp các chain ngắn.

### Bảng băm so với danh sách:

| Thao tác | List (Mảng) | Hash Table (Trung bình) |
|:---|:---|:---|
| **Truy cập bằng chỉ số** | `O(1)` | - (khóa thay cho chỉ số) |
| **Tìm theo giá trị/khóa** | `O(n)` | **`O(1)`** |
| **Chèn** | `O(1)` ở cuối | **`O(1)`** |
| **Xóa theo giá trị/khóa** | `O(n)` | **`O(1)`** |
| **Giữ thứ tự chèn?** | Có | Không (thứ tự theo địa chỉ) |

```
    SỰ ĐÁNH ĐỔI:

    List:       nhanh theo CHỈ SỐ, chậm khi TÌM THEO GIÁ TRỊ
    Hash Table: nhanh theo KHÓA, nhưng khóa phải hashable
                            và một hàm băm kém
                            sẽ làm nó suy giảm về O(n)
```

---

**Bước tiếp theo:** Hãy luyện tập các bài phỏng vấn trong thư mục `Interview` - Two Sum, Group Anagrams, First Non-Repeating Character, Find Duplicates, Subarray Sum, và Item In Common!
