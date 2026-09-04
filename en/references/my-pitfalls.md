# My Recorded Mistakes

> **This file is yours to maintain.** It starts empty. Add an entry every time you get something wrong, and the tutor will check it before reviewing your code — so a repeated mistake gets flagged as repeated rather than explained from scratch again.
>
> A mistake you make three times is a different problem from a mistake you make once. This file exists to make the difference visible.

## How to record one

Keep each entry to three lines. What matters is that the **pattern** is searchable, not that the write-up is complete.

```markdown
### <short name of the pattern>
- **Where**: problem number(s) where it bit you
- **The mistake**: what you actually wrote
- **The fix**: what it should have been, in one line
```

## How the tutor uses it

Before delivering a verdict in Mode B, it scans this file. If your bug matches a recorded pattern, it says so up front:

> This is the same mistake as entry *"mixing binary search templates"* — third time. See below for why the pattern keeps recurring.

Then it spends its words on **why the pattern keeps happening** rather than re-explaining the mechanics.

---

## Entries

<!-- Add yours below. The examples are commented out; delete them or replace them. -->

<!--
### Mixing binary search templates
- **Where**: 852, 33
- **The mistake**: `right = n` with `while left < right` but shrinking via `right = mid - 1`
- **The fix**: pick one template and keep all three parts consistent

### Forgetting the first-column update after compressing to 1-D
- **Where**: 64
- **The mistake**: inner loop starts at `j = 1`, so `dp[0]` is never updated per row
- **The fix**: `dp[0] += grid[i][0]` at the top of each row

### Python integer width
- **Where**: CCI 05.03, CCI 05.08
- **The mistake**: right-shifting a negative number, expecting it to reach 0
- **The fix**: `num &= 0xFFFFFFFF` on input; convert back to signed on output
-->
