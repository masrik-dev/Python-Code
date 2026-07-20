# Restaurant meal combinations
soups = ["Tomato Soup", "Chicken Soup", "Vegetable Soup"]
main_dishes = [
    "Grilled Chicken",
    "Beef Steak",
    "Fish Fillet",
    "Pasta",
    "Vegetable Curry"
]
desserts = [
    "Ice Cream",
    "Cake",
    "Fruit Salad",
    "Pudding",
    "Chocolate Brownie",
    "Cheesecake",
    "Mango Tart"
]

combinations = []
for soup in soups:
    for main in main_dishes:
        for dessert in desserts:
            combinations.append((soup, main, dessert))

print("Total combinations:", len(combinations))
print("\nAll possible meal combinations:")
for combo in combinations:
    soup, main, dessert = combo
    print(f"{soup} + {main} + {dessert}")
