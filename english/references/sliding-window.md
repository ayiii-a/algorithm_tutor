# Sliding Window

## Trigger

> **An optimization problem over a contiguous segment** (longest / shortest / count).

Keywords: **contiguous** subarray or substring + longest / shortest / exactly.

---

## Template

```python
left = 0
for right in range(n):
    add nums[right] to the window

    while the window violates the condition:
        remove nums[left]
        left += 1

    update the answer with (right - left + 1)
```

**Three things to pin down**:
1. **What state the window maintains** (a counter / a hash map / a running sum)
2. **When the left edge shrinks** (the `while` condition)
3. **Where the answer is updated** (after shrinking for longest; before shrinking for shortest)

⚠️ **Longest and shortest update the answer in different places**:
- **Longest**: update after shrinking back to validity (the window stays valid at all times)
- **Shortest**: update as soon as it becomes valid, then keep shrinking to try smaller

---

## Problem map

| Problem | Condition on the window |
|---|---|
| 3 Longest Substring Without Repeating Characters | No repeated character (hash map of positions) |
| 209 Minimum Size Subarray Sum | Sum ≥ target (shortest) |
| 76 Minimum Window Substring | Contains every target character (shortest, hard) |
| **CCI 05.03 Reverse Bits** | At most one 0 |
| 1004 Max Consecutive Ones III | At most k zeros (the generalization of 05.03) |
| 424 Longest Repeating Character Replacement | Non-majority characters in the window ≤ k |
| 438 Find All Anagrams in a String | Fixed-size window + character-count match |

---

## Variant: fixed-size window

When the window size is fixed there is no `while` shrink — just:
```python
for right in range(n):
    add nums[right]
    if right >= k:
        remove nums[right - k]
    if right >= k - 1:
        update the answer
```

---

## Common pitfalls

- Updating the answer in the wrong place (mixing up longest and shortest)
- Forgetting to update the window state while shrinking (hash counts, running sum)
- Computing the window size as `right - left` (it is `right - left + 1`)
- Using `if` instead of `while` to shrink (one step may require several contractions)
