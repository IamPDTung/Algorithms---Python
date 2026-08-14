
---

# Sắp xếp chèn (Insertion Sort)

## 1. Sắp xếp chèn là gì?

**Sắp xếp chèn (Insertion Sort)** là thuật toán sắp xếp dựa trên so sánh (comparison-based sorting algorithm), xây dựng một tiền tố đã sắp xếp từ trái sang phải. Ở mỗi lượt, nó lấy giá trị kế tiếp, tạm giữ trong `temp`, dịch mọi giá trị lớn hơn trong tiền tố sang phải một vị trí, rồi đặt `temp` vào khoảng trống.

### Ý tưởng chính:
> Giữ phần bên trái đã sắp xếp. Lấy một giá trị mới từ bên phải và chèn nó vào đúng vị trí trong phần đã sắp xếp.

### Đặc điểm cốt lõi:
* **Sắp xếp bằng so sánh (comparison sort)** - thứ tự được tìm bằng cách so sánh giá trị hiện tại với các giá trị trước đó.
* **Tại chỗ (in-place)** - dùng danh sách gốc và một số biến phụ cố định.
* **Thích nghi (adaptive)** - làm rất ít việc khi đầu vào đã hoặc gần như đã sắp xếp.
* **Trực tuyến (online)** - có thể giữ tiền tố đã sắp xếp trong khi các giá trị đến từng phần.
* **Ổn định (stable)** - các giá trị bằng nhau không vượt qua nhau khi phép so sánh là chặt.
* **Vùng đã sắp xếp lớn dần từ BÊN TRÁI** - mỗi lượt mở rộng tiền tố thêm một phần tử.

```
        +--------------------------------------------------+
        |              SAP XEP CHEN (INSERTION SORT)      |
        +--------------------------------------------------+
        |                                                  |
        |   [ tien to da sx | hien tai | hau to chua sx ]  |
        |          ^             ^                        |
        |       giu thu tu     temp                        |
        |                                                  |
        |   Dich cac gia tri lon hon sang phai             |
        |   Chen temp vao vi tri mo ra                     |
        |                                                  |
        |   tien to da sap xep lon dan ->                  |
        +--------------------------------------------------+
```

---

## 2. Hình ảnh những lá bài trong tay (Playing-Card Analogy)

Insertion Sort hoạt động giống như một người sắp các lá bài trong tay. Các lá đang cầm đã được sắp xếp. Khi có lá mới, người chơi so sánh nó với các lá từ phải sang trái, dịch các lá lớn hơn sang phải một ô, rồi chèn lá mới vào khoảng trống.

```
     Cac la da co:       [ 2 , 4 , 6 ]   da sap xep
     La moi:                         5   temp

     So sanh 5 voi 6: dich 6 sang phai
     Tay bai:                [ 2 , 4 , 6 , 6 ]

     So sanh 5 voi 4: dung; 4 khong lon hon
     Chen 5 sau 4:
     Tay bai:                [ 2 , 4 , 5 , 6 ]
```

Hình ảnh này giải thích vì sao thuật toán quét ngược: vị trí chèn đúng được tìm bằng cách đi sang trái trong bàn tay đã có thứ tự, chứ không phải bằng cách tìm trong hậu tố chưa sắp xếp.

---

## 3. Tại sao thuật toán này được tạo ra?

Sắp xếp chèn (Insertion Sort) được tạo ra để đáp ứng các ràng buộc khác với Sắp xếp chọn (Selection Sort). Nó không cố giảm số phép so sánh trên mọi đầu vào. Thay vào đó, lượng công việc phụ thuộc vào việc mỗi giá trị cách vị trí đúng của nó bao xa.

### Ba động lực chính:
1. **Tính thích nghi (adaptive)** - dữ liệu gần như đã sắp xếp chỉ cần vài lần dịch.
2. **Tính trực tuyến (online)** - có thể duy trì kết quả đã sắp xếp khi các giá trị đến từng phần.
3. **Tính ổn định (stability)** - các bản ghi có khóa bằng nhau vẫn giữ thứ tự ban đầu.

Thuật toán cũng đơn giản, tại chỗ và thực tế với danh sách nhỏ. Nhiều cài đặt sắp xếp trong thực tế dùng chiến lược Sắp xếp chèn (Insertion Sort) cho các phân mảng nhỏ vì hằng số thời gian thấp, dù trường hợp xấu nhất vẫn là bậc hai.

```
     DIEU KIEN DAU VAO       PHAN UNG CUA SAP XEP CHEN
     -----------------       ---------------------------
     da sap xep               so sanh, khong dich
     gan nhu da sap xep       vai lan dich ngan
     gia tri den dan           chen moi gia tri ngay
     ban ghi khoa bang nhau    giu thu tu ban dau
     dao nguoc                 nhieu lan dich, O(n^2)
```

---

## 4. Nó giải quyết những bài toán nào?

Insertion Sort đặc biệt hữu ích khi đầu vào nhỏ, đến theo thời gian hoặc gần như đã sắp xếp. Nó giải quyết việc mở rộng một tập hợp có thứ tự mà không cần tạo tập hợp thứ hai.

### Các tình huống phù hợp:
* **Mảng gần như đã sắp xếp (nearly sorted)** với ít nghịch thế.
* **Luồng trực tuyến (online stream)**, trong đó mỗi giá trị mới cần được đặt ngay.
* **Sắp xếp ổn định các bản ghi**, khi danh tính của những khóa bằng nhau có ý nghĩa.
* **Các phân mảng nhỏ** bên trong những thuật toán sắp xếp lai nâng cao.
* **Sắp xếp tại chỗ** khi cần không gian phụ `O(1)`.

### Hạn chế:
* Đầu vào đảo ngược khiến mỗi lượt dịch mọi giá trị trước đó.
* Nó không phải lựa chọn tốt nhất cho mảng ngẫu nhiên lớn.
* Trung bình nó vẫn mất thời gian `O(n^2)`.
* Nó không có bảo đảm xấu nhất `O(n log n)` như Sắp xếp trộn (Merge Sort) hoặc Sắp xếp vun đống (Heap Sort).

```
        +--------------------------------------------------+
         |          SAP XEP CHEN PHU HOP O DAU             |
        +--------------------------------------------------+
        |  Dau vao nho ................................ CO |
        |  Dau vao gan nhu da sap xep ................. CO |
        |  Gia tri den truc tuyen ...................... CO |
        |  Khoa bang nhau phai giu thu tu .............. CO |
        |  Dau vao ngau nhien lon .................... KHONG|
        |  Dau vao dao nguoc .......................... CHAM|
        +--------------------------------------------------+
```

---

## 5. Bất biến tiền tố đã sắp xếp

Bất biến quan trọng nhất là:

> Trước lượt `i`, lát cắt `my_list[0:i]` đã sắp xếp. Sau lượt `i`, lát cắt `my_list[0:i+1]` đã sắp xếp và chứa đúng các giá trị như trước lượt đó.

Phần tử ở chỉ số `i` là giá trị kế tiếp cần chèn. Các giá trị trước nó đã sắp xếp, còn các giá trị sau nó vẫn thuộc hậu tố chưa sắp xếp.

```
     Truoc luot i:
     [ tien to da sx dai i | gia tri can chen | hau to chua sx ]
       <------ bat bien ----->       temp

     Trong luot:
     [ tien to da sx | gia tri da dich | o trong | hau to chua sx ]
                          gia tri lon -> phai

     Sau luot i:
     [ tien to da sx dai i+1 | hau to chua sap xep ]
       <------- bat bien duoc khoi phuc ------->
```

### Vì sao dịch vẫn đúng:
Tiền tố bắt đầu trong trạng thái đã sắp xếp. Dịch một giá trị lớn hơn sang phải một vị trí không phá thứ tự giữa các giá trị còn ở bên trái. Khi gặp giá trị đầu tiên không lớn hơn `temp`, `temp` thuộc ngay sau giá trị đó. Nếu mọi giá trị trong tiền tố đều lớn hơn, `temp` thuộc chỉ số `0`.

### Ý nghĩa các ranh giới:
* `i` đánh dấu giá trị chưa sắp xếp đầu tiên.
* `temp` giữ giá trị đó trong khi các vị trí của mảng được sắp xếp lại.
* `j` đi ngược qua tiền tố đã sắp xếp.
* `j + 1` là vị trí chèn khi vòng lặp dừng.

---

## 6. Lần vết từng lượt trên `[4, 2, 6, 5, 1, 3]`

Giá trị đầu tiên `4` tạo thành tiền tố đã sắp xếp gồm một phần tử. Vòng lặp ngoài sau đó xử lý `i = 1` đến `i = 5`. Mỗi lượt dưới đây đều cho thấy các lần dịch, vị trí chèn và trạng thái đầy đủ của mảng sau lượt đó.

### LƯỢT 1 - chèn `2` tại `i = 1`

Tiền tố đã sắp xếp là `[4]`. Vì `2 < 4`, dịch `4` sang phải rồi đặt `2` ở chỉ số `0`.

```
     Truoc:   [ 4 | 2 , 6 , 5 , 1 , 3 ]
                da sx  temp

     temp = 2, j = 0
     2 < 4 -> dich 4 sang phai:
              [ 4 , 4 , 6 , 5 , 1 , 3 ]
     ghi temp tai j = 0:
              [ 2 , 4 , 6 , 5 , 1 , 3 ]
     vi tri chen: 0
```

Sau lượt 1:

```
     [ 2 , 4 | 6 , 5 , 1 , 3 ]
       tien to da sx | hau to chua sx
```

### LƯỢT 2 - chèn `6` tại `i = 2`

Tiền tố `[2, 4]` đã nhỏ hơn `6`, nên không cần dịch.

```
     Truoc:   [ 2 , 4 | 6 , 5 , 1 , 3 ]
                       temp = 6, j = 1

     6 < 4 -> sai
     Dung ngay; vi tri chen: j + 1 = 2
```

Sau lượt 2:

```
     [ 2 , 4 , 6 | 5 , 1 , 3 ]
       tien to da sx | hau to chua sx
```

### LƯỢT 3 - chèn `5` tại `i = 3`

Phép so sánh đầu tiên là với `6`, nên `6` được dịch sang phải. Phép so sánh tiếp theo là với `4`, khiến việc quét dừng lại.

```
     Truoc:   [ 2 , 4 , 6 | 5 , 1 , 3 ]
                             temp = 5, j = 2

     5 < 6 -> dich 6 sang phai:
              [ 2 , 4 , 6 , 6 , 1 , 3 ]
     ghi temp tai chi so 2:
              [ 2 , 4 , 5 , 6 , 1 , 3 ]
     j thanh 1; 5 < 4 -> sai
     vi tri chen: 2
```

Sau lượt 3:

```
     [ 2 , 4 , 5 , 6 | 1 , 3 ]
       tien to da sx    | hau to chua sx
```

### LƯỢT 4 - chèn `1` tại `i = 4`

Mọi giá trị trong tiền tố đều lớn hơn `1`, nên bốn giá trị được dịch sang phải. Vị trí chèn là đầu danh sách.

```
     Truoc:   [ 2 , 4 , 5 , 6 | 1 , 3 ]
                                  temp = 1

     dich 6: [ 2 , 4 , 5 , 6 , 6 , 3 ] -> ghi 1 tai chi so 3
              [ 2 , 4 , 5 , 1 , 6 , 3 ]
     dich 5: [ 2 , 4 , 5 , 5 , 6 , 3 ] -> ghi 1 tai chi so 2
              [ 2 , 4 , 1 , 5 , 6 , 3 ]
     dich 4: [ 2 , 4 , 4 , 5 , 6 , 3 ] -> ghi 1 tai chi so 1
              [ 2 , 1 , 4 , 5 , 6 , 3 ]
     dich 2: [ 2 , 2 , 4 , 5 , 6 , 3 ] -> ghi 1 tai chi so 0
              [ 1 , 2 , 4 , 5 , 6 , 3 ]

     vi tri chen: 0
```

Sau lượt 4:

```
     [ 1 , 2 , 4 , 5 , 6 | 3 ]
       tien to da sx      | hau to chua sx
```

### LƯỢT 5 - chèn `3` tại `i = 5`

Các giá trị `6`, `5` và `4` lớn hơn `3` nên được dịch sang phải. Giá trị `2` không lớn hơn, nên vị trí chèn là sau `2`.

```
     Truoc:   [ 1 , 2 , 4 , 5 , 6 | 3 ]
                                  temp = 3

     dich 6: [ 1 , 2 , 4 , 5 , 6 , 6 ] -> ghi 3 tai chi so 4
              [ 1 , 2 , 4 , 5 , 3 , 6 ]
     dich 5: [ 1 , 2 , 4 , 5 , 5 , 6 ] -> ghi 3 tai chi so 3
              [ 1 , 2 , 4 , 3 , 5 , 6 ]
     dich 4: [ 1 , 2 , 4 , 4 , 5 , 6 ] -> ghi 3 tai chi so 2
              [ 1 , 2 , 3 , 4 , 5 , 6 ]
     j = 1; 3 < 2 -> sai

     vi tri chen: 2
```

Sau lượt 5:

```
     [ 1 , 2 , 3 , 4 , 5 , 6 ]
       tien to da sap xep phu het danh sach
```

### Toàn bộ trạng thái mảng sau MỖI lượt:

```
     Bat dau:       [ 4 , 2 , 6 , 5 , 1 , 3 ]
     Sau luot 1:    [ 2 , 4 | 6 , 5 , 1 , 3 ]
     Sau luot 2:    [ 2 , 4 , 6 | 5 , 1 , 3 ]
     Sau luot 3:    [ 2 , 4 , 5 , 6 | 1 , 3 ]
     Sau luot 4:    [ 1 , 2 , 4 , 5 , 6 | 3 ]
     Sau luot 5:    [ 1 , 2 , 3 , 4 , 5 , 6 ]

     Tien to da sx tang dung mot vi tri sau moi luot.
```

---

## 7. Code thực tế của khóa học

Đây là code lời giải thực tế từ `SOLUTION-Insertion_Sort.py`. Code được chép nguyên văn, bao gồm vị trí của `j > -1` trong điều kiện `while` và các phép ghi `temp` rõ ràng trong mỗi lần dịch.

```python
def insertion_sort(my_list):
    for i in range(1, len(my_list)):
        temp = my_list[i]
        j = i-1
        while temp < my_list[j] and j > -1:
            my_list[j+1] = my_list[j] 
            my_list[j] = temp
            j -= 1
    return my_list





print(insertion_sort([4,2,6,5,1,3]))



"""
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6]
 """

```

```
     LUONG THUC THI
     --------------
     lay my_list[i] lam temp
                |
                v
     so sanh nguoc qua tien to da sx
                |
           gia tri lon hon?
            /           \
          co             khong
           |               |
       dich sang phai     dung
           |               |
           +------> chen temp
                          |
                          v
                   tien to lai da sx
```

### Kết quả mong đợi:

```
     [1, 2, 3, 4, 5, 6]
```

---

## 8. Logic từng dòng

### Vòng lặp ngoài:
`range(1, len(my_list))` bắt đầu ở chỉ số `1` vì tiền tố một phần tử tại chỉ số `0` đã được sắp xếp. Mỗi `i` mới xác định giá trị kế tiếp cần chèn.

### Lưu `temp`:
`temp = my_list[i]` giữ lại giá trị trong khi các giá trị lớn hơn trong tiền tố di chuyển sang phải. Nếu không lưu, lần dịch đầu tiên có thể ghi đè phần tử cần chèn.

### Cho `j` đi lùi:
`j = i - 1` trỏ tới giá trị ngoài cùng bên phải trong tiền tố đã sắp xếp. Thuật toán so sánh với giá trị này trước vì đây là vị trí chèn gần nhất có thể.

### Điều kiện `while`:
`temp < my_list[j]` nghĩa là chỉ các giá trị lớn hơn `temp` mới được dịch sang phải. Code nguồn đặt `j > -1` ở vế thứ hai. Python đánh giá phép so sánh trước rồi mới kiểm tra biên; khi `j` thành `-1`, điều kiện bảo vệ ngăn thân vòng lặp chạy. Code được giữ nguyên đúng như khóa học cung cấp.

### Phép dịch:
`my_list[j+1] = my_list[j]` sao chép một giá trị lớn hơn sang phải một vị trí. `my_list[j] = temp` đặt giá trị đã lưu vào vị trí vừa mở ở bước đó. Sau đó `j -= 1` tiếp tục đi sang trái.

```
     Mot lan dich, voi temp = 5:

     truoc:        [ 2 , 4 , 6 , 6 ]
                               ^ j+1
                           j = 2
     ghi sang phai: [ 2 , 4 , 6 , 6 ]
     ghi temp:      [ 2 , 4 , 5 , 6 ]
                         ^ temp dang o day

     Neu gia tri tiep theo van lon hon, qua trinh lap lai lui mot o.
```

---

## 9. Phân tích Big O

### Bảng thời gian, không gian, tính ổn định và tính thích nghi:

| Phép đo | Kết quả | Giải thích |
|:---|:---|:---|
| **Thời gian tốt nhất** | **`O(n)`** | Danh sách đã sắp xếp chỉ có một phép so sánh thất bại mỗi lượt và không dịch. |
| **Thời gian trung bình** | **`O(n^2)`** | Danh sách ngẫu nhiên có số nghịch thế và số lần dịch kỳ vọng bậc hai. |
| **Thời gian xấu nhất** | **`O(n^2)`** | Thứ tự đảo ngược dịch mọi giá trị của tiền tố ở mọi lượt. |
| **Số lần dịch tốt nhất** | `0` | Mỗi giá trị mới đã đứng sau một giá trị không lớn hơn nó. |
| **Số lần dịch trung bình** | `O(n^2)` | Số nghịch thế kỳ vọng tỉ lệ với `n^2`. |
| **Số lần dịch xấu nhất** | `n(n-1)/2` | Các lượt dịch `1 + 2 + ... + (n-1)` giá trị. |
| **Không gian** | **`O(1)`** | Tại chỗ; chỉ dùng số lượng biến phụ không đổi. |
| **Tính ổn định (stability)** | **Có** | Điều kiện `<` không đưa giá trị bằng nhau vượt qua phần tử trước nó. |
| **Tính thích nghi (adaptive)** | **Có** | Công việc phụ thuộc vào mức độ rối hiện có, đặc biệt là nghịch thế. |
| **Tính trực tuyến (online)** | **Có** | Có thể duy trì tiền tố đã sắp xếp khi giá trị mới đến. |

### Tam giác công việc với thứ tự đảo ngược và `n = 6`:

```
     Chen phan tu 2:  *                 1 lan dich
     Chen phan tu 3:  *  *              2 lan dich
     Chen phan tu 4:  *  *  *           3 lan dich
     Chen phan tu 5:  *  *  *  *        4 lan dich
     Chen phan tu 6:  *  *  *  *  *     5 lan dich
                                      -----------
                                       Tong 15 lan dich

     1 + 2 + 3 + 4 + 5 = 15 = n(n - 1) / 2
```

### Nghịch thế giải thích tính thích nghi:
Một **nghịch thế (inversion)** là cặp `(p, q)` với `p < q` nhưng `my_list[p] > my_list[q]`. Insertion Sort thực hiện gần một lần dịch sang phải cho mỗi nghịch thế. Danh sách gần như đã sắp xếp có ít nghịch thế nên ít việc; danh sách đảo ngược có số nghịch thế lớn nhất.

---

## 10. So sánh Insertion Sort với Bubble và Selection Sort

Cả ba thuật toán cơ bản đều là thuật toán sắp xếp bằng so sánh và có thể mất `O(n^2)`, nhưng chúng phản ứng với sự lộn xộn của đầu vào khác nhau: Sắp xếp nổi bọt (Bubble Sort), Sắp xếp chọn (Selection Sort) và Sắp xếp chèn (Insertion Sort).
| Đặc điểm | Bubble Sort | Selection Sort | Insertion Sort |
|:---|:---|:---|:---|
| **Tốt nhất** | `O(n)` với thoát sớm | `O(n^2)` | `O(n)` |
| **Trung bình** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Xấu nhất** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Không gian** | `O(1)` | `O(1)` | `O(1)` |
| **Di chuyển chính** | Lặp lại hoán đổi kề nhau | Chọn cực tiểu rồi hoán đổi một lần | Dịch giá trị lớn sang phải |
| **Số lần ghi** | Có thể `O(n^2)` | Nhiều nhất `O(n)` lần hoán đổi | Có thể `O(n^2)` lần dịch |
| **Thích nghi** | Có với thoát sớm | Không | Có, mạnh |
| **Trực tuyến** | Không ở dạng code cơ bản | Không | Có |
| **Ổn định** | Có | Không | Có |
| **Vùng đã sắp xếp** | Bên phải, giá trị lớn | Bên trái, cực tiểu được chọn | Bên trái, tiền tố được chèn |

```
     +-------------------+-------------------+-------------------+
     |    SAP XEP NOI BOT|   SAP XEP CHON    |    SAP XEP CHEN   |
     +-------------------+-------------------+-------------------+
     | so sanh ke nhau    | tim MIN toan cuc  | so sanh nguoc     |
     | va hoan doi nhieu  | roi ghi mot lan   | va dich cuc bo    |
     +-------------------+-------------------+-------------------+
     | tot hon voi thoat  | bo qua muc do da  | tot hon nho vao   |
     | som                | sap xep hien co   | thu tu hien co    |
     +-------------------+-------------------+-------------------+
```

### Quy tắc lựa chọn:
* Chọn Insertion Sort cho dữ liệu nhỏ, gần như đã sắp xếp, đến theo luồng hoặc cần ổn định.
* Chọn Selection Sort khi số lần hoán đổi quan trọng hơn tốc độ thích nghi.
* Chọn Bubble Sort chủ yếu để minh họa hoán đổi kề nhau và phần đuôi đã sắp xếp lớn dần.
* Chọn phương pháp `O(n log n)` cho dữ liệu lớn và tổng quát.

Bài học trung tâm của Insertion Sort là tiền tố đã sắp xếp chứa thông tin hữu ích. Thay vì liên tục tìm lại cực tiểu toàn cục, thuật toán giữ thứ tự đã xây dựng và chỉ sửa vị trí của giá trị kế tiếp.

---

**Bước tiếp theo:** So sánh các thuật toán cơ bản này với Merge Sort để thấy việc chia đầu vào có thể cải thiện giới hạn thời gian bậc hai thành `O(n log n)` như thế nào.
