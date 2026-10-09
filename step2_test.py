"""Step 2. The reversal. 'The test is 90 % right' is not 'you are 90 % likely to be ill'."""
import random
from bayes import reverse
from save import save

PEOPLE, ILL, CATCH, ALARM = 10000, 0.01, 0.90, 0.09   # made-up test: 1 in 100 ill, 90 % caught, 9 % false alarms
ill = round(PEOPLE * ILL)
well = PEOPLE - ill
true_pos = round(ill * CATCH)
false_pos = round(well * ALARM)
print(f"{PEOPLE} people: {ill} ill, {well} well")
print(f"positive tests: {true_pos} from the ill, {false_pos} from the well, {true_pos + false_pos} in all")
print(f"ill, given a positive test: {true_pos} / {true_pos + false_pos} = {true_pos / (true_pos + false_pos):.1%}")

chain, p = [ILL], ILL
for n in (1, 2, 3):
    p = reverse(p, CATCH, ALARM)   # yesterday's answer is today's starting point
    chain.append(p)
    print(f"Bayes's rule after {n} positive test{'s' if n > 1 else ''}: {p:.1%}")
print(f"after one negative test instead: {reverse(ILL, 1 - CATCH, 1 - ALARM):.2%}")

random.seed(2)
pos = pos_ill = 0
for _ in range(1000000):           # check by brute force: a million random people
    sick = random.random() < ILL
    if random.random() < (CATCH if sick else ALARM):
        pos += 1
        pos_ill += sick
print(f"a million simulated people: {pos} positive, {pos_ill} of them ill = {pos_ill / pos:.1%}")
save("test", {"people": PEOPLE, "ill": ill, "well": well, "true_pos": true_pos, "false_pos": false_pos,
              "share": true_pos / (true_pos + false_pos), "chain": chain, "neg": reverse(ILL, 1 - CATCH, 1 - ALARM),
              "sim": [pos, pos_ill], "catch": CATCH, "alarm": ALARM})
