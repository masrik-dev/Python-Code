import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Subjects
subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "ICT"]

# Generate random marks (50-100)
student1_marks = np.random.randint(50, 101, size=6)
student2_marks = np.random.randint(50, 101, size=6)

# Create DataFrame
df = pd.DataFrame({
    "Subject": subjects,
    "Student 1": student1_marks,
    "Student 2": student2_marks
})

print("Marks Comparison:\n")
print(df)

print("\nSubject-wise Comparison:")
for i in range(len(subjects)):
    if student1_marks[i] > student2_marks[i]:
        print(f"{subjects[i]}: Student 1 scored higher ({student1_marks[i]} > {student2_marks[i]})")
    elif student2_marks[i] > student1_marks[i]:
        print(f"{subjects[i]}: Student 2 scored higher ({student2_marks[i]} > {student1_marks[i]})")
    else:
        print(f"{subjects[i]}: Both students scored the same ({student1_marks[i]})")

# Display all subject marks separately
print("\nStudent 1 Marks:")
for subject, mark in zip(subjects, student1_marks):
    print(f"{subject}: {mark}")

print("\nStudent 2 Marks:")
for subject, mark in zip(subjects, student2_marks):
    print(f"{subject}: {mark}")

# Total marks and averages
total1 = np.sum(student1_marks)
total2 = np.sum(student2_marks)

avg1 = np.mean(student1_marks)
avg2 = np.mean(student2_marks)

print("\nSummary:")
print(f"Student 1 Total Marks: {total1}")
print(f"Student 1 Average Marks: {avg1:.2f}")

print(f"\nStudent 2 Total Marks: {total2}")
print(f"Student 2 Average Marks: {avg2:.2f}")

# Plot
x = np.arange(len(subjects))
width = 0.35

plt.figure(figsize=(9, 5))
bars1 = plt.bar(x - width/2, student1_marks, width, label="Student 1")
bars2 = plt.bar(x + width/2, student2_marks, width, label="Student 2")

# Add marks on top of bars
for bar in bars1:
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             str(int(bar.get_height())),
             ha='center')

for bar in bars2:
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             str(int(bar.get_height())),
             ha='center')

plt.xlabel("Subjects")
plt.ylabel("Marks")
plt.title("Comparison of Two Students Across Subjects")
plt.xticks(x, subjects)
plt.legend()
plt.tight_layout()
plt.show()