"""Step 5. The weak point: the starting belief is a choice. Three observers, the same balls."""
import random
from bayes import flat, after, guess
from save import save

random.seed(1812)
RATE = 0.30                        # the truth, hidden from all three
rates, even = flat()


def norm(b):
    t = sum(b)
    return [x / t for x in b]


starts = {
    "open": even,                                             # every rate equally likely
    "biased": norm([r ** 20 for r in rates]),                 # as if 20 hits were already seen
    "closed": norm([1.0 if r > 0.5 else 0.0 for r in rates]),  # 'it cannot be under one half'
}
hits, n, rows = 0, 0, []
print(f"true rate {RATE}")
for stop in (0, 10, 100, 1000, 10000):
    while n < stop:
        hits += random.random() < RATE
        n += 1
    row = {"n": n, "hits": hits}
    for name, start in starts.items():
        b = after(rates, start, hits, n - hits)
        row[name] = guess(rates, b)
        row[name + "_curve"] = [round(sum(b[i:i + 5]) * 200, 4) for i in range(0, 1000, 5)]
    print(f"after {n:5d} tries ({hits:4d} hits): open {row['open']:.3f}   biased {row['biased']:.3f}   closed {row['closed']:.3f}")
    rows.append(row)
print(f"open and biased end {abs(rows[-1]['open'] - rows[-1]['biased']):.4f} apart; closed is still {rows[-1]['closed'] - RATE:.3f} from the truth")
save("start", {"rate": RATE, "rows": rows})
