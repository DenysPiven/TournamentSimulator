import pygame
import json
import random
import time

start_time = time.time()

WIDTH, HEIGHT = 1800, 1000
FPS = 60
MATCH_WIDTH = 200
MATCH_HEIGHT = 50
SPACING_X = 240
SPACING_Y = 80

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Elimination Simulator")
font = pygame.font.SysFont("Arial", 16)
clock = pygame.time.Clock()

# Load players
with open("../players.json", "r") as f:
    player_list = json.load(f)
players = {p['id']: p for p in player_list}
player_names = {p['id']: p['name'] for p in player_list}

# Load matches
with open("double_elimination_matches.json", "r") as f:
    matches = json.load(f)

# Initialize match state
for match in matches:
    match['status'] = 'pending'
    match['progress'] = 0
    match['winner'] = None
    match['p1'] = match.get('p1_id')
    match['p2'] = match.get('p2_id')
    match['time_elapsed'] = 0
    match['pause_after'] = 0

# Track player routes
player_origin = {}

# Position calculation
match_coords = {}


def get_match_pos(match):
    hardcoded_positions = {
        # WB matches (id: (x, y))
        1: (100, 100),
        2: (100, 200),
        3: (100, 300),
        4: (100, 400),
        5: (340, 50),
        6: (340, 150),
        7: (340, 250),
        8: (340, 350),
        15: (580, 100),
        16: (580, 300),
        20: (820, 200),
        22: (1060, 250),

        # LB matches
        9: (100, 900),
        10: (100, 800),
        11: (100, 700),
        12: (100, 600),
        13: (340, 850),
        14: (340, 650),
        17: (580, 600),
        18: (580, 800),
        19: (820, 700),
        21: (1060, 650),
    }

    return hardcoded_positions.get(match['id'], (0, 0))


for match in matches:
    match_coords[match['id']] = get_match_pos(match)


def resolve_player(slot, match):
    key = slot + '_from'
    if match[slot] is None and key in match:
        src = match[key]
        origin = next((m for m in matches if m['id'] == src['match']), None)
        if origin and origin['status'] == 'done':
            if src['type'] == 'winner':
                result = origin['winner']
            else:
                result = origin['p1'] if origin['p2'] == origin['winner'] else origin['p2']
            match[slot] = result
            player_origin[result] = match['id']


def draw_match(match):
    x, y = match_coords[match['id']]
    pygame.draw.rect(screen, (50, 50, 50), (x, y, MATCH_WIDTH, MATCH_HEIGHT), border_radius=6)
    pygame.draw.rect(screen, (0, 255, 0) if match['status'] == 'done' else (0, 120, 255),
                     (x, y, MATCH_WIDTH, MATCH_HEIGHT), 2)

    title = f"{match['bracket']} R{match['round']}"
    screen.blit(font.render(title, True, (255, 255, 0)), (x, y - 18))

    if match['p1'] is not None:
        name1 = player_names[match['p1']]
        color1 = (0, 255, 0) if match['status'] == 'done' and match['p1'] == match['winner'] else (255, 0, 0) if match['status'] == 'done' else (255, 255, 255)
        screen.blit(font.render(name1, True, color1), (x + 5, y + 5))

    if match['p2'] is not None:
        name2 = player_names[match['p2']]
        color2 = (0, 255, 0) if match['status'] == 'done' and match['p2'] == match['winner'] else (255, 0, 0) if match['status'] == 'done' else (255, 255, 255)
        screen.blit(font.render(name2, True, color2), (x + 5, y + 25))

    if match['status'] == 'running':
        prog_width = int(MATCH_WIDTH * match['progress'])
        pygame.draw.rect(screen, (0, 255, 0), (x, y + MATCH_HEIGHT - 6, prog_width, 5))


def get_player_busy_status():
    busy = set()
    for m in matches:
        if m['status'] == 'running':
            if m['p1'] is not None:
                busy.add(m['p1'])
            if m['p2'] is not None:
                busy.add(m['p2'])
    return busy


def can_start(match, busy_players):
    resolve_player('p1', match)
    resolve_player('p2', match)

    if match['p1'] is None or match['p2'] is None:
        return False
    if match['p1'] in busy_players or match['p2'] in busy_players:
        return False
    if match['p1'] in player_origin and player_origin[match['p1']] != match['id']:
        return False
    if match['p2'] in player_origin and player_origin[match['p2']] != match['id']:
        return False

    return match['status'] == 'pending'


def run_sim():
    running = True
    tournament_done = False

    while running:
        screen.fill((25, 25, 25))
        busy_players = get_player_busy_status()

        for m in matches:
            draw_match(m)

        # Start new matches
        for m in matches:
            if can_start(m, busy_players):
                m['status'] = 'running'
                m['start_real_time'] = time.time()

        # Update running matches
        for m in matches:
            if m['status'] == 'running':
                p1_speed = players.get(m['p1'], {}).get('speed', 1.0)
                p2_speed = players.get(m['p2'], {}).get('speed', 1.0)
                estimated_time = 30 / ((p1_speed + p2_speed) / 2)
                m['progress'] += 1 / (estimated_time * FPS)
                if m['progress'] >= 1:
                    m['status'] = 'done'
                    m['end_real_time'] = time.time()
                    m['real_duration'] = m['end_real_time'] - m['start_real_time']
                    m['winner'] = random.choice([m['p1'], m['p2']])
                    player_origin[m['winner']] = m['id']
                    print(f"[MATCH DONE] Match {m['id']} ({player_names[m['p1']]} vs {player_names[m['p2']]}) "
                          f"finished in {m['real_duration']:.2f} minutes. Winner: {player_names[m['winner']]}")

        pygame.display.flip()
        clock.tick(FPS)

        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if tournament done (once)
        if not tournament_done and all(m['status'] == 'done' for m in matches):
            print("\n--- FINAL RANKING ---")

            ranking_order = [22, 22, 21, 19, 17, 18, 14, 13, 12, 11, 10, 9]
            used = set()

            for i, match_id in enumerate(ranking_order):
                match = next((m for m in matches if m['id'] == match_id), None)
                if not match:
                    print(f"{i+1}. ??? (match {match_id} not found)")
                    continue

                if i == 0:
                    player_id = match['winner']
                else:
                    player_id = match['p1'] if match['p2'] == match['winner'] else match['p2']

                name = player_names.get(player_id, f"Player_{player_id}")
                print(f"{i+1}. {name}")
                used.add(player_id)

            print("\n--- TOURNAMENT COMPLETE ---")
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"Total duration: ({int(elapsed // 60)} hours, {int(elapsed / 60)} minutes)")

            tournament_done = True

    pygame.quit()


if __name__ == '__main__':
    run_sim()


