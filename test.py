"""
- Modules get used all the time throughout programming
- It helps with creating more files,
    with unique purposes, to help with
    clean maintainable code.
"""

homework_assignment_grades = {
    'homework_1': 85,
    'homework_2': 100,
    'homework_3': 81
}

def calculate_homework(homework_assignments_arg):
    sum_of_grades = 0
    for homework in homework_assignments_arg.values():
        sum_of_grades += homework
    final_grade = round(sum_of_grades / len(homework_assignments_arg), 2)
    print(final_grade)


calculate_homework(homework_assignment_grades)

# Find highest and lowest grades
def find_highest_lowest(homework_assignments_arg):
    highest_grade = max(homework_assignments_arg.values())
    lowest_grade = min(homework_assignments_arg.values())

    print(f"Highest Grade: {highest_grade}")
    print(f"Lowest Grade: {lowest_grade}")

find_highest_lowest(homework_assignment_grades)

print("__________ New test code for 20 student's grade __________")

import random
student_grades = {}

for student_num in range(1, 21):
    student_grades[f"student_{student_num}"] = random.randint(40, 100)

for student, grade in student_grades.items():
    print(f"{student}: {grade}")

sum_of_grades = sum(student_grades.values())
average_grade = round(sum_of_grades/len(student_grades), 2)

highest_grade = max(student_grades.values())
lowest_grade = min(student_grades.values())

highest_student = max(student_grades, key=student_grades.get)
lowest_student = min(student_grades, key=student_grades.get)

print(f"Summary:\nAverage Grade: {average_grade}\nHigest Grade: {highest_grade} ({highest_student})\nLowest Grade: {lowest_grade} ({lowest_student})")
