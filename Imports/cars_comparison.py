class Car:
    def __init__(self, make: str, model: str, year: int, price: float, mpg: float, hp: int):
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.mpg = mpg  # Miles per gallon
        self.hp = hp    # Horsepower

    @property
    def full_name(self) -> str:
        return f"{self.year} {self.make} {self.model}"


def compare_cars(car1: Car, car2: Car):
    print(f"=== COMPARING: {car1.full_name} VS {car2.full_name} ===\n")
    
    # Compare Price (Lower is better)
    if car1.price == car2.price:
        print(f"• Price: Tie (${car1.price:,})")
    else:
        cheaper_car = car1 if car1.price < car2.price else car2
        print(f"• Price: {cheaper_car.full_name} is cheaper (${min(car1.price, car2.price):,} vs ${max(car1.price, car2.price):,})")
    
    # Compare Fuel Economy (Higher is better)
    if car1.mpg == car2.mpg:
        print(f"• Fuel Economy: Tie ({car1.mpg} MPG)")
    else:
        efficient_car = car1 if car1.mpg > car2.mpg else car2
        print(f"• Fuel Economy: {efficient_car.full_name} is better ({max(car1.mpg, car2.mpg)} MPG vs {min(car1.mpg, car2.mpg)} MPG)")
        
    # Compare Horsepower (Higher is better)
    if car1.hp == car2.hp:
        print(f"• Performance: Tie ({car1.hp} HP)")
    else:
        powerful_car = car1 if car1.hp > car2.hp else car2
        print(f"• Performance: {powerful_car.full_name} has more power ({max(car1.hp, car2.hp)} HP vs {min(car1.hp, car2.hp)} HP)")


# Example Usage:
if __name__ == "__main__":
    # Create two car instances
    sedan_a = Car(make="Toyota", model="Camry", year=2024, price=26420, mpg=32, hp=203)
    sedan_b = Car(make="Honda", model="Accord", year=2024, price=27895, mpg=29, hp=192)
    
    # Run comparison
    compare_cars(sedan_a, sedan_b)
