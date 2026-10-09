"""Step 1. Bayes's table. A hidden mark, then balls that only report 'left' or 'right'."""
import random
from bayes import flat, update, after, guess, middle
from save import save

random.seed(1763)                 # the year the essay was read
mark = random.random()            # where the first ball stopped, as a share of the table width
print(f"hidden mark (the program knows it, the observer does not): {mark:.3f}")

rates, belief = flat()
start = belief
left, shown, out = 0, [0, 1, 2, 5, 10, 20, 100, 1000], []
for n in range(0, 1001):
    if n in shown:
        lo, hi = middle(rates, belief)
        print(f"after {n:4d} ball{' ' if n == 1 else 's'}: {left:3d} left   best guess {guess(rates, belief):.3f}   90 % sure it is between {lo:.3f} and {hi:.3f}  (width {hi - lo:.3f})")
        out.append({"n": n, "left": left, "guess": guess(rates, belief), "lo": lo, "hi": hi,
                    "curve": [round(sum(belief[i:i + 5]) * 200, 4) for i in range(0, 1000, 5)]})
    hit = random.random() < mark  # a new ball stops left of the mark with chance `mark`
    left += hit
    belief = update(rates, belief, hit)
    if n < 12:
        out.append({"ball": n + 1, "left": bool(hit)})

once = after(rates, start, left - hit, 1000 - (left - hit))
again = start
for _ in range(left - hit):
    again = update(rates, again, True)
for _ in range(1000 - (left - hit)):
    again = update(rates, again, False)
gap = max(abs(a - b) for a, b in zip(once, again))
print(f"order does not matter: all lefts first, or all at once, same curve (largest gap {gap:.1e})")
save("table", {"mark": mark, "rows": [r for r in out if "n" in r], "balls": [r for r in out if "ball" in r]})
