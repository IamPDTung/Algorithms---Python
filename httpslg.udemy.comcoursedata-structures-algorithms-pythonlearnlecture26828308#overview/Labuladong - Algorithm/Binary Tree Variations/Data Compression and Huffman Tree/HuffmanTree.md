# Data Compression and Huffman Tree

## 1. Goal

A Huffman tree is an optimal prefix-free binary code tree built from
character frequencies. Each leaf stores one character and its frequency;
each internal node stores the sum of its children's frequencies. The code
of a character is the bit string along the path from the root to its leaf,
so frequent characters get SHORT codes and rare characters get LONG codes,
while no code is ever a prefix of another code.

Why it was born: fixed-length encodings such as ASCII spend 8 bits on
every character, whether it appears 1000 times or once. That wastes bits on
frequent characters. If instead we give frequent characters short codes and
rare characters long codes, the same message costs fewer bits — but only if
decoding stays unambiguous. A code table where one code is a prefix of
another can decode a bit string two different ways. Huffman's construction
guarantees the prefix-free property structurally, because every code is a
root-to-leaf path of the tree.

The implementation in `HuffmanTree.py` provides:

- A `HuffmanNode` class (character, frequency, left/right children).
- A `HuffmanCoding` class that builds the tree with a min-heap, builds the
  code table with a DFS, encodes text to bits, and decodes bits to text.
- `weighted_length` to count the total encoded bits.
- Static helpers `is_prefix_free`, `fixed_length_bits`, and `ascii_bits`
  to verify the property and compare encodings.
- An ASCII `draw_tree` rendering of the finished tree.
- A demo that compares ASCII (56 bits), fixed-length (14 bits), and Huffman
  (10 bits) for `"aaabacc"`, plus randomized and sentence roundtrips.

Source references:

- [Data Compression and Huffman Tree](https://labuladong.online/en/algo/data-structure-basic/huffman-tree)

## 2. A Brief Look at Data Compression: Lossless vs Lossy

Compression splits into two families. Lossless compression keeps the data
perfectly intact and is reversible: the restored bytes are identical to the
original. Lossy compression discards information the human eye or ear will
not notice, so the restored data only approximates the original.

```text
         lossless                             lossy
   original == restored                  restored ~= original

   "aaabacc" --zip-->  10 bits       photo --JPEG-->  small file
   "aaabacc" <--unzip-- 10 bits      photo <--decode-- (slightly
        byte-for-byte identical            blurred, forever)

   examples:  zip, gzip, PNG,        examples:  JPEG, MP3, MPEG
              Huffman, LZW
```

Huffman coding is a lossless method: the decoded text equals the encoded
text exactly, which the demo verifies with `assert` on every roundtrip.

## 3. Fixed-Length vs Variable-Length Encoding

Fixed-length encoding gives every character the same number of bits. ASCII
uses 8 bits per character, so the 7 characters of `"aaabacc"` cost
7 x 8 = 56 bits even though `'a'` dominates the text:

```text
"aaabacc" as ASCII:  every character pays 8 bits, frequent or not

   a       a       a       b       a       c       c
01100001 01100001 01100001 01100010 01100001 01100011 01100011

   7 characters x 8 bits = 56 bits
```

A smarter fixed-length scheme needs only 2 bits per character because the
text uses 3 distinct symbols (`a`, `b`, `c`):

```text
3 distinct symbols -> 2 bits each:   a = 00    b = 01    c = 10

   a     a     a     b     a     c     c
  00    00    00    01    00    10    10      = 7 x 2 = 14 bits
```

Variable-length encoding lets the code length follow the frequency. `'a'`
appears 4 times, so it deserves the shortest code; `'b'` and `'c'` appear
once and twice, so they may pay longer codes:

```text
frequencies of "aaabacc":   a = 4    b = 1    c = 2

   a = 0         b = 10         c = 11

   a     a     a     b     a     c     c
   0     0     0    10     0    11    11

   4 x 1 + 1 x 2 + 2 x 2 = 10 bits
```

The same message costs 56 bits, 14 bits, or 10 bits depending on the
encoding. The price of variable-length coding is a decoding problem, solved
in the next section.

The counting helpers used by the demo:

```python
HuffmanCoding.ascii_bits("aaabacc")            # 56
HuffmanCoding.fixed_length_bits("aaabacc", 2)  # 14
```

## 4. The Difficulties of Variable-Length Encoding

A variable-length code table must satisfy two requirements: uniqueness
(decoding is unambiguous) and efficiency (frequent characters have short
codes). Uniqueness means the prefix-free property: no code may be a prefix
of another code.

A bad table violates the property and becomes ambiguous:

```text
bad codes — NOT prefix-free:

   a = 1      b = 10      c = 11

   bit string "11" decodes two different ways:

     "11"          -> c           (one code)
     "1" + "1"     -> a a         (two codes)

   the decoder cannot know which message was meant
```

The good table respects the property: `"10"` is a code and `"11"` is a
code, but neither contains the other as a prefix. Because every bit string
splits at exactly one boundary, concatenations decode uniquely:

```text
good codes — prefix-free:

   a = 0      b = 10      c = 11

   bit string "1011" decodes exactly one way:

     "10" -> b        "11" -> c          -> "bc"

   no code is a prefix of another, so the bit stream splits uniquely
```

A Huffman tree guarantees this property by construction. Codes are exactly
the root-to-leaf paths, and leaves have no children — so a code can never
be extended by more bits:

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

## 5. Principle of Huffman Coding: Merge the Two Smallest

Given the frequencies, Huffman builds the tree bottom-up. Start with one
leaf per distinct character, then repeatedly merge the two smallest
frequencies into a new internal node whose frequency is their sum. When one
root remains, the tree is complete. The demo walks through the full
construction of the tree for `"aaabacc"` (frequencies a=4, b=1, c=2).

Step 0 — a forest of leaves, one per character:

```text
step 0 — leaves only:

   (a:4)    (b:1)    (c:2)
```

Step 1 — the two smallest frequencies are `b` (1) and `c` (2). Merge them
into a new parent node with weight 1 + 2 = 3:

```text
step 1 — merge the two smallest: b(1) and c(2)

        (3)
       /   \
    (b:1) (c:2)

   forest:   (a:4)   (3)
```

Step 2 — the two smallest are now `a` (4) and the internal node (3). Merge
them into the root with weight 4 + 3 = 7:

```text
step 2 — merge the two smallest: a(4) and (3)

          (7)
         /   \
      (a:4)  (3)
            /   \
         (b:1) (c:2)

   forest:   (7)        <- one root left: the Huffman tree is done
```

Step 3 — label every left edge `0` and every right edge `1`. The code of a
character is the bit string along the path from the root to its leaf:

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

The merge loop is a min-heap over the current forest. Each iteration pops
the two smallest nodes and pushes their sum back:

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

A bigger example — the frequencies of `"this is an example of a huffman
tree"` (36 characters, 16 distinct symbols, spaces included). Skewed
frequencies are exactly where Huffman coding shines:

```text
frequencies of "this is an example of a huffman tree":

   ' ':7   a:4   e:4   f:3   t:2   h:2   i:2   s:2
   n:2     m:2   x:1   p:1   l:1   o:1   u:1   r:1

   the three most frequent symbols get 3-bit codes
   six symbols get 4-bit codes, seven symbols get 5-bit codes
   total: 135 bits instead of 36 x 8 = 288 bits
```

## 6. Building the Code Table, Encoding and Decoding

Once the tree exists, a DFS collects the codes. At a leaf the accumulated
prefix becomes the character's code; internal nodes pass `"0"` down the
left edge and `"1"` down the right edge:

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

Encoding replaces every character with its code. For the walkthrough tree
(a = 0, b = 10, c = 11):

```text
encoding "aaabacc" — substitute each character by its code:

   a     a     a     b     a     c     c
   0     0     0    10     0    11    11

   "aaabacc" -> "0001001111"        (10 bits)
```

Decoding walks the tree bit by bit, starting at the root. A `0` goes left,
a `1` goes right; whenever a leaf is reached, its character is emitted and
the walk restarts at the root:

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

The two operations are one table lookup per character and one tree walk per
character:

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

## 7. Complexity

Let `M` be the number of distinct characters and `N` the length of the
text.

| Operation | Time | Extra space | Note |
|:---|:---:|:---:|:---|
| Build tree | `O(M log M)` | `O(M)` | M heap pushes, M-1 merges |
| Encode | `O(N)` | `O(M)` | one code-table lookup per char |
| Decode | `O(N)` | `O(M)` | tree walk, at most `height` steps per char |
| Code table build | `O(M)` | `O(M)` | single DFS over the tree |

```text
M = number of distinct characters, N = length of the text

   build    O(M log M)   heap operations dominate the M-1 merges
   encode   O(N)         one dict lookup per character
   decode   O(N)         each character costs at most `height` steps,
                         and height <= M-1 in the worst case
   space    O(M)         the tree, the code table, the frequency map
```

Compression ratio. The Huffman size is `sum(freq[ch] * len(code[ch]))`
while ASCII costs `8 * N`. For skewed distributions the ratio drops well
below 1 (the sentence example reaches about 0.47). For uniform
distributions the code lengths approach `ceil(log2(M))`, and Huffman
converges to a fixed-length encoding — the savings disappear because there
is no skew to exploit.

## 8. Demo Walkthrough

Run:

```text
python HuffmanTree.py
```

Bit-count comparison for `"aaabacc"` (7 characters, frequencies a=4, b=1,
c=2):

| Encoding | Formula | Bits |
|:---|:---|:---:|
| ASCII | 7 x 8 | 56 |
| Fixed-length (2 bits) | 7 x 2 | 14 |
| Huffman | 4 x 1 + 1 x 2 + 2 x 2 | 10 |

The demo output for the small example. Note the heap tie-breaking produced
the mirror-image table `{'b': '00', 'c': '01', 'a': '1'}` of the walkthrough
table `{'a': '0', 'b': '10', 'c': '11'}` — both are equally optimal, and
the demo asserts only the invariant facts (prefix-free, code lengths 1/2/2,
weighted length 10, roundtrip):

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

The demo then runs a randomized roundtrip over 200 characters drawn from
`a`-`d` with weighted frequencies, and the sentence example with spaces
included in the frequency table:

```text
=== Sentence: "this is an example of a huffman tree" ===
distinct chars: 16 | text length: 36
ASCII bits: 288
Huffman weighted length: 135
compression ratio (huffman / ascii): 0.469
Roundtrip decode(encode(text)) == text: True
```

All three roundtrips are verified with `assert`, so the demo fails loudly
instead of printing wrong results.

## 9. Limitations and Summary

Huffman coding is optimal among prefix-free codes for a fixed, known
frequency table, but it has real-world caveats:

```text
when Huffman helps most:   skewed frequencies, long texts
when it barely helps:      uniform frequencies (it converges to
                           the fixed-length cost)
real-world caveats:        the receiver needs the frequency table or
                           the tree itself; the table is not adaptive
                           to changing statistics mid-stream; on short
                           texts the table overhead can exceed the gain
```

Summary:

- A Huffman tree is an optimal prefix-free binary code tree built from
  character frequencies.
- It was born because fixed-length encodings waste bits on frequent
  characters, and because variable-length codes must stay unambiguous.
- The tree is built by merging the two smallest frequencies with a
  min-heap: `O(M log M)` for `M` distinct characters.
- Encoding is `O(N)` table lookups; decoding is `O(N)` tree walks.
- The prefix-free property is structural: codes are exactly the
  root-to-leaf paths, and leaves have no children.
- For `"aaabacc"` the same message costs 56 bits (ASCII), 14 bits
  (fixed-length), or 10 bits (Huffman).

## 10. Sources

- [Data Compression and Huffman Tree](https://labuladong.online/en/algo/data-structure-basic/huffman-tree)
- [Huffman coding — Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)