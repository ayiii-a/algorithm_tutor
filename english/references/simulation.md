# Construction and Simulation Problems

## Trigger

> **No standard algorithmic framework applies; the work is "spot the mathematical or geometric rule, then translate it into steps". The signature: very short code, very hard-to-find rule.**

The strategy for these: **just memorize the conclusion.** Deriving one on the spot usually takes a flash of insight; recalling it takes a second.

---

## A four-step method for teaching simulation problems

**1. Enumerate the checklist**: list every case that has to be checked or handled
**2. Factor out the shared logic**: find the reusable subroutine so the code is not repeated
**3. Order the checks**: decide what gets tested first (the wrong order misses cases)
**4. Exhaust the edge cases**: empty input, single element, extreme values, degenerate shapes

> **These problems are graded on "did you miss a case", not on algorithmic elegance.**

---

## Let the data structure handle the edge cases

**Return an empty value from the recursion so "skipping" happens automatically** (CCI 16.08 English Int):
```python
def three_digits(n):
    if n == 0: return []          # empty list — concatenation skips it automatically
    if n < 20: return [table[n]]
    if n < 100: return [tens[n//10]] + three_digits(n % 10)
    return [table[n//100], "Hundred"] + three_digits(n % 100)
```
This way `20` never produces "Twenty Zero" and `100` never produces "One Hundred Zero", **with no pile of `if x != 0` checks**.

**Use a list plus `join` for separators** rather than concatenating strings by hand (which invites stray spaces).

---

## Classic construction problems

**31 Next Permutation** (three steps, worth memorizing):
1. Scanning from the right, find **the first descent** at i (`nums[i] < nums[i+1]`) — the pivot
2. Scanning from the right, find **the first element greater than the pivot** and swap them
3. **Reverse everything after i**

When `i = -1` (fully descending = the largest permutation), step 3 reverses the whole array → naturally yielding the smallest permutation.
> **The idea: leave the high-order positions untouched and make the smallest possible increase at the lowest position.** (CCI 05.04 Next Number is its bitwise counterpart.)

**Towers of Hanoi** (CCI 08.06) — the model case for recursive thinking:
```python
def move(n, src, aux, dst):
    if n == 0: return
    move(n-1, src, dst, aux)      # top n-1 disks: src → aux
    dst.append(src.pop())          # the largest: src → dst
    move(n-1, aux, src, dst)      # those n-1 disks: aux → dst
```
> **The mindset for recursion: do not try to unfold every level in your head (it explodes). You only need to ① define clearly how the problem decomposes into a smaller instance of itself and ② write the base case. Then trust the recursion.**
Watch the **role rotation** of the three pegs (the parameter order).

---

## Two rules for geometry problems

**① Use vectors and parametric equations, never slopes**
The slope `k = Δy/Δx` divides by zero on vertical lines. Parametric equations and cross products use only addition, subtraction and multiplication.

**② The cross product is the Swiss army knife of 2-D geometry**
`cross(a, b) = a.x * b.y - a.y * b.x`
- `= 0` → the two vectors are collinear (parallel)
- `> 0 / < 0` → the turn direction (left or right)
- `|cross|` → the area of the parallelogram

Uses: testing for parallelism, segment intersection, convex hull (Graham scan), point-in-triangle tests.
