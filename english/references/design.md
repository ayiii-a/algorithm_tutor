# Data Structure Design

## Three guiding principles

**① When no single structure meets every requirement, combine several, each handling what it is best at.**
(146 LRU: a hash map for O(1) lookup + a doubly linked list for O(1) order maintenance)

**② Do not compute a slow query at query time — maintain the answer eagerly, every time the data changes.**
(155 Min Stack: on push, compute "the current minimum" and push it onto the auxiliary stack)

**③ Decide whether the cost belongs on reads or writes, based on operation frequency.**
(CCI 03.05 Sort of Stacks: pay O(n) on push to buy O(1) on pop/peek)

---

## The derivation order when teaching

1. **List every operation and its required complexity** → these are the constraints
2. **Go through them: which operation would be slow with a naive structure?** → locate the tension
3. **Attach an auxiliary structure for that slow operation** → the combination
4. **Check: does the new structure slow anything else down?** → the trade-off
5. **Spell out which structures each operation must keep in sync** (the thing most often missed)

---

## Classic combinations

| Requirement | Combination | Example |
|---|---|---|
| O(1) lookup + O(1) order maintenance | Hash map + doubly linked list | 146 LRU |
| O(1) min/max query | Main stack + auxiliary stack | 155 |
| Several stacks inside one array | Segment the array, `i*size + offset` | CCI 03.01 |
| A dynamically growing/shrinking set of stacks | A list of stacks | CCI 03.03 Stack of Plates |
| A queue implemented with stacks | Two stacks (reverse twice) | 232 |
| Merge several FIFOs and take the oldest | Multiple queues + a **global timestamp** | CCI 03.06 Animal Shelter |
| **Dynamic insertion + prefix-sum / rank query** | **Binary Indexed Tree** | CCI 10.10 Stream Rank, 315 |
| Median from a data stream | **Max-heap + min-heap** | 295 |

---

## Binary Indexed Tree (BIT)

**Trigger**: you need **dynamic insertion** plus **prefix-sum or rank queries**. A static prefix-sum array costs O(n) to rebuild on every insert; a BIT makes both operations O(log n).

```python
def update(i, delta):          # indices start at 1!
    while i <= n:
        tree[i] += delta
        i += i & (-i)          # jump to the parent

def query(i):                  # prefix sum over [1, i]
    total = 0
    while i > 0:
        total += tree[i]
        i -= i & (-i)          # jump to the preceding block
    return total
```

`i & (-i)` extracts the lowest set bit, which determines the span each node covers. **Indices must start at 1** (0 causes an infinite loop).

---

## Four traps in 146 LRU

1. **The node must store its key** (on eviction you get a node from the list and need the key to delete the hash entry)
2. **Eviction must delete from both structures** (unlink from the list + `del cache[key]`)
3. **`get` must also refresh the order** (the U in LRU is *Used* — a read counts as a use)
4. **The eviction timing and the comparison operator must match**: evict-then-insert uses `>=`, insert-then-evict uses `>`

---

## A note on code organization

**Call the existing public methods when they already do the job**; do not manufacture a set of private helpers just to "remove duplication".
(`dequeueAny` should call `dequeueCat()` / `dequeueDog()` directly rather than a separate `_pop_cat`.)
