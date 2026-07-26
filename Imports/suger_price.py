"""
Compare sugar prices by type, brand, and city.
Covers the top 10 cities in Europe (by population / economic hub size).
Prices are sample EUR / kg values for demonstration.
"""

from collections import defaultdict
from typing import Optional


TOP_10_CITIES = [
    "Istanbul",
    "Moscow",
    "London",
    "Saint Petersburg",
    "Berlin",
    "Madrid",
    "Kyiv",
    "Rome",
    "Paris",
    "Bucharest",
]

SUGAR_TYPES = [
    "White granulated",
    "Brown soft",
    "Caster",
    "Icing / powdered",
    "Raw cane",
]

BRANDS = [
    "Tate & Lyle",
    "Sidzucker",
    "Nordzucker",
    "Cristal Union",
    "Domino",
]


class SugarProduct:
    def __init__(
        self,
        sugar_type: str,
        brand: str,
        city: str,
        price_per_kg: float,
        currency: str = "EUR",
    ):
        self.sugar_type = sugar_type
        self.brand = brand
        self.city = city
        self.price_per_kg = price_per_kg
        self.currency = currency

    @property
    def label(self) -> str:
        return f"{self.brand} | {self.sugar_type} | {self.city}"

    def __repr__(self) -> str:
        return f"{self.label}: {self.price_per_kg:.2f} {self.currency}/kg"


def build_sample_catalog() -> list[SugarProduct]:
    """Realistic-ish demo prices that vary by city cost level and sugar type."""
    city_cost = {
        "Istanbul": 0.85,
        "Moscow": 0.90,
        "London": 1.35,
        "Saint Petersburg": 0.88,
        "Berlin": 1.10,
        "Madrid": 1.05,
        "Kyiv": 0.75,
        "Rome": 1.15,
        "Paris": 1.30,
        "Bucharest": 0.80,
    }
    type_base = {
        "White granulated": 1.10,
        "Brown soft": 1.45,
        "Caster": 1.35,
        "Icing / powdered": 1.60,
        "Raw cane": 1.55,
    }
    brand_premium = {
        "Tate & Lyle": 1.15,
        "Sidzucker": 1.00,
        "Nordzucker": 1.05,
        "Cristal Union": 0.98,
        "Domino": 1.12,
    }

    catalog = []
    for city in TOP_10_CITIES:
        for sugar_type in SUGAR_TYPES:
            for brand in BRANDS:
                price = (
                    type_base[sugar_type]
                    * city_cost[city]
                    * brand_premium[brand]
                )
                catalog.append(
                    SugarProduct(sugar_type, brand, city, round(price, 2))
                )
    return catalog


def filter_products(
    catalog: list[SugarProduct],
    sugar_type: Optional[str] = None,
    brand: Optional[str] = None,
    city: Optional[str] = None,
) -> list[SugarProduct]:
    results = catalog
    if sugar_type:
        results = [p for p in results if p.sugar_type == sugar_type]
    if brand:
        results = [p for p in results if p.brand == brand]
    if city:
        results = [p for p in results if p.city == city]
    return results


def compare_two(a: SugarProduct, b: SugarProduct) -> None:
    print(f"=== COMPARING ===")
    print(f"A: {a}")
    print(f"B: {b}\n")

    if a.price_per_kg == b.price_per_kg:
        print(f"• Price: Tie ({a.price_per_kg:.2f} EUR/kg)")
    else:
        cheaper = a if a.price_per_kg < b.price_per_kg else b
        dearer = b if cheaper is a else a
        diff = abs(a.price_per_kg - b.price_per_kg)
        print(
            f"• Cheaper: {cheaper.label} "
            f"({cheaper.price_per_kg:.2f} vs {dearer.price_per_kg:.2f} EUR/kg, "
            f"saves {diff:.2f} EUR/kg)"
        )


def cheapest_by_city(
    catalog: list[SugarProduct], sugar_type: str
) -> dict[str, SugarProduct]:
    """For one sugar type, find the cheapest brand in each city."""
    winners: dict[str, SugarProduct] = {}
    for city in TOP_10_CITIES:
        options = filter_products(catalog, sugar_type=sugar_type, city=city)
        if options:
            winners[city] = min(options, key=lambda p: p.price_per_kg)
    return winners


def brand_average_by_city(
    catalog: list[SugarProduct], brand: str
) -> dict[str, float]:
    """Average price of a brand across all sugar types, per city."""
    averages = {}
    for city in TOP_10_CITIES:
        items = filter_products(catalog, brand=brand, city=city)
        if items:
            averages[city] = sum(p.price_per_kg for p in items) / len(items)
    return averages


def type_price_matrix(catalog: list[SugarProduct]) -> None:
    """Print average price of each sugar type in each top city."""
    print("\n=== AVERAGE PRICE BY SUGAR TYPE x CITY (EUR/kg) ===\n")
    header = f"{'City':<18}" + "".join(f"{t[:12]:>13}" for t in SUGAR_TYPES)
    print(header)
    print("-" * len(header))

    for city in TOP_10_CITIES:
        row = f"{city:<18}"
        for sugar_type in SUGAR_TYPES:
            items = filter_products(catalog, sugar_type=sugar_type, city=city)
            avg = sum(p.price_per_kg for p in items) / len(items)
            row += f"{avg:>13.2f}"
        print(row)


def brand_ranking(catalog: list[SugarProduct], city: str) -> None:
    """Rank brands by average price in one city (cheapest first)."""
    print(f"\n=== BRAND RANKING IN {city.upper()} (avg EUR/kg) ===\n")
    averages = []
    for brand in BRANDS:
        items = filter_products(catalog, brand=brand, city=city)
        avg = sum(p.price_per_kg for p in items) / len(items)
        averages.append((brand, avg))

    averages.sort(key=lambda x: x[1])
    for rank, (brand, avg) in enumerate(averages, start=1):
        print(f"{rank}. {brand:<16} {avg:.2f} EUR/kg")


def cheapest_overall(catalog: list[SugarProduct], n: int = 10) -> None:
    print(f"\n=== TOP {n} CHEAPEST SUGAR OPTIONS (all cities) ===\n")
    ranked = sorted(catalog, key=lambda p: p.price_per_kg)[:n]
    for i, product in enumerate(ranked, start=1):
        print(f"{i:2}. {product}")


def most_expensive_overall(catalog: list[SugarProduct], n: int = 10) -> None:
    print(f"\n=== TOP {n} MOST EXPENSIVE SUGAR OPTIONS (all cities) ===\n")
    ranked = sorted(catalog, key=lambda p: p.price_per_kg, reverse=True)[:n]
    for i, product in enumerate(ranked, start=1):
        print(f"{i:2}. {product}")


def city_cost_summary(catalog: list[SugarProduct]) -> None:
    print("\n=== CITY COST INDEX (avg price across all types & brands) ===\n")
    city_avgs = []
    for city in TOP_10_CITIES:
        items = filter_products(catalog, city=city)
        avg = sum(p.price_per_kg for p in items) / len(items)
        city_avgs.append((city, avg))

    city_avgs.sort(key=lambda x: x[1])
    cheapest_avg = city_avgs[0][1]
    for city, avg in city_avgs:
        index = (avg / cheapest_avg) * 100
        print(f"{city:<18} {avg:.2f} EUR/kg  (index {index:.0f})")


if __name__ == "__main__":
    catalog = build_sample_catalog()

    print("Sugar price comparison — Top 10 European cities")
    print("=" * 52)
    print(f"Cities: {', '.join(TOP_10_CITIES)}")
    print(f"Types:  {', '.join(SUGAR_TYPES)}")
    print(f"Brands: {', '.join(BRANDS)}")
    print(f"Total products in catalog: {len(catalog)}")

    # Side-by-side product comparison
    product_a = filter_products(
        catalog,
        sugar_type="White granulated",
        brand="Sidzucker",
        city="Berlin",
    )[0]
    product_b = filter_products(
        catalog,
        sugar_type="White granulated",
        brand="Tate & Lyle",
        city="London",
    )[0]
    print()
    compare_two(product_a, product_b)

    # Cheapest white sugar brand per city
    print("\n=== CHEAPEST WHITE GRANULATED BRAND PER CITY ===\n")
    for city, winner in cheapest_by_city(catalog, "White granulated").items():
        print(f"{city:<18} → {winner.brand} @ {winner.price_per_kg:.2f} EUR/kg")

    type_price_matrix(catalog)
    brand_ranking(catalog, "Paris")
    city_cost_summary(catalog)
    cheapest_overall(catalog)
    most_expensive_overall(catalog)
