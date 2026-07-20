import random

# Restaurant meal combinations with weighted random selection
soups = ["Tomato Soup", "Chicken Soup", "Vegetable Soup"]
soup_weights = [0.45, 0.35, 0.20]

main_dishes = [
    "Grilled Chicken",
    "Beef Steak",
    "Fish Fillet",
    "Pasta",
    "Vegetable Curry"
]
main_weights = [0.30, 0.25, 0.15, 0.20, 0.10]

desserts = [
    "Ice Cream",
    "Cake",
    "Fruit Salad",
    "Pudding",
    "Chocolate Brownie",
    "Cheesecake",
    "Mango Tart"
]
dessert_weights = [0.25, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10]


def weighted_choice(options, weights):
    chosen = random.choices(options, weights=weights, k=1)[0]
    print(f"Selected from {options}: {chosen}")
    return chosen


print("Weighted meal selection")
print("======================")
print("The program will now randomly choose one soup, one main dish, and one dessert.")

for i in range(3):
    print(f"\nMeal {i + 1}")
    print("---------")
    soup = weighted_choice(soups, soup_weights)
    main = weighted_choice(main_dishes, main_weights)
    dessert = weighted_choice(desserts, dessert_weights)
    print(f"Final meal choice: {soup} + {main} + {dessert}")
