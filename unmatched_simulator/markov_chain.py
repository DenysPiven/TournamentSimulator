import numpy as np
import pandas as pd
import os

# === 1. Завантаження таблиць ===
probs_df = pd.read_csv("assets/probabilities.csv", index_col=0)
matches_df = pd.read_csv("assets/matches_count.csv", index_col=0)

# === 1.1. Фільтрація персонажів
filtered_names = [name for name in probs_df.index if " alt " not in name.lower() and "yennefer" not in name.lower()]
probs_df = probs_df.loc[filtered_names, filtered_names]
matches_df = matches_df.loc[filtered_names, filtered_names]

# === 2. Побудова матриці ймовірностей з урахуванням матчів
M = np.zeros_like(probs_df.values, dtype=float)
for i, name1 in enumerate(probs_df.index):
    for j, name2 in enumerate(probs_df.columns):
        count = matches_df.iloc[i, j]
        prob = probs_df.iloc[i, j]
        if count < 5 or prob == -2:
            M[i, j] = 50
        else:
            M[i, j] = prob

# === 3. Стохастична матриця
row_sums = M.sum(axis=1)
P = M / row_sums[:, np.newaxis]

# === 4. Стаціонарний розподіл (Марков)
pi = np.ones(M.shape[0]) / M.shape[0]
for _ in range(1000):
    pi_next = pi @ P
    if np.allclose(pi, pi_next, atol=1e-10):
        break
    pi = pi_next

# === 5. Формування результатів
ranking = pd.Series(pi, index=probs_df.index).sort_values(ascending=False)
ranking = (ranking / ranking.sum()) * 100  # нормалізація до 100%

# === 6. Формування тексту
lines = ["Tournament Winner Rankings (markov):"]
for i, (name, percent) in enumerate(ranking.items(), start=1):
    lines.append(f"{i}. {name} - {percent:.2f}% wins")
output = "\n".join(lines)

# === 7. Вивід у консоль
print(output)

# === 8. Запис у файл
os.makedirs("log/markov_chain", exist_ok=True)
with open("log/markov_chain/summary.txt", "w", encoding="utf-8") as f:
    f.write(output)
