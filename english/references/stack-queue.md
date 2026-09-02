# Stacks and Queues

## Always start with one question: what does the stack hold?

Ask this and the right variant identifies itself immediately.

| What the stack holds | Which variant | Examples |
|---|---|---|
| **Indices**, kept increasing or decreasing | ① Monotonic stack | 739, 901, 84, 42, 496 |
| An **aggregate** for each step | ② Auxiliary stack | 155 Min Stack |
| **The context from before entering a nesting level** | ③ Nesting parser stack | 394, 20, 32, 224 |
| The elements themselves, but the in/out order must change | ④ Two-stack simulation | 232, 225, CCI 03.05 |
| **Nodes still to visit** | ⑤ Iterative traversal | 94/144/145, 105 |

---

## ① Monotonic stack

**Trigger**: find the **first greater/smaller** element to the left or to the right.

**Direction rule**: looking for greater → keep the stack **decreasing**; looking for smaller → keep it **increasing**. (The stack's monotonicity is the **opposite** of what you are looking for.)

```python
stack = []
for i in range(n):
    while stack and nums[stack[-1]] < nums[i]:   # looking for greater → decreasing stack
        j = stack.pop()
        # settle j: i is the first greater element to j's right
    stack.append(i)
```

**Store indices, not values** (distances need indices, and values can be looked up from them).

**What gets settled on pop — three levels of difficulty** (say which level the problem is at):

| Level | What is settled | Examples |
|---|---|---|
| Uses **one side** only | An index difference | 739 Daily Temperatures |
| The stack **carries an aggregate** | Accumulated span (the stack holds `(value, span)`) | 901 Stock Span |
| Uses **both sides** | `height × (right bound - left bound - 1)` | **84 Largest Rectangle in Histogram**, 42 Trapping Rain Water |

**Four key points in 84** (the hardest monotonic stack problem):
- Increasing stack (finding the first shorter bar on each side)
- On pop: `height = heights[popped]`, `right bound = i`, `left bound = the new stack top after popping`, `width = i - stack[-1] - 1`
- **Append a sentinel bar of height 0** to force the stack to drain
- Amortized O(n): every index is pushed and popped exactly once

---

## ② Auxiliary stack

**Trigger**: a single stack, but min/max queries must also be **O(1)**.

The main stack and the auxiliary stack **push and pop in lockstep**, and the auxiliary top always holds the current minimum/maximum.
**The core: maintain it eagerly on push, so pop automatically rolls back to the previous state.**

Optimized form: only push when `val <= min_stack[-1]` (⚠️ use `<=`, not `<`, or repeated minima get lost).

---

## ③ Nesting parser stack

**Trigger**: brackets, nesting, matched pairs.

**The stack holds the context from before entering the bracket**: on an opening symbol, push and clear the current state; on a closing symbol, pop and merge the inner result back into the outer one.

**A recursive solution is exactly equivalent** (the call stack *is* the stack you were maintaining by hand).

**32 Longest Valid Parentheses** (hard, far harder than 20):
It is not just validity but the **longest contiguous valid run**, which involves joining across an already-closed substring.
The recommended approach is **store indices, with a `-1` sentinel at the bottom**: push on `(`; on `)` pop, and if the stack is now empty push the current `)` as the new sentinel, otherwise `max_len = max(max_len, i - stack[-1])`.

---

## ④ Two-stack simulation (two flavours)

| Problem | Flavour | When to transfer |
|---|---|---|
| 232 / CCI 03.04 Queue via stacks | **Bulk reversal** (reversing twice restores the original order) | Only when `out` is empty → **amortized O(1)** |
| CCI 03.05 Sort of Stacks | **Insert one at a time** (insertion sort on a stack) | On every push → keeps the stack sorted |

The design trade-off in 03.05: **pay O(n) on push to buy O(1) on pop/peek**. This is the same "decide whether the cost belongs on reads or writes, based on operation frequency" idea behind 155 Min Stack and 146 LRU.

---

## Common pitfalls

- Using `if` instead of `while` in a monotonic stack (every element violating monotonicity must be popped)
- Getting the monotonicity direction backwards
- Computing 84's width as `i - j + 1` (it should be `i - stack[-1] - 1`)
- Forgetting the trailing sentinel, leaving elements in the stack unsettled
- Using `<` instead of `<=` in the optimized min stack
