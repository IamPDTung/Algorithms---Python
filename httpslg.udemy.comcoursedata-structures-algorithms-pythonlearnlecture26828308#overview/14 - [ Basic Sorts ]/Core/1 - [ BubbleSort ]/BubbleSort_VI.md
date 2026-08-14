
---

# Sắp xếp nổi bọt (Bubble Sort)

## 1. Sắp xếp nổi bọt là gì?

**Sắp xếp nổi bọt (Bubble Sort)** là thuật toán sắp xếp dựa trên so sánh (comparison sort) đơn giản nhất. Nó lặp lại việc duyệt qua danh sách, so sánh các **cặp phần tử kề nhau (adjacent pairs)**, và **hoán đổi (swap)** chúng nếu chúng sai thứ tự. Sau mỗi lượt duyệt (pass), **giá trị lớn nhất chưa được sắp xếp** sẽ "nổi lên" đúng vị trí cuối cùng của nó ở cuối danh sách — giống như bọt khí nổi lên mặt nước.

### Ý tưởng chính:
> So sánh hai phần tử cạnh nhau. Nếu phần tử bên trái lớn hơn, hoán đổi chúng. Cứ tiếp tục. Sau mỗi lượt, thêm một giá trị ở cuối được khóa vĩnh viễn vào đúng vị trí.

### Đặc điểm cốt lõi:
* **Sắp xếp bằng so sánh (comparison sort)** — mọi quyết định chỉ dựa trên việc so sánh hai phần tử.
* **Chỉ hoán đổi cặp kề nhau** — mỗi phần tử di chuyển đúng một vị trí sau mỗi lần hoán đổi.
* **Tại chỗ (in-place)** — không cần mảng phụ, mọi thứ diễn ra ngay trong danh sách gốc.
* **Vùng đã sắp xếp (sorted region) lớn dần từ bên PHẢI** — phần đuôi của danh sách dần được lấp đầy bởi các giá trị đúng vị trí cuối cùng.

```
        +--------------------------------------------------+
        |            SAP XEP NOI BOT (BUBBLE SORT)         |
        +--------------------------------------------------+
        |                                                  |
        |   Lap lai:                                       |
        |     +----------------------------------------+   |
        |     |  So sanh cap (j, j+1)                  |   |
        |     |  neu trai > phai  ->  HOAN DOI         |   |
        |     +----------------------------------------+   |
        |                                                  |
        |   Ket qua moi luot:                              |
        |     Gia tri LON NHAT chua sap xep ve cuoi        |
        |                                                  |
        |   [ vung chua sap xep | vung da sap xep -> ]     |
        |        thu nho <-          lon dan ->            |
        +--------------------------------------------------+
```

---

## 2. Tại sao thuật toán này được tạo ra?

Sắp xếp nổi bọt về mặt lịch sử là **thuật toán sắp xếp nhập môn** — thuật toán sắp xếp đầu tiên mà hầu như mọi lập trình viên đều học:

* **Dễ hiểu** — logic chỉ là "so sánh hai phần tử cạnh nhau, hoán đổi nếu sai".
* **Dễ cài đặt** — hai vòng lặp lồng nhau (nested loops) và một biến `temp`. Vậy thôi.
* **Dễ lần vết (trace)** — bạn có thể quan sát từng lần hoán đổi diễn ra theo từng bước.

Nó **hiếm khi được dùng trong thực tế (production)** — đơn giản vì quá chậm với dữ liệu lớn. Giá trị thực sự của nó nằm ở **mục đích giáo dục**: nó là **chuẩn mực (baseline)** mà mọi thuật toán sắp xếp khác được đem ra so sánh. Khi bạn học Selection Sort, Insertion Sort, Merge Sort hay Quick Sort, câu hỏi đầu tiên luôn là: *"Nó nhanh hơn Bubble Sort bao nhiêu?"*

```
        +--------------------------------------------------+
        |  VI SAO BUBBLE SORT QUAN TRONG                   |
        +--------------------------------------------------+
        |                                                  |
        |   1. Thuat toan sap xep dau tien moi nguoi hoc   |
        |   2. Day co che HOAN DOI (bien temp)             |
        |   3. Day bat bien vong lap (loop invariant)      |
        |   4. La CHUAN MUC ma cac thuat toan khac vuot    |
        |                                                  |
        |   Dung thuc te:  gan nhu khong                   |
        |   Gia tri day hoc:  rat lon                      |
        +--------------------------------------------------+
```

---

## 3. Nó giải quyết những bài toán nào?

* **Sắp xếp dữ liệu rất nhỏ** — với một vài phần tử, sự đơn giản thắng tất cả.
* **Dữ liệu gần như đã sắp xếp (nearly-sorted)** — với tối ưu chuẩn (dừng nếu một lượt không có hoán đổi nào), nó nhận ra dữ liệu đã sắp xếp trong `O(n)`.
* **Dạy cơ chế hoán đổi** — mẫu hoán đổi bằng `temp` xuất hiện khắp nơi trong các thuật toán.
* **Dạy bất biến vòng lặp (loop invariant)** — "sau lượt k, k phần tử cuối đã ở vị trí cuối cùng" là một bất biến đầu tiên hoàn hảo để học.

### Trong khóa học này:
Cùng một logic "nổi bọt" được tái sử dụng để sắp xếp một **Danh sách liên kết (Linked List)** — xem **`Bubble Sort of LL`** trong thư mục `Interview`, nơi bạn đẩy các giá trị "nổi" dọc theo chuỗi các node thay vì mảng.

```
        +--------------------------------------------------+
        |  BUBBLE SORT PHU HOP O DAU                       |
        +--------------------------------------------------+
        |                                                  |
        |   Danh sach nho (n < 10) .............. OK       |
        |   Gan nhu da sap xep .................. OK (O(n))|
        |   Day hoan doi/bat bien ............... HOAN HAO |
        |   Sap xep Linked List (khoa hoc) ...... CO       |
        |   Du lieu lon ngau nhien .............. KHONG    |
        +--------------------------------------------------+
```

---

## 4. Nó hoạt động như thế nào?

Ta lần vết đúng code của khóa học trên danh sách **`[4, 2, 6, 5, 1, 3]`**.

Vòng lặp ngoài chạy `i` từ `len-1` xuống `1`. Vòng lặp trong chạy `j` từ `0` đến `i-1`, so sánh cặp kề nhau `(j, j+1)`. Hãy chú ý vòng lặp trong **thu nhỏ lại một đơn vị** sau mỗi lượt — vì phần đuôi đã được sắp xếp rồi.

### LƯỢT 1 — mọi phép so sánh và hoán đổi kề nhau (i = 5):

```
    Bat dau: [ 4 , 2 , 6 , 5 , 1 , 3 ]

    j=0:  so sanh 4 va 2   ->  4 > 2  ->  HOAN DOI
          [ 2 , 4 , 6 , 5 , 1 , 3 ]

    j=1:  so sanh 4 va 6   ->  4 < 6  ->  khong doi
          [ 2 , 4 , 6 , 5 , 1 , 3 ]

    j=2:  so sanh 6 va 5   ->  6 > 5  ->  HOAN DOI
          [ 2 , 4 , 5 , 6 , 1 , 3 ]

    j=3:  so sanh 6 va 1   ->  6 > 1  ->  HOAN DOI
          [ 2 , 4 , 5 , 1 , 6 , 3 ]

    j=4:  so sanh 6 va 3   ->  6 > 3  ->  HOAN DOI
          [ 2 , 4 , 5 , 1 , 3 , 6 ]
                                   ^
                    6 da NOI LEN dung vi tri cuoi cung!
```

### Mảng SAU MỖI LƯỢT — quan sát vùng đã sắp xếp lớn dần:

```
    Bat dau:      [ 4 , 2 , 6 , 5 , 1 , 3 ]
                   <----- chua sap xep ---->

    Sau luot 1:   [ 2 , 4 , 5 , 1 , 3 | 6 ]
                   <-- chua sap xep --> |da sx|

    Sau luot 2:   [ 2 , 4 , 1 , 3 | 5 , 6 ]
                   <- chua sap xep -> | da sx |

    Sau luot 3:   [ 2 , 1 , 3 | 4 , 5 , 6 ]
                   <- chua sx --> |  da sx    |

    Sau luot 4:   [ 1 , 2 | 3 , 4 , 5 , 6 ]
                   chua sx  |     da sx      |

    Sau luot 5:   [ 1 | 2 , 3 , 4 , 5 , 6 ]
                           | TAT CA DA SX    |

    Ket qua:      [ 1 , 2 , 3 , 4 , 5 , 6 ]
```

### Vòng lặp trong thu nhỏ sau mỗi lượt:

```
    Luot 1:  j chay 0..4   (5 phep so sanh)  -> khoa vi tri 6
    Luot 2:  j chay 0..3   (4 phep so sanh)  -> khoa vi tri 5
    Luot 3:  j chay 0..2   (3 phep so sanh)  -> khoa vi tri 4
    Luot 4:  j chay 0..1   (2 phep so sanh)  -> khoa vi tri 3
    Luot 5:  j chay 0..0   (1 phep so sanh)  -> khoa vi tri 2

    Tong phep so sanh: 5 + 4 + 3 + 2 + 1 = 15  =  n*(n-1)/2

    [ vung chua sap xep thu nho | vung da sap xep lon dan ]
             <------------- n-1 phan tu ----------------->
```

### Cơ chế hoán đổi chi tiết:

```
    De hoan doi my_list[j] va my_list[j+1] ta can bien TEMP,
    neu khong mot gia tri se bi ghi de va mat luon:

        temp = my_list[j]           <- cuu gia tri ben trai
        my_list[j] = my_list[j+1]   <- ben phai chuyen sang trai
        my_list[j+1] = temp         <- gia tri da cuu sang phai

        j       j+1                 j       j+1
      +-----+ +-----+             +-----+ +-----+
      |  4  | |  2  |    ==>      |  2  | |  4  |
      +-----+ +-----+             +-----+ +-----+
        |                            ^
        +-- duoc luu trong temp -----+
```

---

## 5. Code

Đây là code lồi giải thực tế từ khóa học (`SOLUTION-Bubble_Sort.py`):

```python
def bubble_sort(my_list):
    for i in range(len(my_list) - 1, 0 ,-1):
        for j in range(i):
            if my_list[j] > my_list[j+1]:
                temp = my_list[j]
                my_list[j] = my_list[j+1]
                my_list[j+1] = temp
    return my_list





print(bubble_sort([4,2,6,5,1,3]))
```

```
    EXPECTED OUTPUT:
    ----------------
    [1, 2, 3, 4, 5, 6]
```

### Phân tích từng dòng:

```
    for i in range(len(my_list) - 1, 0, -1):
        i dem NGUOC tu 5 ve 1.
        i = ranh gioi giua vung chua sap xep va da sap xep.

        for j in range(i):
            j chay 0 .. i-1, chi cham vao vung CHUA sap xep.

            if my_list[j] > my_list[j+1]:
                Cap ke nhau sai thu tu -> HOAN DOI.
                Dung ">" (khong phai ">=") nghia la cac phan tu
                bang nhau khong bao gio bi hoan doi
                -> Bubble Sort la ON DINH (stable).
```

---

## 6. Phân tích Big O

### Độ phức tạp thờ i gian (Time Complexity):

| Trường hợp | Số phép so sánh | Số lần hoán đổi | Độ phức tạp | Lý do |
|:---|:---|:---|:---|:---|
| **Tốt nhất** (đã sắp xếp) | `n-1` | `0` | **`O(n)`** | Với kiểm tra "không hoán đổi => dừng", một lượt đủ để kết luận đã sắp xếp (ghi chú của khóa học) |
| **Trung bình** (ngẫu nhiên) | `n(n-1)/2` | ~`n(n-1)/4` | **`O(n^2)`** | Hai vòng lặp lồng nhau trên vùng thu nhỏ dần |
| **Xấu nhất** (ngược hoàn toàn) | `n(n-1)/2` | `n(n-1)/2` | **`O(n^2)`** | Mọi phép so sánh đều gây ra hoán đổi |

### Độ phức tạp không gian (Space Complexity):

| Độ phức tạp | Giá trị | Lý do |
|:---|:---|:---|
| **Không gian** | **`O(1)`** | Tại chỗ (in-place) — chỉ cần biến `temp`, không cần mảng phụ |

### Hình dung khối lượng công việc O(n^2):

```
    Tam giac so sanh voi n = 6:

    Luot 1:  *  *  *  *  *        (5)
    Luot 2:  *  *  *  *           (4)
    Luot 3:  *  *  *              (3)
    Luot 4:  *  *                 (2)
    Luot 5:  *                    (1)

    Dien tich tam giac ~ n^2 / 2  =>  O(n^2)
    Gap doi dau vao, cong viec tang GAP BON lan.
```

---

## 7. So sánh Bubble Sort với các thuật toán sắp xếp cơ bản khác

Cả ba thuật toán sắp xếp cơ bản đều là `O(n^2)` — nhưng khác nhau ở các chi tiết:

| Đặc điểm | Bubble Sort | Selection Sort | Insertion Sort |
|:---|:---|:---|:---|
| **Thờ i gian (tốt nhất)** | `O(n)` | `O(n^2)` | `O(n)` |
| **Thờ i gian (trung bình)** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Thờ i gian (xấu nhất)** | `O(n^2)` | `O(n^2)` | `O(n^2)` |
| **Không gian** | `O(1)` | `O(1)` | `O(1)` |
| **Số lần hoán đổi** | Nhiều — tới `O(n^2)` | Tối thiểu — `O(n)` tổng cộng | Dồn phần tử — tới `O(n^2)` lần ghi |
| **Thích nghi (adaptive)** — nhanh khi gần sắp xếp | Có (với thoát sớm) | Không | Có |
| **Ổn định (stable)** | Có | Không | Có |
| **Vùng sắp xếp lớn từ** | Phải (max nổi lên) | Trái (chọn min) | Trái (chèn lá bài) |

```
    +-------------------+-------------------+-------------------+
    |    BUBBLE SORT    |  SELECTION SORT   |  INSERTION SORT   |
    +-------------------+-------------------+-------------------+
    | doi cho hang xom  | tim MIN, doi cho  | chen la bai ke    |
    | nhieu lan         | MOT lan moi luot  | tiep vao tay bai  |
    +-------------------+-------------------+-------------------+
    | tot nhat O(n)     | luon luon O(n^2)  | tot nhat O(n)     |
    | thay giao tuyet   | it lan ghi nhat   | tot nhat thuc te  |
    +-------------------+-------------------+-------------------+
```

---

**Bước tiếp theo:** Bây giờ hãy xem **Sắp xếp chọn (Selection Sort)** — "anh em họ" của Bubble Sort nhưng chỉ thực hiện MỘT lần hoán đổi mỗi lượt thay vì nhiều lần!
