# DFA and NFA

Python coursework that simulates a deterministic finite automaton (DFA) and a nondeterministic one (NFA), including epsilon transitions.

`main.py` writes two sample automata to JSON and tests every string of length 2 over `{a, b}`:

- `a_b_dfa.json` — zero or more `a`s followed by a single `b`
- `ba_dfa.json` — the string `ba`

It then reverses each DFA into an NFA: transitions are flipped, a new start state reaches the old final states by epsilon, and the old start state becomes the only final state. The same strings are tested on that reversed language.

## Run

```bash
python3 main.py
```

The script also has a small JSON helper. These commands write or print a sample file; they are separate from the automaton test at the bottom of the file, which always runs:

```bash
python3 main.py write test   # writes test.json
python3 main.py read test    # prints test.json
```

`write trans` saves a tiny word automaton (`The`/`A`/`My`/`Your`, then `cat`/`mouse`, then a verb, then `.`) as `trans.json`.
