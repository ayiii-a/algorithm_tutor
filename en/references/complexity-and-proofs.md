# Complexity Analysis and Correctness Proofs

Tools for **arguing** about an algorithm, not for designing one. Reach for this file when the derivation needs a complexity that is not obvious, or when a greedy/two-pointer solution needs its correctness justified rather than asserted.

---

## The Master Theorem

For a divide-and-conquer recurrence

$$T(n) = a\,T(n/b) + f(n), \qquad a \ge 1,\; b > 1$$

compare $f(n)$ against $n^{\log_b a}$:

| Case | Condition | Result |
|---|---|---|
| 1 | $f(n) = O(n^{\log_b a - \varepsilon})$ — the leaves dominate | $T(n) = \Theta(n^{\log_b a})$ |
| 2 | $f(n) = \Theta(n^{\log_b a})$ — evenly balanced | $T(n) = \Theta(n^{\log_b a}\log n)$ |
| 3 | $f(n) = \Omega(n^{\log_b a + \varepsilon})$ and regularity holds — the root dominates | $T(n) = \Theta(f(n))$ |

Worked examples:

| Recurrence | $n^{\log_b a}$ | Case | Result |
|---|---|---|---|
| Merge sort $T(n)=2T(n/2)+n$ | $n$ | 2 | $\Theta(n\log n)$ |
| Binary search $T(n)=T(n/2)+1$ | $n^0=1$ | 2 | $\Theta(\log n)$ |
| Quickselect (expected) $T(n)=T(n/2)+n$ | $n^0=1$ | 3 | $\Theta(n)$ |
| Karatsuba $T(n)=3T(n/2)+n$ | $n^{1.585}$ | 1 | $\Theta(n^{1.585})$ |

**Use it to explain a result, not to replace the reasoning.** The line worth saying out loud is usually the intuition behind the case — "quickselect recurses into one side only, so the work halves each time and the top level dominates, giving O(n)" — with the theorem as the formal backing.

---

## Amortized Analysis

Needed whenever a loop *looks* quadratic but is not: monotonic stacks, two-stack queues, quickselect partitioning, dynamic array growth, Union-Find.

Three methods, in increasing power:

### Aggregate method (usually enough)

Bound the **total** work across all n operations, then divide by n.

> Monotonic stack: every index is pushed once and popped at most once, so the total number of stack operations across the whole loop is ≤ 2n. The inner `while` may run many times on one iteration, but never more than 2n times overall → **amortized O(1) per step, O(n) total**.

This is the argument to give for almost every "looks O(n²), is actually O(n)" situation in this skill's references.

### Accounting method

Charge each operation more than it costs and bank the surplus to pay for expensive ones later.

> Two-stack queue: charge 3 units on `push` — 1 for pushing onto `in`, and 2 banked to pay for eventually moving that element to `out` and popping it. Every expensive transfer is paid for in advance → **amortized O(1)**.

### Potential method

Define a potential Φ over the data structure's state; the amortized cost is the actual cost plus ΔΦ.

> Dynamic array doubling: let Φ = 2·(size) − capacity. A normal append costs 1 with ΔΦ = 2, so amortized 3. A resize costs `size` but drives Φ from `size` back to ~0, cancelling it → **amortized O(1)**.

**Which to use when teaching**: the aggregate method covers nearly every case here and is the easiest to state in one sentence. Reach for accounting or potential only when the aggregate count is genuinely hard to bound.

---

## Loop Invariants

The standard way to prove an iterative algorithm correct. State a property that holds before every iteration, then show three things:

1. **Initialization** — it holds before the first iteration
2. **Maintenance** — if it holds before an iteration, it still holds before the next
3. **Termination** — when the loop ends, the invariant plus the exit condition give the desired result

Worth writing out when a pointer scheme's correctness is not obvious:

> **11 Container With Most Water.** Invariant: the optimal pair is always within `[left, right]`.
> *Initialization*: the window is the whole array.
> *Maintenance*: moving the shorter wall inward can only discard pairs whose area is bounded by that wall's height and a narrower width — all strictly worse. So the optimum stays inside.
> *Termination*: when the pointers meet, every candidate has been considered or provably discarded.

This is what makes "move the shorter side" a proof rather than a hunch.

---

## Exchange Argument (for greedy)

The standard proof that a greedy rule is optimal:

1. Take any optimal solution O and the greedy solution G
2. Find the first position where they differ
3. Show that swapping O's choice for G's choice keeps O **valid** and **no worse**
4. Repeat — O transforms into G without ever getting worse, so G is optimal

> **435 Non-overlapping Intervals.** Sorted by right endpoint, greedy keeps the interval that finishes earliest. If an optimal solution keeps a different one at that position, swap it for the greedy one: the greedy interval finishes no later, so everything O kept afterwards still fits. The count is unchanged, and the solutions now agree one step further.

**If you cannot build this argument, the greedy rule is probably wrong** — that is the practical value of the technique. (322 Coin Change is the standard counterexample: no exchange argument exists, and greedy genuinely fails.)

---

## Lower Bounds Worth Knowing

Useful for answering "can this be faster?" honestly instead of hand-waving.

| Problem | Bound | Consequence |
|---|---|---|
| Comparison sorting | $\Omega(n\log n)$ | Beating it requires leaving the comparison model (counting sort, radix sort) |
| Edit distance, LCS | No $O(n^{2-\varepsilon})$ under SETH | Only space can be optimized, not the time order |
| Element distinctness | $\Omega(n\log n)$ in the comparison model | Hashing sidesteps it by changing models |
| Any problem whose output is size k | $\Omega(k)$ | Enumerating all subsets cannot beat $O(2^n)$ — the output is that large |

**The last row is the one most often forgotten**: when a problem asks for every solution, the exponential cost is the output, not the algorithm. Say so rather than apologizing for the complexity.
