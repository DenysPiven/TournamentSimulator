import pygame
import pandas as pd
import json
import random

MATCH_WIDTH = 180
MATCH_HEIGHT = 60
PADDING_Y = 20
SCROLL_SPEED = 20
FPS = 60

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Unmatched Tournament Simulator")
font = pygame.font.SysFont("Arial", 16)
clock = pygame.time.Clock()

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
        if i + 1 < len(player_list):
            pairs.append((player_list[i], player_list[i+1]))
        else:
            next_round.append(player_list[i])
    return pairs, next_round

def simulate_round(current_players, round_num, start_match_id, logs):
    pairs, next_round = generate_pairs(current_players)
    round_matches = []
    for p1, p2 in pairs:
        prob = get_match_probability(p1, p2)
        name1 = id2name[p1]
        name2 = id2name[p2]
        winner = p1 if random.randint(1, 100) <= prob else p2
        logs.append(
            f"Round {round_num}: {name1} vs {name2}, Prob: {prob:.1f}%, Matches: {matches_df.loc[name1, name2]}, Winner: {id2name[winner]}"
        )
        next_round.append(winner)
        round_matches.append({
            "id": start_match_id,
            "round": round_num,
            "p1": p1,
            "p2": p2,
            "winner": winner
        })
        start_match_id += 1
    return round_matches, next_round, start_match_id

def run_tournament():
    all_matches = []
    rounds = []
    logs = []
    random.shuffle(players)
    current_players = [p['id'] for p in players]
    round_num = 1
    match_id = 1

    while len(current_players) > 1:
        round_matches, current_players, match_id = simulate_round(current_players, round_num, match_id, logs)
        rounds.append(round_matches)
        all_matches.extend(round_matches)
        round_num += 1

    match_coords = {}
    for r_idx, round_matches in enumerate(rounds):
        offset_y = ((MATCH_HEIGHT + PADDING_Y) * (2 ** r_idx)) // 2
        for m_idx, match in enumerate(round_matches):
            spacing_y = (MATCH_HEIGHT + PADDING_Y) * (2 ** r_idx)
            match_coords[match['id']] = (
                50 + r_idx * (MATCH_WIDTH + 50),
                offset_y + m_idx * spacing_y,
            )
    return all_matches, match_coords, rounds, logs

def draw_match(m, offset_x, offset_y):
    x, y = match_coords[m['id']]
    x += offset_x
    y += offset_y

    pygame.draw.rect(screen, (50, 50, 50), (x, y, MATCH_WIDTH, MATCH_HEIGHT), border_radius=6)
    pygame.draw.rect(screen, (0, 255, 0), (x, y, MATCH_WIDTH, MATCH_HEIGHT), 2)

    winner = m['winner']
    p1name = id2name.get(m['p1'], "???")
    p2name = id2name.get(m['p2'], "???")

    color_p1 = (0, 255, 0) if m['p1'] == winner else (255, 0, 0)
    color_p2 = (0, 255, 0) if m['p2'] == winner else (255, 0, 0)

    screen.blit(font.render(p1name, True, color_p1), (x + 5, y + 5))
    screen.blit(font.render(p2name, True, color_p2), (x + 5, y + 30))

all_matches, match_coords, rounds, logs = run_tournament()

running = True
scroll_x, scroll_y = 0, 0
max_matches_in_round = max(len(r) for r in rounds)
total_width = len(rounds) * (MATCH_WIDTH + 50) + 100
total_height = (MATCH_HEIGHT + PADDING_Y) * (2 ** (len(rounds)-1)) + 100

for log in logs:
    print(log)

while running:
    screen.fill((20, 20, 20))
    for m in all_matches:
        draw_match(m, scroll_x, scroll_y)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_SHIFT:
                scroll_x += event.y * SCROLL_SPEED
                scroll_x = min(0, max(scroll_x, screen.get_width() - total_width))
            else:
                scroll_y += event.y * SCROLL_SPEED
                scroll_y = min(0, max(scroll_y, screen.get_height() - total_height))
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                all_matches, match_coords, rounds, logs = run_tournament()
                for log in logs:
                    print(log)
    clock.tick(FPS)

pygame.quit()
