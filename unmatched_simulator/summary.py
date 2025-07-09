import pandas as pd


def read_summary(path):
    data = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if " - " in line and "% wins" in line:
                name = line.split(" - ")[0].split(". ", 1)[-1].strip()
                percent = float(line.split(" - ")[1].replace("% wins", "").strip())
                data[name] = percent
    return data


# === Шляхи до файлів ===
path_markov = "log/markov_chain/summary.txt"
path_sim = "log/sim/summary.txt"

# === Зчитування даних ===
markov = read_summary(path_markov)
sim = read_summary(path_sim)

# === Об'єднання у DataFrame ===
all_names = sorted(set(markov) | set(sim))
df = pd.DataFrame(index=all_names)
df["Simulation Wins (%)"] = pd.Series(sim)
df["Markov Wins (%)"] = pd.Series(markov)
df["Diff (Markov - Sim)"] = (df["Markov Wins (%)"] - df["Simulation Wins (%)"]).abs().round(2)
df["Average Wins (%)"] = ((df["Simulation Wins (%)"] + df["Markov Wins (%)"]) / 2).round(2)

# === Сортування за середнім
df = df.sort_values("Average Wins (%)", ascending=False)

# === Збереження у CSV ===
output_path = "log/markov_chain/markov_vs_simulation_comparison.csv"
df.to_csv(output_path, index_label="Character")

# === Виведення логів ===
print(f"✅ CSV saved to: {output_path}")
print(f"🔢 Total characters: {len(df)}")
print("\n🏅 Top 10 by average win rate:")
print(df.head(10))
