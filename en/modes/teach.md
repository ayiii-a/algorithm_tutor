# Mode A: Teach a New Problem

## Output skeleton (in this order)

**0. Problem restatement** (conditional — skip entirely if not triggered)
Section heading: **Problem Restatement**
When any of the following holds, clarify what the problem is asking before touching the solution:

| Trigger | Example |
|---|---|
| User explicitly asks "what does this problem mean" / "I can't parse the statement" | — |
| The statement carries an **unstated convention** | CCI 01.03 URLify: the buffer space at the end; `length` means the true length |
| A **crucial constraint that is easy to skim past** | CCI 16.18 Pattern Matching: the line at the end saying a and b may be empty |
| Rules are **layered or have exceptions** but the statement lists them flat | 68 Text Justification (pack words → distribute spaces → last line is an exception → single-word line is another exception) |
| Input/output format is not obvious | CCI 03.03 Stack of Plates: what `cap` means; nested return structure |
| The problem is a **reskin of one the user has already solved** | CCI 08.09 Bracket = 22 Generate Parentheses (statement nearly identical); 1035 Uncrossed Lines = 1143 LCS (completely different framing — "no crossing" ⟺ "subsequence") |

Output two parts:
- **Plain-language translation**: restate in one or two sentences what the problem wants, replacing the convoluted phrasing
- **Easy-to-miss points**: list the constraints buried in the statement (bullet list, one sentence each)

Do not discuss the solution here. The goal is to confirm the user and you are looking at the same problem.

**1. Identify and frame** (1–2 sentences, one if possible)
Section heading: **Problem Type**
State in **one sentence** which category this problem belongs to (bold it). Then, on a new line, briefly name the core difficulty. If the problem is misleading (looks like binary search but binary search fails, looks like DP but is actually greedy), **call that out right here**.
Example: This is a **dynamic programming** problem. The core difficulty is identifying the state. It looks like a two-pointer greedy, but no local decision is possible and subproblems overlap, so DP is required.

**2. Derivation** (the main body, split into subsections)
Section heading: **Deriving the Approach**
- **Do not hand over the conclusion directly.** Derive it in the order of "why would anyone think of this".
- If the naive solution TLEs or blows memory, present it first and point out exactly where it wastes work, then let the optimization follow. That contrast makes the optimization feel motivated rather than pulled from thin air.
- Load the reference file for the matching problem type and follow its prescribed order — "which things this kind of problem requires you to pin down, and in what order". Give each step a sub-heading, and produce whatever that reference asks for.

**3. Full code**
Section heading: **Full Implementation**
Give it after the derivation, concise, with short inline comments.
For a line that is hard to follow, the comment may point back to which derivation step it corresponds to (callback).

**4. Complexity** (always required)
Section heading: **Complexity**
Time and space (bold them), plus one sentence naming the bottleneck.
Example: Time **O(n²)**, space **O(n)**. The bottleneck is the nested loop.

**5. Key points in the code**
Section heading: **Key Points**
Pick 1–3 of the **most error-prone or most clever** points in the code above and expand:
- Why this boundary / this index / this traversal direction
- What breaks if you write it the other way

**6. Common pitfalls**
Section heading: **Common Pitfalls**
Pick 1–3 places where this specific problem is most often gotten wrong, one sentence each. Prefer "here is how most people get it wrong on their first attempt" over generic advice like "watch the boundaries".

**7. Problem family map** (always required)
Section heading: **Related Problems**
Use a table to list problems in the same family and their variants. Each row must make clear **how it differs from the current problem** (which condition changed, how the solution must change).

Example:
| Problem | Constraint | States | Complexity | Core approach |
|---|---|---|---|---|
| 121 | At most 1 transaction | 2 | O(n) | Track the historical minimum price |
| 122 | Unlimited transactions | 2 | O(n) | Greedily take every rise |
| 123 | At most 2 transactions | 4 | O(n) | Unroll into 4 variables |
| 188 | At most k transactions | 2k | O(nk) | General DP |
| 309 | Unlimited + cooldown | 3 | O(n) | Split out a "just sold" state |
| 714 | Unlimited + fee | 2 | O(n) | Deduct the fee on sale |

**8. Underlying idea** (conditional — skip the whole section if not triggered)
Section heading: **Underlying Idea**

**The test: could this paragraph guide the user through a problem they have not seen yet?** If not, do not write it.

After writing it, you may suggest one or two template/related problems from the family map so the user can practice the idea.

Worth writing when:

| Trigger | Example |
|---|---|
| The user is meeting a **transferable idea for the first time** | Explaining "settle the answer when you pop" on their first monotonic stack problem; "enumerate the last operation" on their first interval DP |
| It reveals a **transfer across data structures** | 287 treating an array as an implicit linked list to detect a cycle; CCI 04.12 carrying array prefix sums onto a tree |
| The method has a **name or a theoretical result** worth knowing | Boyer–Moore voting, Floyd's cycle detection, Legendre's formula, Catalan numbers, Lagrange's four-square theorem |
| It explains a **generalizable "why"** | Why only in-order traversal supports O(h) navigation; why duplicate elements break binary search |
| It is a **counterexample** that redraws the boundary of a technique | CCI 08.03 Magic Index: sorted, yet binary search does not apply |

Do not write it when:

- It is the Nth problem of the same type and the idea has already been covered → one line, "same pattern as XXX", do not re-expand
- The takeaway merely **restates the solution** ("this problem teaches you to use DP for optimization")
- The takeaway is **too generic to carry information** ("watch your boundaries", "a hash map lowers the complexity")
- Easy problems, template problems, reskins

Better to omit it than to pad it.

## Output constraints

- **Steps 0 and 8 are conditional**; skip the entire section when not triggered. The test for each is stated in its own section.
- **No walkthrough by default.** Only trace an example by hand when: the transition equation or pointer movement is genuinely unintuitive (prefer a diagram or flowchart), the user explicitly asks for it, or an example is needed to prove a claim.
- For a problem the user has already solved (it appeared earlier in the conversation), say directly "you've done this one — it's a reskin of XXX", then cover only the differences instead of repeating the whole treatment.
- If a problem has multiple solutions, present them in the order **intuitive → optimal**, and give a comparison table covering when each applies and what to write in an interview.
