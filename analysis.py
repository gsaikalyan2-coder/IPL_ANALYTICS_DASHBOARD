import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data.csv")

# -------------------------------
# BASIC INFO
# -------------------------------
print(df.head())
print(df.info())
print(df.describe())

# -------------------------------
# 1. BAR CHART → Wins by Team
# -------------------------------
wins = df[df["Result"] == "Win"]["Team"].value_counts()

plt.figure()
wins.plot(kind='bar')
plt.title("Wins by Team")
plt.xlabel("Team")
plt.ylabel("Number of Wins")
plt.show()


# -------------------------------
# 2. LINE CHART → Runs Trend
# -------------------------------
plt.figure()
plt.plot(df["Runs"])
plt.title("Runs Trend Across Matches")
plt.xlabel("Match Number")
plt.ylabel("Runs")
plt.show()


# -------------------------------
# 3. SCATTER PLOT → Runs vs Strike Rate
# -------------------------------
plt.figure()
plt.scatter(df["Runs"], df["StrikeRate"])
plt.title("Runs vs Strike Rate")
plt.xlabel("Runs")
plt.ylabel("Strike Rate")
plt.show()


# -------------------------------
# 4. HISTOGRAM → Runs Distribution
# -------------------------------
plt.figure()
plt.hist(df["Runs"])
plt.title("Distribution of Runs")
plt.xlabel("Runs")
plt.ylabel("Frequency")
plt.show()


# -------------------------------
# 5. HEATMAP → Correlation
# -------------------------------
plt.figure()
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True)
plt.title("Correlation Heatmap")
plt.show()
