# Proof Techniques

Tools for **arguing that an algorithm is correct**, as opposed to figuring out how to code it. Load this for course-style questions: correctness proofs, reductions, "why does this greedy rule work", "show that this bound is tight".

For complexity derivations specifically (Master Theorem, amortized analysis, loop invariants), see `complexity-and-proofs.md` — the two files are meant to be used together.

---

## First: which kind of argument is being asked for

| The question | The tool that fits |
|---|---|
| Prove this algorithm produces a correct/optimal output | Induction, exchange argument, or a structural property (cut property, greedy-stays-ahead) |
| Prove this terminates | A decreasing measure into a well-founded set |
| Prove this bound | Recurrence, amortized analysis, or an adversary argument for lower bounds |
| Prove X is NP-hard | Reduction **from** a known hard problem |
| Show a heuristic fails | A single counterexample — construct it, do not describe it |

**Naming the tool before using it is half the teaching.** Students usually know the definitions but do not know which weapon the situation calls for.

---

## Induction, in its four working forms

### Weak induction
Base case, then P(n-1) → P(n). Adequate for simple recurrences.

### Strong induction
Assume P(k) for **all** k < n. Necessary whenever the recursion splits into pieces of unpredictable size — quicksort, divide-and-conquer with uneven splits, most tree algorithms.

> Merge sort correctness: assume both recursive calls sort **arbitrary shorter** arrays correctly (strong), then show `merge` preserves sortedness. Weak induction cannot express this — the two halves are not "n-1".

### Structural induction
Induct over how the object is built, not over a number. The natural form for trees, expressions, and grammars.

> BST in-order traversal is sorted: base case is the empty tree; the inductive step assumes it for both subtrees, then uses the BST invariant to show the concatenation `left ++ [root] ++ right` is sorted.

### Loop invariant = induction on iterations
Initialization is the base case, maintenance is the inductive step, termination is where the conclusion is read off. See `complexity-and-proofs.md` for the full pattern.

---

## Greedy: two standard skeletons

### Exchange argument
Transform any optimal solution into the greedy one, one swap at a time, never getting worse. Covered in `complexity-and-proofs.md`.

### Greedy stays ahead
Show that after every step k, the greedy partial solution is at least as good as any other solution's first k steps, by some measure. Then it must be optimal at the end.

> Interval scheduling: after picking k intervals, greedy's kth interval finishes no later than the kth interval of any other valid schedule. Induct on k.

**When to use which**: exchange arguments suit "the optimum is a set and we swap members"; stays-ahead suits "the solution is built in a sequence and we compare prefixes".

---

## The cut property (MST correctness)

The single lemma behind both Kruskal and Prim:

> For any cut of the graph, if an edge crossing that cut has strictly minimum weight among all crossing edges, it belongs to **every** MST.

**Proof shape (worth reproducing, it is the model for exchange arguments on graphs)**: suppose some MST T excludes that edge e. Adding e to T creates a cycle, and that cycle must cross the cut a second time via some edge f. Since w(e) < w(f), swapping f for e gives a lighter spanning tree — contradicting that T was minimum.

- **Kruskal** applies it to the cut separating the two components being joined
- **Prim** applies it to the cut between the grown tree and the rest

**When a student asks "why is Kruskal correct", the answer is the cut property plus which cut it is applied to** — not a walkthrough of the algorithm.

---

## Dijkstra: the invariant that carries the proof

> When a vertex is removed from the priority queue, its recorded distance is final and correct.

Prove by induction on the extraction order. The contradiction step: if u were extracted with a non-final distance, the true shorter path to u must leave the settled set at some vertex y with a smaller distance — so y, not u, would have been extracted first.

**Notice where non-negativity is used**: the step that concludes "the remainder of the path can only add weight". This is exactly why negative edges break Dijkstra, and saying so pins the assumption to the line of the proof that needs it. **The most useful thing to point out about a proof is often where each hypothesis is actually consumed.**

---

## Reductions (NP-hardness)

To show X is NP-hard, reduce a **known** hard problem **to** X: `KNOWN ≤ₚ X`.

Three things must be shown, and the third is the one that gets dropped:

1. The transformation runs in **polynomial time**
2. A yes-instance of KNOWN maps to a yes-instance of X
3. **A yes-instance of X maps back to a yes-instance of KNOWN** — the converse

> **The direction is the number-one error.** "X is hard, so I reduce X to 3-SAT" proves nothing about X's hardness; it only shows X is no harder than 3-SAT. The known-hard problem is the *source*, never the target.

To show X is in NP, exhibit a certificate verifiable in polynomial time. NP-complete = in NP **and** NP-hard; a proof of NP-completeness must do both.

---

## Termination

Find a quantity that strictly decreases with every step and cannot decrease forever — a natural number, or any well-founded ordering.

- Euclid's algorithm: the second argument strictly decreases and stays non-negative
- Union-Find with union by rank: the number of components decreases
- A loop with `left < right` and both moving inward: `right - left` decreases

**When a student's recursion runs forever, the missing piece is almost always this measure** — that is the useful diagnostic question: *what is getting strictly smaller here?*

---

## Five gaps that void a proof

The place to look when a student's proof "feels" wrong but they cannot see why:

| Gap | What it looks like |
|---|---|
| **Induction hypothesis too weak** | The step needs a stronger claim than the one being inducted on. Fix by strengthening the statement — counterintuitively, proving *more* is often easier |
| **Base case does not cover reality** | Proved for n=1, but the recursion bottoms out at n=0 or n=2 |
| **Only one direction of an equivalence** | Especially in reductions and in "if and only if" claims |
| **Assuming the conclusion** | "The greedy choice is optimal, therefore greedy is optimal" |
| **"Clearly" doing the real work** | The word marks the exact step that was skipped. Whenever it appears, that is the step to expand |

**When reviewing a student's proof, check these five before anything else.** Nearly every broken proof at this level is one of them.

---

## Textbook anchors

Students often need the standard name so they can find it in their course materials.

| Topic | CLRS |
|---|---|
| Loop invariants, asymptotic notation | Ch. 2–3 |
| Master Theorem, recurrences | Ch. 4 |
| Amortized analysis (all three methods) | Ch. 17 |
| Greedy, exchange arguments, matroids | Ch. 16 |
| MST and the cut property | Ch. 23 |
| Dijkstra and Bellman-Ford | Ch. 24 |
| NP-completeness and reductions | Ch. 34 |

Give the chapter when the student appears to be following a course — it lets them check the canonical statement rather than trusting a paraphrase.
