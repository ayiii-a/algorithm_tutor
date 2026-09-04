# Binary Trees

## First decide which pattern this is

| Signature | Pattern |
|---|---|
| Build a tree from traversal sequences / a sorted array | **Divide-and-conquer construction** |
| BST + search / successor / kth smallest / LCA | **BST navigation** (exploit left < root < right) |
| Compute some property of the tree (depth / diameter / path sum / balance) | **Tree recursion: aggregate through return values** |
| Decide subtree / substructure containment | **Tree recursion: two functions with split duties** |
| Tree + another technique | Prefix sums, backtracking, hashing |

---

## Pattern 1: Divide-and-conquer construction

**The core: determine "which node is the root" plus "the ranges of the left and right subtrees", then recurse.**

| Problem | How the root is chosen | Left/right ranges |
|---|---|---|
| 105 Preorder + Inorder | Current position in the preorder array | Left/right of the root within inorder |
| 106 Inorder + Postorder | **Tail** of postorder | Same idea (the pointer moves backwards, so **build the right subtree first**) |
| CCI 04.02 / 108 Sorted array → balanced BST | **Midpoint of the array** (guarantees balance = minimum height) | Left half / right half of the midpoint |
| 109 Sorted list → BST | Midpoint of the list (fast/slow pointers) | Before / after the midpoint |

**Two crucial points in 105**:
1. Store inorder as a hash map of "value → index", otherwise the per-level `index()` scan degrades the whole thing to O(n²)
2. **The left subtree must be built before the right** (the preorder pointer advances in one direction; reversing the order misaligns the entire tree)

---

## Pattern 2: BST navigation

> **The defining property of a BST: an in-order traversal is sorted ascending.** Any operation that can be rephrased "in order of value" can navigate in O(h) instead of traversing in O(n).

**Navigation template** (finding the in-order successor, i.e. the smallest value greater than p):
```python
while cur:
    if cur.val > p.val:
        successor = cur      # a candidate — record it, then go left for a smaller one
        cur = cur.left
    else:
        cur = cur.right      # not large enough, go right
```

**⚠️ Why does only in-order work this way?**

| Traversal | Relation to BST values | Finding a successor |
|---|---|---|
| **In-order** | **= ascending**, a one-to-one match with value order | **O(h) navigation by value** |
| Pre-order / post-order | Order is dictated by **tree shape**, unrelated to values | Only an O(n) simulated traversal |

**This is exactly why "in-order successor in a BST" is a classic problem while the pre-order and post-order versions are not.**

Other BST navigation problems: 700 Search, 701 Insert, 235 LCA of a BST, 230 Kth Smallest, 98 Validate BST.

---

## Pattern 3: Two ways to organize tree recursion

### ① One function, aggregating through the return value (post-order)

Recurse into both subtrees first, then let their results decide what this node returns.

**236 LCA is the model case**:
```python
if root is None or root == p or root == q: return root
left = lca(root.left); right = lca(root.right)
if left and right: return root          # p and q sit on opposite sides → this node is the LCA
return left if left else right
```
**The return value does double duty**: it means both "I found p or q" and "I am the LCA". The early return on `root == p` handles "a node is its own ancestor" naturally.

Same family (all "recurse into both sides, then merge into this node's return value"): 124 Maximum Path Sum, 543 Diameter, 110 Balanced, 337 House Robber III.
**When teaching these, spell out what information the return value carries upward.**

### ② Two functions with split duties

- **Outer**: walk the tree to **find a starting point**, joined with `or` (a match anywhere suffices)
- **Inner**: from that start, **test for a match**, joined with `and` (every position must agree)

572 / CCI 04.10 Check SubTree is the model case. ⚠️ Distinguish "subtree" (must match all the way down to the leaves) from "substructure" (B only needs to be a portion of A) — the two handle null nodes differently.

---

## Pattern 4: Serialization (+ substring matching)

Turn the tree into a unique string so that "is it a subtree" becomes "is it a substring". **Three traps you will hit**:

1. **No separator between numbers** → `12` and `1,2` run together and produce a false match → prefix every value with `,`
2. **Null nodes unmarked** → different shapes serialize identically → mark nulls with `N`
3. **Incomplete null marking** → you match a *partial* subtree rather than a complete one → mark every null child

**In one line: the serialization must be unique and carry its own boundaries.** Emitting the separator once at the top of the loop is the cleanest way to do it.
(`s2 in s1` is O(mn) worst case; a true O(m+n) needs KMP.)

---

## Pattern 5: Tree + another technique

- **Tree + prefix sum + hash map** (437 / CCI 04.12 Paths with Sum): treat "the sum from the root to the current node" as the prefix sum and query `prefix_count.get(cur_sum - target)`. ⚠️ **Before returning from the recursion, do `prefix_count[cur_sum] -= 1`** (a backtracking removal — the prefix sum is only valid for descendants on the current branch)
- **Tree + backtracking** (113 Path Sum II, 257 Binary Tree Paths)
- **Tree + dynamic-candidate-set backtracking** (CCI 04.09 BST Sequences)

---

## Iterative traversal (stack)

When converting recursion to iteration, the stack holds either "nodes still to visit" or "the path down from the root".
- Iterative in-order: push all the way left → pop and visit → turn right
- The iterative solution to 105: the stack maintains the current left-boundary path, and the inorder pointer decides when to stop going left and turn right

---

## Common pitfalls

- Forgetting the hash map in 105 → O(n²)
- Building the subtrees in the wrong order in 105/106
- Not handling `root is None` in the recursion
- Reading the answer from the wrong place for "ending at i" style properties
- Stack overflow on a very deep tree (Python's limit is 1000) → consider iteration
