import json
import pandas as pd
import random
from collections import Counter

with open("players.json") as f:
    players = json.load(f)

matches_df = pd.read_csv("matches_count.csv", index_col=0)
probs_df = pd.read_csv("probabilities.csv", index_col=0)
id2name = {p['id']: p['name'] for p in players}

def get_match_probability(p1, p2):
    name1 = id2name[p1]
    name2 = id2name[p2]
    count = matches_df.loc[name1, name2]
    if count < 5:
        return 50
    prob = probs_df.loc[name1, name2]
    if prob == -2:
        prob = 50
    return 100 - prob

def generate_pairs(player_list):
    pairs = []
    next_round = []
    for i in range(0, len(player_list), 2):
        if i+1 < len(player_list):
            pairs.append((player_list[i], player_list[i+1]))
        else:
            next_round.append(player_list[i])
    return pairs, next_round

def simulate_round(current_players):
    pairs, next_round = generate_pairs(current_players)
    for p1, p2 in pairs:
        prob = get_match_probability(p1, p2)
        winner = p1 if random.randint(1, 100) <= prob else p2
        next_round.append(winner)
    return next_round

def run_tournament():
    current_players = [p['id'] for p in players]
    random.shuffle(current_players)
    while len(current_players) > 1:
        current_players = simulate_round(current_players)
    return current_players[0]

def run_simulations(num_simulations=10000):
    winners = []
    for _ in range(num_simulations):
        winner = run_tournament()
        winners.append(id2name[winner])
    winner_counts = Counter(winners)
    for p in players:
        if p['name'] not in winner_counts:
            winner_counts[p['name']] = 0
    rankings = sorted(winner_counts.items(), key=lambda x: x[1], reverse=True)
    return rankings, num_simulations

if __name__ == "__main__":
    rankings, num_simulations = run_simulations(100000)
    print("Tournament Winner Rankings:")
    for rank, (name, wins) in enumerate(rankings, start=1):
        percent = wins / num_simulations * 100
        print(f"{rank}. {name} - {percent:.2f}% wins")