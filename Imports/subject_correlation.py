import random
import pandas as pd
import matplotlib.pyplot as plt

# Generate marks for 20 students
data = []

for _ in range(20):

    math = random.randint(40, 100)

    # Physics depends on Math
    physics = min(100, max(0, math + random.randint(-10, 10)))

    biology = random.randint(40, 100)

    # Chemistry depends on Biology
    chemistry = min(100, max(0, biology + random.randint(-10, 10)))

    # English is mostly independent
    english = random.randint(40, 100)

    data.append([
        math,
        physics,
        chemistry,
        biology,
        english
    ])

# Create DataFrame
df = pd.DataFrame(
    data,
    columns=["Math", "Physics", "Chemistry", "Biology", "English"]
)

# Correlation matrix
corr = df.corr()

# Plot
plt.figure(figsize=(7, 6))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

plt.xticks(range(len(corr.columns)), corr.columns)
plt.yticks(range(len(corr.columns)), corr.columns)

# Add correlation values
for i in range(len(corr)):
    for j in range(len(corr)):
        plt.text(
            j,
            i,
            f"{corr.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.colorbar(label="Correlation")
plt.title("Subject Correlation Matrix")
plt.tight_layout()
plt.show()