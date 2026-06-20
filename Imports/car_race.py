import random
from dataclasses import dataclass, field
from typing import List


@dataclass
class Car:
    driver: str
    model: str
    team: str
    lap_times: List[float] = field(default_factory=list)

    def add_lap_time(self, time: float) -> None:
        self.lap_times.append(time)

    @property
    def total_time(self) -> float:
        return sum(self.lap_times)

    @property
    def average_time(self) -> float:
        return self.total_time / len(self.lap_times) if self.lap_times else 0.0

    @property
    def best_lap(self) -> float:
        return min(self.lap_times) if self.lap_times else 0.0


@dataclass
class RaceResult:
    race_number: int
    cars: List[Car]

    def sorted_cars(self) -> List[Car]:
        return sorted(self.cars, key=lambda car: car.total_time)

    def display(self) -> None:
        print(f"Race {self.race_number} Results")
        print("=" * 40)
        print(f"{'Pos':<4}{'Driver':<15}{'Team':<15}{'Model':<12}{'Total':<8}{'AvgLap':<8}{'Best':<8}")
        for position, car in enumerate(self.sorted_cars(), start=1):
            print(
                f"{position:<4}"
                f"{car.driver:<15}"
                f"{car.team:<15}"
                f"{car.model:<12}"
                f"{car.total_time:<8.3f}"
                f"{car.average_time:<8.3f}"
                f"{car.best_lap:<8.3f}"
            )
        print()
        print("Lap details per car:")
        for car in self.sorted_cars():
            lap_list = ', '.join(f"{lap:.3f}s" for lap in car.lap_times)
            print(f"- {car.driver} ({car.team} {car.model}): {lap_list}")
        print("\n" + "#" * 40 + "\n")


def generate_cars() -> List[Car]:
    drivers = [
        ("Ava", "Falcon GT", "Red Arrow"),
        ("Leo", "Stealth R", "Blue Horizon"),
        ("Mia", "Vortex X", "Silver Pulse"),
        ("Noah", "Cyclone Z", "Green Thunder"),
        ("Zoe", "Comet S", "Black Stallion"),
    ]
    return [Car(driver=name, model=model, team=team) for name, model, team in drivers]


def simulate_race(race_number: int, base_lap: float = 70.0, lap_count: int = 6) -> RaceResult:
    cars = generate_cars()
    for car in cars:
        car.lap_times.clear()
        for lap_index in range(1, lap_count + 1):
            # Each car has slightly different pace and variability
            time_variation = random.uniform(-2.2, 2.2)
            driver_adjustment = random.uniform(-1.0, 1.0)
            lap_time = base_lap + time_variation + driver_adjustment
            lap_time = max(lap_time, 62.0)
            car.add_lap_time(round(lap_time, 3))
    return RaceResult(race_number=race_number, cars=cars)


def simulate_race_series(count: int = 5) -> List[RaceResult]:
    random.seed(42)
    results = []
    for race_number in range(1, count + 1):
        results.append(simulate_race(race_number=race_number, base_lap=70.0 + race_number * 0.5))
    return results


def display_series(results: List[RaceResult]) -> None:
    print("Generating 5 car race results with full race information...\n")
    for result in results:
        result.display()


if __name__ == "__main__":
    race_series = simulate_race_series(count=5)
    display_series(race_series)
