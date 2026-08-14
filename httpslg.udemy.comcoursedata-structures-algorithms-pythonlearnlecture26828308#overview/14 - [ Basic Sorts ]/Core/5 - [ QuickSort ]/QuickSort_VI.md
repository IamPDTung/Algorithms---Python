
---

# Sắp xếp nhanh (Quick Sort)

## 1. Sắp xếp nhanh là gì?

**Sắp xếp nhanh (Quick Sort)** là một thuật toán **sắp xếp tại chỗ (in-place), chia để trị (divide-and-conquer)**. Thay vì liên tục chọn phần tử nhỏ nhất hoặc dịch mọi phần tử đi một vị trí, nó chọn một **phần tử chốt (pivot)**, sắp xếp lại mảng xung quanh phần tử chốt đó, rồi đệ quy sắp xếp hai phía.

Thuật toán có hai phần thiết yếu:

* `pivot(my_list, pivot_index, end_index)` — **phân hoạch (partition)** một đoạn sao cho pivot nằm ở vị trí cuối cùng của nó trong danh sách đã sắp xếp.
* `quick_sort_helper(my_list, left, right)` — áp dụng đệ quy quá trình phân hoạch cho đoạn bên trái và đoạn bên phải.

Cam kết quan trọng sau khi phân hoạch là:

> Mọi giá trị bên trái pivot đều nhỏ hơn pivot, và mọi giá trị bên phải đều lớn hơn hoặc bằng pivot.

Hai phía chưa nhất thiết đã được sắp xếp. Chúng chỉ mới được tách thành các bài toán nhỏ độc lập. Điều đó là đủ để đệ quy hoàn thành công việc.

```
        +--------------------------------------------------+
        |                    SẮP XẾP NHANH                |
        +--------------------------------------------------+
        |                                                  |
        |   1. CHỌN PIVOT                                  |
        |          |                                       |
        |          v                                       |
        |   2. PHÂN HOẠCH: nhỏ hơn | pivot | lớn hơn       |
        |          |                  |                    |
        |          +----------+-------+                    |
        |                     |                            |
        |        đệ quy sắp xếp cả hai phía                 |
        |                                                  |
        |   pivot()  ---------------->  quick_sort_helper() |
        +--------------------------------------------------+
```

---

## 2. Vì sao Sắp xếp nhanh được tạo ra?

Các sắp xếp cơ bản trong khóa học — sắp xếp nổi bọt (Bubble Sort), sắp xếp chọn (Selection Sort) và sắp xếp chèn (Insertion Sort) — có thể cần **`O(n^2)`** phép so sánh và di chuyển. Sắp xếp trộn (Merge Sort) phá vỡ rào cản thời gian đó với `O(n log n)`, nhưng cách triển khai thông thường cho mảng tạo các mảng phụ và vì vậy dùng `O(n)` không gian bổ sung.

Sắp xếp nhanh được tạo ra như một lựa chọn nhanh cho **mảng trong bộ nhớ (in-memory arrays)**:

* Giữ được thời gian trung bình hữu ích `O(n log n)`.
* Phân hoạch **tại chỗ**, vì vậy không cần mảng thứ hai chứa toàn bộ `n` giá trị.
* Các phép hoán đổi và các lần quét tuần tự thường có **tính địa phương bộ nhớ đệm (cache locality)** tốt: các vị trí mảng gần nhau được truy cập khi phân hoạch.
* Dùng ngăn xếp gọi hàm cho đệ quy thay vì cấp phát một bộ đệm trộn đầy đủ.

Đây là một sự đánh đổi, không phải cải tiến tuyệt đối. Pivot kém vẫn có thể tạo `O(n^2)`, và triển khai đơn giản dưới đây không ổn định.

```
    SẮP XẾP CƠ BẢN                     SẮP XẾP NHANH
    +------------------+                +-------------------------+
    | lặp lại nhiều     |                | chọn pivot               |
    | cặp so sánh       |                | quét một đoạn liên tục   |
    | O(n^2)            |       --->     | hoán đổi ngay trong mảng |
    +------------------+                | trung bình O(n log n)    |
                                        +-------------------------+

```

---

## 3. Sắp xếp nhanh giải quyết những vấn đề nào?

Sắp xếp nhanh là lựa chọn mạnh khi dữ liệu là một mảng hoặc danh sách đã nằm trong bộ nhớ và chương trình muốn tốc độ mà không cấp phát thêm một mảng `O(n)`.

Nó giải quyết một số vấn đề thực tế:

* **Mảng lớn trong bộ nhớ** — thời gian trung bình tốt hơn nhiều so với các sắp xếp cơ bản bậc hai.
* **Bộ nhớ phụ trợ hạn chế** — phân hoạch sắp xếp lại danh sách hiện có thay vì tạo danh sách kết quả đã trộn.
* **Dữ liệu liên tục** — mỗi phân hoạch quét một đoạn mảng giới hạn từ trái sang phải, thân thiện với bộ nhớ đệm CPU.
* **Phân rã đệ quy** — sau khi cố định một pivot, đoạn trái và đoạn phải có thể được giải độc lập.

Nó không giải quyết mọi yêu cầu sắp xếp:

* Không bảo đảm `O(n log n)` khi các lựa chọn pivot liên tục kém.
* Hoán đổi tùy ý có thể làm thay đổi thứ tự tương đối của các giá trị bằng nhau, vì vậy triển khai này không ổn định.
* Đệ quy mất cân bằng sâu có thể dùng `O(n)` không gian ngăn xếp.

```
        +--------------------------+-----------------------------+
        | VẤN ĐỀ                   | PHẢN HỒI CỦA SẮP XẾP NHANH |
        +--------------------------+-----------------------------+
        | Quá nhiều bước O(n^2)    | Trung bình O(n log n)      |
        +--------------------------+-----------------------------+
        | Mảng phụ quá tốn kém     | Hoán đổi trong danh sách   |
        +--------------------------+-----------------------------+
        | Dữ liệu ở bộ nhớ         | Quét các đoạn liên tục     |
        +--------------------------+-----------------------------+
        | Một bài toán quá lớn     | Chia quanh một pivot       |
        +--------------------------+-----------------------------+
        | Cần giới hạn chắc chắn   | Đổi chiến lược hoặc cải   |
        |                          | thiện việc chọn pivot     |
        +--------------------------+-----------------------------+
```

---

## 4. Chia để trị (Divide and Conquer)

Sắp xếp nhanh tuân theo mẫu **chia để trị** gồm ba phần:

1. **Chia:** chọn pivot và phân hoạch đoạn hiện tại quanh nó.
2. **Chinh phục:** đệ quy sắp xếp đoạn trước pivot và đoạn sau pivot.
3. **Kết hợp:** không cần phép trộn riêng. Khi hai lời gọi đệ quy trở về, toàn bộ đoạn đã sắp xếp vì pivot đã ở vị trí cuối cùng.

Giả sử pivot đầu tiên là `4` trong `[4,6,1,7,3,2,5]`. Phân hoạch tạo ra:

```
    TRƯỚC:        [ 4, 6, 1, 7, 3, 2, 5 ]
                   ^
                 pivot = 4

    SAU MỘT LẦN PHÂN HOẠCH:
                  [ 2, 1, 3 | 4 | 6, 7, 5 ]
                    nhỏ hơn  ^   lớn hơn/bằng
                              vị trí cuối cùng

    Các thanh dọc KHÔNG có nghĩa hai phía đã được sắp xếp.
    Chúng có nghĩa không giá trị nào bên trái thuộc về sau 4,
    và không giá trị nào bên phải thuộc về trước 4.

    CÁC BÀI TOÁN ĐỆ QUY:
                  sắp xếp [ 2, 1, 3 ] và sắp xếp [ 6, 7, 5 ]
```

Trường hợp cơ sở là một đoạn có không hoặc một phần tử. Trong mã nguồn, `left < right` là điều kiện bảo vệ đệ quy. Đoạn một phần tử không cần làm gì, và đoạn rỗng cũng đã được sắp xếp.

---

## 5. Pivot và Phân hoạch Chi tiết

Triển khai được cung cấp luôn bắt đầu với `pivot_index` là vị trí pivot. Ở lời gọi đầu tiên, điều đó có nghĩa là **phần tử đầu tiên** là pivot. Giá trị tại vị trí đó được đọc lặp lại qua `my_list[pivot_index]` trong lúc quét.

`swap_index` có một ý nghĩa chính xác:

* Bắt đầu tại `pivot_index`.
* Đánh dấu cuối vùng chứa các giá trị nhỏ hơn pivot.
* Khi `my_list[i] < my_list[pivot_index]`, tăng `swap_index` rồi hoán đổi giá trị nhỏ hơn mới tìm thấy vào biên đó.
* Cuối cùng, hoán đổi pivot với `my_list[swap_index]`.

```
    pivot_index                         end_index
         |                                  |
         v                                  v
    [ pivot ][ nhỏ hơn ][ chưa biết ... ][ còn lại ]
       4          < 4            ?              ?
                    ^             ^
              swap_index          i quét sang phải

    Sau phép hoán đổi cuối:

    [ mọi giá trị < 4 ][ 4 ][ mọi giá trị >= 4 ]
```

Phép so sánh là nghiêm ngặt: `<`, không phải `<=`. Vì vậy các giá trị bằng pivot ở lại phía bên phải. Điều này đúng về mặt kết quả, nhưng cũng góp phần làm mất cân bằng khi có nhiều giá trị bằng nhau.

`i` hỏi: “Giá trị nào tôi chưa phân loại?” `swap_index` hỏi: “Vị trí tiếp theo cho một giá trị nhỏ hơn pivot ở đâu?” Một giá trị có thể được phát hiện ở rất xa bên phải và được chuyển về vị trí tiếp theo trong vùng nhỏ hơn, trong khi việc quét tiếp tục từ `i + 1`.

---

## 6. Truy vết Phân hoạch Đầy đủ

Truy vết `pivot(my_list, 0, 6)` trên:

```python
[4,6,1,7,3,2,5]
```

Pivot là giá trị tại chỉ mục `0`, vì vậy `pivot = 4`. Ban đầu `swap_index = 0`, và `i` quét các chỉ mục từ `1` đến `6`.

### Mọi lần quét và mọi lần hoán đổi

```
    Ban đầu: pivot = 4, pivot_index = 0, swap_index = 0
             [ 4, 6, 1, 7, 3, 2, 5 ]
               P  i
```

| Bước | `i` | `my_list[i]` | `pivot` | `swap_index` (trước -> sau) | Hành động | Mảng sau hành động |
|:---:|---:|---:|---:|---:|:---|:---|
| 1 | 1 | 6 | 4 | `0 -> 0` | `6 < 4` sai; không hoán đổi | `[4, 6, 1, 7, 3, 2, 5]` |
| 2 | 2 | 1 | 4 | `0 -> 1` | hoán đổi chỉ mục 1 và 2 | `[4, 1, 6, 7, 3, 2, 5]` |
| 3 | 3 | 7 | 4 | `1 -> 1` | `7 < 4` sai; không hoán đổi | `[4, 1, 6, 7, 3, 2, 5]` |
| 4 | 4 | 3 | 4 | `1 -> 2` | hoán đổi chỉ mục 2 và 4 | `[4, 1, 3, 7, 6, 2, 5]` |
| 5 | 5 | 2 | 4 | `2 -> 3` | hoán đổi chỉ mục 3 và 5 | `[4, 1, 3, 2, 6, 7, 5]` |
| 6 | 6 | 5 | 4 | `3 -> 3` | `5 < 4` sai; không hoán đổi | `[4, 1, 3, 2, 6, 7, 5]` |
| 7 | cuối | pivot `4` | 4 | `3 -> 3` | hoán đổi chỉ mục 0 và 3 | `[2, 1, 3, 4, 6, 7, 5]` |

Khi trả về, các chỉ mục `0..2` chứa giá trị nhỏ hơn `4`, còn các chỉ mục `4..6` chứa giá trị lớn hơn hoặc bằng `4`. Phía bên phải là `[6,7,5]`, vì vậy nó vẫn cần một lời gọi đệ quy.

---

## 7. Cây Đệ quy của Sắp xếp nhanh

Sau lần phân hoạch đầu tiên, bài toán ban đầu trở thành hai đoạn nhỏ hơn. Mã nguồn sắp xếp đoạn trái trước, sau đó đoạn phải.

```
    quick_sort([4, 6, 1, 7, 3, 2, 5])
    pivot = 4, chỉ mục trả về 3
    /                                      \
   /                                        \
  sắp xếp [2, 1, 3]                     sắp xếp [6, 7, 5]
       pivot = 2                              pivot = 6
       chỉ mục = 1                            chỉ mục = 5
       /          \                           /          \
  sắp xếp [1]  sắp xếp [3]                 sắp xếp [5]  sắp xếp [7]
   cơ sở          cơ sở                     cơ sở          cơ sở

    mảng cuối: [1, 2, 3, 4, 5, 6, 7]
```

Không có bước nối (concatenation) tường minh. Các lời gọi đệ quy biến đổi cùng một danh sách, còn các pivot đã cố định vẫn nằm giữa hai phía đã sắp xếp của chúng.

---

## 8. Mã Sắp xếp nhanh

Mã được tách thành hàm hoán đổi có thể dùng lại, hàm phân hoạch, hàm trợ giúp đệ quy và hàm bao công khai:

```
    quick_sort(my_list)
          |
          v
    helper(0, len(my_list)-1)
       |       \
    pivot()   helper(left) + helper(right)
       |
    swap() trong lúc quét
```

### Mã pivot, nguyên văn

```python
def swap(my_list, index1, index2):
    temp = my_list[index1]
    my_list[index1] = my_list[index2]
    my_list[index2] = temp


def pivot(my_list, pivot_index, end_index):
    swap_index = pivot_index

    for i in range(pivot_index+1, end_index+1):
        if my_list[i] < my_list[pivot_index]:
            swap_index += 1
            swap(my_list, swap_index, i)
    swap(my_list, pivot_index, swap_index)
    return swap_index




my_list = [4,6,1,7,3,2,5]

print('List before running pivot():')
print(my_list)

returned_pivot_index = pivot(my_list, 0, 6)

print('\nList after running pivot():')
print(my_list)

print('\nPivot Index:')
print(returned_pivot_index)



"""
    EXPECTED OUTPUT:
    ----------------
    List before running pivot():
    [4, 6, 1, 7, 3, 2, 5]

    List after running pivot():
    [2, 1, 3, 4, 6, 7, 5]

    Pivot Index:
    3

 """
```

### Mã Quick Sort đầy đủ, nguyên văn

```python
def swap(my_list, index1, index2):
    temp = my_list[index1]
    my_list[index1] = my_list[index2]
    my_list[index2] = temp


def pivot(my_list, pivot_index, end_index):
    swap_index = pivot_index

    for i in range(pivot_index+1, end_index+1):
        if my_list[i] < my_list[pivot_index]:
            swap_index += 1
            swap(my_list, swap_index, i)
    swap(my_list, pivot_index, swap_index)
    return swap_index


def quick_sort_helper(my_list, left, right):
    if left < right:
        pivot_index = pivot(my_list, left, right)
        quick_sort_helper(my_list, left, pivot_index-1)  
        quick_sort_helper(my_list, pivot_index+1, right)       
    return my_list
    

def quick_sort(my_list):
    quick_sort_helper(my_list, 0, len(my_list)-1)

 
 


my_list = [4,6,1,7,3,2,5]

quick_sort(my_list)

print(my_list)



"""
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6, 7]
 """
```

---

## 9. Hành vi Tốt nhất, Trung bình và Xấu nhất

Một lần quét phân hoạch tốn `O(n)` cho đoạn có kích thước `n`. Tổng thời gian phụ thuộc vào việc pivot chia đoạn đều đến mức nào.

### Trường hợp tốt nhất: phân hoạch cân bằng

Nếu mỗi pivot chia đoạn thành hai phần gần bằng nhau, đệ quy có khoảng `log n` mức. Mỗi mức quét tổng cộng khoảng `n` phần tử.

### Trường hợp trung bình: các phép chia thường hữu ích

Với dữ liệu đa dạng và pivot đại diện hợp lý, các phân hoạch thường khá cân bằng, nên tổng kỳ vọng vẫn là `O(n log n)`.

### Trường hợp xấu nhất: phân hoạch một phía

Nếu mọi pivot đều là giá trị nhỏ nhất hoặc lớn nhất trong đoạn của nó, một phía có kích thước không và phía kia có kích thước `n - 1`.

```
    n
    |
    n-1       quét n-1 giá trị
    |
    n-2       quét n-2 giá trị
    |
    n-3       quét n-3 giá trị
    |
    ...
    1

    công việc = n + (n-1) + (n-2) + ... + 1
              = n(n+1)/2
              = O(n^2)
```

Vì vậy thuật toán nhanh trong trung bình, chứ không được bảo đảm nhanh trên mọi đầu vào và mọi chính sách chọn pivot.

| Trường hợp | Hình dạng phân hoạch | Công thức truy hồi | Thời gian |
|:---|:---|:---|:---|
| **Tốt nhất** | Hai nửa bằng nhau | `T(n) = 2T(n/2) + O(n)` | **`O(n log n)`** |
| **Trung bình** | Các phần chia nhìn chung hợp lý | Hành vi cân bằng kỳ vọng | **`O(n log n)`** |
| **Xấu nhất** | `0` và `n-1` mỗi lần | `T(n) = T(n-1) + O(n)` | **`O(n^2)`** |

---

## 10. Đầu vào Đã sắp xếp với Pivot Đầu tiên

Mã nguồn được cung cấp chọn phần tử đầu tiên của mỗi đoạn. Lựa chọn đó suy biến ngay trên danh sách đã sắp xếp như `[1,2,3,4,5,6,7]`.

Ở lời gọi đầu tiên, pivot `1` nhỏ hơn mọi giá trị còn lại. Điều kiện `my_list[i] < 1` không bao giờ đúng, nên `swap_index` vẫn là `0`. Phép hoán đổi cuối đổi chỉ mục `0` với chính nó, và đệ quy nhận các đoạn `[]` và `[2,3,4,5,6,7]`.

```
    [1, 2, 3, 4, 5, 6, 7]
     ^
    pivot = 1, không có giá trị nào nhỏ hơn

    [1] | [2, 3, 4, 5, 6, 7]
     ^                  ^
     cố định            đệ quy trên n-1 giá trị

    [1] | [2] | [3, 4, 5, 6, 7]
    [1] | [2] | [3] | [4, 5, 6, 7]
    [1] | [2] | [3] | [4] | ...

    Cây là một chuỗi, không phải cây cân bằng.
```

---

## 11. Big O, Không gian, Tính địa phương và Tính ổn định

### Thời gian và không gian phụ trợ

Phân hoạch của Sắp xếp nhanh được thực hiện tại chỗ: `swap()` thay đổi vị trí trong danh sách ban đầu, và không tạo danh sách `combined`. Ngăn xếp đệ quy tách biệt với vùng lưu trữ mảng.

```
    MẢNG (tái sử dụng): [ 2 | 1 | 3 | 4 | 6 | 7 | 5 ]
                              < pivot | pivot | >= pivot

    NGĂN XẾP: helper(...) -> helper(...) -> ...
    Cây cân bằng: O(log n) khung; chuỗi: O(n) khung
```

| Thuộc tính | Tốt nhất | Trung bình | Xấu nhất |
|:---|:---:|:---:|:---:|
| **Thời gian** | `O(n log n)` | `O(n log n)` | `O(n^2)` |
| **Công việc phân hoạch** | `O(n)` mỗi mức | `O(n)` mỗi mức | `O(n)` mỗi mức còn lại |
| **Không gian mảng phụ** | `O(1)` | `O(1)` | `O(1)` |
| **Ngăn xếp đệ quy** | `O(log n)` | `O(log n)` | `O(n)` |
| **Ổn định?** | Không | Không | Không |

### Tính địa phương bộ nhớ đệm

Mảng là vùng lưu trữ liên tục. Trong lúc phân hoạch, `i` tiến qua một đoạn liên tục, và các giá trị được di chuyển bởi `swap()` vẫn nằm trong đoạn đó. Mẫu này thường sử dụng tốt các dòng bộ nhớ đệm CPU so với thuật toán liên tục cấp phát và duyệt các cấu trúc tách rời.

Tính địa phương bộ nhớ đệm là lý do hiệu năng thực tế, không thay thế cho phân tích tiệm cận. Pivot xấu vẫn tạo công việc bậc hai dù mỗi lần quét thân thiện với bộ nhớ đệm.

### Tính ổn định

Các phép hoán đổi không bảo toàn thứ tự tương đối của các khóa bằng nhau. Nếu các bản ghi có khóa sắp xếp bằng nhau và thứ tự ban đầu quan trọng, hãy dùng thuật toán ổn định hoặc thêm chỉ mục ban đầu làm tiêu chí phá hòa.

---

## 12. Sắp xếp trộn so với Sắp xếp nhanh

Cả hai thuật toán đều dùng chia để trị và có thời gian trung bình `O(n log n)`, nhưng chúng đưa ra các lựa chọn ngược nhau về bộ nhớ và bảo đảm.

| Tiêu chí | Sắp xếp trộn | Sắp xếp nhanh |
|:---|:---|:---|
| **Thời gian tốt nhất** | `O(n log n)` | `O(n log n)` |
| **Thời gian trung bình** | `O(n log n)` | `O(n log n)` |
| **Thời gian xấu nhất** | `O(n log n)` | `O(n^2)` với pivot kém |
| **Không gian phụ cho mảng** | `O(n)` | `O(1)` ngoài ngăn xếp |
| **Không gian ngăn xếp trung bình** | `O(log n)` | `O(log n)` |
| **Ổn định** | Có, nếu xử lý trộn ổn định | Không trong triển khai này |
| **Di chuyển dữ liệu** | Sao chép vào mảng kết quả | Hoán đổi trong đầu vào |
| **Trường hợp mạnh** | Ổn định, danh sách liên kết, sắp xếp ngoài, bảo đảm | Mảng trong bộ nhớ, ít bộ nhớ phụ, tốc độ thực tế |

### Nên chọn thuật toán nào?

Chọn Sắp xếp trộn khi tính ổn định, thời gian xấu nhất dự đoán được, cấu trúc danh sách liên kết hoặc dữ liệu ngoài là ưu tiên. Chọn Sắp xếp nhanh khi dữ liệu ở bộ nhớ, việc cấp phát phụ quan trọng và tốc độ trung bình có giá trị.

```
    BẢO ĐẢM HOẶC ỔN ĐỊNH? --có--> SẮP XẾP TRỘN
              |
           không
              v
    ÍT KHÔNG GIAN MẢNG PHỤ? --có--> SẮP XẾP NHANH
              |
           không --> chọn theo dữ liệu và ràng buộc
```

Chỉ tên thuật toán không quyết định hiệu năng. Chính sách chọn pivot, hình dạng dữ liệu, chi phí so sánh, phân cấp bộ nhớ và biện pháp bảo vệ đệ quy đều quan trọng trong triển khai thực tế.

---

## 13. Mô hình Tư duy về Sắp xếp nhanh

Cách ngắn gọn và đáng tin cậy nhất để ghi nhớ triển khai này là:

1. Chọn giá trị đầu tiên trong đoạn hiện tại làm pivot.
2. Quét bằng `i`.
3. Chỉ di chuyển `swap_index` khi tìm thấy giá trị nhỏ hơn pivot.
4. Đặt pivot giữa vùng nhỏ hơn và vùng lớn hơn hoặc bằng.
5. Đệ quy lặp lại trên hai đoạn không bao gồm pivot đã cố định.

```
    quét                         đặt pivot                  đệ quy
    [ P | chưa biết ... ]  --->  [ nhỏ hơn | P | >= P ]  ---> trái + phải
       i ->                              ^                    /       \
                                  vị trí cuối cùng       giải      giải

    Phân hoạch cân bằng cho O(n log n) trung bình.
    Các cực trị lặp lại ở phần tử đầu cho O(n^2) xấu nhất.
```

Thành tựu chính của Sắp xếp nhanh không phải là tránh mọi công việc. Nó thực hiện một lần phân hoạch tuyến tính, cố định vĩnh viễn một phần tử và tái sử dụng vùng lưu trữ ban đầu trong khi đệ quy thu nhỏ bài toán còn lại.

---

**Bước tiếp theo:** Hãy đối chiếu truy vết phân hoạch này với truy vết trộn của Sắp xếp trộn. Sắp xếp trộn kết hợp hai danh sách đã sắp xếp bằng không gian phụ; Sắp xếp nhanh đặt pivot bằng hoán đổi rồi sắp xếp hai đoạn còn lại.
