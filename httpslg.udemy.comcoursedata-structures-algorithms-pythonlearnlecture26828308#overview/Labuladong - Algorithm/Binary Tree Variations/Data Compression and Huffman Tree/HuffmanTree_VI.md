# Nén dữ liệu và cây Huffman

## 1. Mục tiêu

Cây Huffman là một cây mã nhị phân tiền tố tự do (prefix-free) tối ưu được
xây dựng từ tần suất của các ký tự. Mỗi lá chứa một ký tự và tần suất của
nó; mỗi nút trong chứa tổng tần suất của hai con. Mã của một ký tự là chuỗi
bit dọc theo đường đi từ gốc tới lá của nó, nhờ đó ký tự xuất hiện nhiều
được mã NGẮN và ký tự hiếm được mã DÀI hơn, trong khi không mã nào là tiền
tố của mã khác.

Vì sao nó ra đời: các mã hóa độ dài cố định như ASCII tốn 8 bit cho mọi ký
tự, dù ký tự đó xuất hiện 1000 lần hay chỉ một lần. Điều đó lãng phí bit cho
những ký tự xuất hiện nhiều. Nếu thay vào đó ta cho ký tự thường gặp mã ngắn
và ký tự hiếm mã dài, cùng một thông điệp sẽ tốn ít bit hơn — nhưng chỉ khi
việc giải mã không còn mơ hồ. Một bảng mã mà mã này là tiền tố của mã khác
có thể giải mã cùng một chuỗi bit theo hai cách khác nhau. Cách dựng của
Huffman đảm bảo tính tiền tố tự do về mặt cấu trúc, vì mọi mã đều là đường
đi từ gốc tới lá của cây.

Cài đặt trong `HuffmanTree.py` cung cấp:

- Lớp `HuffmanNode` (ký tự, tần suất, hai con trái/phải).
- Lớp `HuffmanCoding` dựng cây bằng min-heap, xây bảng mã bằng DFS, mã hóa
  văn bản thành bit, và giải mã bit thành văn bản.
- `weighted_length` để đếm tổng số bit mã hóa.
- Các hàm tĩnh `is_prefix_free`, `fixed_length_bits` và `ascii_bits` để
  kiểm tra tính chất và so sánh các kiểu mã hóa.
- `draw_tree` vẽ cây hoàn chỉnh bằng ASCII.
- Demo so sánh ASCII (56 bit), mã độ dài cố định (14 bit), và Huffman
  (10 bit) cho `"aaabacc"`, kèm roundtrip ngẫu nhiên và với một câu mẫu.

Nguồn tham khảo:

- [Data Compression and Huffman Tree](https://labuladong.online/en/algo/data-structure-basic/huffman-tree)

## 2. Sơ lược về nén dữ liệu: nén không mất dữ liệu và nén mất dữ liệu

Nén chia làm hai họ. Nén không mất dữ liệu (lossless) giữ dữ liệu nguyên
vẹn và có thể hoàn nguyên: các byte khôi phục giống hệt bản gốc. Nén mất dữ
liệu (lossy) loại bỏ thông tin mà mắt hoặc tai người khó nhận ra, nên dữ
liệu khôi phục chỉ xấp xỉ bản gốc.

```text
         lossless                             lossy
   original == restored                  restored ~= original

   "aaabacc" --zip-->  10 bits       photo --JPEG-->  small file
   "aaabacc" <--unzip-- 10 bits      photo <--decode-- (slightly
        byte-for-byte identical            blurred, forever)

   examples:  zip, gzip, PNG,        examples:  JPEG, MP3, MPEG
              Huffman, LZW
```

Mã Huffman là phương pháp không mất dữ liệu: văn bản giải mã ra giống hệt
văn bản gốc, và demo kiểm chứng điều đó bằng `assert` ở mọi roundtrip.

## 3. Mã hóa độ dài cố định và độ dài thay đổi

Mã hóa độ dài cố định cho mọi ký tự cùng một số bit. ASCII dùng 8 bit cho
mỗi ký tự, nên 7 ký tự của `"aaabacc"` tốn 7 x 8 = 56 bit dù `'a'` chiếm đa
số văn bản:

```text
"aaabacc" as ASCII:  every character pays 8 bits, frequent or not

   a       a       a       b       a       c       c
01100001 01100001 01100001 01100010 01100001 01100011 01100011

   7 characters x 8 bits = 56 bits
```

Một phương án độ dài cố định khôn ngoan hơn chỉ cần 2 bit mỗi ký tự vì văn
bản chỉ dùng 3 ký tự phân biệt (`a`, `b`, `c`):

```text
3 distinct symbols -> 2 bits each:   a = 00    b = 01    c = 10

   a     a     a     b     a     c     c
  00    00    00    01    00    10    10      = 7 x 2 = 14 bits
```

Mã hóa độ dài thay đổi để độ dài mã đi theo tần suất. `'a'` xuất hiện 4 lần
nên xứng đáng có mã ngắn nhất; `'b'` và `'c'` xuất hiện một và hai lần nên
có thể trả giá bằng mã dài hơn:

```text
frequencies of "aaabacc":   a = 4    b = 1    c = 2

   a = 0         b = 10         c = 11

   a     a     a     b     a     c     c
   0     0     0    10     0    11    11

   4 x 1 + 1 x 2 + 2 x 2 = 10 bits
```

Cùng một thông điệp tốn 56 bit, 14 bit, hay 10 bit tùy kiểu mã hóa. Cái giá
của mã độ dài thay đổi là bài toán giải mã, được giải ở phần tiếp theo.

Các hàm đếm bit dùng trong demo:

```python
HuffmanCoding.ascii_bits("aaabacc")            # 56
HuffmanCoding.fixed_length_bits("aaabacc", 2)  # 14
```

## 4. Khó khăn của mã hóa độ dài thay đổi

Bảng mã độ dài thay đổi phải thỏa mãn hai yêu cầu: tính duy nhất (giải mã
không mơ hồ) và hiệu quả (ký tự thường gặp có mã ngắn). Tính duy nhất nghĩa
là tính tiền tố tự do: không mã nào là tiền tố của mã khác.

Một bảng mã xấu vi phạm tính chất và trở nên mơ hồ:

```text
bad codes — NOT prefix-free:

   a = 1      b = 10      c = 11

   bit string "11" decodes two different ways:

     "11"          -> c           (one code)
     "1" + "1"     -> a a         (two codes)

   the decoder cannot know which message was meant
```

Bảng mã tốt tôn trọng tính chất: `"10"` là một mã và `"11"` là một mã,
nhưng không mã nào chứa mã kia làm tiền tố. Vì mọi chuỗi bit chỉ tách đúng
tại một ranh giới, các chuỗi ghép giải mã duy nhất:

```text
good codes — prefix-free:

   a = 0      b = 10      c = 11

   bit string "1011" decodes exactly one way:

     "10" -> b        "11" -> c          -> "bc"

   no code is a prefix of another, so the bit stream splits uniquely
```

Cây Huffman đảm bảo tính chất này ngay từ cấu trúc. Mã chính xác là các
đường đi từ gốc tới lá, và lá không có con — nên một mã không bao giờ bị
kéo dài thêm bit:

```text
why the tree is automatically prefix-free:

   every code is a root-to-leaf path; a leaf has no children, so no path
   can be extended into a longer code:

            (7)
           /   \
        (a:4)  (3)
              /   \
           (b:1) (c:2)

   a = "0"      the path stops at a leaf
   b = "10"     the path stops at a leaf
   c = "11"     the path stops at a leaf

   "10" can never be extended into "101": 'b' is a leaf, so no child
   exists after it. Prefix-free is a structural guarantee, not luck.
```

## 5. Nguyên lý mã Huffman: trộn hai tần suất nhỏ nhất

Với các tần suất đã biết, Huffman dựng cây từ dưới lên. Bắt đầu với một lá
cho mỗi ký tự phân biệt, rồi lặp lại việc trộn hai tần suất nhỏ nhất thành
một nút trong mới có tần suất bằng tổng của chúng. Khi chỉ còn một gốc, cây
hoàn thành. Demo đi qua toàn bộ quá trình dựng cây cho `"aaabacc"` (tần
suất a=4, b=1, c=2).

Bước 0 — một rừng các lá, mỗi lá một ký tự:

```text
step 0 — leaves only:

   (a:4)    (b:1)    (c:2)
```

Bước 1 — hai tần suất nhỏ nhất là `b` (1) và `c` (2). Trộn chúng thành nút
cha mới có trọng số 1 + 2 = 3:

```text
step 1 — merge the two smallest: b(1) and c(2)

        (3)
       /   \
    (b:1) (c:2)

   forest:   (a:4)   (3)
```

Bước 2 — hai tần suất nhỏ nhất bây giờ là `a` (4) và nút trong (3). Trộn
chúng thành gốc với trọng số 4 + 3 = 7:

```text
step 2 — merge the two smallest: a(4) and (3)

          (7)
         /   \
      (a:4)  (3)
            /   \
         (b:1) (c:2)

   forest:   (7)        <- one root left: the Huffman tree is done
```

Bước 3 — gán nhãn mọi cạnh trái là `0` và mọi cạnh phải là `1`. Mã của một
ký tự là chuỗi bit dọc theo đường đi từ gốc tới lá của nó:

```text
step 3 — annotate the edges: left = 0, right = 1

          (7)
        0/   \1
      (a:4)   (3)
            0/  \1
          (b:1) (c:2)

   a -> 0       (1 bit)   frequent character, short code
   b -> 10      (2 bits)  rare character, longer code
   c -> 11      (2 bits)  rare character, longer code
```

Vòng lặp trộn là một min-heap trên rừng hiện tại. Mỗi vòng lặp lấy ra hai
nút nhỏ nhất và đẩy lại tổng của chúng:

```python
def _build_tree(freq):
    heap = [HuffmanNode(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)       # smallest
        right = heapq.heappop(heap)      # second smallest
        heapq.heappush(
            heap, HuffmanNode(None, left.freq + right.freq, left, right)
        )

    return heap[0]                       # the single remaining root
```

Một ví dụ lớn hơn — tần suất của `"this is an example of a huffman tree"`
(36 ký tự, 16 ký tự phân biệt, có cả dấu cách). Tần suất lệch chính là nơi
mã Huffman phát huy sức mạnh:

```text
frequencies of "this is an example of a huffman tree":

   ' ':7   a:4   e:4   f:3   t:2   h:2   i:2   s:2
   n:2     m:2   x:1   p:1   l:1   o:1   u:1   r:1

   the three most frequent symbols get 3-bit codes
   six symbols get 4-bit codes, seven symbols get 5-bit codes
   total: 135 bits instead of 36 x 8 = 288 bits
```

## 6. Xây bảng mã, mã hóa và giải mã

Khi cây đã xong, một DFS thu thập các mã. Ở một lá, tiền tố tích lũy trở
thành mã của ký tự; nút trong truyền `"0"` xuống cạnh trái và `"1"` xuống
cạnh phải:

```python
def _build_codes(node, prefix):
    if node is None:
        return
    if node.is_leaf:
        codes[node.char] = prefix or "0"
        return
    _build_codes(node.left, prefix + "0")
    _build_codes(node.right, prefix + "1")
```

Mã hóa thay từng ký tự bằng mã của nó. Với cây trong ví dụ (a = 0, b = 10,
c = 11):

```text
encoding "aaabacc" — substitute each character by its code:

   a     a     a     b     a     c     c
   0     0     0    10     0    11    11

   "aaabacc" -> "0001001111"        (10 bits)
```

Giải mã đi trong cây từng bit một, bắt đầu từ gốc. Bit `0` sang trái, bit
`1` sang phải; mỗi khi tới một lá, ký tự của nó được xuất ra và việc đi lại
bắt đầu lại từ gốc:

```text
decoding "0001001111" — walk from the root, one bit at a time:

   bit 0  root -> left             -> leaf 'a'   output: a   back to root
   bit 0  root -> left             -> leaf 'a'   output: a   back to root
   bit 0  root -> left             -> leaf 'a'   output: a   back to root
   bit 1  root -> right -> left    -> leaf 'b'   output: b   back to root
   bit 0  root -> left             -> leaf 'a'   output: a   back to root
   bit 1  root -> right -> right   -> leaf 'c'   output: c   back to root
   bit 1  root -> right -> right   -> leaf 'c'   output: c   back to root

   "0001001111" -> "aaabacc"        roundtrip closed
```

Hai thao tác này là một lần tra bảng cho mỗi ký tự và một lần đi cây cho
mỗi ký tự:

```python
def encode(text):
    return "".join(codes[ch] for ch in text)

def decode(bits):
    out, node = [], root
    for bit in bits:
        node = node.left if bit == "0" else node.right
        if node.is_leaf:
            out.append(node.char)
            node = root
    return "".join(out)
```

## 7. Độ phức tạp

Gọi `M` là số ký tự phân biệt và `N` là độ dài văn bản.

| Thao tác | Thời gian | Bộ nhớ thêm | Ghi chú |
|:---|:---:|:---:|:---|
| Dựng cây | `O(M log M)` | `O(M)` | M lần push heap, M-1 lần trộn |
| Mã hóa | `O(N)` | `O(M)` | một lần tra bảng mã mỗi ký tự |
| Giải mã | `O(N)` | `O(M)` | đi cây, tối đa `chiều cao` bước mỗi ký tự |
| Xây bảng mã | `O(M)` | `O(M)` | một DFS duy nhất qua cây |

```text
M = number of distinct characters, N = length of the text

   build    O(M log M)   heap operations dominate the M-1 merges
   encode   O(N)         one dict lookup per character
   decode   O(N)         each character costs at most `height` steps,
                         and height <= M-1 in the worst case
   space    O(M)         the tree, the code table, the frequency map
```

Tỷ lệ nén. Kích thước mã Huffman là `sum(freq[ch] * len(code[ch]))` trong
khi ASCII tốn `8 * N`. Với phân bố lệch, tỷ lệ này giảm xuống rõ rệt dưới 1
(ví dụ câu mẫu đạt khoảng 0.47). Với phân bố đều, độ dài mã tiến tới
`ceil(log2(M))`, và Huffman hội tụ về chi phí của mã độ dài cố định — khoản
tiết kiệm biến mất vì không có sự lệch nào để khai thác.

## 8. Chạy thử demo

Chạy:

```text
python HuffmanTree.py
```

So sánh số bit cho `"aaabacc"` (7 ký tự, tần suất a=4, b=1, c=2):

| Kiểu mã hóa | Công thức | Bit |
|:---|:---|:---:|
| ASCII | 7 x 8 | 56 |
| Độ dài cố định (2 bit) | 7 x 2 | 14 |
| Huffman | 4 x 1 + 1 x 2 + 2 x 2 | 10 |

Đầu ra của demo cho ví dụ nhỏ. Lưu ý cách phá hòa của heap tạo ra bảng mã
phản chiếu `{'b': '00', 'c': '01', 'a': '1'}` của bảng trong phần 5
`{'a': '0', 'b': '10', 'c': '11'}` — cả hai đều tối ưu như nhau, và demo chỉ
khẳng định các sự kiện bất biến (tiền tố tự do, độ dài mã 1/2/2, trọng số
10, roundtrip):

```text
=== Huffman coding demo: 'aaabacc' (freq a=4, b=1, c=2) ===
Code table: {'b': '00', 'c': '01', 'a': '1'}
Prefix-free check: True
ASCII bits: 56
Fixed-length bits (2 bits per char): 14
Huffman weighted length: 10
encoded 'aaabacc' -> 1110010101 (10 bits)
decoded '1110010101' -> 'aaabacc'
Tree:
(7)
    +-0-(3)
        +-0-(b:1)
        +-1-(c:2)
    +-1-(a:4)
```

Demo sau đó chạy một roundtrip ngẫu nhiên với 200 ký tự rút từ `a`-`d` theo
tần suất có trọng số, và ví dụ câu mẫu với dấu cách được đưa vào bảng tần
suất:

```text
=== Sentence: "this is an example of a huffman tree" ===
distinct chars: 16 | text length: 36
ASCII bits: 288
Huffman weighted length: 135
compression ratio (huffman / ascii): 0.469
Roundtrip decode(encode(text)) == text: True
```

Cả ba roundtrip đều được kiểm chứng bằng `assert`, nên demo sẽ báo lỗi rõ
ràng thay vì in ra kết quả sai.

## 9. Hạn chế và tổng kết

Mã Huffman là tối ưu trong số các mã tiền tố tự do khi bảng tần suất cố
định và đã biết trước, nhưng nó có những hạn chế thực tế:

```text
when Huffman helps most:   skewed frequencies, long texts
when it barely helps:      uniform frequencies (it converges to
                           the fixed-length cost)
real-world caveats:        the receiver needs the frequency table or
                           the tree itself; the table is not adaptive
                           to changing statistics mid-stream; on short
                           texts the table overhead can exceed the gain
```

Tổng kết:

- Cây Huffman là cây mã nhị phân tiền tố tự do tối ưu được dựng từ tần
  suất của các ký tự.
- Nó ra đời vì mã hóa độ dài cố định lãng phí bit cho ký tự thường gặp, và
  vì mã độ dài thay đổi phải luôn giải mã được duy nhất.
- Cây được dựng bằng cách trộn hai tần suất nhỏ nhất với min-heap:
  `O(M log M)` cho `M` ký tự phân biệt.
- Mã hóa là `O(N)` lần tra bảng; giải mã là `O(N)` lần đi cây.
- Tính tiền tố tự do mang tính cấu trúc: mã chính xác là các đường đi từ
  gốc tới lá, và lá không có con.
- Với `"aaabacc"`, cùng một thông điệp tốn 56 bit (ASCII), 14 bit (độ dài
  cố định), hay 10 bit (Huffman).

## 10. Nguồn tham khảo

- [Data Compression and Huffman Tree](https://labuladong.online/en/algo/data-structure-basic/huffman-tree)
- [Huffman coding — Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)