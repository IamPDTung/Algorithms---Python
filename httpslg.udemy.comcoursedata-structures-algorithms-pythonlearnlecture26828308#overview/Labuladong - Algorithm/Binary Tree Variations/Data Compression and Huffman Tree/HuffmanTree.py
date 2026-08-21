"""Huffman coding: build an optimal prefix-free binary code tree from
character frequencies, then use it to compress and restore text.

Fixed-length encodings such as ASCII spend 8 bits on every character
whether it is frequent or rare. Huffman coding assigns SHORT codes to
frequent characters and LONG codes to rare ones, while guaranteeing that
no code is a prefix of another, so decoding is always unambiguous. This
module implements the tree build (min-heap merge), the code table (DFS),
encode/decode, prefix-free verification, and fixed-vs-variable length
comparisons.
"""

from __future__ import annotations

import heapq
import itertools
import random
from collections import Counter
from typing import Dict, List, Optional

_SEQ = itertools.count()


class HuffmanNode:
    """A node in a Huffman tree.

    Leaf nodes carry a character and its frequency; internal nodes carry
    no character and a frequency equal to the sum of their two children.
    """

    def __init__(
        self,
        char: Optional[str],
        freq: int,
        left: Optional[HuffmanNode] = None,
        right: Optional[HuffmanNode] = None,
    ) -> None:
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        self.seq = next(_SEQ)

    def __lt__(self, other: HuffmanNode) -> bool:
        """Heap ordering by frequency; the insertion sequence breaks ties
        so that the heap behavior is fully deterministic."""
        return (self.freq, self.seq) < (other.freq, other.seq)

    def __repr__(self) -> str:
        if self.is_leaf:
            return f"{self.char}:{self.freq}"
        return str(self.freq)

    @property
    def is_leaf(self) -> bool:
        """True when this node stores a character (has no children)."""
        return self.left is None and self.right is None


class HuffmanCoding:
    """Build a Huffman tree from character frequencies and use it to
    encode and decode text with variable-length prefix-free codes.
    """

    def __init__(self, freq: Dict[str, int]) -> None:
        """Store a copy of the frequencies, build the tree with a min-heap,
        and derive the code table with a DFS over the finished tree.

        The tree is built by repeatedly popping the two smallest-frequency
        nodes and pushing a new internal node whose frequency is their sum;
        the last remaining node is the root. The code table is stored
        internally and exposed through the read-only `codes` property.
        """
        self.freq: Dict[str, int] = dict(freq)
        self.root: Optional[HuffmanNode] = self._build_tree(self.freq)
        self._codes: Dict[str, str] = {}
        self._build_codes(self.root, "")

    def _build_tree(self, freq: Dict[str, int]) -> Optional[HuffmanNode]:
        """Merge the two smallest-frequency nodes until one root remains."""
        heap: List[HuffmanNode] = [HuffmanNode(ch, f) for ch, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            heapq.heappush(
                heap, HuffmanNode(None, left.freq + right.freq, left, right)
            )

        return heap[0] if heap else None

    def _build_codes(self, node: Optional[HuffmanNode], prefix: str) -> None:
        """DFS from the root: left edges append '0', right edges append '1';
        a leaf receives the accumulated bit string as its code."""
        if node is None:
            return

        if node.is_leaf:
            self._codes[node.char] = prefix if prefix else "0"
            return

        self._build_codes(node.left, prefix + "0")
        self._build_codes(node.right, prefix + "1")

    @property
    def codes(self) -> Dict[str, str]:
        """The code table mapping each character to its bit string (copy)."""
        return dict(self._codes)

    def encode(self, text: str) -> str:
        """Return the bit string for `text`; unknown characters raise
        KeyError because they are absent from the code table."""
        return "".join(self._codes[ch] for ch in text)

    def decode(self, bits: str) -> str:
        """Walk the tree from the root one bit at a time; every time a leaf
        is reached, append its character and reset to the root. Raises
        ValueError when the bits do not follow a root-to-leaf path."""
        if self.root is None:
            return ""

        out: List[str] = []
        node = self.root

        for bit in bits:
            node = node.left if bit == "0" else node.right
            if node is None:
                raise ValueError("invalid bit string: no such path in the tree")
            if node.is_leaf:
                out.append(node.char)
                node = self.root

        return "".join(out)

    def weighted_length(self) -> int:
        """Total encoded length in bits: sum of freq[ch] * len(code[ch])."""
        return sum(
            self.freq[ch] * len(code) for ch, code in self._codes.items()
        )

    @staticmethod
    def is_prefix_free(codes: Dict[str, str]) -> bool:
        """True when no code is a prefix of another, so any concatenation
        of codes decodes unambiguously."""
        ordered = sorted(codes.values(), key=len)
        for index, code in enumerate(ordered):
            if not code:
                return False
            for other in ordered[index + 1:]:
                if other.startswith(code):
                    return False
        return True

    @staticmethod
    def fixed_length_bits(text: str, bits_per_char: int) -> int:
        """Size of `text` under a fixed-length encoding with
        `bits_per_char` bits per character."""
        return len(text) * bits_per_char

    @staticmethod
    def ascii_bits(text: str) -> int:
        """Size of `text` under plain ASCII: 8 bits per character."""
        return len(text) * 8

    def draw_tree(self) -> List[str]:
        """Compact ASCII rendering of the tree: leaves show `char:freq`,
        internal nodes show the summed frequency, and edges are labeled
        with their bit."""
        lines: List[str] = []

        def render(node: Optional[HuffmanNode], indent: str, edge: str) -> None:
            if node is None:
                return
            prefix = f"+-{edge}-({node})" if edge else f"({node})"
            lines.append(f"{indent}{prefix}")
            child_indent = indent + "    "
            render(node.left, child_indent, "0")
            render(node.right, child_indent, "1")

        render(self.root, "", "")
        return lines


if __name__ == "__main__":
    freq_small = {"a": 4, "b": 1, "c": 2}
    hc = HuffmanCoding(freq_small)
    codes_small = hc.codes

    assert HuffmanCoding.is_prefix_free(codes_small)
    assert hc.weighted_length() == 10
    assert len(codes_small["a"]) == 1
    assert len(codes_small["b"]) == 2
    assert len(codes_small["c"]) == 2

    text_small = "aaabacc"
    bits_small = hc.encode(text_small)
    assert len(bits_small) == 10
    assert hc.decode(bits_small) == text_small

    print("=== Huffman coding demo: 'aaabacc' (freq a=4, b=1, c=2) ===")
    print("Code table:", codes_small)
    print("Prefix-free check:", HuffmanCoding.is_prefix_free(codes_small))
    print("ASCII bits:", HuffmanCoding.ascii_bits(text_small))
    print("Fixed-length bits (2 bits per char):",
          HuffmanCoding.fixed_length_bits(text_small, 2))
    print("Huffman weighted length:", hc.weighted_length())
    print(f"encoded '{text_small}' -> {bits_small} ({len(bits_small)} bits)")
    print(f"decoded '{bits_small}' -> '{hc.decode(bits_small)}'")
    print("Tree:")
    for line in hc.draw_tree():
        print(line)

    rng = random.Random(2026)
    alphabet = ["a", "b", "c", "d"]
    weights = [7, 2, 4, 1]
    random_text = "".join(rng.choices(alphabet, weights=weights, k=200))
    hc_rand = HuffmanCoding(Counter(random_text))
    assert HuffmanCoding.is_prefix_free(hc_rand.codes)
    assert hc_rand.decode(hc_rand.encode(random_text)) == random_text

    print()
    print("=== Random roundtrip (200 chars over a-d, weighted) ===")
    print("distinct chars:", len(hc_rand.codes))
    print("Prefix-free check:", HuffmanCoding.is_prefix_free(hc_rand.codes))
    print("Roundtrip decode(encode(text)) == text: True")

    sentence = "this is an example of a huffman tree"
    hc_sent = HuffmanCoding(Counter(sentence))
    assert HuffmanCoding.is_prefix_free(hc_sent.codes)
    assert hc_sent.decode(hc_sent.encode(sentence)) == sentence
    sent_ascii = HuffmanCoding.ascii_bits(sentence)
    sent_huffman = hc_sent.weighted_length()
    ratio = sent_huffman / sent_ascii

    print()
    print('=== Sentence: "this is an example of a huffman tree" ===')
    print("distinct chars:", len(hc_sent.codes), "| text length:", len(sentence))
    print("ASCII bits:", sent_ascii)
    print("Huffman weighted length:", sent_huffman)
    print("compression ratio (huffman / ascii):", round(ratio, 3))
    print("Roundtrip decode(encode(text)) == text: True")