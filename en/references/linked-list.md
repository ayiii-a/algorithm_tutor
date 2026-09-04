# Linked Lists

## Three fundamentals

1. **Dummy sentinel node**: a head node holding no data, which removes every "special-case the first node" headache
2. **Fast/slow pointers**: find the middle (876), find the cycle entrance (142), delete the kth from the end (19), detect a cycle
3. **Reverse a list** (206): three pointers `prev / cur / next`

**Many advanced problems are just these three combined**:
- 234 Palindrome Linked List = find middle + reverse the second half + compare with two pointers
- 143 Reorder List = find middle + reverse the second half + interleave
- 148 Sort List = find middle + merge sort

---

## Key reminders when teaching

### When rewiring while traversing: save `next` before you change it

```python
nxt = cur.next        # save it first!
cur.next = ...        # then rewire
cur = nxt
```
Skip the save and you lose the traversal path.

### After any rearrangement: set the tail's `next` to None

**This is the number-one source of linked-list bugs** (infinite loops and TLEs both trace back to it). After rearranging, some chain's tail may still point at a node in the original list → **cycle**.

### The standard in-place deletion pattern

```python
if cur should be removed:
    prev.next = cur.next
    cur = prev.next        # prev stays put (a new node now follows it)
else:
    prev = cur             # keep it, prev advances
    cur = cur.next
```
**"Delete → prev stays; keep → prev advances."** Getting this wrong is the usual bug in problems like CCI 02.04 Partition List.

### Two stopping conditions for fast/slow midpoint search

- `while fast and fast.next`: slow lands on **the middle** (right of centre for even lengths)
- `while fast.next and fast.next.next`: slow lands **one before the middle** (left of centre for even lengths)

**148 Sort List must use the second form** (starting from `fast = head.next`), or a single-node list never splits and the recursion loops forever.

---

## Splitting and merging

**When partitioning nodes into groups, build separate new chains and join them at the end** — far clearer than shuffling pointers in place. One dummy plus one tail pointer per chain.

(But if the user already wrote a correct in-place extraction version, do not force it into the two-chain form — both are valid.)

**Merging two sorted lists** (21) is the primitive behind 148 and 23; it should be second nature.

---

## The heart of the classic problems

| Problem | The heart of it |
|---|---|
| 138 Copy List with Random Pointer | Hash map `old→new` / **node interleaving in O(1) space** (insert each copy right after its original, then `cur.next.random = cur.random.next`) |
| 148 Sort List | Merge sort (merging only rewires pointers, which cancels merge sort's one drawback). Merge sort is **the champion for sequentially-accessed structures** |
| 23 Merge k Sorted Lists | Divide and conquer O(kn·logk) / min-heap (⚠️ push `(val, i, node)`; **i is the tie-breaker**, without it comparing ListNodes raises TypeError) |
| 142 Linked List Cycle II | Floyd's algorithm: after they meet, send one pointer back to the head and advance both one step at a time; they meet again at the cycle entrance |

---

## Common pitfalls

- Skipping the dummy and writing a pile of special cases for the first node
- Rewiring without saving `next`
- Leaving the tail connected after a rearrangement → cycle
- Advancing `prev` at the wrong time during in-place deletion
- Choosing the wrong start or stop condition for fast/slow pointers, causing an infinite loop
