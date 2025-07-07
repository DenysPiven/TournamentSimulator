# 🏆 Tournament Simulator

Visual simulation of **Swiss System**, **Double Elimination**, and **Single Elimination** tournaments using **Python** and **Pygame**, plus an **Unmatched Tournament Simulator** extension. The Unmatched simulator uses character data from the UM League, randomizes brackets, applies matchup-based probabilities, and corrects for missing data by adjusting to 50/50 where appropriate. It then ranks fighters by win rate after 100,000 simulated tournaments.

---

### 📆 Folder Structure

```
TournamentSimulator/
├── double_elimination/
│   ├── double_elimination.py            # Double Elimination simulation script
│   └── double_elimination_matches.json  # Match structure for DE bracket
│
├── swiss/
│   ├── swiss.py                         # Swiss System simulation script
│   └── swiss_matches.json               # Matches by round (pre-paired)
│
├── single_elimination/
│   ├── single_elimination.py            # Single Elimination simulation script
│   └── single_elimination_matches.json  # Match structure for SE bracket
│
├── unmatched_simulator/
│   ├── main.py
│   ├── matches_count.csv
│   ├── players.json
│   ├── probabilities.csv
│   └── sim.py
│
├── players.json                         # List of players and their speeds
├── LICENSE
├── README.md
└── .gitignore
```

---

### 🧪 Features

* 🖼️ Real-time bracket rendering
* 🔄 Automatic match progression with round scheduling
* ⏱️ Simulated time acceleration (1 sec = 1 min)
* 📆 Round-by-round visual flow
* 🏁 Rankings printed at tournament end
* 💡 Fully customizable match/winner setup via JSON

---

### 🛠 Requirements

* Python 3.8+
* `pygame`

```bash
pip install pygame
```

---

### ▶️ Run

```bash
# Swiss System
python swiss/swiss.py

# Double Elimination
python double_elimination/double_elimination.py

# Single Elimination
python single_elimination/single_elimination.py
```

---

### 📊 Input Files

#### `players.json`

```json
[
  { "id": 1, "name": "Player_1", "speed": 1.3 },
  { "id": 2, "name": "Player_2", "speed": 1.1 }
]
```

#### `*_matches.json`

Each match supports:

```json
{
  "id": 1,
  "round": 1,
  "p1_id": 1,
  "p2_id": 2,
  "winner": 1,         // optional; predefined outcome
  "p1_from": {...},    // for later rounds (by winner/loser)
  "p2_from": {...}
}
```

---

### 📈 Output

* Match progress visualized
* Console shows real-time match logs
* Final rankings printed at the bottom
* Real duration calculated using `time.time()`

#### ⌛ Sample Simulated Durations

* ⭐ Single Elimination: **2 hours 16 minutes**
* ⭐ Swiss System: **3 hours 30 minutes**
* ⭐ Double Elimination: **4 hours 13 minutes**

---

### 📹 Demo Video

📺 [Watch on YouTube](https://youtu.be/0ObABWuc9Eg)

---

I also extended this with an **Unmatched Tournament Simulator**, taking all characters from the Unmatched table on the referenced site, running 100,000 random tournaments, and ranking them by win rates while handling missing match data with fallback probabilities.
For more data, see the official Unmatched statistics table: https://www.umleague.net/fighterstats

**Simulation-based Tournament Winner Rankings (100,000 tournaments):**
1. Medusa - 4.73% wins
2. Sherlock Holmes - 4.59% wins
3. Sun Wukong - 3.57% wins
4. Houdini - 3.52% wins
5. Elektra - 3.40% wins
6. T. Rex - 3.33% wins
7. Golden Bat - 3.21% wins
8. Luke Cage - 3.15% wins
9. Bigfoot - 2.68% wins
10. Doctor Strange - 2.50% wins
11. Achilles - 2.50% wins
12. Dr. Jill Trent - 2.29% wins
13. Raptors - 2.27% wins
14. Nikola Tesla - 2.26% wins
15. Eredin - 2.16% wins
16. She-Hulk - 2.08% wins
17. Triss - 1.77% wins
18. Squirrel Girl - 1.75% wins
19. Ciri - 1.74% wins
20. Chupacabra - 1.67% wins
21. Little Red Riding Hood - 1.62% wins
22. Buffy Xander - 1.62% wins
23. Blackbeard - 1.57% wins
24. Pandora - 1.52% wins
25. Sinbad - 1.49% wins
26. Oda Nobunaga - 1.44% wins
27. Cloak & Dagger - 1.43% wins
28. Dracula - 1.42% wins
29. Loki - 1.41% wins
30. Yennefer - 1.40% wins
31. Ancient Leshen - 1.36% wins
32. Annie Christmas - 1.35% wins
33. Tomoe Gozen - 1.32% wins
34. Spike - 1.28% wins
35. Moon Knight - 1.27% wins
36. Geralt of Rivia - 1.26% wins
37. InGen - 1.19% wins
38. Deadpool - 1.18% wins
39. Angel - 1.18% wins
40. Bruce Lee - 1.16% wins
41. The Wayward Sisters - 1.09% wins
42. Buffy Giles - 1.08% wins
43. Alice - 1.06% wins
44. Titania - 1.05% wins
45. Willow - 1.00% wins
46. Black Panther - 0.91% wins
47. Shakespeare - 0.91% wins
48. Dr. Sattler - 0.86% wins
49. Daredevil - 0.77% wins
50. Spider-Man - 0.76% wins
51. The Genie - 0.71% wins
52. Jekyll & Hyde - 0.71% wins
53. Ms. Marvel - 0.66% wins
54. Beowulf - 0.66% wins
55. Black Widow - 0.62% wins
56. Winter Soldier - 0.61% wins
57. Ghost Rider - 0.56% wins
58. Hamlet - 0.56% wins
59. Bloody Mary - 0.55% wins
60. Philippa - 0.54% wins
61. Bullseye - 0.50% wins
62. Robin Hood - 0.48% wins
63. Invisible Man - 0.42% wins
64. King Arthur - 0.32% wins

### 📜 License

MIT

---

Built with ❤️ by Denys
