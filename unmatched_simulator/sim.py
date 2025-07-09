import json
import pandas as pd
import random
import csv
import os
import sys
from collections import Counter


# === Tee for stdout and log ===
class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()


# === Paths ===
ASSET_DIR = "assets"
LOG_DIR = "log/sim"
os.makedirs(LOG_DIR, exist_ok=True)
sys.stdout = Tee(sys.__stdout__, open(os.path.join(LOG_DIR, "summary.txt"), "w", encoding="utf-8"))

# === Load data ===
with open(os.path.join(ASSET_DIR, "players.json")) as f:
    players = json.load(f)

matches_df = pd.read_csv(os.path.join(ASSET_DIR, "matches_count.csv"), index_col=0)
probs_df = pd.read_csv(os.path.join(ASSET_DIR, "probabilities.csv"), index_col=0)
id2name = {p['id']: p['name'] for p in players}


# === Helper functions ===
def get_match_probability(p1, p2):
    name1 = id2name[p1]
    name2 = id2name[p2]
    count = matches_df.loc[name1, name2]
    if count < 5:
        return 50
    prob = probs_df.loc[name1, name2]
    return 50 if prob == -2 else 100 - prob


def generate_pairs(player_list):
    pairs = []
    next_round = []
    for i in range(0, len(player_list), 2):
        if i + 1 < len(player_list):
            pairs.append((player_list[i], player_list[i + 1]))
        else:
            next_round.append(player_list[i])
    return pairs, next_round


def run_tournament_with_rounds():
    current_players = [p['id'] for p in players]
    random.shuffle(current_players)
    all_rounds = []
    all_matches = []

    while len(current_players) > 1:
        next_players = []
        this_round = []
        for i in range(0, len(current_players), 2):
            if i + 1 < len(current_players):
                p1, p2 = current_players[i], current_players[i + 1]
                prob = get_match_probability(p1, p2)
                winner = p1 if random.randint(1, 100) <= prob else p2
                loser = p2 if winner == p1 else p1
                next_players.append(winner)
                this_round.append((winner, loser))
            else:
                next_players.append(current_players[i])
        all_rounds.append(this_round)
        current_players = next_players

    winner_id = current_players[0]
    winner_name = id2name[winner_id]

    # Переможені по раундах
    defeated_per_round = []
    for rnd in all_rounds:
        defeated_this_round = [id2name[loser] for winner, loser in rnd if winner == winner_id]
        defeated_per_round.append(defeated_this_round)

    return winner_name, defeated_per_round


def run_simulations(num_simulations=10000):
    winners = []
    rows = []
    max_rounds = 0

    for i in range(1, num_simulations + 1):
        winner, rounds = run_tournament_with_rounds()
        winners.append(winner)
        row = {"tournament": i, "winner": winner}
        for r, defeated_list in enumerate(rounds, start=1):
            row[f"round_{r}"] = ", ".join(defeated_list)
        max_rounds = max(max_rounds, len(rounds))
        rows.append(row)

    # Write CSV
    fieldnames = ["tournament", "winner"] + [f"round_{i}" for i in range(1, max_rounds + 1)]
    with open(LOG_DIR + "/tournament_log.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
            quotechar='"'
        )
        writer.writeheader()
        writer.writerows(rows)

    # Final stats
    winner_counts = Counter(winners)
    for p in players:
        if p['name'] not in winner_counts:
            winner_counts[p['name']] = 0
    rankings = sorted(winner_counts.items(), key=lambda x: x[1], reverse=True)
    return rankings, num_simulations


# === Run ===
if __name__ == "__main__":
    rankings, num_simulations = run_simulations(100000)
    print("Tournament Winner Rankings:")
    for rank, (name, wins) in enumerate(rankings, start=1):
        percent = wins / num_simulations * 100
        print(f"{rank}. {name} - {percent:.2f}% wins")
