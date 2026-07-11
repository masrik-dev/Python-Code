import random


def generate_students(total=100):
    relationship_types = ["No relationship", "Close / living together", "Long distance"]
    weights = [0.40, 0.35, 0.25]
    students = []

    for student_id in range(1, total + 1):
        relation = random.choices(relationship_types, weights=weights, k=1)[0]

        if relation == "No relationship":
            cheating = "N/A"
        elif relation == "Close / living together":
            cheating = random.choices(["Yes", "No"], weights=[0.15, 0.85], k=1)[0]
        else:
            cheating = random.choices(["Yes", "No"], weights=[0.20, 0.80], k=1)[0]

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
        "Close / living together": {"Yes": 0, "No": 0},
        "Long distance": {"Yes": 0, "No": 0},
    }

    for student in students:
        relation = student["relationship"]
        relation_counts[relation] = relation_counts.get(relation, 0) + 1

        if relation in cheating_by_relation and student["cheating"] in ("Yes", "No"):
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
        total_relation = yes + no
        print(f"- {relation}: Yes {yes} ({yes / total_relation * 100:.1f}%), No {no} ({no / total_relation * 100:.1f}%)")

    partnered = relation_counts.get("Close / living together", 0) + relation_counts.get("Long distance", 0)
    cheating_yes = cheating_by_relation["Close / living together"]["Yes"] + cheating_by_relation["Long distance"]["Yes"]
    print(f"Partnered students: {partnered} ({partnered / total * 100:.1f}%)")
    print(f"Students reporting cheating: {cheating_yes} ({cheating_yes / partnered * 100:.1f}% of partnered students)")


def main():
    students = generate_students()
    summarize_students(students)


if __name__ == "__main__":
    main()
