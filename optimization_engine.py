# optimization_engine.py — AI 230 · Project 3 · Optimization Engine
# Two cashiers race to make change with the FEWEST coins:
#   the sprinter (greedy, Notes 08)  vs  the notebook (dynamic programming, Notes 09).
# Mission: write greedy_coins, then invent a coin set that fools it.

import time

def greedy_coins(coins, amount):
    """The sprinter: grab the biggest coin that still fits, again and again.
    Return how many coins it used (or None if it gets stuck)."""
    
    coins = sorted(coins, reverse = True)
    count = 0

    for c in coins:
        while amount >= c:
            amount -= c
            count += 1

    if amount == 0:
        return count
    else:
        return None

def fewest_coins(coins, amount):
    """The notebook, straight from Notes 09: any coin set, always right."""
    best = [0] + [None] * amount          # best[a] = fewest coins for amount a
    for a in range(1, amount + 1):        # answer every amount, small to large
        for c in coins:                   # try every possible first grab
            if c <= a and best[a - c] is not None:
                option = best[a - c] + 1  # the grab, plus the looked-up rest
                if best[a] is None or option < best[a]:
                    best[a] = option      # write the winner in the notebook
    return best[amount]

# ======================================================================
# YOUR TRAP CURRENCY GOES HERE — a coin set that fools the greedy cashier.
# Rules: include a 1, use at least 3 different coins, and don't reuse
# the class examples {1,3,4}, {1,4,5} or {1,5,7}. Name your currency for
# zero points and eternal glory:   # The Brooklyn Bagel Dollar
MY_COINS = [1,6,7]
# ======================================================================

AMOUNTS = range(1, 301)   # every amount from 1 to 300

def race(name, coins):
    start = time.perf_counter()
    g = [greedy_coins(coins, a) for a in AMOUNTS]
    t_greedy = time.perf_counter() - start
    start = time.perf_counter()
    d = [fewest_coins(coins, a) for a in AMOUNTS]
    t_dp = time.perf_counter() - start
    wrong = [a for a, x, y in zip(AMOUNTS, g, d) if x != y]
    print(f"  {name:<22} greedy {t_greedy*1000:6.1f} ms   notebook {t_dp*1000:6.1f} ms"
          f"   greedy wrong on {len(wrong):3d} of {len(AMOUNTS)} amounts")
    if wrong:
        a = wrong[0]
        print(f"  {'':<22} first trap: make {a} -> greedy says "
              f"{g[a - 1]} coins, notebook says {d[a - 1]}")
    return wrong

if __name__ == "__main__":
    if greedy_coins([25, 10, 5, 1], 41) is None:
        print("greedy_coins isn't written yet -- open the file and write it first.")
        raise SystemExit

    print(f"THE RACE: every amount from 1 to {AMOUNTS[-1]}, fewest coins wins\n")
    us = race("US coins 25 10 5 1", [25, 10, 5, 1])
    tiny = race("Notes 08 coins 4 3 1", [4, 3, 1])

    # is your greedy really greedy? It must be perfect on US coins
    # AND fall for the famous trap: 3 coins for 6 with {1, 3, 4}.
    if not us and greedy_coins([4, 3, 1], 6) == 3:
        print("\n  GREEDY CHECK PASSED: perfect on US coins, fooled by {1, 3, 4} like a true sprinter")
    else:
        print("\n  GREEDY CHECK not yet: greedy should be perfect on US coins and say 3 for 6 with {1, 3, 4}")

    mine = sorted(set(MY_COINS), reverse=True)
    if not mine:
        print("  no trap currency yet -- put your coins in MY_COINS.")
    elif 1 not in mine or len(mine) < 3 or set(mine) in ({1, 3, 4}, {1, 4, 5}, {1, 5, 7}):
        print("  MY_COINS breaks a rule: include a 1, use 3+ different coins, no class examples.")
    else:
        print()
        trap = race("YOUR coins " + " ".join(map(str, mine)), mine)
        if trap:
            print(f"\n  TRAP CHECK PASSED: your currency fools greedy on {len(trap)} amounts")
        else:
            print("\n  TRAP CHECK not yet: greedy got every amount right -- this currency is greedy-safe. Try again!")
