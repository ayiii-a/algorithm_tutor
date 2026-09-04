# Algorithm Tutor

A [Claude Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that gives algorithm work a **fixed, predictable structure** — whether you are learning a new problem, debugging your own code, planning what to practice, or proving something for a class.

This is not a tool for solving more problems; Claude can already do that. It is a tool for making the *response* consistent: the same sections, in the same order, with the same things pinned down, every time.

Available in **English** and **Chinese (中文)**. See [Install](#install).

---

## The problem it solves

Ask an LLM about an algorithm problem twice and you get two differently-shaped answers. One time it opens with code, another time with a long analogy. Sometimes it walks through an example you did not need; sometimes it skips the boundary condition you were actually stuck on. When you are working through a few hundred problems, that inconsistency is the friction.

This skill fixes the shape of the answer so you always know where to look — and, just as importantly, defines when a section should be **left out** rather than padded.

---

## Six modes

The skill first works out what kind of help you need, then loads only that mode's template.

| You post | Mode |
|---|---|
| A problem statement | **A — Teach a new problem** |
| Your own code + "what's wrong with it" | **B — Review code** |
| "How do I define DP states?" | **C — Topic explanation** |
| "Where do I start? What should I do next?" | **D — Practice planning** |
| "Quiz me" / "hints only" | **E — Interview simulation** |
| "Prove this is correct" / "derive the bound" | **F — Course question** |

**C vs F**: Mode C asks how to *use* a technique; Mode F asks *why it works* and expects a formal argument.

### Mode A — Teach a new problem

```
0. Problem Restatement     (conditional)
1. Problem Type
2. Deriving the Approach   ← the main body
3. Full Implementation
4. Complexity
5. Key Points
6. Common Pitfalls
7. Related Problems
8. Underlying Idea         (conditional)
```

Two sections are **conditional**, each with an explicit test:

- **Problem Restatement** appears only when the statement itself is the obstacle — an unstated convention, a constraint that is easy to skim past, layered rules presented flat, or a reskin of something you already solved.
- **Underlying Idea** appears only if it passes this test: *could this paragraph guide you through a problem you have not seen yet?* If the takeaway would just restate the solution ("this problem teaches you to use DP"), it is dropped.

A shorter answer is explicitly preferred over a padded one.

### Mode B — Review code

```
0. Check your recorded mistakes   (silent)
1. Verdict first                  ← "correct" / "right idea, buggy" / "wrong approach"
2. Pinpoint the bug               ← construct a concrete failing input
3. Root cause                     ← why it went wrong, not just where
4. Fixed code                     ← minimal edit, your variable names preserved
4b. Verify before presenting      ← actually run it
5. Key Points
6. Summary table
7. Lesson
```

Three rules matter more than the skeleton:

- If the code is correct, **say so and stop** — no inventing flaws to seem useful
- **Your approach is not rewritten into a preferred one.** Ask for a fix within your framework and you get one
- **Never presents code it has not run**, when a code execution tool is available (see [Verification](#verification))

### Mode F — Course question

Coursework is a different job from interview prep, so it gets a different skeleton: classify the argument → pin down the definitions → **name the proof tool and say why it fits** → build the skeleton of the argument → common gaps → **where each hypothesis actually gets used**.

That last one is often the most illuminating thing to say about a proof: *Dijkstra's correctness uses non-negativity precisely at the step concluding "the rest of the path can only add weight" — which is exactly why negative edges break it.*

Step 4 gives the **structure** of the argument by default and fills in a step when you say where you are stuck. Not as a policy about academic honesty, but because the difficulty of these questions lives entirely in constructing the argument, and a proof handed over intact teaches nothing.

### Modes D and E

**D — Practice planning** reads `references/roadmap.md`, a 50-problem path ordered by *what each problem teaches*, and hands you one stage at a time rather than the whole list.

**E — Interview simulation** withholds the answer and escalates one hint level at a time — category → guiding question → state definition → transition → code — stopping after each. A wrong answer gets a question that exposes the problem, the way an interviewer would, rather than a correction.

---

## How the references work

The core of this skill is not the output skeletons — it is the reference files. Each one answers a single question for its problem type:

> **What does this kind of problem require you to pin down, and in what order?**

`references/dp.md` does not list DP problems. It says: derive the state definition first (using a freeze test and a drop-dimension test), then the transition, then the base cases, then the traversal order, then where the answer lives — and it explains what goes wrong at each step.

| Reference | Covers |
|---|---|
| `dp.md` | Five families, knapsack's two orthogonal dimensions, rolling-array direction |
| `binary-search.md` | Four things to pin down, and when duplicates break binary search |
| `backtracking.md` | The four quadrants (permutation/combination × distinct/duplicate) |
| `tree.md` | Five patterns, and why only in-order enables O(h) BST navigation |
| `stack-queue.md` | "What does the stack hold?" — five answers |
| `graph.md` | Building the graph, BFS vs DFS, whether `visited` is undone |
| `linked-list.md` | Three fundamentals and the traps around rewiring |
| `greedy.md` | Exchange arguments, interval sort keys, implicit BFS layering |
| `sliding-window.md` | Where the answer is updated differs for longest vs shortest |
| `bit-math.md` | Bit tools, plus two Python-specific traps |
| `design.md` | Three principles for combining structures |
| `array-techniques.md` | Prefix sums, two pointers, canonical forms, cancellation |
| `simulation.md` | When there is no framework and you just need the rule |
| `complexity-and-proofs.md` | Master Theorem, amortized analysis, loop invariants, lower bounds |
| `proof-techniques.md` | Induction's four forms, the cut property, reductions, five gaps that void a proof |
| `roadmap.md` | The 50-problem practice path |
| `my-pitfalls.md` | **Yours to maintain** — see below |

---

## Two things you maintain

### Your mistake log

`references/my-pitfalls.md` starts empty. Add three lines whenever you get something wrong:

```markdown
### Mixing binary search templates
- **Where**: 852, 33
- **The mistake**: `right = n` with `while left < right` but shrinking via `right = mid - 1`
- **The fix**: pick one template and keep all three parts consistent
```

Mode B checks this file before every verdict. When your bug matches a recorded pattern, it says so up front — *"this is the same mistake as 'mixing binary search templates', third time"* — and spends its words on **why the pattern keeps recurring** instead of re-explaining the mechanics.

A mistake made three times is a different problem from one made once. This file makes the difference visible.

### Verification

`scripts/verify.py` runs a candidate solution against test cases before it is shown to you:

```bash
python3 scripts/verify.py sol.py --method minPathSum \
    --cases '[{"args": [[[1,3,1],[1,5,1],[4,2,1]]], "expect": 7}]'
```

```
1/2 passed

--- case 0 FAILED ---
  args     : [[[1, 3, 1], [1, 5, 1], [4, 2, 1]]]
  expected : 7
  got      : 4
```

Supports `--unordered` for problems where any output order is accepted, `"inplace": 0` for problems that mutate their first argument, and a per-case timeout.

Mode B is instructed to run this before presenting a fix, and to **say so explicitly** when no execution tool is available rather than implying the code was tested.

---

## Repository layout

```
algorithm_tutor/
├── english/                    # English edition
│   ├── SKILL.md                #   77 lines — routing and universal rules only
│   ├── modes/                  #   5 files — one output skeleton each
│   ├── references/             #   17 files
│   └── scripts/verify.py
├── cn/                         # 中文版 — same structure
└── LICENSE
```

**Progressive disclosure.** `SKILL.md` is loaded every conversation, so it holds only the mode-detection table, the type-routing table, and the rules that apply everywhere. Each mode's skeleton lives in its own file and is read only when that mode fires. A conversation about a proof never loads the 100 lines describing how to teach a coding problem — roughly 10,000–16,000 characters saved per conversation compared to keeping everything in one file.

The two language editions are **the same skill**, section for section. Pick one; installing both gives Claude two skills with conflicting names.

**Which one?** Either replies in whatever language you write in. The difference is terminology: the Chinese edition has its Chinese terms fixed in place, so the wording stays identical across sessions instead of being re-translated each time. If you work in Chinese, `cn/` is the more consistent choice.

---

## Install

```bash
git clone https://github.com/ayiii-a/algorithm_tutor.git
cd algorithm_tutor

# English edition
cp -r english algorithm_tutor && zip -r algorithm_tutor.skill algorithm_tutor/ && rm -rf algorithm_tutor

# Chinese edition — same command with `cn` in place of `english`
```

> The copy step matters. The folder inside the archive must be named `algorithm_tutor` to match the `name:` field in `SKILL.md`. Zipping `english/` directly produces a folder called `english`, and the skill will not load.

Then add the `.skill` file through the Claude interface, paste a problem, and ask how to solve it.

---

## Customizing it

Everything is plain Markdown. The pieces you are most likely to touch:

**Change a mode's output** — edit `modes/<name>.md`. Nothing outside that file depends on its internals.

**Want a worked example every time?** Example walkthroughs are suppressed by default because they are usually padding. Remove the "No walkthrough by default" line in `modes/teach.md`.

**Want it to stop before showing code?** Change step 3 in `modes/teach.md` so it presents the approach and waits.

**Add a problem type** — two steps:

1. Write `references/your-type.md`, structured around *what this kind of problem requires you to pin down, and in what order*
2. Add a row to the routing table in `SKILL.md`

**Add a mode** — write `modes/your-mode.md` and add a row to the mode table in `SKILL.md`. That is the whole extension mechanism.

---

## Notes on the problem references

Problems are cited by number. Two numbering systems appear:

- Bare numbers are **LeetCode** (`84 Largest Rectangle in Histogram`)
- `CCI xx.xx` is **Cracking the Coding Interview** (`CCI 08.03 Magic Index`)

Some of the pitfalls are unusually specific — the exact wrong width formula in problem 84, the two Python integer-width traps, why duplicate elements break the decision criterion in binary search. They are specific because they came out of actually getting them wrong.

---

## Contributing

Useful contributions, roughly in order of value:

- **A pitfall that is not yet recorded** — especially one you hit yourself
- **A new reference file** for an uncovered type (segment trees, string matching, computational geometry, number theory)
- **A correction** — if a reference states something wrong, that is the highest-priority issue

Please keep the existing shape: references describe *what to pin down and in what order*, not lists of problems and solutions.

**If you change one edition, mirror it in the other** so `english/` and `cn/` stay in sync. A PR touching only one side is still welcome — just say so, and the other side can follow in a separate commit.

---

## License

MIT
