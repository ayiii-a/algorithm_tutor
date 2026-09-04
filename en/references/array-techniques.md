# Array and String Techniques

## Prefix sums

**Trigger**: frequent "range sum" queries, or "count the contiguous segments summing to k".

**The core identity**: `sum of range [i,j] = prefix[j+1] - prefix[i]`

**"Number of subarrays summing to k"** (560) uses **prefix sums + a hash map**:
```python
count = {0: 1}          # prefix sum 0 seen once (covers segments starting at index 0)
for x in nums:
    cur += x
    ans += count.get(cur - k, 0)     # query: how many earlier prefix sums equal cur-k
    count[cur] = count.get(cur, 0) + 1
```

**This transfers onto trees** (437 / CCI 04.12): treat "the sum from the root to the current node" as the prefix sum. ⚠️ **Before the recursion returns, do `count[cur] -= 1`** (a backtracking removal — the prefix sum is only valid for descendants on the current branch).

**Dynamic version**: when you must interleave insertions with prefix-sum queries → use a **Binary Indexed Tree** (see design.md).

---

## Two pointers

| Pattern | Scenario |
|---|---|
| **Converging pointers** (both ends toward the middle) | Two Sum on a sorted array, Container With Most Water, reversal |
| **Fast/slow pointers** | In-place removal/relocation of elements, cycle detection in a list |
| **Sliding window** | Contiguous segments (see sliding-window.md) |
| **Merge pointers** | Merging two sorted sequences |

### Filling from the back

> **When modifying in place, if the new data would overwrite data you have not read yet, fill from the back.** The write position then always sits to the right of the read position (in the empty buffer or the already-processed region).

Examples: 88 / CCI 10.01 Merge Sorted Array (three pointers `i=m-1, j=n-1, k=m+n-1`, placing the larger value at the end first), CCI 01.03 URLify, 977 Squares of a Sorted Array.

**The test: make sure the write pointer can never catch up with the read pointer.**

---

## Hash grouping: design a canonical form for each equivalence class

> **To group objects that are "equivalent in some sense", the key is to design a unique canonical form per equivalence class and use it as the hash key.**

| Problem | Equivalence relation | Canonical form |
|---|---|---|
| 49 / CCI 10.02 Group Anagrams | Same multiset of letters | The sorted string / a **26-element count tuple** (faster) |
| 205 Isomorphic Strings | Isomorphic character mapping | Sequence of first-occurrence positions |
| 249 Group Shifted Strings | Same relative shift | Differences of each character from the first |
| 572 / CCI 04.10 Check SubTree | Identical tree structure | **A serialized string** (mind the three separator traps) |

⚠️ A Python dict key must be **hashable**: use `tuple(count)`, never a `list`.

---

## The cancellation idea

**Boyer–Moore voting** (169 / CCI 17.10 Majority Element): find the element occurring more than n/2 times in **O(n) time and O(1) space**.

```python
candidate, count = None, 0
for x in nums:
    if count == 0: candidate, count = x, 1
    elif x == candidate: count += 1
    else: count -= 1
```

**Why it works**: the majority element outnumbers all others combined, so after pairwise cancellation some of it must survive.
⚠️ **If the problem does not guarantee a majority element exists, a second pass must verify** `count(candidate) * 2 > n`.

The harder 229 (> n/3) uses **two candidates**. Same family: 136 cancels with XOR.

---

## Matrix techniques

**Rotation** (48 / CCI 01.07): **clockwise 90° = transpose (about the main diagonal) + reverse each row**
- Counter-clockwise 90° = transpose + flip vertically
- 180° = flip vertically + flip horizontally
- The reason: **two reflections compose into a rotation**

**Staircase search** (240 / CCI 10.09): when rows and columns are both ascending, **start from the top-right corner** — too large, go left (values decrease); too small, go down (values increase). O(m+n).
> **The key to choosing the starting corner: the two movement directions must change the value in opposite ways** for a decision to be possible. The top-left and bottom-right corners increase (or decrease) in both directions, so they do not work.

⚠️ Contrast with 74 (globally sorted — each row's first element exceeds the previous row's last): there you can **binary search it as a 1-D array** in O(log mn). The matrix properties differ; do not conflate them.

**Record first, modify second** (73 / CCI 01.08 Zero Matrix):
> **When modifying the data would corrupt the criterion used for later decisions, split it into two passes: pass one only reads and records, pass two applies all the changes.**

⚠️ Zeroing a matrix is **not a propagation problem** — a newly written zero must not trigger further zeroing, so DFS is the wrong tool.
The O(1) space trick: **use the first row and first column as marker bits** (record separately whether the first row/column themselves contain a zero, and handle them last).

---

## Values as indices

**When the value range consists of valid indices**, the array can be read as an implicit linked list `i → nums[i]`:
- 287 Find the Duplicate Number: the duplicate is the cycle entrance → **Floyd's cycle detection** (the array version of 142)
- 41 First Missing Positive, 442 Find All Duplicates: **mark in place** (negate `nums[|x|-1]`)

**Bounded key range → bucket by key**: 347 Top K Frequent (bucket by frequency, replacing a sort with O(n)), counting sort.

---

## Top K

| Scenario | Use |
|---|---|
| Top k / data stream / online | **A heap** (a min-heap of size k; its top is the kth largest) O(n log k) |
| The kth element / one-shot / O(n) required | **Quickselect** (after partitioning, recurse into one side only) |

⚠️ **Quickselect degrades to O(n²) on heavily duplicated input** → use **three-way partitioning** (Dutch national flag, 75): split into `<pivot / ==pivot / >pivot` so the equal block is excluded in one shot.
