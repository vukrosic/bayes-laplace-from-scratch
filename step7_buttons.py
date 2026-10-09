"""Step 7. Three versions of a button. Which one do you show the next visitor? (Thompson, 1933)"""
import random
from bayes import flat, after
from save import save

RATES = [0.04, 0.05, 0.07]         # true click rates, hidden from every strategy
VISITORS, REPEATS, TRIAL = 20000, 200, 100
BEST = RATES.index(max(RATES))


def even(shown, clicks, n):
    """Classic test: every version gets the same share, all the way."""
    return n % 3


def test_then_commit(shown, clicks, n):
    """Show each version TRIAL times, then keep the best-looking one for good."""
    if n < 3 * TRIAL:
        return n % 3
    return max(range(3), key=lambda i: clicks[i] / shown[i])


def thompson(shown, clicks, n):
    """One draw from each belief curve; show the version with the highest draw."""
    draws = [random.betavariate(clicks[i] + 1, shown[i] - clicks[i] + 1) for i in range(3)]
    return draws.index(max(draws))


def run(pick, trace=None):
    shown, clicks = [0, 0, 0], [0, 0, 0]
    for n in range(VISITORS):
        i = pick(shown, clicks, n)
        shown[i] += 1
        clicks[i] += random.random() < RATES[i]
        if trace is not None and n + 1 in (30, 100, 300, 1000, 5000, 20000):
            trace.append({"n": n + 1, "shown": shown[:], "clicks": clicks[:]})
    return shown, clicks


print(f"true click rates {RATES}, {VISITORS} visitors, average of {REPEATS} runs. Always the best version: {VISITORS * max(RATES):.0f} clicks")
out = {"rates": RATES, "visitors": VISITORS, "repeats": REPEATS, "trial": TRIAL, "ideal": VISITORS * max(RATES), "runs": {}}
for name, pick in (("even split", even), ("test then commit", test_then_commit), ("thompson", thompson)):
    random.seed(1933)
    totals, best_share, ended_wrong = [], 0, 0
    for _ in range(REPEATS):
        shown, clicks = run(pick)
        totals.append(sum(clicks))
        best_share += shown[BEST] / VISITORS
        ended_wrong += max(range(3), key=lambda i: shown[i]) != BEST
    totals.sort()
    mean, unlucky = sum(totals) / REPEATS, sum(totals[:REPEATS // 10]) / (REPEATS // 10)
    wrong = "never chooses" if pick is even else f"settled on a worse version in {ended_wrong} of {REPEATS} runs"
    print(f"{name:17s} {mean:7.1f} clicks   unluckiest tenth of runs {unlucky:7.1f}   best version shown to {best_share / REPEATS:5.1%}   {wrong}")
    out["runs"][name] = {"clicks": mean, "unlucky": unlucky, "best_share": best_share / REPEATS,
                         "wrong": None if pick is even else ended_wrong, "hist": totals[::4]}

random.seed(7)
trace = []
run(thompson, trace)
rates, start = flat()
print("one Thompson run, visitor by visitor")
for t in trace:
    t["curves"] = [[round(sum(b[i:i + 2]) * 500, 3) for i in range(0, 200, 2)]
                   for b in (after(rates, start, t["clicks"][k], t["shown"][k] - t["clicks"][k]) for k in range(3))]
    print(f"  after {t['n']:4d}: shown {t['shown']}  clicks {t['clicks']}")
out["trace"] = trace
save("buttons", out)
