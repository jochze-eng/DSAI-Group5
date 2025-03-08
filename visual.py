import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Load the CSV file
#file_path = "/mnt/data/jobs_cleaned.csv"
df = pd.read_csv("jobs_cleaned.csv")

# Display basic information and the first few rows
df.info(), df.head()

# Define salary bins and labels
salary_bins = [0, 3000, 5000, 7000, 10000, float('inf')]
salary_labels = ["Below 3K", "3K-5K", "5K-7K", "7K-10K", "10K Above"]

# Create a new column for salary bins
df["Salary Bin"] = pd.cut(df["Min Salary"].fillna(0), bins=salary_bins, labels=salary_labels, right=False)

# Count occurrences in each salary bin for Pareto Chart
salary_counts = df["Salary Bin"].value_counts().sort_index()
salary_cumsum = salary_counts.cumsum() / salary_counts.sum() * 100

# Pareto Chart
fig, ax1 = plt.subplots(figsize=(8, 5))

ax1.bar(salary_counts.index, salary_counts, color="royalblue", alpha=0.7, label="Count")
ax1.set_ylabel("Number of Jobs", color="royalblue")

ax2 = ax1.twinx()
ax2.plot(salary_counts.index, salary_cumsum, color="red", marker="o", linestyle="-", label="Cumulative %")
ax2.set_ylabel("Cumulative Percentage", color="red")

plt.title("Pareto Chart of Salary Binning")
fig.tight_layout()
plt.show()

# Stacked Bar Chart for Skills/Industry
skill_counts = df["Skills/Industry"].str.get_dummies(sep=", ").sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
skill_counts.plot(kind="bar", color="skyblue", alpha=0.8)
plt.title("Skill/Industry Analysis")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Job Type Analysis
job_type_counts = df["Job Type"].value_counts()

plt.figure(figsize=(6, 4))
sns.barplot(x=job_type_counts.index, y=job_type_counts.values, palette="viridis")
plt.title("Job Type Distribution")
plt.ylabel("Number of Jobs")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
