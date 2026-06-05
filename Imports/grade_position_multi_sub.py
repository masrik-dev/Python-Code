import random

# Number of students
num_students = 100

# Subjects
subjects = ["Math", "Physics", "Chemistry", "English", "Biology"]

# Store student data
students = []

# Generate random marks
for i in range(1, num_students + 1):
    student = {
        "name": f"Student_{i}"
    }

    total = 0

    for subject in subjects:
        mark = random.randint(40, 100)
        student[subject] = mark
        total += mark

    student["total"] = total
    student["average"] = round(total / len(subjects), 2)

    students.append(student)

# Sort students by total marks (highest first)
students.sort(key=lambda x: x["total"], reverse=True)

# Assign positions
for position, student in enumerate(students, start=1):
    student["position"] = position

# Print Top 10 Students
print("\n===== TOP 10 STUDENTS =====\n")

for student in students[:10]:
    print(
        f"Position: {student['position']:2d} | "
        f"Name: {student['name']:12s} | "
        f"Total: {student['total']:3d} | "
        f"Average: {student['average']:.2f}"
    )

# Highest scorer
topper = students[0]

# Lowest scorer
last_student = students[-1]

print("\n===== EXAM SUMMARY =====\n")
print(f"Topper: {topper['name']}")
print(f"Total Marks: {topper['total']}")
print(f"Average: {topper['average']}")

print()

print(f"Last Position: {last_student['name']}")
print(f"Total Marks: {last_student['total']}")
print(f"Average: {last_student['average']}")

# Search for a student
student_name = input("\nEnter student name (e.g., Student_25): ")

found = False

for student in students:
    if student["name"].lower() == student_name.lower():
        print("\n===== STUDENT RESULT =====")
        print(f"Position : {student['position']}")
        print(f"Name     : {student['name']}")

        for subject in subjects:
            print(f"{subject:10s}: {student[subject]}")

        print(f"Total    : {student['total']}")
        print(f"Average  : {student['average']}")
        found = True
        break

if not found:
    print("Student not found.")