
---

# Sắp xếp trộn (Merge Sort)

## 1. Sắp xếp trộn là gì?

**Sắp xếp trộn (Merge Sort)** là một thuật toán sắp xếp **chia để trị (Divide and Conquer)**. Nó xử lý bài toán sắp xếp qua hai giai đoạn:

1. **CHIA (DIVIDE)** — đệ quy chia danh sách thành **hai nửa** cho đến khi chỉ còn các danh sách có **một phần tử** (danh sách một phần tử đã được sắp xếp một cách hiển nhiên).
2. **CHINH PHỤC / TRỘN (CONQUER / MERGE)** — lần lượt **trộn** các nửa đã sắp xếp lại với nhau ở từng mức, cho đến khi xây dựng lại toàn bộ danh sách theo thứ tự.

Sắp xếp trộn thực sự gồm **hai phần** phối hợp:

* `merge(list1, list2)` — hàm trợ giúp (helper) kết hợp **hai danh sách đã được sắp xếp** thành **một danh sách đã sắp xếp**.
* `merge_sort(my_list)` — hàm chia đệ quy, phá danh sách thành các phần nhỏ, sau đó gọi `merge()` khi quay ngược lên trong ngăn xếp gọi hàm.

### Ý tưởng cốt lõi:
> "Một danh sách có một phần tử vốn đã được sắp xếp."
> — Sắp xếp trộn chia cho đến khi việc sắp xếp trở nên tầm thường, rồi thực hiện toàn bộ công việc thật sự trong lúc **trộn** khi quay lên.

```
        +--------------------------------------------------+
        |                  SẮP XẾP TRỘN                   |
        +--------------------------------------------------+
        |                                                  |
        |   Giai đoạn 1             Giai đoạn 2            |
        |   +------------------+   +------------------+  |
        |   |       CHIA        |   |       TRỘN        |  |
        |   |  chia đôi đệ quy  | + | kết hợp các nửa   |  |
        |   |                  |   | đã sắp xếp       |  |
        |   +------------------+   +------------------+  |
        |                                                  |
        |   Hai hàm:                                       |
        |   +------------------+     +------------------+  |
        |   |   merge_sort()   | --> |     merge()      |  |
        |   | (bộ phận chia)   |     | (bộ phận trộn)   |  |
        |   +------------------+     +------------------+  |
        +--------------------------------------------------+
```

---

## 2. Vì sao Sắp xếp trộn được tạo ra?

Các **thuật toán sắp xếp cơ bản (basic sorts)** (Bubble Sort, Selection Sort, Insertion Sort) đều có cùng một giới hạn: thời gian **`O(n^2)`**. Chúng so sánh các phần tử **từng cặp**, vì vậy khi tăng gấp đôi dữ liệu thì công việc tăng **gấp bốn**. Với các tập dữ liệu lớn, cách này đơn giản là quá chậm.

Sắp xếp trộn được tạo ra để vượt qua giới hạn đó. Nó cung cấp:

* Thời gian **`O(n log n)` được đảm bảo** — trong cả trường hợp **tốt nhất, trung bình VÀ xấu nhất**. Không có bất ngờ xấu.
* **Tính ổn định (stability)** — các phần tử bằng nhau giữ nguyên thứ tự tương đối ban đầu (Bubble/Insertion cũng ổn định, còn Selection thì không).

### Cái giá phải trả:
> Sắp xếp trộn **đổi KHÔNG GIAN lấy TỐC ĐỘ**. Nó không sắp xếp tại chỗ — cần các **mảng phụ (auxiliary arrays)** để chứa kết quả đã trộn: **`O(n)` không gian bổ sung**.

```
        n = 1,000,000 phần tử:

        +------------------+----------------------------------+
        | Sắp xếp cơ bản   |   O(n^2) = 1,000,000,000,000     |
        | (Bubble/Sel/Ins) |   ~ 1 NGHÌN TỶ phép toán         |
        +------------------+----------------------------------+
        | Sắp xếp trộn      |   O(n log n) = 1,000,000 x 20    |
        |                  |   ~ 20 TRIỆU phép toán           |
        +------------------+----------------------------------+

        Đó xấp xỉ là tốc độ nhanh hơn 50.000 lần. Bước nhảy O(n^2) -> O(n log n)
        là một trong những bước tiến quan trọng nhất của DSA.
```

---

## 3. Nó giải quyết những vấn đề nào?

* **Tập dữ liệu lớn cần tốc độ được đảm bảo** — khi không thể mạo hiểm với trường hợp xấu `O(n^2)` của Sắp xếp nhanh (Quick Sort), bảo đảm `O(n log n)` trong MỌI trường hợp của Sắp xếp trộn là lựa chọn thắng thế.
* **Sắp xếp danh sách liên kết (Linked Lists)** — việc trộn hai danh sách liên kết đã sắp xếp chỉ cần nối lại các con trỏ, vì vậy Sắp xếp trộn chỉ cần **`O(1)` không gian bổ sung** trong trường hợp này (xem bài tập phỏng vấn *"Merge Two Sorted LL"*). Đây là lựa chọn hàng đầu cho danh sách liên kết.
* **Sắp xếp ngoài (External Sorting)** — dữ liệu quá lớn để nằm trong bộ nhớ có thể được sắp xếp theo từng phần từ đĩa: sắp xếp từng phần, sau đó trộn các phần. Bước trộn của Sắp xếp trộn được thiết kế chính xác cho việc này.
* **Yêu cầu sắp xếp ổn định** — ví dụ sắp xếp bản ghi theo khóa phụ trong khi vẫn giữ thứ tự theo khóa chính của các bản ghi bằng nhau.

```
        +---------------------+----------------------------+
        |    TÌNH HUỐNG       |   VÌ SAO PHÙ HỢP            |
        +---------------------+----------------------------+
        | Tập dữ liệu rất lớn | Bảo đảm O(n log n)         |
        +---------------------+----------------------------+
        | Danh sách liên kết  | O(1) không gian bổ sung    |
        +---------------------+----------------------------+
        | Dữ liệu trên đĩa    | Bước trộn = I/O tuần tự    |
        +---------------------+----------------------------+
        | Phải ổn định        | Phần tử bằng nhau giữ thứ |
        |                     | tự                         |
        +---------------------+----------------------------+
```

---

## 4. Cách hoạt động — Phần 1: Bước Trộn (Merge Step)

Trước khi hiểu đệ quy, trước hết phải nắm vững **`merge()`** — trái tim của thuật toán.

`merge()` nhận **hai danh sách đã sắp xếp** và tạo ra **một danh sách đã kết hợp, được sắp xếp**. Nó sử dụng **hai con trỏ chỉ mục (index pointers)**, `i` và `j`, mỗi con trỏ tương ứng với một danh sách:

1. So sánh **hai phần tử đầu**: `list1[i]` với `list2[j]`.
2. Thêm phần tử **nhỏ hơn** vào `combined` và tăng con trỏ của danh sách đó.
3. Lặp lại cho đến khi một danh sách cạn.
4. **Xả các phần tử còn lại (drain the leftovers)** của danh sách kia (chúng đã được sắp xếp và đều lớn hơn).

### Truy vết đầy đủ — `merge([1, 3, 7, 8], [2, 4, 5, 6])`:

```
    list1 = [ 1, 3, 7, 8 ]      list2 = [ 2, 4, 5, 6 ]
              i                          j

    So sánh hai phần tử đầu, lấy phần tử NHỎ HƠN, tăng con trỏ tương ứng.
```

### Bảng từng bước:

```
    +------+-----+-----+----------+----------+---------------+-------------------------+
    | Bước |  i  |  j  | list1[i] | list2[j] |    Hành động  |        combined         |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  1   |  0  |  0  |    1     |    2     | lấy 1 (list1) | [ 1 ]                   |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  2   |  1  |  0  |    3     |    2     | lấy 2 (list2) | [ 1, 2 ]                |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  3   |  1  |  1  |    3     |    4     | lấy 3 (list1) | [ 1, 2, 3 ]             |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  4   |  2  |  1  |    7     |    4     | lấy 4 (list2) | [ 1, 2, 3, 4 ]          |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  5   |  2  |  2  |    7     |    5     | lấy 5 (list2) | [ 1, 2, 3, 4, 5 ]       |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  6   |  2  |  3  |    7     |    6     | lấy 6 (list2) | [ 1, 2, 3, 4, 5, 6 ]    |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    | list2 cạn (j = 4) -> vòng lặp chính kết thúc, XẢ phần còn lại của list1:       |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  7   |  2  |  4  |    7     |    -     | xả 7 (list1)  | [ 1, 2, 3, 4, 5, 6, 7 ] |
    +------+-----+-----+----------+----------+---------------+-------------------------+
    |  8   |  3  |  4  |    8     |    -     | xả 8 (list1)  | [ 1,2,3,4,5,6,7,8 ]     |
    +------+-----+-----+----------+----------+---------------+-------------------------+

    KẾT QUẢ TRẢ VỀ: [ 1, 2, 3, 4, 5, 6, 7, 8 ]
```

### Vì sao việc xả phần còn lại hoạt động?

```
    Khi một danh sách cạn, MỌI phần tử còn lại trong danh sách kia
    chắc chắn:

        (a) đã được sắp xếp bên trong, và
        (b) >= mọi phần tử đã có trong combined

    list1 = [ 1, 3, 7, 8 ]      list2 = [ 2, 4, 5, 6 ]
                   ^   ^                             ^
                   +---+                             +-- đã cạn
                   phần còn lại: 7, 8 -> chỉ cần nối chúng theo thứ tự!
```

---

## 5. Mã Trộn (Merge Code)

```python
def merge(list1, list2):
    combined = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            combined.append(list1[i])
            i += 1
        else:
            combined.append(list2[j])
            j += 1
    
    while i < len(list1):
        combined.append(list1[i])
        i += 1

    while j < len(list2):
        combined.append(list2[j])
        j += 1

    return combined
```

### Đối chiếu từng dòng với truy vết:

```
    while i < len(list1) and j < len(list2):   <- bước 1-6 (cả hai danh sách còn phần tử)
        if list1[i] < list2[j]:                <- so sánh hai phần tử đầu
            combined.append(list1[i]); i += 1  <- lấy từ list1, tăng i
        else:
            combined.append(list2[j]); j += 1  <- lấy từ list2, tăng j

    while i < len(list1): ...                  <- bước 7-8: xả phần còn lại của list1
    while j < len(list2): ...                  <- (bỏ qua ở đây: list2 đã rỗng)
```

### Lưu ý — Merge YÊU CẦU hai danh sách đã sắp xếp:

```python
# MERGE REQUIRES TWO SORTED LISTS:
print(merge([1,2,7,8], [3,4,5,6]))
# EXPECTED OUTPUT: [1, 2, 3, 4, 5, 6, 7, 8]
```

> Nếu một trong hai danh sách đầu vào chưa được sắp xếp, kỹ thuật hai con trỏ sẽ hỏng. Đó chính là lý do `merge_sort()` chia đến tận các danh sách **một phần tử** — những danh sách duy nhất được bảo đảm là đã sắp xếp.

---

## 6. Cách hoạt động — Phần 2: Đệ quy Sắp xếp trộn

Bây giờ là toàn bộ thuật toán. `merge_sort()` chỉ làm ba việc:

1. **Trường hợp cơ sở (base case):** nếu `len(my_list) == 1`, trả về nó — một phần tử đã được sắp xếp.
2. **Chia:** tìm điểm giữa, đệ quy sắp xếp **nửa trái** và **nửa phải**.
3. **Kết hợp:** `return merge(left, right)`.

### Cây đệ quy đầy đủ — `merge_sort([8, 3, 5, 4, 7, 6, 1, 2])`:

```
    ============================ CHIA (đi XUỐNG) ================================

                            [ 8, 3, 5, 4, 7, 6, 1, 2 ]
                            /                          \
                    [ 8, 3, 5, 4 ]                [ 7, 6, 1, 2 ]
                    /            \                /            \
               [ 8, 3 ]      [ 5, 4 ]        [ 7, 6 ]      [ 1, 2 ]
               /     \       /     \         /     \       /     \
             [ 8 ] [ 3 ]   [ 5 ] [ 4 ]     [ 7 ] [ 6 ]   [ 1 ] [ 2 ]

              ^                                                      ^
              +---------- danh sách một phần tử = TRƯỜNG HỢP CƠ SỞ ----------+
                        (mỗi danh sách hiển nhiên đã được sắp xếp!)

    ============================ TRỘN (đi ngược LÊN) =============================

             [ 8 ] [ 3 ]   [ 5 ] [ 4 ]     [ 7 ] [ 6 ]   [ 1 ] [ 2 ]
               \     /       \     /         \     /       \     /
               [ 3, 8 ]      [ 4, 5 ]        [ 6, 7 ]      [ 1, 2 ]
                  \              /               \             /
                [ 3, 4, 5, 8 ]                    [ 1, 2, 6, 7 ]
                        \                              /
                        [ 1, 2, 3, 4, 5, 6, 7, 8 ]

                        ĐÃ SẮP XẾP! Trả về cho hàm gọi ban đầu.
```

### Cách đọc cây:

```
    - Đi XUỐNG: danh sách được chia đôi ở mỗi mức
                 (n -> n/2 -> n/4 -> ... -> 1)

    - Không có phép so sánh nào xảy ra trong lúc chia.
      TOÀN BỘ công việc sắp xếp thật sự xảy ra trên đường đi LÊN,
      bên trong merge(), nơi hai nửa đã sắp xếp trở thành một.

    - Mỗi lần gọi merge() nhận hai danh sách ĐÃ SẮP XẾP và trả về
      một danh sách ĐÃ SẮP XẾP lớn hơn — vì vậy bất biến "merge() cần
      đầu vào đã sắp xếp" luôn được duy trì.
```

---

## 7. Mã Sắp xếp trộn (Merge Sort Code)

```python
def merge(array1, array2):
    combined = []
    i = 0
    j = 0
    while i < len(array1) and j < len(array2):
        if array1[i] < array2[j]:
            combined.append(array1[i])
            i += 1
        else:
            combined.append(array2[j])
            j += 1
              
    while i < len(array1):
        combined.append(array1[i])
        i += 1

    while j < len(array2):
        combined.append(array2[j])
        j += 1

    return combined


def merge_sort(my_list):
    if len(my_list) == 1:
        return my_list
    mid_index = int(len(my_list)/2)
    left = merge_sort(my_list[:mid_index])
    right = merge_sort(my_list[mid_index:])
    
    return merge(left, right)
```

### Chú thích:

```
    def merge_sort(my_list):
        if len(my_list) == 1:          <- TRƯỜNG HỢP CƠ SỞ: đã sắp xếp hiển nhiên
            return my_list
        mid_index = int(len(my_list)/2)          <- tìm phần tử giữa
        left  = merge_sort(my_list[:mid_index])  <- đệ quy nửa TRÁI
        right = merge_sort(my_list[mid_index:])  <- đệ quy nửa PHẢI
        return merge(left, right)                <- kết hợp hai nửa đã sắp xếp
```

### Chạy thuật toán:

```python
original_list = [3,1,4,2]

sorted_list = merge_sort(original_list)

print('Original List:', original_list)
# Original List: [3, 1, 4, 2]

print('\nSorted List:', sorted_list)
# Sorted List: [1, 2, 3, 4]
```

---

## 8. Phân tích Big O (Big O Analysis)

### Thời gian — Vì sao là `O(n log n)` trong MỌI trường hợp:

Công việc của Sắp xếp trộn dễ hiểu nhất theo công thức **số mức x công việc mỗi mức**:

```
    Mức 0:          [ - - - - - - - - ]                công việc trộn: n
                    /                  \
    Mức 1:       [ - - - - ]        [ - - - - ]       công việc trộn: n/2 + n/2 = n
                  /        \          /        \
    Mức 2:     [ - - ]  [ - - ]  [ - - ]  [ - - ]     công việc trộn: n
                /   \    /   \    /   \    /   \
    Mức 3:    [ - ][ - ][ - ][ - ][ - ][ - ][ - ][ - ] trường hợp cơ sở

    +------------------------------------------------------------+
    | SỐ MỨC             = log2(n)  (danh sách được chia đôi)    |
    | CÔNG VIỆC mỗi mức  = O(n)     (mỗi phần tử được trộn       |
    |                                  đúng một lần ở mỗi mức)    |
    |                                                            |
    | TỔNG THỜI GIAN = O(n) x O(log n) = O(n log n)              |
    +------------------------------------------------------------+
```

Việc chia **luôn** thành hai nửa hoàn hảo — không phụ thuộc vào dữ liệu. Vì vậy trường hợp tốt nhất, trung bình và xấu nhất đều tạo ra **cùng hình dạng cây** và cùng công việc `O(n log n)`. Không có trường hợp suy biến.

### Không gian — `O(n)` phụ trợ:

```
    merge() tạo một danh sách combined hoàn toàn mới:

        left  [ - - - - ]  +  right [ - - - - ]
                    \                /
                     combined [ - - - - - - - - ]   <- n ô bộ nhớ
                                                       BỔ SUNG

    Các danh sách con ban đầu bị loại bỏ sau mỗi lần trộn, nhưng ở mức
    trên cùng vẫn cần một bản sao đầy đủ của n phần tử => O(n) không gian.
```

### Tính ổn định — CÓ:

Khi `array1[i] == array2[j]`, mã lấy phần tử từ danh sách **bên phải** (`if array1[i] < array2[j]` là false chỉ khi bên trái `>=` bên phải — hãy kiểm tra: khi bằng nhau, nhánh `else` lấy bên phải). Bất kể chi tiết xử lý phần tử bằng nhau, Sắp xếp trộn tiêu chuẩn được triển khai để **ổn định**: các phần tử bằng nhau giữ nguyên thứ tự tương đối ban đầu.

### Bảng tóm tắt Big O:

| Độ phức tạp | Giá trị | Lý do |
|:---|:---|:---|
| **Thời gian (Tốt nhất)** | `O(n log n)` | Luôn chia đôi; mỗi mức luôn trộn trong `O(n)` |
| **Thời gian (Trung bình)** | `O(n log n)` | Hình dạng cây không đổi theo thứ tự đầu vào |
| **Thời gian (Xấu nhất)** | `O(n log n)` | **Được đảm bảo** — không có đầu vào suy biến |
| **Không gian** | `O(n)` | Các mảng `combined` phụ được tạo khi trộn |
| **Ổn định?** | **Có** | Các phần tử bằng nhau giữ nguyên thứ tự ban đầu |

---

## 9. Sắp xếp trộn so với các Sắp xếp cơ bản và Quick Sort

```
    +------------------+-----------+-----------+-----------+---------+---------+
    |    THUẬT TOÁN    |   TỐT NHẤT|  TRUNG BÌNH|   XẤU NHẤT| KHÔNG GIAN| ỔN ĐỊNH?|
    +------------------+-----------+-----------+-----------+---------+---------+
    | Bubble Sort      |   O(n)    |   O(n^2)  |   O(n^2)  |   O(1)  |   Có    |
    +------------------+-----------+-----------+-----------+---------+---------+
    | Selection Sort   |   O(n^2)  |   O(n^2)  |   O(n^2)  |   O(1)  |   Không |
    +------------------+-----------+-----------+-----------+---------+---------+
    | Insertion Sort   |   O(n)    |   O(n^2)  |   O(n^2)  |   O(1)  |   Có    |
    +------------------+-----------+-----------+-----------+---------+---------+
    | SẮP XẾP TRỘN     | O(n log n)| O(n log n)| O(n log n)|   O(n)  |   Có    |
    +------------------+-----------+-----------+-----------+---------+---------+
    | Quick Sort       | O(n log n)| O(n log n)|   O(n^2)  | O(log n)|   Không |
    +------------------+-----------+-----------+-----------+---------+---------+
```

### Bước nhảy lớn — `O(n^2)` -> `O(n log n)`:

Sắp xếp trộn là thuật toán đầu tiên trong khóa học thoát khỏi cái bẫy `O(n^2)` của các sắp xếp cơ bản. Cái giá phải trả là `O(n)` không gian bổ sung (các thuật toán cơ bản sắp xếp tại chỗ với `O(1)`).

### Sắp xếp trộn nằm ở đâu so với Quick Sort:

| Tiêu chí | Sắp xếp trộn | Quick Sort |
|:---|:---|:---|
| **Bảo đảm thời gian** | `O(n log n)` **luôn luôn** | `O(n log n)` **trung bình**, xấu nhất `O(n^2)` |
| **Không gian bổ sung** | `O(n)` mảng phụ | Chỉ ngăn xếp gọi hàm `O(log n)` |
| **Ổn định?** | Có | Không |
| **Phù hợp nhất** | Danh sách liên kết, sắp xếp ngoài, cần ổn định | Mảng trong bộ nhớ, sắp xếp mục đích chung |

> **Quy tắc ngón tay cái:** cần *bảo đảm* hoặc *tính ổn định* (hoặc sắp xếp danh sách liên kết)? Chọn **Sắp xếp trộn**. Cần tốc độ trong bộ nhớ và ít bộ nhớ nhất? Chọn **Quick Sort**.

---

**Bước tiếp theo:** Bây giờ hãy xem thuật toán chia để trị tuyệt vời còn lại — **Quick Sort** — đạt `O(n log n)` trung bình trong khi sắp xếp **tại chỗ**, bằng thủ thuật **pivot/partition** thay vì trộn.
