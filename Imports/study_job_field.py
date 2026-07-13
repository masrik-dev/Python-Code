import random


def generate_students(total=100):
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

    job_fields = [
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
        study_field = random.choice(study_fields)
        job_field = random.choice(job_fields)
        students.append({
            "id": student_id,
            "study_field": study_field,
            "job_field": job_field,
        })

    return students


def summarize_discrepancy(students):
    total = len(students)
    same_count = 0
    mismatch_count = 0

    study_counts = {}
    job_counts = {}
    mismatch_summary = {}

    for student in students:
        study = student["study_field"]
        job = student["job_field"]

        study_counts[study] = study_counts.get(study, 0) + 1
        job_counts[job] = job_counts.get(job, 0) + 1

        if study == job:
            same_count += 1
        else:
            mismatch_count += 1
            key = f"{study} -> {job}"
            mismatch_summary[key] = mismatch_summary.get(key, 0) + 1

    print("Survey Report: Study Field vs Potential Job Field")
    print("=" * 50)
    print(f"Total students surveyed: {total}")
    print(f"Students with matching study and job field: {same_count} ({same_count / total * 100:.1f}%)")
    print(f"Students with study-job discrepancy: {mismatch_count} ({mismatch_count / total * 100:.1f}%)")

    print("\nMost common study fields:")
    for field, count in sorted(study_counts.items(), key=lambda item: item[1], reverse=True)[:5]:
        print(f"- {field}: {count}")

    print("\nMost common potential job fields:")
    for field, count in sorted(job_counts.items(), key=lambda item: item[1], reverse=True)[:5]:
        print(f"- {field}: {count}")

    print("\nTop study-to-job mismatches:")
    for pair, count in sorted(mismatch_summary.items(), key=lambda item: item[1], reverse=True)[:10]:
        print(f"- {pair}: {count}")


def main():
    students = generate_students()
    summarize_discrepancy(students)


if __name__ == "__main__":
    main()
