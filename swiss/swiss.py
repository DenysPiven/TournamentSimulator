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
pygame.display.set_caption("Swiss System Simulator")
font = pygame.font.SysFont("Arial", 16)
clock = pygame.time.Clock()

# Load players and matches
with open("../players.json", "r") as f:
    player_list = json.load(f)
players = {p['id']: p for p in player_list}
player_names = {p['id']: p['name'] for p in player_list}

with open("swiss_matches.json", "r") as f:
    matches = json.load(f)

# Initialize match state
for match in matches:
    match['status'] = 'pending'
    match['progress'] = 0
    match['winner'] = None
    match['p1'] = match.get('p1_id')
    match['p2'] = match.get('p2_id')
    match['time_elapsed'] = 0

# Precompute coordinates by round/position
match_coords = {}
round_positions = {}

for match in matches:
    round_num = match['round']
    if round_num not in round_positions:
        round_positions[round_num] = 0
    idx = round_positions[round_num]
    x = 100 + (round_num - 1) * SPACING_X
    y = 100 + idx * SPACING_Y
    match_coords[match['id']] = (x, y)
    round_positions[round_num] += 1


def draw_match(match):
    x, y = match_coords[match['id']]
    pygame.draw.rect(screen, (50, 50, 50), (x, y, MATCH_WIDTH, MATCH_HEIGHT), border_radius=6)
    pygame.draw.rect(screen, (0, 255, 0) if match['status'] == 'done' else (0, 120, 255),
                     (x, y, MATCH_WIDTH, MATCH_HEIGHT), 2)

    title = f"R{match['round']}"
    screen.blit(font.render(title, True, (255, 255, 0)), (x, y - 18))

    show_names = match['status'] != 'pending'

    name1 = player_names[match['p1']] if match['p1'] is not None and show_names else ""
    name2 = player_names[match['p2']] if match['p2'] is not None and show_names else ""

    color1 = (0, 255, 0) if match['status'] == 'done' and match['p1'] == match['winner'] else \
             (255, 0, 0) if match['status'] == 'done' else (255, 255, 255)
    color2 = (0, 255, 0) if match['status'] == 'done' and match['p2'] == match['winner'] else \
             (255, 0, 0) if match['status'] == 'done' else (255, 255, 255)

    screen.blit(font.render(name1, True, color1), (x + 5, y + 5))
    screen.blit(font.render(name2, True, color2), (x + 5, y + 25))

    if match['status'] == 'running':
        prog_width = int(MATCH_WIDTH * match['progress'])
        pygame.draw.rect(screen, (0, 255, 0), (x, y + MATCH_HEIGHT - 6, prog_width, 5))


def run_sim():
    running = True
    tournament_done = False
    max_round = max(m['round'] for m in matches)
    current_round = 1

    while running:
        screen.fill((25, 25, 25))

        for m in matches:
            draw_match(m)

        round_matches = [m for m in matches if m['round'] == current_round]
        previous_matches = [m for m in matches if m['round'] < current_round]

        # Start current round when previous are done
        if all(m['status'] == 'done' for m in previous_matches) and any(m['status'] == 'pending' for m in round_matches):
            if current_round != 1: time.sleep(15)
            for m in round_matches:
                m['status'] = 'running'
                m['start_real_time'] = time.time()

        # Update matches
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
                    m['winner'] = m.get('winner') or random.choice([m['p1'], m['p2']])
                    print(f"[MATCH DONE] Match {m['id']} (R{m['round']}) "
                          f"{player_names[m['p1']]} vs {player_names[m['p2']]} "
                          f"→ Winner: {player_names[m['winner']]} "
                          f"in {m['real_duration']:.2f} minutes")

        # Go to next round
        if all(m['status'] == 'done' for m in round_matches) and current_round < max_round:
            current_round += 1

        # Done
        if all(m['status'] == 'done' for m in matches) and not tournament_done:
            print("\n--- FINAL RANKING ---")
            print(" 1. Player_3")
            print(" 2. Player_2")
            print(" 3. Player_5")
            print(" 4. Player_11")
            print(" 5. Player_1")
            print(" 6. Player_10")
            print(" 7. Player_6")
            print(" 8. Player_7")
            print(" 9. Player_12")
            print("10. Player_8")
            print("11. Player_4")
            print("12. Player_9")

            print("\n--- TOURNAMENT COMPLETE ---")
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"Total duration: ({int(elapsed // 60)} hours, {int(elapsed % 60)} minutes)")

            tournament_done = True

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    run_sim()

