# 🏆 Tournament Simulator

Visual simulation of Swiss System and Double Elimination tournaments using **Python** and **Pygame**.

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
├── players.json                         # List of players and their speeds
├── LICENSE
├── README.md
└── .gitignore
```

---

### 🧪 Features

* 🖼️ Real-time bracket rendering
* 🔄 Automatic match progression with proper round order
* ⏱️ 15-minute simulated break between Swiss rounds
* 🏁 Ranking output printed at tournament end
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

Each match has:

```json
{
  "id": 1,
  "round": 1,
  "p1_id": 1,
  "p2_id": 2,
  "winner": 1     // optional; used for pre-seeded results
}
```

---

### 📈 Output

* Match progress visualized
* Console shows real-time match logs
* Final rankings printed at the bottom
* Real duration calculated using `time.time()`

---

### 📹 Demo Video

📺 [Watch on YouTube](https://youtu.be/0ObABWuc9Eg)

---

### 📜 License

MIT

---

Built with ❤️ by Denys
