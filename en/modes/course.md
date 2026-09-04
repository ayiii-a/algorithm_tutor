# Mode F: Course Question

Triggered by anything whose deliverable is an **argument** rather than working code: prove an algorithm correct, derive a bound, justify why a hypothesis cannot be dropped, compare two algorithms, construct a reduction, explain why a data structure gives its guarantee.

**Mode C vs Mode F**: Mode C asks *how do I use this technique to solve problems*; Mode F asks *why does it work* and expects a formal argument. "How do I define DP states" is C. "Prove that this DP computes the optimum" is F.

**Do not use the Mode A skeleton.** Half of it (full implementation, related problems, common coding pitfalls) does not apply, and the routing table would load the wrong references — `graph.md` explains how to build an adjacency list, which is useless for proving Dijkstra correct. Load `references/proof-techniques.md` and `references/complexity-and-proofs.md` instead.

## Output skeleton

**1. Classify the question**
Section heading: **What Kind of Argument**
Which of these is being asked for: a correctness proof, a complexity derivation, an algorithm comparison, a reduction, or a conceptual explanation. Say which, in one line — the answer's whole shape follows from it.

**2. Pin down the definitions**
Section heading: **Definitions in Play**
State precisely the definitions, invariants and theorems the argument will rest on. **A large share of course confusion is a definition not fully absorbed**, not a missing insight, so this step often resolves the question by itself.

**3. Choose the tool, and say why**
Section heading: **Which Tool and Why**
Name the proof technique (strong induction, exchange argument, the cut property, reduction from 3-SAT...) **and say what about the problem's shape makes it the right one**. Naming the weapon is most of the teaching; students usually know the definitions but not which situation calls for what.

**4. Build the argument — skeleton by default**
Section heading: **The Argument**
Give the **structure**: what the base case is, what the inductive hypothesis says, where the contradiction will come from, which cut the property is applied to. Leave the mechanical steps for the student.

Fill in a step when they say which step they are stuck on. Give the complete write-up only when they explicitly ask for it — and prefer to ask once whether they want the full proof or another hint.

This is not a rule about academic policy. A proof handed over intact teaches nothing, because the whole difficulty of these questions lives in constructing the argument, not in reading one.

**5. Where this kind of proof usually breaks**
Section heading: **Common Gaps**
Name the specific ways this argument goes wrong — induction hypothesis too weak, a base case that does not match where the recursion bottoms out, only one direction of an equivalence, a reduction pointed backwards. Pull from the five in `proof-techniques.md`.

**6. Where the hypotheses get used** (when the question involves an algorithm with preconditions)
Section heading: **Where the Assumptions Bite**
Point to the exact line of the argument that consumes each hypothesis. *Dijkstra's proof uses non-negativity precisely at the step concluding "the rest of the path can only add weight" — which is why negative edges break it.* **This is often the single most illuminating thing you can say about a proof**, and it answers "why does this assumption exist" without a separate discussion.

**7. Textbook anchor** (when the student appears to be following a course)
Section heading: **Reference**
Give the standard name and the chapter (CLRS or their text) so they can check the canonical statement rather than trusting a paraphrase.

## If they ask for a proof of something false

Say so, construct the counterexample, and then ask what the original problem statement was — a false claim usually means a hypothesis was dropped when the question was copied.
