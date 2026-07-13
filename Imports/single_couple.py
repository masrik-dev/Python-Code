import random


def generate_survey(total=100):
    study_fields = [
        "Computer Science",
        "Engineering",
        "Business",
        "Medicine",
        "Law",
        "Arts",
        "Education",
        "Social Science",
        "Agriculture",
        "Environmental Science",
    ]

    work_fields = [
        "Software Development",
        "Engineering",
        "Finance",
        "Healthcare",
        "Legal Services",
        "Design",
        "Teaching",
        "Research",
        "Agribusiness",
        "Environmental Services",
    ]

    students = []

    for student_id in range(1, total + 1):
        relationship = random.choice(["Single", "In a relationship", "Do not want to answer"])
        study_field = random.choice(study_fields)
        work_field = random.choice(work_fields)

        students.append({
            "id": student_id,
            "relationship": relationship,
            "study_field": study_field,
            "work_field": work_field,
        })

    return students


def summarize_survey(students):
    total = len(students)

    counts = {
        "Single": 0,
        "In a relationship": 0,
        "Do not want to answer": 0,
    }

    study_counts = {}
    work_counts = {}

    for student in students:
        counts[student["relationship"]] += 1
        study_counts[student["study_field"]] = study_counts.get(student["study_field"], 0) + 1
        work_counts[student["work_field"]] = work_counts.get(student["work_field"], 0) + 1

    print("Survey Summary")
    print("=" * 30)
    print(f"Total students surveyed: {total}")
    print("Relationship status:")
    for status in ["Single", "In a relationship", "Do not want to answer"]:
        count = counts[status]
        print(f"- {status}: {count} ({count / total * 100:.1f}%)")

    print("\nStudy field distribution:")
    for field, count in sorted(study_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"- {field}: {count} ({count / total * 100:.1f}%)")

    print("\nPotential work field distribution:")
    for field, count in sorted(work_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"- {field}: {count} ({count / total * 100:.1f}%)")


def main():
    students = generate_survey()
    summarize_survey(students)


if __name__ == "__main__":
    main()
