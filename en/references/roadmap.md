# Practice Roadmap

A 50-problem path from "I know how to code" to "I can recognize what a problem is asking for". Use it when the user asks where to start, what to do next, or how to prepare from scratch.

**The ordering principle**: each problem introduces **exactly one new idea**, and every stage assumes only what earlier stages taught. That is why some famous problems appear late and some obscure ones appear early — the sequence is built around what each one *teaches*, not around difficulty ratings.

**How to use this file when advising**:
- If the user is starting out, give them **one stage at a time**, not the whole list. Fifty problems presented at once is a wall, not a plan.
- Name what each problem teaches. "Do 704 next" is useless; "do 704 next — it is where you fix the binary search template you will reuse twelve more times" is a reason.
- Cross-check `references/my-pitfalls.md`. If a recorded pattern touches an upcoming stage, say so and suggest re-doing the relevant problem before moving on.
- Do not let anyone skip stage 1. It is short and everything else assumes it.

---

## Stage 1 — Hashing and prefix sums (5)

The habit to build: **before scanning again, ask whether something could have been recorded on the first pass.**

| # | Problem | What it teaches |
|---|---|---|
| 1 | 1 Two Sum | A hash map turns "search for a complement" from O(n) into O(1) |
| 2 | 49 Group Anagrams | Designing a **canonical form** to serve as a grouping key |
| 3 | 560 Subarray Sum Equals K | **Prefix sum + hash map**: `cur - k` seen before means a segment sums to k |
| 4 | 238 Product of Array Except Self | Prefix and suffix passes replace division |
| 5 | 128 Longest Consecutive Sequence | A set plus "only start counting from a sequence's head" gives O(n) |

→ reference: `array-techniques.md`

---

## Stage 2 — Two pointers and sliding window (5)

The habit to build: **when the window must stay contiguous, two indices beat any nested loop.**

| # | Problem | What it teaches |
|---|---|---|
| 6 | 125 Valid Palindrome | Converging pointers, the simplest form |
| 7 | 11 Container With Most Water | **Why moving the shorter side is provably safe** (the first loop invariant worth stating) |
| 8 | 3 Longest Substring Without Repeating | The window template; state kept in a hash map |
| 9 | 209 Minimum Size Subarray Sum | **Shortest updates the answer in a different place from longest** |
| 10 | 424 Longest Repeating Character Replacement | A window condition that is a derived quantity, not a raw count |

→ reference: `sliding-window.md`, `array-techniques.md`

---

## Stage 3 — Binary search (5)

The habit to build: **pick one template and never mix two.**

| # | Problem | What it teaches |
|---|---|---|
| 11 | 704 Binary Search | The template itself — write it until it is automatic |
| 12 | 35 Search Insert Position | `lower_bound`: what the loop returns when the target is absent |
| 13 | 34 First and Last Position | **Boundary search: on a hit, keep squeezing instead of returning** |
| 14 | 153 Find Minimum in Rotated Sorted Array | Deciding direction from "which half is sorted" rather than from the values |
| 15 | 875 Koko Eating Bananas | **Binary search on the answer** — the array is not even sorted |

→ reference: `binary-search.md`

---

## Stage 4 — Stacks (4)

The habit to build: **ask what the stack holds before writing any of it.**

| # | Problem | What it teaches |
|---|---|---|
| 16 | 20 Valid Parentheses | The stack as a matching device |
| 17 | 155 Min Stack | An **auxiliary stack**: maintain the answer eagerly instead of computing it on query |
| 18 | 739 Daily Temperatures | The **monotonic stack**, and settling an answer on pop |
| 19 | 84 Largest Rectangle in Histogram | Settling with information from **both sides** — the hardest version of the same idea |

→ reference: `stack-queue.md`

---

## Stage 5 — Linked lists (5)

The habit to build: **save `next` before rewiring, and check the tail afterwards.**

| # | Problem | What it teaches |
|---|---|---|
| 20 | 206 Reverse Linked List | The three-pointer primitive that half of this stage depends on |
| 21 | 21 Merge Two Sorted Lists | The dummy node plus a tail pointer |
| 22 | 876 Middle of the Linked List | Fast and slow pointers |
| 23 | 142 Linked List Cycle II | **Floyd's algorithm** and why the second phase lands on the entrance |
| 24 | 143 Reorder List | Composing all three: find the middle, reverse the back half, interleave |

→ reference: `linked-list.md`

---

## Stage 6 — Trees (7)

The habit to build: **decide what the return value carries upward before writing the recursion.**

| # | Problem | What it teaches |
|---|---|---|
| 25 | 104 Maximum Depth of Binary Tree | Recursion on trees in its smallest form |
| 26 | 102 Binary Tree Level Order Traversal | BFS on a tree, and processing one level at a time |
| 27 | 98 Validate Binary Search Tree | The BST property is about **ranges**, not just the immediate children |
| 28 | 235 Lowest Common Ancestor of a BST | **Navigation**: using value comparisons to descend in O(h) |
| 29 | 236 Lowest Common Ancestor of a Binary Tree | Aggregating through the return value, with no BST property to lean on |
| 30 | 105 Construct Binary Tree from Preorder and Inorder | Divide and conquer: which node is the root, and what the two ranges are |
| 31 | 543 Diameter of Binary Tree | **The return value differs from the answer** — return the depth, record the diameter |

→ reference: `tree.md`

---

## Stage 7 — Graphs (5)

The habit to build: **build the adjacency list first, and check the edge direction.**

| # | Problem | What it teaches |
|---|---|---|
| 32 | 200 Number of Islands | A grid is a graph; `visited` is not undone here |
| 33 | 133 Clone Graph | A `visited` map doing double duty as the old→new mapping |
| 34 | 994 Rotting Oranges | **Multi-source BFS**, and why BFS gives the shortest time |
| 35 | 207 Course Schedule | **Topological sort**; in-degree means "prerequisites still unmet" |
| 36 | 547 Number of Provinces | **Union-Find** as the alternative to DFS for connectivity |

→ reference: `graph.md`

---

## Stage 8 — Backtracking (5)

The habit to build: **choose → recurse → undo, with the undo restoring everything the choice touched.**

| # | Problem | What it teaches |
|---|---|---|
| 37 | 78 Subsets | Collecting at **every node**, and the `path[:]` snapshot |
| 38 | 46 Permutations | The `used` array, and collecting at the leaves instead |
| 39 | 39 Combination Sum | Passing `i` instead of `i+1` to allow reuse |
| 40 | 90 Subsets II | **Same-level deduplication** — the hardest small detail in backtracking |
| 41 | 79 Word Search | Backtracking on a grid; here `visited` **is** undone |

→ reference: `backtracking.md`

---

## Stage 9 — Dynamic programming (10)

The largest stage, and the one worth slowing down for. The habit to build: **write the brute-force recursion's signature first; its parameters are the state.**

| # | Problem | What it teaches |
|---|---|---|
| 42 | 70 Climbing Stairs | A 1-D transition in its smallest form |
| 43 | 198 House Robber | The "first i" state, and a choice at each step |
| 44 | 53 Maximum Subarray | **"Ending at i"**, and why the answer is `max(dp)` rather than `dp[n-1]` |
| 45 | 300 Longest Increasing Subsequence | Why the ending element must be pinned down; later, the O(n log n) version |
| 46 | 322 Coin Change | **Unbounded knapsack**; `inf` as the marker for unreachable |
| 47 | 416 Partition Equal Subset Sum | **0/1 knapsack**, and why the capacity loop runs backwards |
| 48 | 62 Unique Paths | Grid DP, and compressing to a rolling array |
| 49 | 1143 Longest Common Subsequence | **Two-string DP**: one index per string |
| 50 | 5 Longest Palindromic Substring | **Interval DP**, recurring by interval length |

→ reference: `dp.md`

---

## Where to go next

The fifty above cover recognition. What they do not cover:

| Direction | Start with |
|---|---|
| Design problems | 146 LRU Cache, 155 Min Stack (revisited), 295 Find Median from Data Stream |
| Heaps and Top-K | 215 Kth Largest Element, 347 Top K Frequent Elements, 23 Merge k Sorted Lists |
| Greedy | 55 Jump Game, 45 Jump Game II, 435 Non-overlapping Intervals |
| Bit manipulation | 136 Single Number, 338 Counting Bits, 191 Number of 1 Bits |
| Harder DP | 72 Edit Distance, 312 Burst Balloons, 10 Regular Expression Matching |
| Advanced structures | 208 Implement Trie, 307 Range Sum Query (BIT), 208 → 212 Word Search II |

---

## Advising notes

**On pace.** One stage is roughly a week at 3–5 problems a week. Whether a stage is finished is not about having seen the answers — it is about being able to write stage 3 from a blank editor without looking anything up. Say this explicitly; people measure progress by problems attempted and get a false reading.

**On getting stuck.** Twenty minutes of genuine effort, then read the solution — but afterwards, close it and rewrite from scratch. Reading a solution creates recognition, not the ability to produce one, and the gap between the two is where the whole difficulty lives.

**On revisiting.** Redo the problems marked as teaching a specific idea (13, 19, 23, 31, 40, 44, 47) about two weeks later. If any of them fails the second time, that idea was recognized, not learned.

**On this list versus others.** Roughly the same ground as NeetCode 150, cut to a third. The cut is deliberate: 150 problems is a curriculum, and 50 is something a person actually finishes. Once these are solid, extra volume from any list is fine — the recognition is already in place by then.
