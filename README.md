# 🏆 Tournament Simulator

Visual simulation of **Swiss System**, **Double Elimination**, and **Single Elimination** tournaments using **Python** and **Pygame**.

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

### 📜 License

MIT

---

Built with ❤️ by Denys
