#!/usr/bin/env python3
"""Can't decide what to read next? Let fate (and a PRNG) decide.

Usage:
  python picker.py            # one random pick
  python picker.py 3          # three picks, no repeats
  python picker.py --tag 神作  # filter by tag
"""
import argparse
import json
import random
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

DATA = Path(__file__).parent / "games.json"


def load_games():
    return json.loads(DATA.read_text(encoding="utf-8"))


def fmt(game):
    stars = "*" * game.get("rating", 8)
    return "{title} ({year}) [{tags}]\n  {stars}\n  {note}".format(
        title=game["title"], year=game["year"], tags="/".join(game["tags"]),
        stars=stars, note=game["note"],
    )


def main():
    ap = argparse.ArgumentParser(description="Random galgame picker")
    ap.add_argument("count", nargs="?", type=int, default=1)
    ap.add_argument("--tag", help="filter by tag")
    args = ap.parse_args()

    games = load_games()
    if args.tag:
        games = [g for g in games if args.tag in g["tags"]]
    if not games:
        sys.exit("no game matches")

    args.count = max(1, min(args.count, len(games)))
    for g in random.sample(games, args.count):
        print(fmt(g), end="\n\n")


if __name__ == "__main__":
    main()
