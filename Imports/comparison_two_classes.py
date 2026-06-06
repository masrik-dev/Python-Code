import random

# Generate marks for Class A
class_a = {}
for i in range(1, 21):
    class_a[f"Student_A{i}"] = random.randint(40, 100)

# Generate marks for Class B
class_b = {}
for i in range(1, 21):
    class_b[f"Student_B{i}"] = random.randint(40, 100)

# Calculate averages
avg_a = sum(class_a.values()) / len(class_a)
avg_b = sum(class_b.values()) / len(class_b)

# Highest and lowest marks
highest_a = max(class_a.values())
lowest_a = min(class_a.values())

highest_b = max(class_b.values())
lowest_b = min(class_b.values())

# Top students
top_student_a = max(class_a, key=class_a.get)
top_student_b = max(class_b, key=class_b.get)

# Display results
print("===== CLASS A =====")
print(f"Average Mark : {avg_a:.2f}")
print(f"Highest Mark : {highest_a} ({top_student_a})")
print(f"Lowest Mark  : {lowest_a}")

print("\n===== CLASS B =====")
print(f"Average Mark : {avg_b:.2f}")
print(f"Highest Mark : {highest_b} ({top_student_b})")
print(f"Lowest Mark  : {lowest_b}")

# Compare classes
print("\n===== COMPARISON =====")

if avg_a > avg_b:
    print(f"Class A performed better.")
    print(f"Average Difference = {avg_a - avg_b:.2f}")
elif avg_b > avg_a:
    print(f"Class B performed better.")
    print(f"Average Difference = {avg_b - avg_a:.2f}")
else:
    print("Both classes performed equally.")

# Pass rate comparison
pass_a = sum(1 for mark in class_a.values() if mark >= 40)
pass_b = sum(1 for mark in class_b.values() if mark >= 40)

print(f"\nClass A Pass Rate: {pass_a}/20 ({pass_a/20*100:.1f}%)")
print(f"Class B Pass Rate: {pass_b}/20 ({pass_b/20*100:.1f}%)")