import random

# Generate grades for 100 students
student_grades = {}

for student_num in range(1, 101):
    student_grades[f"student_{student_num}"] = random.randint(40, 100)

# Display all student grades
for student, grade in student_grades.items():
    print(f"{student}: {grade}")

# Calculate average grade
sum_of_grades = sum(student_grades.values())
average_grade = round(sum_of_grades / len(student_grades), 2)

# Find highest and lowest grades
highest_grade = max(student_grades.values())
lowest_grade = min(student_grades.values())

# Find the students with highest and lowest grades
highest_student = max(student_grades, key=student_grades.get)
lowest_student = min(student_grades, key=student_grades.get)

print("\n______ Summary ______")
print(f"Average Grade: {average_grade}")
print(f"Highest Grade: {highest_grade} ({highest_student})")
print(f"Lowest Grade: {lowest_grade} ({lowest_student})")