import random


def calculate_date_cost(relationship, city_type, date_style, restaurant_level, dinner_cost, drinks, activity_cost, transport_mode, distance_km, gift_cost, photos_cost, reservation_fee, parking_fee, tip_percent, service_tax_percent):
    meal_multiplier = {
        "small town": 0.9,
        "big city": 1.2,
    }[city_type]

    style_multiplier = {
        "casual": 1.0,
        "moderate": 1.3,
        "luxury": 1.8,
    }[date_style]

    restaurant_multiplier = {
        "cheap": 0.9,
        "mid": 1.2,
        "fine": 1.8,
    }[restaurant_level]

    transport_rate = {
        "walk": 0,
        "bus": 15,
        "train": 20,
        "taxi": 35,
        "ride_share": 45,
        "car": 25,
    }[transport_mode]

    dinner_total = dinner_cost * 2 * meal_multiplier * restaurant_multiplier * style_multiplier
    drinks_total = drinks * 80 * style_multiplier
    activity_total = activity_cost * 2 * style_multiplier
    transport_total = distance_km * transport_rate * 0.8
    extra_total = reservation_fee + parking_fee
    gift_total = gift_cost
    photo_total = photos_cost

    subtotal = dinner_total + drinks_total + activity_total + transport_total + extra_total + gift_total + photo_total

    tax = subtotal * (service_tax_percent / 100)
    tip = subtotal * (tip_percent / 100)

    if relationship == "married":
        relationship_adjustment = subtotal * 0.08
        relationship_label = "married couple"
    else:
        relationship_adjustment = subtotal * 0.12
        relationship_label = "unmarried couple"

    total = subtotal + tax + tip + relationship_adjustment
    return {
        "relationship_label": relationship_label,
        "subtotal": subtotal,
        "tax": tax,
        "tip": tip,
        "relationship_adjustment": relationship_adjustment,
        "total": total,
        "per_person": total / 2,
    }


def main():
    print("=== Couple Date Expense Survey ===")
    print("This survey compares costs for married and unmarried couples.\n")

    city_type = random.choice(["small town", "big city"])
    date_style = random.choice(["casual", "moderate", "luxury"])
    restaurant_level = random.choice(["cheap", "mid", "fine"])
    transport_mode = random.choice(["walk", "bus", "train", "taxi", "ride_share", "car"])

    dinner_cost = round(random.uniform(80, 180), 2)
    drinks = random.randint(1, 3)
    activity_cost = round(random.uniform(60, 150), 2)
    distance_km = random.randint(3, 15)
    gift_cost = round(random.uniform(0, 250), 2)
    photos_cost = round(random.uniform(0, 120), 2)
    reservation_fee = round(random.uniform(0, 80), 2)
    parking_fee = round(random.uniform(0, 50), 2)
    tip_percent = random.randint(10, 18)
    service_tax_percent = random.randint(7, 12)

    married_result = calculate_date_cost(
        relationship="married",
        city_type=city_type,
        date_style=date_style,
        restaurant_level=restaurant_level,
        dinner_cost=dinner_cost,
        drinks=drinks,
        activity_cost=activity_cost,
        transport_mode=transport_mode,
        distance_km=distance_km,
        gift_cost=gift_cost,
        photos_cost=photos_cost,
        reservation_fee=reservation_fee,
        parking_fee=parking_fee,
        tip_percent=tip_percent,
        service_tax_percent=service_tax_percent,
    )

    unmarried_result = calculate_date_cost(
        relationship="unmarried",
        city_type=city_type,
        date_style=date_style,
        restaurant_level=restaurant_level,
        dinner_cost=dinner_cost,
        drinks=drinks,
        activity_cost=activity_cost,
        transport_mode=transport_mode,
        distance_km=distance_km,
        gift_cost=gift_cost,
        photos_cost=photos_cost,
        reservation_fee=reservation_fee,
        parking_fee=parking_fee,
        tip_percent=tip_percent,
        service_tax_percent=service_tax_percent,
    )

    print("\n=== Estimated Expense Report ===")
    print(f"City type: {city_type}")
    print(f"Date style: {date_style}")
    print(f"Restaurant level: {restaurant_level}")
    print(f"Transport mode: {transport_mode}")
    print()
    print("Married couple:")
    print(f"  Subtotal: {married_result['subtotal']:.2f}")
    print(f"  Tax: {married_result['tax']:.2f}")
    print(f"  Tip: {married_result['tip']:.2f}")
    print(f"  Relationship adjustment: {married_result['relationship_adjustment']:.2f}")
    print(f"  Estimated total: {married_result['total']:.2f}")
    print(f"  Estimated per person: {married_result['per_person']:.2f}")
    print()
    print("Unmarried couple:")
    print(f"  Subtotal: {unmarried_result['subtotal']:.2f}")
    print(f"  Tax: {unmarried_result['tax']:.2f}")
    print(f"  Tip: {unmarried_result['tip']:.2f}")
    print(f"  Relationship adjustment: {unmarried_result['relationship_adjustment']:.2f}")
    print(f"  Estimated total: {unmarried_result['total']:.2f}")
    print(f"  Estimated per person: {unmarried_result['per_person']:.2f}")
    print()
    print("Difference:")
    print(f"  Unmarried - Married = {unmarried_result['total'] - married_result['total']:.2f}")


if __name__ == "__main__":
    main()
