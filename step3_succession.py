"""Step 3. Laplace's rule of succession, checked three ways. Then the sunrise."""
import random
from bayes import flat, after, guess, below, succession
from save import save

random.seed(1774)                  # the year of Laplace's memoir
WORLDS, TRIES = 1000000, 10
seen = [[0, 0] for _ in range(TRIES + 1)]   # for each count of hits: worlds seen, and how many hit again
for _ in range(WORLDS):
    rate = random.random()         # a world with an unknown rate, every rate equally likely
    hits = sum(random.random() < rate for _ in range(TRIES))
    seen[hits][0] += 1
    seen[hits][1] += random.random() < rate   # try number eleven
rates, start = flat(10000)
rows = []
print(f"{WORLDS} made-up worlds, {TRIES} tries each, then one more try")
for hits in (10, 7, 5, 0):
    counted = seen[hits][1] / seen[hits][0]
    curve = guess(rates, after(rates, start, hits, TRIES - hits))
    print(f"{hits:2d} of {TRIES}: next try hits in {counted:.4f} of {seen[hits][0]} worlds   curve {curve:.4f}   rule ({hits}+1)/({TRIES}+2) = {succession(hits, TRIES):.4f}")
    rows.append({"hits": hits, "worlds": seen[hits][0], "counted": counted, "curve": curve, "rule": succession(hits, TRIES)})

print("two restaurants")
food = []
for name, good, total in (("new place", 10, 10), ("old place", 480, 500)):
    b = after(rates, start, good, total - good)
    under = below(rates, b, 0.9)
    print(f"{name}: {good} of {total} good reviews = {good / total:.1%}   next visit good {succession(good, total):.1%}   chance its true rate is under 90 %: {f'{under:.1%}' if under >= 0.001 else 'less than 0.1%'}")
    food.append({"name": name, "good": good, "total": total, "raw": good / total, "next": succession(good, total), "under": under,
                 "curve": [round(sum(b[i:i + 20]) * 500, 4) for i in range(5000, 10000, 20)]})

DAYS = 1826213                     # Laplace: 5,000 years of sunrises
print(f"sunrise: {DAYS} of {DAYS} days. Tomorrow: {DAYS + 1}/{DAYS + 2} = {succession(DAYS, DAYS):.9f}, odds {DAYS + 1} to 1")
again = (DAYS + 1) / (DAYS + DAYS + 1)      # the same curve asked about m more days in a row: (n+1)/(n+m+1)
print(f"sunrise every day for the next {DAYS} days as well: {again:.4f}")
print(f"nothing seen yet, 0 of 0: {succession(0, 0):.2f}")
save("succession", {"worlds": WORLDS, "tries": TRIES, "rows": rows, "food": food, "days": DAYS,
                    "tomorrow": succession(DAYS, DAYS), "again": again, "seen": seen})
