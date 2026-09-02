# Algorithm Tutor

A [Claude Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that gives algorithm explanations a **fixed, predictable structure**.

This is not a tool for solving more problems — Claude can already do that. It is a tool for making the *explanation* consistent: the same sections, in the same order, with the same things pinned down, every time you ask about a problem.

Available in **English** and **Chinese (中文)**. See [Install](#install).

---

## The problem it solves

Ask an LLM about an algorithm problem twice and you get two differently-shaped answers. One time it opens with code, another time with a long analogy. Sometimes it walks through an example you did not need; sometimes it skips the boundary condition you were actually stuck on. When you are working through a few hundred problems, that inconsistency is the friction.

This skill fixes the shape of the answer so you always know where to look:

- Where the complexity analysis is
- Where the "here is how people get this wrong" note is
- Where the related-problems table is

And, just as importantly, it defines when a section should be **left out** rather than padded.

---

## What it does

### Three modes

The skill first decides which situation you are in:

| You post | Mode |
|---|---|
| A problem statement | **A — Teach a new problem** |
| Your own code + "what's wrong with it" | **B — Review code** |
| A question about a technique ("how do I define DP states") | **C — Topic explanation** |

### Mode A skeleton

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

Two of those sections are **conditional**, each with an explicit test:

- **Problem Restatement** only appears when the statement itself is the obstacle — an unstated convention, a constraint that is easy to skim past, layered rules presented flat, or a reskin of a problem you have already solved.
- **Underlying Idea** only appears when it passes this test: *could this paragraph guide you through a problem you have not seen yet?* If the takeaway would just restate the solution ("this problem teaches you to use DP"), it is omitted.

The skill explicitly prefers a shorter answer over a padded one.

### Mode B skeleton

```
1. Verdict first           ← "correct" / "right idea, buggy" / "wrong approach"
2. Pinpoint the bug        ← construct a concrete failing input
3. Root cause              ← why it went wrong, not just where
4. Fixed code              ← minimal edit, your variable names preserved
5. Key Points
6. Summary table           ← your version | problem | fix
7. Lesson
```

Mode B has three rules that matter more than the skeleton:

- If the code is correct, **say so and stop** — do not invent flaws to seem useful
- **Do not rewrite your approach into a preferred one.** If you say "fix it within my approach", it works inside your framework
- **You may be right.** If you challenge the explanation, it verifies rather than deflects

---

## How the references work

The core of this skill is not the output skeleton — it is the 13 reference files. Each one answers a single question for its problem type:

> **What does this kind of problem require you to pin down, and in what order?**

For example, `references/dp.md` does not list DP problems. It says: derive the state definition first (using a freeze test and a drop-dimension test), then the transition, then the base cases, then the traversal order, then where the answer lives — and it explains what goes wrong at each step.

`references/binary-search.md` says: decide what you are bisecting, pick a template (**and never mix two templates**), handle mid and out-of-bounds, then the equality on the boundary.

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

Only the reference files matching the problem type are loaded, so the context cost stays small.

---

## Repository layout

```
algorithm_tutor/
├── english/                    # English edition
│   ├── SKILL.md
│   └── references/             # 13 files
├── cn/                         # 中文版
│   ├── SKILL.md
│   └── references/             # 13 个文件
└── LICENSE
```

The two editions are **the same skill**, section for section — only the language differs. Pick one; installing both at once gives Claude two skills with conflicting names.

**Which one?** Either edition replies in whatever language you write in. The difference is the terminology it reaches for: the Chinese edition has the Chinese terms fixed in place (同层去重, 以 i 结尾, 滚动数组), so the wording stays identical across sessions instead of being re-translated each time. If you work in Chinese, `cn/` is the more consistent choice. Otherwise use `english/`.

---

## Install

Clone the repo and package the edition you want:

```bash
git clone https://github.com/ayiii-a/algorithm_tutor.git
cd algorithm_tutor

# English edition
cp -r english algorithm_tutor && zip -r algorithm_tutor.skill algorithm_tutor/ && rm -rf algorithm_tutor

# Chinese edition — same command with `cn` in place of `english`
```

> The copy step matters. The folder inside the archive must be named `algorithm_tutor` to match the `name:` field in `SKILL.md`. Zipping `english/` directly produces a folder called `english`, and the skill will not load.

Then add the `.skill` file through the Claude interface, start a conversation, paste a problem, and ask how to solve it.

---

## Customizing it

The output shape is entirely defined by `SKILL.md`. Every section is plain Markdown — edit it.

Common adjustments:

**Want a worked example every time?** The skill suppresses example walkthroughs by default (they are usually padding). Remove the "No walkthrough by default" line under *Output constraints*.

**Want it to stop before showing code?** Change step 3 so it presents the approach and waits.

**Want different sections?** Add, remove or reorder them in the skeleton. Nothing else depends on the numbering.

### Adding a new problem type

Two steps:

1. Write `references/your-type.md`, structured around *what this kind of problem requires you to pin down, and in what order*
2. Add a row to the routing table in `SKILL.md`:

```markdown
| Segment tree, range updates | `references/segment-tree.md` |
```

That is the whole extension mechanism.

---

## Notes on the problem references

Problems are cited by number. Two numbering systems appear:

- Bare numbers are **LeetCode** (`84 Largest Rectangle in Histogram`)
- `CCI xx.xx` is **Cracking the Coding Interview** (`CCI 08.03 Magic Index`)

Some of the pitfalls recorded in the references are unusually specific — the exact wrong width formula in problem 84, the two Python integer-width traps, why duplicate elements break the decision criterion in binary search. They are specific because they came out of actually getting them wrong.

---

## Contributing

Useful contributions, roughly in order of value:

- **A pitfall that is not yet recorded** — especially one you hit yourself
- **A new reference file** for an uncovered type (segment trees, string matching, computational geometry, math/number theory)
- **A correction** — if a reference states something wrong, that is the highest-priority issue

Please keep the existing shape: references describe *what to pin down and in what order*, not lists of problems and solutions.

**If you change one edition, mirror it in the other** so `english/` and `cn/` stay in sync. A PR touching only one side is still welcome — just say so, and the other side can follow in a separate commit.

---

## License

MIT
