# Backtracking

## The heartbeat

```
def backtrack(path, choices):
    if end condition met:
        results.append(snapshot of path)     # path[:] or ''.join(path)
        return
    for choice in choices:
        make the choice        # mutate path and state
        backtrack(...)         # descend
        undo the choice        # restore path and state  ← the soul of it
```

**However many pieces of state the choice mutated, the undo must restore exactly that many.** (N-Queens mutates the board plus 3 sets, so 4 things must be restored.)

---

## Four things to pin down

### 1. Is this a permutation or a combination

| | Controls the choice space | When to collect |
|---|---|---|
| **Permutation** (order matters) | `used` array, each level starts from 0 | Collect at the **leaves** (`len(path)==n`) |
| **Combination / subset** (order does not matter) | `start` pointer, `for i in range(start, n)` | Subsets collect at **every node** (put the append at the top of the function, with no `if` guarding it) |

### 2. What to pass down the recursion

- `backtrack(i+1)`: each element used **at most once**
- `backtrack(i)`: each element may be **reused without limit** (39 Combination Sum)
- `backtrack(0)` + `used`: permutation

**A one-character difference changes the behaviour entirely.**

### 3. Whether deduplication is needed (when elements repeat)

**One rule: sort, then skip duplicates within the same level.**

| What controls the space | Dedup condition |
|---|---|
| `start` pointer (combination/subset) | `if i > start and nums[i] == nums[i-1]: continue` |
| `used` array (permutation) | `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue` |

**The core: never try the same value twice at the same level, but do allow several equal values across levels.**
- Both `[2]` and `[2,2]` must be kept (across levels)
- Trying the same value twice in the same position must be skipped (same level)

**What `not used[i-1]` means**: the previous equal element has not been used → this is a same-level repeat → skip. If it is currently in use → this is a cross-level pick → keep.

### 4. Pruning conditions

Pruning is what separates "correct" from "fast" in backtracking. Three sources:

| Source of the prune | Examples |
|---|---|
| **Constraint counters** (check `right < left` before placing a `)`) | 22 Generate Parentheses |
| **Geometric conflicts** (`row±col` for diagonals) | 51 N-Queens |
| **Feasibility lookahead** (not enough elements left / current sum already exceeds the target) | 39, 216 |
| **Memoizing failed states** (a `failed` set of positions known to lead nowhere) | CCI 08.02 Robot in a Grid |

⚠️ **Memoization is only valid for "find one path / decide feasibility", never for "enumerate all solutions"** (it would prune away valid ones).

---

## The four quadrants

|  | Distinct elements | Duplicate elements |
|---|---|---|
| **Combination / subset** | 78, 39, 216 | 90, 40 (`i > start`) |
| **Permutation** | 46 | 47 (`not used[i-1]`) |

---

## Notable variants

**Partition type** (131 Palindrome Partitioning, 93 Restore IP Addresses, 139/140 Word Break)
The choice is not "which element to pick" but "**where the current segment ends**". Same skeleton; only the validity test for each segment changes.

**Grid backtracking** (79 Word Search)
- Mark in place with `board[i][j] = '#'` and restore on the way out
- Put the bounds / out-of-range / mismatch checks all at the **entry of the recursion**, not repeated at each of the four call sites
- ⚠️ **Enumerating all paths requires undoing `visited`; testing connectivity does not** (200 Number of Islands)

**Dynamic candidate set** (CCI 04.09 BST Sequences)
The candidate set changes with each choice: after picking a node, remove it from the candidates and add its children. This is really "all topological orders of a tree".

---

## Common pitfalls

- **The `path[:]` snapshot** (the number-one trap): `append(path)` stores a reference, so once backtracking clears the path every entry becomes empty. For strings, `''.join(path)` is a snapshot by construction
- Putting the append inside an `if` in a subset problem (it belongs at the top of the function so every node is collected)
- Writing the dedup condition as `i > 0` instead of `i > start` → this also prunes the legitimate cross-level repeats
- Forgetting to restore one piece of state on undo
- Forgetting `nonlocal` when a scalar counter has to be updated (Python scoping)
