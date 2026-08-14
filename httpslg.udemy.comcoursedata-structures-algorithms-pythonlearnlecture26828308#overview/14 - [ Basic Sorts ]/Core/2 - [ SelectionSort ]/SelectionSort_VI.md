
---

# Sắp xếp chọn (Selection Sort)

## 1. Sắp xếp chọn là gì?

**Sắp xếp chọn (Selection Sort)** là thuật toán sắp xếp dựa trên so sánh (comparison-based sorting algorithm). Thuật toán liên tục chọn giá trị nhỏ nhất trong phần chưa sắp xếp của danh sách, rồi đặt nó vào vị trí kế tiếp của phần đã sắp xếp. Thay vì di chuyển các giá trị mỗi khi phát hiện một cặp ngược thứ tự, nó quét xong trước, ghi nhớ vị trí nhỏ nhất, sau đó thực hiện nhiều nhất một lần hoán đổi (swap).

### Ý tưởng chính:
> Tìm phần tử nhỏ nhất trong vùng chưa sắp xếp. Đặt phần tử đó ở mép trái của vùng chưa sắp xếp. Lặp lại cho đến khi không còn vùng chưa sắp xếp.

### Đặc điểm cốt lõi:
* **Sắp xếp bằng so sánh (comparison sort)** - thuật toán tìm thứ tự bằng cách so sánh các giá trị.
* **Tại chỗ (in-place)** - sắp xếp ngay trong danh sách gốc, không cần danh sách phụ.
* **Vùng đã sắp xếp lớn dần từ BÊN TRÁI** - mỗi lượt khóa một giá trị nhỏ nhất vào vị trí cuối cùng.
* **Mỗi lượt nhiều nhất một lần hoán đổi** - phép quét có thể dài, nhưng số lần ghi được giới hạn có chủ ý.
* **Không thích nghi (not adaptive)** - ngay cả danh sách đã sắp xếp vẫn được quét đầy đủ ở mọi hậu tố.

```
        +--------------------------------------------------+
        |              SAP XEP CHON (SELECTION SORT)      |
        +--------------------------------------------------+
        |                                                  |
        |   Lap lai voi moi vi tri i:                      |
        |     1. Gia su i la vi tri nho nhat               |
        |     2. Quet phan con lai cua danh sach           |
        |     3. Ghi nho min_index                         |
        |     4. Hoan doi vao vi tri i                     |
        |                                                  |
        |   [ vung da sap xep | vung chua sap xep ]         |
        |        lon dan ->          thu nho <-             |
        |                                                  |
        |   Ket qua moi luot: mot gia tri nho nhat bi khoa  |
        +--------------------------------------------------+
```

---

## 2. Tại sao thuật toán này được tạo ra?

Sắp xếp chọn được xây dựng quanh một đánh đổi đơn giản: dùng nhiều phép so sánh để tránh các lần ghi không cần thiết. Sắp xếp nổi bọt (Bubble Sort) có thể hoán đổi các phần tử kề nhau nhiều lần trong lúc một giá trị lớn đi qua danh sách. Sắp xếp chọn quét trước, chờ đến khi biết chắc giá trị nhỏ nhất, rồi đưa trực tiếp giá trị đó đến đích.

Thiết kế này quan trọng khi thao tác ghi đắt hơn thao tác đọc. Tuy nhiên, thuật toán vẫn có thời gian bậc hai nên không phải lời giải sản xuất cho mọi trường hợp. Giá trị của nó nằm ở việc hiểu các thuật toán nhạy với số lần ghi và những môi trường lưu trữ bị giới hạn.
### Ngân sách ghi:
* Một lượt thực hiện nhiều **phép so sánh (comparisons)** khi quét hậu tố.
* Một lượt thực hiện **không hoặc một lần hoán đổi** sau khi quét.
* Code của khóa học dùng ba phép gán với biến `temp` để thực hiện một lần hoán đổi.
* Toàn bộ lần chạy có nhiều nhất `n - 1` lần hoán đổi, tức nhiều nhất `3(n - 1)` phép gán từ các lần hoán đổi đó.

```
     SAP XEP NOI BOT                     SAP XEP CHON
     -------------                       ---------------
     so sanh -> hoan doi                 so sanh -> ghi nho
     so sanh -> hoan doi                 so sanh -> ghi nho
     so sanh -> hoan doi                 so sanh -> ghi nho
     ... nhieu lan ghi ...               quet xong
                                           mot lan hoan doi truc tiep

     Muc tieu: di chuyen dan dan         Muc tieu: chon truoc,
               bang hoan doi ke nhau              ghi mot lan
```

---

## 3. Nó giải quyết những bài toán nào?

Sắp xếp chọn giải quyết bài toán cơ bản: sắp thứ tự một danh sách hữu hạn tại chỗ trong khi hạn chế việc di chuyển dữ liệu. Đây là lựa chọn phù hợp để học hoặc xử lý đầu vào nhỏ khi tính đơn giản, lượng bộ nhớ nhỏ và hành vi dễ dự đoán quan trọng hơn tốc độ.

### Các tình huống phù hợp:
* **Danh sách rất nhỏ**, khi code đơn giản có giá trị.
* **Môi trường nhạy với thao tác ghi (write-sensitive)**, nơi cần tránh ghi thừa.
* **Học bất biến vòng lặp (loop invariant)**: sau lượt `i`, `i + 1` giá trị đầu tiên là giá trị cuối cùng.
* **Học cách chọn cực tiểu**: một lần quét có thể tìm phần tử tiếp theo mà không sắp xếp cả hậu tố.
* **Công việc dễ dự đoán**: số phép so sánh không phụ thuộc thứ tự ban đầu.

### Các bài toán nó không giải quyết tốt:
* Nó không chạy tuyến tính với danh sách đã sắp xếp.
* Nó không tận dụng dữ liệu gần như đã sắp xếp như Sắp xếp chèn (Insertion Sort).
* Nó chậm hơn nhiều so với các thuật toán `O(n log n)` trên danh sách lớn.
* Dạng thông thường tại chỗ của nó không giữ được tính ổn định (stable).

```
        +--------------------------------------------------+
        |        SELECTION SORT PHU HOP O DAU             |
        +--------------------------------------------------+
        |  Dau vao nho / code don gian .............. CO   |
        |  Can it lan ghi ........................... CO   |
        |  So phep so sanh de doan .................. CO   |
        |  Dau vao gan nhu da sap xep ............... KHONG|
        |  Dau vao ngau nhien lon ................... KHONG|
        |  Ban ghi phai giu thu tu bang nhau ........ KHONG|
        +--------------------------------------------------+
        * Dạng hoán đổi thông thường không ổn định.
```

---

## 4. Vòng quét `min_index` hoạt động thế nào?

Vòng lặp ngoài chọn ranh giới `i`. Mọi phần tử trước `i` đã được sắp xếp và không được chạm lại. Vòng lặp trong bắt đầu tại `i + 1` và tìm kiếm toàn bộ vùng chưa sắp xếp còn lại.

### Một lượt, từng bước:
1. Đặt `min_index = i`. Giá trị đầu tiên của vùng chưa sắp xếp là ứng viên nhỏ nhất hiện biết.
2. Cho `j` đi qua mọi chỉ số sau đó, từ `i + 1` đến chỉ số cuối.
3. Nếu `my_list[j] < my_list[min_index]`, cập nhật `min_index` thành `j`.
4. Sau khi quét xong, chỉ hoán đổi vị trí `i` và `min_index` nếu chúng khác nhau.
5. Tăng `i`; tiền tố đã sắp xếp có thêm một giá trị cuối cùng.

```
     i                  j quet ve ben phai
     |                  ------------------->
     v
     [ vung da sap xep | ung vien | vung chua sap xep ]
                                  ^
                            min_index bat dau o day

     Moi gia tri nho hon chi doi min_index,
     mang chua doi cho den khi quet xong.
```

---

## 5. Lần vết từng lượt trên `[4, 2, 6, 5, 1, 3]`

Ta lần vết đúng thuật toán của khóa học. Danh sách có sáu giá trị nên vòng lặp ngoài chạy năm lượt: `i = 0, 1, 2, 3, 4`. Mỗi lượt quét toàn bộ hậu tố chưa sắp xếp, kể cả khi không cần hoán đổi.

### LƯỢT 1 - `i = 0`

Bắt đầu với `min_index = 0`, giá trị `4`.

```
     Bat dau: [ 4 , 2 , 6 , 5 , 1 , 3 ]
                ^
            min_index = 0, gia tri 4

     j=1: 2 < 4  -> min_index = 1
     j=2: 6 < 2  -> khong doi
     j=3: 5 < 2  -> khong doi
     j=4: 1 < 2  -> min_index = 4
     j=5: 3 < 1  -> khong doi

     Tim thay cuc tieu: gia tri 1 o chi so 4
     Hoan doi chi so 0 voi chi so 4
```

Sau lượt 1:

```
     [ 1 | 2 , 6 , 5 , 4 , 3 ]
       tien to da sap xep | vung chua sap xep
       gia tri cuoi cung: 1
```

### LƯỢT 2 - `i = 1`

`min_index` bắt đầu ở chỉ số 1, nơi giá trị đã là `2`.

```
     Hien tai: [ 1 | 2 , 6 , 5 , 4 , 3 ]
                       ^
                   min_index = 1

     j=2: 6 < 2  -> khong doi
     j=3: 5 < 2  -> khong doi
     j=4: 4 < 2  -> khong doi
     j=5: 3 < 2  -> khong doi

     Tim thay cuc tieu: gia tri 2 o chi so 1
     i == min_index -> khong hoan doi
```

Sau lượt 2:

```
     [ 1 , 2 | 6 , 5 , 4 , 3 ]
       tien to da sap xep | vung chua sap xep
       gia tri cuoi cung: 1, 2
```

### LƯỢT 3 - `i = 2`

Giá trị hiện tại là `6`, nhưng giá trị nhỏ nhất trong hậu tố là `3`.

```
     Hien tai: [ 1 , 2 | 6 , 5 , 4 , 3 ]
                           ^
                       min_index = 2, gia tri 6

     j=3: 5 < 6  -> min_index = 3
     j=4: 4 < 5  -> min_index = 4
     j=5: 3 < 4  -> min_index = 5

     Tim thay cuc tieu: gia tri 3 o chi so 5
     Hoan doi chi so 2 voi chi so 5
```

Sau lượt 3:

```
     [ 1 , 2 , 3 | 5 , 4 , 6 ]
       tien to da sap xep | vung chua sap xep
       gia tri cuoi cung: 1, 2, 3
```

### LƯỢT 4 - `i = 3`

Hậu tố bắt đầu bằng `5`; giá trị kế tiếp `4` trở thành cực tiểu mới.

```
     Hien tai: [ 1 , 2 , 3 | 5 , 4 , 6 ]
                              ^
                          min_index = 3, gia tri 5

     j=4: 4 < 5  -> min_index = 4
     j=5: 6 < 4  -> khong doi

     Tim thay cuc tieu: gia tri 4 o chi so 4
     Hoan doi chi so 3 voi chi so 4
```

Sau lượt 4:

```
     [ 1 , 2 , 3 , 4 | 5 , 6 ]
       tien to da sap xep | vung chua sap xep
       gia tri cuoi cung: 1, 2, 3, 4
```

### LƯỢT 5 - `i = 4`

Chỉ còn hai giá trị. Giá trị tại chỉ số 4 đã là giá trị nhỏ hơn.

```
     Hien tai: [ 1 , 2 , 3 , 4 | 5 , 6 ]
                                  ^
                              min_index = 4

     j=5: 6 < 5  -> khong doi
     Tim thay cuc tieu: gia tri 5 o chi so 4
     i == min_index -> khong hoan doi
```

Sau lượt 5:

```
     [ 1 , 2 , 3 , 4 , 5 | 6 ]
       tien to da sap xep  | gia tri cuoi

     Ket qua: [ 1 , 2 , 3 , 4 , 5 , 6 ]
```

### Toàn bộ trạng thái mảng sau MỖI lượt:

```
     Bat dau:       [ 4 , 2 , 6 , 5 , 1 , 3 ]
     Sau luot 1:    [ 1 | 2 , 6 , 5 , 4 , 3 ]
     Sau luot 2:    [ 1 , 2 | 6 , 5 , 4 , 3 ]
     Sau luot 3:    [ 1 , 2 , 3 | 5 , 4 , 6 ]
     Sau luot 4:    [ 1 , 2 , 3 , 4 | 5 , 6 ]
     Sau luot 5:    [ 1 , 2 , 3 , 4 , 5 | 6 ]
     Ket qua cuoi:  [ 1 , 2 , 3 , 4 , 5 , 6 ]

     Dau vach di sang phai mot vi tri sau moi luot.
```

---

## 6. Code thực tế của khóa học

Đây là code lời giải thực tế từ `SOLUTION-Selection_Sort.py`. Khối code dưới đây được chép nguyên văn, bao gồm cách hoán đổi bằng biến tạm và ví dụ kết quả.

```python
def selection_sort(my_list):
    for i in range(len(my_list)-1):
        min_index = i
        for j in range(i+1, len(my_list)):
            if my_list[j] < my_list[min_index]:
                min_index = j
        if i != min_index:
            temp = my_list[i]
            my_list[i] = my_list[min_index]
            my_list[min_index] = temp
    return my_list





print(selection_sort([4,2,6,5,1,3]))

 

"""
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6]
 """

```

```
     LUONG THUC THI
     --------------
     danh sach dau vao
             |
             v
     chon i va min_index
             |
             v
     quet j qua hau to
             |
             v
     hoan doi mot lan, hoac bo qua
             |
             v
     tra ve chinh doi tuong danh sach
```

### Kết quả mong đợi:

```
     [1, 2, 3, 4, 5, 6]
```

---

## 7. Logic từng dòng và các bất biến

### Vòng lặp ngoài:
`range(len(my_list) - 1)` tạo các chỉ số từ `0` đến `n - 2`. Không cần lượt cho chỉ số cuối: khi `n - 1` vị trí đầu đã chứa các giá trị nhỏ nhất theo đúng thứ tự, vị trí cuối buộc phải chứa giá trị lớn nhất còn lại.

### Ứng viên cực tiểu:
`min_index = i` có ý nghĩa quan trọng. Nó nói rằng giá trị đầu tiên trong hậu tố là ứng viên tốt nhất cho đến khi có bằng chứng khác. Thuật toán lưu một chỉ số chứ không sao chép giá trị nhỏ nhất, vì vậy có thể hoán đổi trực tiếp với giá trị ở cuối lượt quét.

### Vòng lặp trong:
`range(i + 1, len(my_list))` bỏ qua tiền tố đã sắp xếp và kiểm tra mọi ứng viên còn lại. Nó không thay đổi mảng khi so sánh; nó chỉ thay đổi `min_index`.

### Phép so sánh chặt:
`my_list[j] < my_list[min_index]` chỉ cập nhật ứng viên khi gặp giá trị nhỏ hơn thực sự. Nếu hai giá trị bằng nhau, ứng viên cũ vẫn được giữ. Điều đó giảm thay đổi ứng viên không cần thiết, nhưng không làm thuật toán ổn định vì một lần hoán đổi xa có thể vượt qua các giá trị bằng nhau.

### Hoán đổi có điều kiện:
`if i != min_index` tránh hoán đổi một vị trí với chính nó. Nếu vị trí hiện tại đã chứa giá trị nhỏ nhất của hậu tố, lượt đó vẫn tốn phép so sánh nhưng không ghi dữ liệu.

```
     Truoc luot i:  [ tien to da sap xep | hau to chua sap xep ]
                       khong cham lai         chi quet

     Trong khi quet: [ tien to da sap xep | cung cac gia tri   ]
                                             min_index di chuyen

     Sau khi quet:   [ tien to da sap xep | cuc tieu | phan con ]
                                             hoan doi vao i

     Bat bien: moi gia tri ben trai i da dung vi tri va da sap xep.
```

---

## 8. Phân tích Big O

### Bảng thời gian, không gian và tính ổn định:

| Phép đo | Kết quả | Giải thích |
|:---|:---|:---|
| **Thời gian tốt nhất** | **`O(n^2)`** | Danh sách đã sắp xếp vẫn quét mọi hậu tố; không có kiểm tra thoát sớm. |
| **Thời gian trung bình** | **`O(n^2)`** | Hai vòng lặp thực hiện cùng số phép so sánh với mọi thứ tự đầu vào. |
| **Thời gian xấu nhất** | **`O(n^2)`** | Danh sách đảo ngược vẫn cần quét mọi hậu tố và thường có hoán đổi. |
| **Số phép so sánh** | `n(n-1)/2` | Có `n-1` lượt, rồi `n-2`, giảm dần đến `1`. |
| **Hoán đổi tốt nhất** | `0` | Đầu vào đã sắp xếp giữ `min_index` bằng `i` ở mọi lượt. |
| **Hoán đổi trung bình** | `O(n)` | Mỗi lượt nhiều nhất một lần; dữ liệu ngẫu nhiên thường ít hơn `n` lần. |
| **Hoán đổi xấu nhất** | `n-1` | Mỗi lượt có thể chọn một cực tiểu khác vị trí hiện tại. |
| **Không gian** | **`O(1)`** | Tại chỗ; chỉ có `i`, `j`, `min_index` và `temp` là biến phụ. |
| **Tính ổn định (stability)** | **Không** | Hoán đổi xa có thể đảo thứ tự các giá trị bằng nhau. |

### Tam giác so sánh với `n = 6`:

```
     Luot 1:  *  *  *  *  *        5 phep so sanh
     Luot 2:  *  *  *  *           4 phep so sanh
     Luot 3:  *  *  *              3 phep so sanh
     Luot 4:  *  *                 2 phep so sanh
     Luot 5:  *                    1 phep so sanh
                               -------------------
                                Tong cong 15 phep

     5 + 4 + 3 + 2 + 1 = 15 = n(n - 1) / 2
     Tam giac van day ngay ca khi dau vao da sap xep.
```

### Vì sao tốt nhất, trung bình và xấu nhất đều là bậc hai:
Vòng lặp ngoài luôn tiến từ chỉ số đầu đến chỉ số kế cuối. Với mỗi `i`, vòng lặp trong luôn đi qua toàn bộ hậu tố. Thứ tự đầu vào thay đổi chỉ số được chọn và việc có hoán đổi hay không, nhưng không loại bỏ các lần quét.

---

## 9. Tính ổn định, số lần ghi và so sánh các thuật toán cơ bản

### Vì sao Sắp xếp chọn không ổn định:
Hãy tưởng tượng các bản ghi có khóa bằng nhau nhưng có nhãn nhận dạng. Ở lượt đầu dưới đây, thuật toán chọn `1` rồi hoán đổi nó với số `2` đầu tiên:

```
     Truoc:  [ (2,A), (2,B), (1,X) ]
                         ^ cuc tieu

     Hoan doi chi so 0 va chi so 2:
     Sau:    [ (1,X), (2,B), (2,A) ]

     Cac khoa bang nhau doi thu tu: A truoc B,
     nhung sau do B lai truoc A.
     Vi vay dang selection-sort bang hoan doi KHONG on dinh.
```

### So sánh các thuật toán sắp xếp cơ bản:

| Đặc điểm | Bubble Sort | Selection Sort | Insertion Sort |
|:---|:---|:---|:---|
| **Tốt nhất** | `O(n)` với thoát sớm | `O(n^2)` | `O(n)` |
| **Trung bình** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Xấu nhất** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Không gian** | `O(1)` | `O(1)` | `O(1)` |
| **Di chuyển** | Nhiều hoán đổi kề nhau | Nhiều nhất một hoán đổi mỗi lượt | Dịch giá trị lớn sang phải |
| **Số lần ghi** | Có thể là `O(n^2)` | `O(n)` lần hoán đổi | Có thể là `O(n^2)` |
| **Thích nghi (adaptive)** | Có, với thoát sớm | Không | Có |
| **Ổn định (stable)** | Có | Không | Có |
| **Vùng đã sắp xếp** | Bên phải, giá trị lớn nhất | Bên trái, cực tiểu được chọn | Bên trái, giá trị được chèn |

```
     +-------------------+-------------------+-------------------+
     |    SAP XEP NOI BOT|   SAP XEP CHON    |    SAP XEP CHEN   |
     +-------------------+-------------------+-------------------+
     | nhieu hoan doi     | tim MIN, sau do   | lay gia tri ke    |
     | ke nhau            | MOT lan hoan doi  | tiep va dich phai |
     +-------------------+-------------------+-------------------+
     | co the thich nghi  | it lan ghi nhat    | thich nghi + on   |
     | on dinh            | nhung luon quet   | dinh, tot voi     |
     |                    | het hau to        | du lieu gan sx    |
     +-------------------+-------------------+-------------------+
```

### Quy tắc lựa chọn:
* Chọn Sắp xếp chọn (Selection Sort) khi mục tiêu chính là giảm số lần hoán đổi và `n` nhỏ.
* Chọn Sắp xếp chèn (Insertion Sort) cho dữ liệu truyền đến từng phần, dữ liệu gần như đã sắp xếp hoặc dữ liệu cần ổn định.
* Chọn Sắp xếp nổi bọt (Bubble Sort) chủ yếu để học hoán đổi kề nhau hoặc minh họa bất biến vòng lặp.
* Chọn thuật toán `O(n log n)` cho các bộ dữ liệu tổng quát và lớn.

Bài học lâu dài của Sắp xếp chọn (Selection Sort) rất rõ: số phép so sánh có thể nhiều, trong khi số lần ghi vẫn bị giới hạn. Bất biến tiền tố đã sắp xếp và vòng quét `min_index` là nền tảng để hiểu các kỹ thuật chọn và phân hoạch nâng cao hơn.

---

**Bước tiếp theo:** Học **Sắp xếp chèn (Insertion Sort)**, cũng mở rộng một tiền tố đã sắp xếp nhưng chèn từng giá trị mới bằng cách dịch các giá trị lớn hơn sang phải thay vì chọn cực tiểu rồi hoán đổi.
