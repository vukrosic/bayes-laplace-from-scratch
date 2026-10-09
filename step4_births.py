"""Step 4. Laplace's question about Paris: are boys really more likely, or is it luck?"""
import math
from save import save

BOYS, GIRLS = 251527, 241945       # Paris baptisms 1745-1770, the counts Laplace used


def not_above_half(boys, girls, cells=2000000):
    """Share of the belief curve at or below one half. Logs keep the tiny numbers alive."""
    logs = [boys * math.log((i + 0.5) / cells) + girls * math.log(1 - (i + 0.5) / cells) for i in range(cells)]
    top = max(logs)
    return sum(math.exp(x - top) for x in logs[:cells // 2]) / sum(math.exp(x - top) for x in logs)


share = BOYS / (BOYS + GIRLS)
print(f"{BOYS} boys, {GIRLS} girls, {BOYS + GIRLS} births: {share:.2%} boys, {BOYS - GIRLS} more boys than girls")
rows = []
for births in (100, 1000, 10000, 100000, BOYS + GIRLS):
    boys = BOYS if births == BOYS + GIRLS else round(births * share)
    p = not_above_half(boys, births - boys)
    print(f"{births:6d} births with {boys} boys: chance that boys are NOT more likely = {p:.3g}")
    rows.append({"births": births, "boys": boys, "p": p})
p = rows[-1]["p"]
zeros = -math.floor(math.log10(p)) - 1
print(f"written out: 0.{'0' * zeros}{p * 10 ** (zeros + 3):.0f}  ({zeros} zeros after the point)")
print("Laplace's own figure, by hand: 1.1521 / 10^42")
save("births", {"boys": BOYS, "girls": GIRLS, "share": share, "rows": rows, "zeros": zeros, "laplace": 1.1521e-42})
