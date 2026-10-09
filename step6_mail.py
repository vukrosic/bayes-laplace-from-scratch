"""Step 6. A junk-mail filter from word counts. Laplace's 'plus one' is what keeps it alive."""
import math
from bayes import succession
from mail import JUNK, WANTED, TEST_JUNK, TEST_WANTED
from save import save


def count(messages):
    words = {}
    for m in messages:
        for w in m.split():
            words[w] = words.get(w, 0) + 1
    return words


junk, wanted = count(JUNK), count(WANTED)
known = set(junk) | set(wanted)
print(f"learned from {len(JUNK)} junk and {len(WANTED)} wanted messages: {sum(junk.values())} and {sum(wanted.values())} words, {len(known)} different")


def word_rate(word, counts, plus):
    """How often this word shows up in one pile. plus=1 is Laplace: one made-up sighting of every word."""
    return (counts.get(word, 0) + plus) / (sum(counts.values()) + plus * len(known))


def judge(message, plus):
    """Bayes's rule with many clues: start from the share of junk, then weigh every word."""
    j = math.log(succession(len(JUNK), len(JUNK) + len(WANTED)))
    w = math.log(1 - succession(len(JUNK), len(JUNK) + len(WANTED)))
    for word in message.split():
        if word not in known:
            continue                 # a word never seen anywhere says nothing
        rj, rw = word_rate(word, junk, plus), word_rate(word, wanted, plus)
        j = j + math.log(rj) if rj > 0 and j is not None else None   # None: this pile is ruled out for good
        w = w + math.log(rw) if rw > 0 and w is not None else None
    if j is None and w is None:
        return None, None            # both piles ruled out: the filter has no answer
    if j is None or w is None:
        return ("junk" if w is None else "wanted"), (1.0 if w is None else 0.0)
    p = 1 / (1 + math.exp(w - j))
    return ("junk" if p > 0.5 else "wanted"), p


out = {"train": [len(JUNK), len(WANTED)], "words": len(known), "runs": {}}
tests = [(m, "junk") for m in TEST_JUNK] + [(m, "wanted") for m in TEST_WANTED]
for plus in (0, 1):
    right = wrong = stuck = by_zero = 0
    rows = []
    for message, truth in tests:
        verdict, p = judge(message, plus)
        right += verdict == truth
        stuck += verdict is None
        wrong += verdict is not None and verdict != truth
        by_zero += p in (0.0, 1.0)   # one missing word ruled a pile out; nothing was weighed
        rows.append({"m": message, "truth": truth, "verdict": verdict, "p": p})
    print(f"plus {plus}: {right} right, {wrong} wrong, {stuck} with no answer, out of {len(tests)}   (verdicts forced by a zero: {by_zero})")
    out["runs"][str(plus)] = {"right": right, "wrong": wrong, "stuck": stuck, "by_zero": by_zero, "rows": rows}

show = "we won free tickets to the game come with us"
print(f'one message: "{show}"')
detail = []
for word in show.split():
    cj, cw = junk.get(word, 0), wanted.get(word, 0)
    lean = word_rate(word, junk, 1) / word_rate(word, wanted, 1) if word in known else 1.0
    print(f"  {word:8s} junk {cj}  wanted {cw}   plain counts: {'ZERO in junk' if cj == 0 and cw else 'ZERO in wanted' if cw == 0 and cj else 'new word' if cj + cw == 0 else 'ok':14s}  with plus one: {lean:5.2f} times as likely in junk")
    detail.append({"w": word, "junk": cj, "wanted": cw, "lean": lean})
print(f"  plain counts say: {judge(show, 0)[0]}.  With plus one: {judge(show, 1)[0]}, junk chance {judge(show, 1)[1]:.1%}")
out["show"] = {"m": show, "words": detail, "plain": judge(show, 0)[0], "plus": judge(show, 1)[0], "p": judge(show, 1)[1]}
top = sorted(sorted(known), key=lambda x: word_rate(x, junk, 1) / word_rate(x, wanted, 1))
out["top_wanted"] = [[x, junk.get(x, 0), wanted.get(x, 0)] for x in top[:6]]
out["top_junk"] = [[x, junk.get(x, 0), wanted.get(x, 0)] for x in top[-6:][::-1]]
print("most junk-like words:", ", ".join(x[0] for x in out["top_junk"]), "| most wanted-like:", ", ".join(x[0] for x in out["top_wanted"]))
save("mail", out)
