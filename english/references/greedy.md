# Greedy

## Trigger

> **A locally optimal choice provably leads to the global optimum, and no choice ever needs to be revisited.**

**Two things the explanation must do**:
1. **State the greedy rule precisely** (by what criterion each step chooses)
2. **Argue why the rule is correct** — use an **exchange argument**: assume an optimal solution differs from the greedy one at some step, swap that step for the greedy choice, and show the result is no worse

If you cannot make that argument, greedy probably does not apply — consider DP.

---

## Interval greedy: three sort keys to keep straight

| Problem | Sort by | Core move |
|---|---|---|
| 435 Non-overlapping Intervals | **Right endpoint** | On a conflict, drop the current one |
| 452 Minimum Arrows to Burst Balloons | **Right endpoint** | Nearly the same problem as 435 (the difference is `>` vs `>=`) |
| 56 Merge Intervals | **Left endpoint** | On a conflict, merge and extend the right edge |
| 253 Meeting Rooms II | **Left endpoint** + min-heap | The heap top holds the earliest finish time |

**Rule of thumb: keeping the most / using the fewest resources → sort by right endpoint; merging or covering → sort by left endpoint.**

**The key argument in 435**: after sorting by right endpoint, drop the current interval on a conflict — its right endpoint is larger and it occupies more room, so dropping it is **never worse**.

---

## Jump Game: implicit BFS layering

**45 (minimum jumps)** maintains three quantities:
- `cur_end`: the **right boundary** reachable with the current number of jumps
- `farthest`: across every position in the current layer, **the farthest the next jump can reach**
- `jumps`: the jump count

Iterate up to `n-1`, updating `farthest` each step; when `i == cur_end`, do `jumps += 1; cur_end = farthest`.

**Two things to point out**:
1. **You never explicitly choose a landing spot** — `farthest` records the layer's best landing spot automatically
2. **This is BFS layering in disguise**: `cur_end` is the current layer's right boundary, and hitting it means entering the next layer

> **BFS collapses into greedy here because the reachable range is contiguous** (contiguous → two boundary variables replace the queue, O(1) space). When the reachable set is discrete (279/322, where each step subtracts one square or one coin), you need a real BFS queue.

---

## When DP collapses into greedy

**When "the exact value of some quantity does not matter — only its extremum affects the future", DP collapses into greedy.**

435 Non-overlapping Intervals: the DP is O(n²) and TLEs; greedy is O(n log n).

**When teaching a problem whose DP would time out, check for this collapse.**

---

## Common pitfalls

- Assuming greedy works when the rule is actually wrong (322 Coin Change with `coins=[1,3,4], amount=6`: greedily taking the largest gives 4+1+1 = 3 coins, but the optimum is 3+3 = 2 → **DP is mandatory**)
- Choosing the wrong sort key (sorting by left endpoint where right endpoint is required)
- Iterating to `n` instead of `n-1` in 45, which counts one jump too many
