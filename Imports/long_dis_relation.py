import random


def generate_students(total=100):
    relationship_types = ["No relationship", "Close / living together", "Long distance"]
    students = []

    for student_id in range(1, total + 1):
        relation = random.choice(relationship_types)

        if relation == "No relationship":
            cheating = random.choice(["Yes", "No", "Do not want to answer"])
        elif relation == "Close / living together":
            cheating = random.choice(["Yes", "No", "Do not want to answer"])
        else:
            cheating = random.choice(["Yes", "No", "Do not want to answer"])

        students.append({
            "id": student_id,
            "relationship": relation,
            "cheating": cheating,
        })

    return students


def summarize_students(students):
    total = len(students)
    relation_counts = {}
    cheating_by_relation = {
        "Close / living together": {"Yes": 0, "No": 0, "Do not want to answer": 0},
        "Long distance": {"Yes": 0, "No": 0, "Do not want to answer": 0},
    }

    for student in students:
        relation = student["relationship"]
        relation_counts[relation] = relation_counts.get(relation, 0) + 1

        if relation in cheating_by_relation and student["cheating"] in ("Yes", "No", "Do not want to answer"):
            cheating_by_relation[relation][student["cheating"]] += 1

    print(f"Total students: {total}")
    print("Relationship distribution:")
    for relation in ["No relationship", "Close / living together", "Long distance"]:
        count = relation_counts.get(relation, 0)
        print(f"- {relation}: {count} ({count / total * 100:.1f}%)")

    print("Cheating status among partnered students:")
    for relation in ["Close / living together", "Long distance"]:
        yes = cheating_by_relation[relation]["Yes"]
        no = cheating_by_relation[relation]["No"]
        no_answer = cheating_by_relation[relation]["Do not want to answer"]
        total_relation = yes + no + no_answer
        print(f"- {relation}: Yes {yes} ({yes / total_relation * 100:.1f}%), No {no} ({no / total_relation * 100:.1f}%), No answer {no_answer} ({no_answer / total_relation * 100:.1f}%)")

    partnered = relation_counts.get("Close / living together", 0) + relation_counts.get("Long distance", 0)
    cheating_yes = cheating_by_relation["Close / living together"]["Yes"] + cheating_by_relation["Long distance"]["Yes"]
    no_answer_total = cheating_by_relation["Close / living together"]["Do not want to answer"] + cheating_by_relation["Long distance"]["Do not want to answer"]
    print(f"Partnered students: {partnered} ({partnered / total * 100:.1f}%)")
    print(f"Students reporting cheating: {cheating_yes} ({cheating_yes / partnered * 100:.1f}% of partnered students)")
    print(f"Students who did not answer: {no_answer_total} ({no_answer_total / partnered * 100:.1f}% of partnered students)")


def main():
    students = generate_students()
    summarize_students(students)


if __name__ == "__main__":
    main()
