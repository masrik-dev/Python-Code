import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "Music"]

student_marks = np.random.randint(50, 101, size=6)

df = pd.DataFrame({
    "Subject": subjects,
    "Student marks": student_marks
})

print("Student's mark on different subject:\n")
print(df)

x = np.arange(len(subjects))
width = 0.35

plt.figure(figsize=(9, 5))
bars = plt.bar(x, student_marks, width, label="Students' Mark")

for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             str(int(bar.get_height())),
             ha='center')
    
plt.xlabel("Subjects")
plt.ylabel("Marks")
plt.title("Students' Mark Across Subjects")
plt.xticks(x, subjects)
plt.legend()
plt.tight_layout()
plt.show()