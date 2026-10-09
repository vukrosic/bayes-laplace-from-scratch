# Bayes and Laplace from scratch

Code for the video **Become Bayes and Laplace in 16 Minutes**.
Thomas Bayes left an essay in his papers when he died in 1761: how to go from what you saw back to what is probably true. Pierre-Simon Laplace found the same rule in 1774 and turned it into a tool. It is one move: for every candidate answer, multiply your belief by the chance that this candidate gives what you just saw, then scale the beliefs to add up to 1.
These seven small programs rebuild the rule and use it. 468 lines of Python 3, standard library only, nothing to install.

```bash
./run_all.sh          # runs all seven steps; about 40 seconds; expected output is in demo-output.txt
```

| File | Idea | What the run shows |
| --- | --- | --- |
| `bayes.py` | The rule | `flat` (1,000 candidate rates, all equally believed), `update` (multiply, then scale), `guess`, `middle` (the range that holds 90 % of the belief) and `succession` (Laplace's shortcut). Every step imports it. |
| `step1_table.py` | Bayes's table | A hidden mark at 0.711. After 1 ball the guess is 0.667, after 10 balls the range is 0.435 to 0.865, after 1,000 balls it is 0.684 to 0.732. The order of the balls does not matter. |
| `step2_test.py` | A medical test | 1 person in 100 is ill, the test catches 90 % and gives a false alarm for 9 %. A positive result means 9.2 % ill, not 90 %. A second positive: 50.3 %. A third: 91.0 %. |
| `step3_succession.py` | Laplace's rule: (hits + 1) / (tries + 2) | A million made-up worlds agree with the rule: after 10 of 10 the next try works 91.7 % of the time. A new place with 10 good meals of 10 scores below an old place with 480 of 500 (95.8 %). The sunrise: 1,826,214 to 1. |
| `step4_births.py` | His real data | 251,527 boys and 241,945 girls baptised in Paris, 1745 to 1770. The chance that boys are not more likely is 1.15e-42. Laplace printed 1.1521 divided by 10 to the 42. |
| `step5_start.py` | The weak point: where you start | Three observers with different starting beliefs watch the same tries. Two end 0.0014 apart after 10,000 tries. The one who started with zero belief below one half never gets there. |
| `step6_mail.py` | A junk mail filter | Plain counts: 21 of 24 right, and all 21 verdicts are forced by one word with a zero count; 3 messages get no answer. Add one to every count: 24 of 24. |
| `step7_buttons.py` | Thompson sampling (1933) | Three buttons with click rates 4 %, 5 % and 7 %, 20,000 visitors, 200 runs. Test 100 each then commit: 1,310 clicks, a worse button kept in 40 runs. Draw from each belief curve: 1,366 clicks, a worse button once. |

`save.py` writes each step's numbers to `runs/`, and the animation reads them from there, so every number on screen comes from these runs.
Python 3.12 and 3.13 print the same output for all seven steps.

## What this is not

- Not real data, except step 4. The medical test, the two restaurants, the 60 mail messages and the three buttons are made-up teaching examples; their inputs are at the top of each file.
- Not a real mail filter. `mail.py` holds 60 short messages. Real filters learn from millions and look at more than single words.
- Not how large models are fitted. A grid of 1,000 candidates works for one unknown rate. With many unknowns the grid is too big, and other methods estimate the same belief.
- Not a way around the starting belief. Step 5 shows what the start does: it fades with data unless it gives a zero to the truth.

Sources for the history: MacTutor biographies of Bayes and Laplace; "An Essay towards solving a Problem in the Doctrine of Chances", Philosophical Transactions 53 (1763); Laplace, "Essai philosophique sur les probabilités" (1814); W. R. Thompson, Biometrika 25 (1933).

## Try it

In `step5_start.py`, change `RATE` to 0.6 and run it again. The closed observer now ends near the truth. Why?

MIT licence.
