# Mode B: Review Code

## Output skeleton (in this order)

**0. Check the recorded mistakes** (silent step — no output of its own)
Read `references/my-pitfalls.md`. If the bug matches a pattern recorded there, say so in the verdict: *"this is the same pattern as 'mixing binary search templates' — you've hit it before."* Then spend the explanation on **why the pattern keeps recurring** rather than re-teaching the mechanics from scratch.
If the file is empty or nothing matches, proceed normally and do not mention it.

**1. Verdict first** (1–2 sentences)
Is the code "fully correct", "right idea but buggy", or "the approach itself is wrong"? **Do not open with praise and then pivot — state the verdict directly.**

If the code is **fully correct**, say so plainly — "this code is correct, no changes needed" — then explain which key decisions it got right (reinforce what worked), and only then consider optional optimizations or style notes. Do not invent flaws to seem useful.

**2. Pinpoint the bug**
- **Give a counterexample**: construct a concrete input that makes this code fail, and state what it outputs versus what it should output.
- If the user supplied a failing test case, trace that exact case and pinpoint the line and step where it starts to diverge.
- With multiple bugs, list them separately and mark severity (fatal / serious / minor / style).

**3. Explain the root cause**
Do not stop at "this line is wrong" — explain **why it went wrong**: a conceptual mismatch (e.g. treating a non-propagating problem as a DFS propagation), a template mix-up (e.g. mixing closed-interval and half-open binary search), or a boundary oversight.

**4. Fixed code**
Preserve the **user's original approach and variable names** wherever possible; make the minimal edit. If the user's approach genuinely cannot work, first explain why, then offer an alternative — but state clearly that this is a change of approach, not a patch.

**4b. Verify before presenting** (whenever a code execution tool is available)
Run the fixed code through `scripts/verify.py` against the user's failing case plus a few edge cases (empty input, single element, duplicates, extreme values) before showing it. State the result in one line: `verified: 5/5 cases pass`.

```bash
python3 scripts/verify.py sol.py --method minPathSum \
    --cases '[{"args": [[[1,3,1],[1,5,1],[4,2,1]]], "expect": 7}]'
```

Add `--unordered` when any output order is acceptable, and `"inplace": 0` to a case when the problem mutates its first argument instead of returning.
If verification fails, **fix it before presenting** — do not show code you have not run. If no execution tool is available, say so instead of implying the code was tested.

**5. Key points**
Walk through each fix and what the change means.

**6. Summary table**
A table with: `Your version | Problem | Fix`.

**7. Lesson / takeaway** (always required)
Extract one transferable lesson from this bug. For example: "passing all the samples ≠ correct logic", "don't mix binary search templates", "duplicate elements break the decision criterion of binary search".

If this is a bug worth remembering, offer the three-line entry ready to paste into `references/my-pitfalls.md` — pattern name, where it bit, the fix. Offer it once; do not push if it is ignored.

## Special care

*(The universal rules in `SKILL.md` also apply here — in particular "the user may be right" and "do not rewrite their approach". Both matter most in this mode.)*

- When the user finds a clever non-standard but correct solution, **acknowledge it and explain why it works**, and you may note where its applicability ends.
- A correct solution written in an unusual style is not a bug. Style suggestions belong after the verdict, clearly marked as optional.
