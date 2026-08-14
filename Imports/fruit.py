from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Fruit:
	name: str
	price_per_unit: float
	quantity: int = 0
	category: Optional[str] = None

	def value(self) -> float:
		return self.price_per_unit * self.quantity


class FruitList:
	def __init__(self, fruits: Optional[List[Fruit]] = None):
		self.fruits: List[Fruit] = fruits or []

	def add_fruit(self, fruit: Fruit) -> None:
		existing = self.find_fruit(fruit.name)
		if existing:
			existing.quantity += fruit.quantity
			existing.price_per_unit = fruit.price_per_unit
		else:
			self.fruits.append(fruit)

	def remove_fruit(self, name: str) -> bool:
		f = self.find_fruit(name)
		if f:
			self.fruits.remove(f)
			return True
		return False

	def find_fruit(self, name: str) -> Optional[Fruit]:
		name = name.strip().lower()
		for f in self.fruits:
			if f.name.strip().lower() == name:
				return f
		return None

	def list_fruits(self) -> List[dict]:
		return [asdict(f) for f in self.fruits]

	def sort_by_name(self, reverse: bool = False) -> None:
		self.fruits.sort(key=lambda f: f.name.lower(), reverse=reverse)

	def sort_by_price(self, reverse: bool = False) -> None:
		self.fruits.sort(key=lambda f: f.price_per_unit, reverse=reverse)

	def total_inventory_value(self) -> float:
		return sum(f.value() for f in self.fruits)


def sample_fruits() -> FruitList:
	fruits = FruitList([
		Fruit("Apple", 0.80, 120, "Pome"),
		Fruit("Banana", 0.30, 200, "Tropical"),
		Fruit("Orange", 0.60, 150, "Citrus"),
		Fruit("Strawberry", 2.50, 50, "Berry"),
		Fruit("Grapes", 1.80, 80, "Vine"),
	])
	return fruits


def demo():
	fl = sample_fruits()

	print("Initial fruits:")
	for item in fl.list_fruits():
		print(f" - {item['name']}: ${item['price_per_unit']:.2f} x {item['quantity']}")

	print(f"\nTotal inventory value: ${fl.total_inventory_value():,.2f}\n")

	print("Adding 30 Apples at $0.85:")
	fl.add_fruit(Fruit("Apple", 0.85, 30))
	print("Removing Grapes")
	fl.remove_fruit("Grapes")

	print("\nAfter updates:")
	fl.sort_by_name()
	for item in fl.list_fruits():
		print(f" - {item['name']}: ${item['price_per_unit']:.2f} x {item['quantity']}")

	print(f"\nTotal inventory value: ${fl.total_inventory_value():,.2f}")


if __name__ == "__main__":
	demo()

