import random

# Subjects
subjects = ["Math", "Physics", "Chemistry", "English", "Biology"]

# Generate random scores for 5 students
students = {}

for i in range(1, 6):
    students[f"Student_{i}"] = {
        subject: random.randint(40, 100) for subject in subjects
    }

# Analyze each student
for student, scores in students.items():
    print(f"\n{'=' * 50}")
    print(f"Student: {student}")

    # Display scores
    print("\nSubject Scores:")
    for subject, score in scores.items():
        print(f"{subject:<10}: {score}")

    # Calculate average
    average = sum(scores.values()) / len(scores)

    # Find strongest and weakest subjects
    strongest_subject = max(scores, key=scores.get)
    weakest_subject = min(scores, key=scores.get)

    print(f"\nAverage Score      : {average:.2f}")
    print(f"Strongest Subject  : {strongest_subject} ({scores[strongest_subject]})")
    print(f"Weakest Subject    : {weakest_subject} ({scores[weakest_subject]})")

    # Overall Evaluation
    if average >= 80:
        performance = "Excellent"
    elif average >= 70:
        performance = "Good"
    elif average >= 60:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    print(f"Overall Performance: {performance}")

    # Subjects needing improvement
    focus_subjects = [
        subject for subject, score in scores.items()
        if score < 70
    ]

    if focus_subjects:
        print("\nSubjects Needing More Focus:")
        for subject in focus_subjects:
            print(f"- {subject} ({scores[subject]})")
    else:
        print("\nAll subjects are performing well.")

    print(f"\nPriority Subject to Improve: {weakest_subject}")