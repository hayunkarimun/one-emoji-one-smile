#!/usr/bin/env python3
"""One Emoji, One Smile — pick the single emoji most likely to make a
stranger smile, scored against the judge's five criteria.

The judge weighs, most important first:
  1. a single emoji a stranger reads as warm and friendly
  2. warmth at first glance, no context needed
  3. universality: any age or background reads it the same way
  4. chosen rather than default: picked for the moment, not the first
     smiley that comes to mind, while staying instantly readable
  5. right for a stranger: no intimacy, sarcasm or flirtation

Weights 5/4/3/2/1 follow that order. Each candidate is scored 1-5 per
criterion; the highest total wins. The winner is written alone, with no
trailing newline, to /output/entry.txt — exactly one emoji, nothing else.
"""

import os

# (emoji, name, scores per criterion 1..5)
CANDIDATES = [
    ("\U0001faf6", "Heart Hands", [5, 5, 5, 5, 4]),
    ("\U0001f917", "Hugging Face", [5, 5, 4, 4, 4]),
    ("\U0001f31e", "Sun with Face", [4, 4, 5, 5, 5]),
    ("\U0001f979", "Face Holding Back Tears", [4, 4, 4, 4, 3]),
    ("\U0001f60a", "Smiling Face with Smiling Eyes", [5, 5, 5, 2, 5]),
    ("\U0001f423", "Hatching Chick", [3, 4, 4, 5, 5]),
]

WEIGHTS = [5, 4, 3, 2, 1]


def score(candidate):
    emoji, name, marks = candidate
    total = sum(w * m for w, m in zip(WEIGHTS, marks))
    return total


def gate_ok(text):
    """Mirror the sealed gate: UTF-8 text of 1 to 8 characters, not
    only white space, and exactly one emoji with nothing else."""
    return 1 <= len(text) <= 8 and text.strip() != "" and len(text) == 1


def main():
    table = []
    for cand in CANDIDATES:
        table.append((score(cand), len(cand[0].encode("utf-8")), cand[0], cand[1]))
    # Highest total wins; ties break to the fewest bytes, then the emoji.
    table.sort(key=lambda row: (-row[0], row[1], row[2]))
    for total, _nbytes, emoji, name in table:
        print(f"{total:3d}  {emoji}  {name}")
    winner = table[0][2]
    assert gate_ok(winner), f"winner fails the gate: {winner!r}"
    print(f"winner: {winner}")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
