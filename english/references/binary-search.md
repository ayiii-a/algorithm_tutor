# Binary Search

## The essential idea (state this first when teaching)

> **Binary search does not require the whole array to be sorted. It only requires that at each mid you can decide, in O(1), which half the answer lies in.**

That directional information can come from: global sortedness / which half is sorted / a local trend (uphill vs downhill) / monotonicity of the answer space.

---

## Four things to pin down

### 1. What exactly are you bisecting

| Bisecting what | Scenario | Examples |
|---|---|---|
| **Array index** | Find a value or a boundary in a sorted array | 34, 35, 704 |
| **Which half is sorted** | Rotated array | 33, 153 |
| **Local trend** | Find a peak (array is unsorted) | 162, 852 |
| **The range of the answer** | **Binary search on the answer** (the most common advanced form) | 875, 1011, 410 |
| **The value range** | Find the duplicate, find the kth smallest | 287 |
| **A partition position** | Median of two sorted arrays | 4 |

**How to spot "binary search on the answer"**: the problem asks for "the minimum possible maximum", "the maximum possible minimum", or "the fewest X needed", **and given a candidate answer you can verify feasibility in O(n)**.

### 2. Which template (never mix them!)

| | Closed-interval template | Shrink-to-a-point template |
|---|---|---|
| Init | `right = n-1` | `right = n-1` |
| Loop | `while left <= right` | `while left < right` |
| Shrink | `right = mid - 1` | `right = mid` |
| Return | Inside the loop, or `left` | `left` (at which point `left == right`) |
| Use when | mid can be ruled out | **mid itself might be the answer** |

**The deciding question: "could mid still be the answer?"**
- It can be ruled out (already compared, not equal to target) → `mid ± 1`
- **It might be the answer** (finding a peak, finding a boundary) → **`right = mid`**, paired with `while left < right`

⚠️ **Mixing templates is the single most common bug**: `right = n` + `while left < right` + `right = mid - 1` will either miss the answer or loop forever.

### 3. Computing mid, and out-of-bounds

- `mid = left + (right - left) // 2` avoids overflow (required in C++/Java; make it a habit in Python too)
- **If the loop body reads `arr[mid+1]`, `right` must start at `n-1`** (otherwise mid can reach n-1 and the read goes out of bounds)

### 4. Boundaries and equality

When searching for a boundary, **do not stop on a hit — keep squeezing toward the target side**:
- Left boundary: on a hit, `right = mid - 1`
- Right boundary: on a hit, `left = mid + 1`

**The ±0.5 trick** (integer arrays): the insertion point of `target-0.5` is the left boundary, `target+0.5` gives the right boundary, which sidesteps the equality branch entirely. A sturdier integer version uses `target+1`. This is equivalent to `bisect_left` / `bisect_right`.

---

## ⚠️ When binary search breaks down (duplicates)

**Duplicate elements destroy the criterion binary search relies on.** Always call this out on the relevant problems:

| What breaks | Response | Examples |
|---|---|---|
| `nums[i]-i` is no longer monotonic | **Abandon binary search**, fall back to an O(n) scan | CCI 08.03 Magic Index |
| `arr[left]==arr[mid]`, so you cannot tell which half is sorted | Conservatively `left += 1`, or search both halves; O(n) worst case | 81, CCI 10.03 |

**An extra wrinkle when the smallest index is required**
> **"Find any one" and "find the first" prune with different strength.** For any one, confirming the target lies in one half lets you discard the other. For the first, **even if the right half contains it, the left half must still be searched** (its indices are smaller).

---

## Template for binary search on the answer

```python
def check(x):
    """Given candidate answer x, is it feasible? Must be monotonic in x."""
    ...

lo, hi = smallest_possible_answer, largest_possible_answer
while lo < hi:
    mid = (lo + hi) // 2
    if check(mid):
        hi = mid          # feasible, try a smaller/better one
    else:
        lo = mid + 1
return lo
```

**Two things the explanation must make clear**:
1. **The range of the answer** (how lo and hi are determined)
2. **The monotonicity of the predicate**: why `check(x)` being true implies `check(x+1)` is true (or the reverse)

---

## Common pitfalls

- **Mixing templates** (by far the most frequent)
- `right = mid` paired with `while left <= right` → infinite loop
- Reading `arr[mid+1]` while `right = n` → out of bounds
- Returning on the first hit when looking for a boundary → you get an arbitrary one, not the first
- Forcing a no-duplicates template onto an array with duplicates
- Forgetting the case where target does not exist (return -1, or the insertion point)
