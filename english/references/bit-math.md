# Bit Manipulation and Math

## Bit manipulation: pick the tool first

| Requirement | Tool |
|---|---|
| Count the set bits | `n &= n-1` in a loop (iterations = number of set bits) |
| Test for a power of two | `n & (n-1) == 0` |
| Extract the lowest set bit | `n & (-n)` |
| Find "which bits differ" | **XOR** `a ^ b` |
| Find the element appearing once | **XOR cancellation** (`a^a=0`) |
| Membership / small sets (≤64 kinds) | **A bitmask as a set** |
| Modify a range of bits | **Clear → shift → merge** |
| Operate on "every kth bit" in bulk | **Mask separation** (`0x55555555` and friends) |
| Multiplication / division / exponentiation | **Binary decomposition / doubling** |

---

## Three properties of XOR

- `a ^ a = 0` (self-cancelling → isolate the lone element: 136, 268)
- `a ^ 0 = a`
- **Each 1 in `a ^ b` marks a bit where the two numbers differ** → **Hamming distance = popcount(a^b)** (461, CCI 05.06)

⚠️ **The XOR result is a mask of "which bits differ", not "how many differ"** — you still have to count the set bits. (1318 is where this trips people up.)

---

## A bitmask as a set

When there are at most 64 kinds of element, use the bits of one integer to represent a set:

| Operation | Code |
|---|---|
| Is element i present | `mask & (1 << i)` |
| Add element i | `mask \|= (1 << i)` |
| Remove element i | `mask &= ~(1 << i)` |
| Toggle element i | `mask ^= (1 << i)` |

Applications: CCI 01.01 Is Unique, enumerating subsets in 78 by bitmask, **bitmask DP**, N-Queens optimization.

---

## Modifying a range of bits: clear → shift → merge

```python
ones = ((1 << (j-i+1)) - 1) << i     # build a mask with bits i..j set
num &= ~ones                          # ① clear
num |= (M << i)                       # ② shift ③ merge
```

**The key mask-building trick**: `(1 << k) - 1` gives k consecutive ones. When you need "zeros in the middle, ones outside", negate it.

---

## Mask separation + bulk shifting

To operate uniformly on "every kth bit", filter them all out with a mask, shift the group as a whole, then merge:

```python
# swap odd and even bits
return ((num & 0x55555555) << 1) | ((num & 0xAAAAAAAA) >> 1)
```

**Classic constants**: `0x55555555` (even bits), `0xAAAAAAAA` (odd bits), `0x33333333` (every 2 bits), `0x0F0F0F0F` (every 4 bits).
After shifting, the two extracted groups occupy complementary positions, so `|` merges them without collision. This is the basis of divide-and-conquer bit tricks (parallel popcount, 190 Reverse Bits).

---

## Binary decomposition / doubling

```python
while B:
    if B & 1: result += A       # this bit is set, accumulate
    A <<= 1                      # double A
    B >>= 1                      # halve B
```

`A × B = Σ(A << i)` over the set bits i of B. O(log B).

**Isomorphic to fast exponentiation** (50): replace `+= A, A <<= 1` with `*= x, x *= x`. This is exactly how hardware multipliers work.

⚠️ If the problem **forbids bit operations** (CCI 16.09), use `acc += acc` in place of `acc <<= 1` — the idea is identical.

---

## ⚠️⚠️ Two Python-specific traps

Python integers have **arbitrary precision**, so anything involving fixed-width integers needs both ends handled manually:

| Situation | Problem | Fix |
|---|---|---|
| **Input may be negative** | A negative number's two's complement has infinitely many leading 1s, so `>>` keeps padding 1 and the logic loops or breaks | `num &= 0xFFFFFFFF` to **truncate** |
| **Output must be signed** | `0xFFFFFFFF` is a positive number in Python, not -1 | `v - 2**32 if v >= 2**31 else v` to **convert to signed** |

**Whenever the problem says "32-bit integer", check both of these reflexively.** In C++/Java an `int` is 32 bits by construction, so the issue never arises.

---

## The mindset for math problems

> **Do not brute-force it — find an equivalent formulation that is easier to compute.**

**CCI 16.05 Factorial Zeros** has a model derivation chain:
number of trailing zeros → number of factors of 10 → `min(factors of 2, factors of 5)` → **5 is scarcer than 2, so it is just the count of factors of 5** → count them in layers, `⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ...`

**Legendre's formula**: the exponent of prime p in `n!` equals `Σ⌊n/pⁱ⌋`. Each term counts "one extra" occurrence.

**Other useful results**:
- Lagrange's four-square theorem: every positive integer is the sum of **at most 4** perfect squares (so the answer to 279 is always in {1,2,3,4})
- Catalan numbers: valid parenthesis strings, distinct BST shapes, stack-permutation counts
- Pigeonhole principle: n+1 items in n boxes forces a repeat (287)

---

## Base conversion

- **Integer to base k**: divide by k and take remainders (low digit → high digit)
- **Fraction to base k**: multiply by k and take the integer part (high digit → low digit); it may repeat forever → cap the digit count and report ERROR

> This explains **why 0.1 is inexact on a computer**: 0.1 in binary repeats forever, so a double stores only an approximation → `0.1 + 0.2 != 0.3`.
