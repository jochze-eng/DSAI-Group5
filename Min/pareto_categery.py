import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned CSV file
df = pd.read_csv("jobs_cleaned.csv")

# Define salary bins and labels
salary_bins = [0, 3000, 5000, 7000, 10000, float('inf')]
salary_labels = ["Below 3K", "3K-5K", "5K-7K", "7K-10K", "10K Above"]

# Create a new column for salary bins
df["Salary Bin"] = pd.cut(df["Min Salary"].fillna(0), bins=salary_bins, labels=salary_labels, right=False)

# Explode the Skills/Industry column into separate rows (handling multiple skills per job)
df_exploded = df.assign(Skills_Industry=df["Skills/Industry"].str.split(", ")).explode("Skills_Industry")

# Define Finance-related keywords
finance_keywords = ["Finance", "Banking", "Investment", "Accounting", "Fintech", "finance"]

# Identify Finance-related rows
df_exploded["Is_Finance"] = df_exploded["Skills_Industry"].str.contains('|'.join(finance_keywords), case=False, na=False)

# Count occurrences of each Salary Bin within each Skill/Industry
salary_skill_counts = df_exploded.groupby(["Salary Bin", "Skills_Industry"]).size().unstack(fill_value=0)

# Compute total job counts per salary bin
salary_total_counts = salary_skill_counts.sum(axis=1)

# Compute cumulative percentage for Pareto line
cumulative_percentage = salary_total_counts.cumsum() / salary_total_counts.sum() * 100

# Define custom colors: Blue for Finance-related, Grey for others
colors = ["blue" if any(fin in skill for fin in finance_keywords) else "grey" for skill in salary_skill_counts.columns]

# Plot stacked bar chart for salary bins grouped by industry/skill
fig, ax1 = plt.subplots(figsize=(12, 7))

# Stacked bar chart with custom colors
salary_skill_counts.plot(kind="bar", stacked=True, ax=ax1, color=colors, alpha=0.8)
ax1.set_ylabel("Number of Jobs")
ax1.set_title("Pareto Chart of Salary Range Grouped by Industry/Skill\n(Blue = Finance, Grey = Other Industries)")

# Secondary axis for Pareto curve
ax2 = ax1.twinx()
ax2.plot(salary_total_counts.index, cumulative_percentage, color="red", marker="o", linestyle="-", linewidth=2, label="Cumulative %")
ax2.set_ylabel("Cumulative Percentage")
ax2.set_ylim(0, 110)

# Show legend
ax1.legend(title="Industry/Skill", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.show()
