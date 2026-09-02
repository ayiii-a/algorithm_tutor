# Dynamic Programming

## Five things to pin down, in order

Derive in this order. **Never skip ahead to the transition equation.**

### 1. State definition (what `dp[...]` means)

Derive it with this procedure:

```
Write the signature of the brute-force recursion → its parameter list is the candidate state
```

Then run two checks:
- **Freeze test**: given only the values of the state variables (all other memory wiped), can you still make the next decision? If not → add a dimension
- **Drop-dimension test**: any index the transition never actually uses → drop it

**Should a quantity go into the index or into the value?**
- Must be known exactly (different values determine what the future can do) → **into the index**
- Only its optimum matters (bigger/smaller is better, it does not constrain the future) → **into the value**

Rule of thumb: **quantities you can be greedy about go into the value; quantities that must be exact go into the index.**
(416 Partition Equal Subset Sum: the sum must land *exactly* on target, so the sum goes into the index. 0/1 knapsack: capacity into the index, value into the value.)

**"Ending at i" vs "the first i"**
If the transition needs to know **which specific element is at the boundary** → you must nail down the ending element.
- 300 LIS: to decide whether a new element can be appended you must know what the current sequence ends with → "ending at nums[i]"
- 198 House Robber: you only need to know "did I rob i-1", and that is already encoded in the dp structure → "the first i"

**Tip**: prefer using **length** (0..n) rather than index (0..n-1) for i in `dp[i]`; then `i=0` naturally means "empty" and the boundaries stay clean.

### 2. Transition equation

Ask: **which predecessor states can reach this state?** Or in reverse: **what was the last operation?**

- Linear DP asks "how is the last element handled"
- Interval DP asks "where was the last operation" (enumerate the split point)

⚠️ **A "smaller subproblem" is not necessarily `i-1`**:
- 279 Perfect Squares: `i - j²`
- 322 Coin Change: `i - coin`
- 338 Counting Bits: `i >> 1` or `i & (i-1)`

### 3. Base cases

Make `i=0` (or the empty interval) carry a clear, unambiguous meaning. Common ones:
- `dp[0] = 0` (making 0 requires 0 items)
- `dp[0] = 1` (there is 1 way to make 0 — choose nothing; this 1 is the seed for every other count)
- Boolean form: `dp[0] = True`
- When minimizing, initialize to `inf` (`inf` naturally encodes "unreachable" and propagates all the way through)

### 4. Traversal order

**Dependencies dictate the order: whatever you depend on must be computed first.**

| Type | Traversal |
|---|---|
| Linear | Index ascending |
| Knapsack | See "Knapsack: two orthogonal dimensions" below |
| Grid | Both rows and columns ascending |
| **Interval** | **By interval length, shortest first** (it depends on shorter inner intervals) |
| Two-string | Both indices ascending |

### 5. Where the answer lives

- "Ending at i" form: the answer is usually `max(dp)`, not `dp[n-1]` (300 LIS, 53, 152)
- "First i" form: the answer is `dp[n]`
- Interval form: `dp[0][n-1]`

---

## The five families at a glance

| Type | State | Representative problems |
|---|---|---|
| Linear | `dp[i]` | 300 LIS, 152 Maximum Product Subarray, 53, 198 |
| Knapsack | `dp[j]` over capacity | 416, 322, 279, 518 |
| Grid | `dp[i][j]` over row/column | 62, 64, 63 |
| Interval | `dp[i][j]` over an interval | 5 Longest Palindromic Substring, 312 Burst Balloons, 241 |
| Two-string | `dp[i][j]` over two indices | 72 Edit Distance, 1143 LCS |

**Grid vs two-string**: both are `dp[i][j]` but the meaning differs — grid indices are row/column coordinates (transition from above/left), two-string indices are each string's progress (compare the trailing characters).

---

## Knapsack: two orthogonal dimensions

**Dimension one: how many times can each item be used → determines the direction of the inner capacity loop**

| | 0/1 knapsack (once) | Unbounded knapsack (unlimited) |
|---|---|---|
| Inner capacity loop | **Descending** | **Ascending** |

**Why descending**: in the 1-D form `dp[j] = f(dp[j], dp[j-w])`, `dp[j-w]` must be the **previous row's old value** (before the current item was placed). Ascending lets it be overwritten within this same pass, so it already includes the current item → the item gets reused.

**The 2-D version does not have this problem** (the two rows are physically separate), so either direction works → **write the 2-D version first to get the logic straight, then compress to 1-D once it is confirmed correct.**

**Dimension two: what you are computing → determines the nesting order of the two loops**

| | Optimum (min/max) | Number of ways |
|---|---|---|
| Loop order | Either way | **Items outer, capacity inner** (yields combinations) |

Items on the outside fixes the order in which items are used, so `1+5` and `5+1` are counted once → combinations.
Capacity on the outside counts permutations instead (377 Combination Sum IV actually wants permutations, so it puts capacity on the outside).

---

## Two shapes of interval DP

**① Peel the ends** (5 Longest Palindromic Substring)
`dp[i][j] = (s[i]==s[j]) and dp[i+1][j-1]`

**② Enumerate the split point** (312 Burst Balloons, 241 Different Ways to Add Parentheses, CCI 08.14 Boolean Evaluation)
Enumerate k, "the operation performed last", and split the interval into `[i,k-1]` and `[k+1,j]`.
The standard triple loop: **length → start → split point**.

⚠️ Some interval DPs need the dp value to **carry several quantities at once** (CCI 08.14 tracks both "number of ways to get 0" and "number of ways to get 1"), because merging needs both.

---

## Space optimization: choosing the rolling-array direction

**Look at the smaller-index value you are reusing and ask which row it should come from:**
- **Needs the previous row's old value → descending** (0/1 knapsack)
- **Needs this row's new value → ascending** (grid 62/64, two-string 72/1143)

⚠️ **After compressing to 1-D, boundaries with a "single source" are easily skipped by the inner loop.**
(64 Minimum Path Sum: with the inner `j` starting at 1, the per-row first column update `dp[0] += grid[i][0]` gets dropped.)

⚠️ Two-string DP that depends on the **top-left** `dp[i-1][j-1]` needs a temporary `prev` to hold it when compressed to 1-D (it gets overwritten by this row's update).

---

## Which DPs can be sped up

- **Can be**: when there is extra exploitable structure. LIS has monotonicity → binary search takes O(n²) down to O(n log n)
- **Cannot be**: intrinsically quadratic problems. Edit distance / LCS have a theoretical lower bound (under SETH), as does grid pathing. Only space can be reduced

**The test**: is there extra exploitable structure (monotonicity, a bounded value range)?

---

## Memoized search ↔ bottom-up

**Two implementations of the same DP.** To convert:
- Recursion parameters → dp array indices
- The recursion's dependency relation → the loop's traversal order

Memoization computes on demand (only the states actually needed); tabulation fills everything in. Interval DP is often easier to write with memoized recursion (it handles "shortest interval first" automatically).

---

## DP or something else

| What you need | Use |
|---|---|
| Every concrete solution | **Backtracking** |
| Feasibility / count / optimum | **DP** |
| A local optimum provably leads to the global optimum | **Greedy** (consider it when DP would TLE) |

Example: 131 Palindrome Partitioning (list all partitions) uses backtracking; 139 Word Break (can it be done) uses DP.

**DP collapsing into greedy**: when "the exact value of some quantity does not matter — only its extremum affects the future", DP can collapse into greedy (435 Non-overlapping Intervals: the DP is O(n²) and TLEs, while sorting by right endpoint and being greedy is O(n log n)).

---

## Common pitfalls

- Reading the answer off `dp[n-1]` instead of `max(dp)` (the classic mistake for the "ending at i" family)
- Using an ascending inner loop for 0/1 knapsack → items get reused
- Putting capacity on the outside when counting ways → you count permutations
- Losing a boundary's separate update after compressing to 1-D
- With mutually dependent states, updating one before computing the other (152 must stash all three candidates before updating max/min)
