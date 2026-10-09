"""Bayes's rule in plain Python. No libraries."""
import math


def reverse(start, if_true, if_false):
    """Bayes's rule for one yes-or-no question.
    start: how likely 'yes' was before the clue.
    if_true, if_false: how likely the clue is when the answer is yes, and when it is no."""
    yes = start * if_true
    no = (1 - start) * if_false
    return yes / (yes + no)


def flat(cells=1000):
    """Candidate rates from 0 to 1, all believed equally: Bayes's starting point."""
    rates = [(i + 0.5) / cells for i in range(cells)]
    return rates, [1 / cells] * cells


def update(rates, belief, hit):
    """One try comes in. Weigh every candidate rate by how well it predicted the result."""
    new = [b * (r if hit else 1 - r) for r, b in zip(rates, belief)]
    total = sum(new)
    return [x / total for x in new]


def after(rates, start, hits, misses):
    """The belief after many tries at once. Same as calling update() for each try."""
    logs = [math.log(b) + hits * math.log(r) + misses * math.log(1 - r) if b > 0 else None
            for r, b in zip(rates, start)]
    top = max(x for x in logs if x is not None)
    new = [math.exp(x - top) if x is not None else 0.0 for x in logs]
    total = sum(new)
    return [x / total for x in new]


def guess(rates, belief):
    """The chance the next try is a hit: the average of the belief."""
    return sum(r * b for r, b in zip(rates, belief))


def middle(rates, belief, share=0.9):
    """The range that holds the middle 90 % of the belief."""
    edge, run, lo, hi = (1 - share) / 2, 0.0, None, None
    for r, b in zip(rates, belief):
        run += b
        if lo is None and run >= edge:
            lo = r
        if hi is None and run >= 1 - edge:
            hi = r
    return lo, hi


def below(rates, belief, limit):
    """How much of the belief sits at or below a rate."""
    return sum(b for r, b in zip(rates, belief) if r <= limit)


def succession(hits, tries):
    """Laplace's rule of succession: the chance of a hit on the next try."""
    return (hits + 1) / (tries + 2)
