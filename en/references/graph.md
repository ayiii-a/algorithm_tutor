# Graphs

## Three things to settle first

### 1. How to build the graph

The input is usually an **edge list** `[[a,b], ...]` that must be converted into an **adjacency list**.

⚠️ **Do not reverse the direction**: if `[a, b]` reads "a depends on b", draw it as `b → a` (prerequisite points to dependent):
```python
graph[b].append(a)
indegree[a] += 1
```
Reverse it and the meaning of "in-degree" flips, which breaks the entire algorithm. **This is the single most common careless error in topological sort.**

### 2. BFS or DFS

| Requirement | Use |
|---|---|
| **Shortest path** (unweighted) | **BFS** (expands level by level; the first arrival is the shortest) |
| Connectivity / reachability | Either |
| Enumerate all paths | DFS + backtracking |
| Topological sort | Either (Kahn is BFS, three-colour marking is DFS) |
| **Large or deep graph** | **BFS** (a DFS 10⁵ levels deep overflows the stack; Python's limit is 1000) |

### 3. Whether `visited` must be undone

> **Enumerating all paths → undo it** (this route failed, but another route may legitimately pass through this cell)
> **Connectivity / shortest path → do not undo it** (once visited, mark it permanently)

---

## Topological sort

**Reformulation**: can all tasks be completed ⟺ **is the directed graph acyclic** (acyclic = DAG).

### BFS / Kahn (recommended)

1. Build the graph and count each node's **in-degree**
2. Enqueue every node with in-degree 0
3. Dequeue one → decrement the in-degree of each successor → enqueue any that hit 0
4. **`finished == total number of nodes`** → acyclic

**What in-degree means: how many prerequisites are still unmet; it can start only at 0.**
When a cycle exists, the in-degrees of the nodes on it **never reach 0**, so they never enter the queue and `finished` ends up short of the total.

**Free by-product**: the dequeue order is a valid topological ordering (210 uses it directly).

### DFS with three-colour marking

- `0` unvisited / `1` **in progress (grey)** / `2` finished (black)
- **Hitting a node marked "in progress (1)" → there is a cycle** (you looped back to an ancestor on the current path)
- "Finished (2)" acts as memoization, preventing repeated exploration from degenerating into exponential time

**Grey ≠ black is the heart of cycle detection**: only re-encountering a node on the *current* DFS path counts as a cycle; meeting a fully-explored black node just means two paths converged.

---

## Union-Find

**Trigger**: dynamic connectivity, merging sets, detecting a cycle in an undirected graph.

```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])    # path compression
    return parent[x]

def union(x, y):
    rx, ry = find(x), find(y)
    if rx == ry: return False           # already connected (in an undirected graph, a cycle)
    parent[rx] = ry
    return True
```

With **union by rank** this is near O(1). Applies to: 547 Number of Provinces, 200 Islands (DFS also works), 684 Redundant Connection, 990 Satisfiability of Equality Equations.

---

## Common pitfalls

- Building the edges in the wrong direction
- Forgetting `visited` → self-loops and cycles cause infinite loops
- Treating a directed graph as undirected (adding edges both ways)
- The `start == target` edge case
- Recursive DFS overflowing the stack on a large graph
