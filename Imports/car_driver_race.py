import random
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Driver:
    name: str
    skill: float  # 0.0 to 1.0, higher means better performance
    consistency: float  # 0.0 to 1.0, lower means more stable lap-to-lap
    aggression: float  # 0.0 to 1.0, higher means riskier faster laps

    def performance_modifier(self) -> float:
        """Return a base modifier used to influence lap times."""
        return 1.0 - 0.15 * self.skill + 0.05 * (1.0 - self.consistency)


@dataclass
class Car:
    model: str
    team: str
    driver: Driver
    lap_times: List[float] = field(default_factory=list)

    def add_lap_time(self, lap_time: float) -> None:
        self.lap_times.append(lap_time)

    @property
    def total_time(self) -> float:
        return sum(self.lap_times)

    @property
    def average_lap(self) -> float:
        return self.total_time / len(self.lap_times) if self.lap_times else 0.0

    @property
    def best_lap(self) -> float:
        return min(self.lap_times) if self.lap_times else float("inf")

    @property
    def consistency_score(self) -> float:
        if not self.lap_times:
            return 0.0
        mean = self.average_lap
        variance = sum((lap - mean) ** 2 for lap in self.lap_times) / len(self.lap_times)
        return 1.0 / (1.0 + variance)


@dataclass
class RaceResult:
    race_number: int
    cars: List[Car]

    def sorted_by_total(self) -> List[Car]:
        return sorted(self.cars, key=lambda car: car.total_time)

    def display(self) -> None:
        print(f"Race {self.race_number} Results")
        print("=" * 58)
        print(
            f"{'Pos':<4}{'Driver':<15}{'Team':<12}{'Model':<12}{'Total(s)':<10}{'Avg(s)':<10}{'Best(s)':<10}{'Cons':<6}"
        )
        for position, car in enumerate(self.sorted_by_total(), start=1):
            print(
                f"{position:<4}"
                f"{car.driver.name:<15}"
                f"{car.team:<12}"
                f"{car.model:<12}"
                f"{car.total_time:<10.3f}"
                f"{car.average_lap:<10.3f}"
                f"{car.best_lap:<10.3f}"
                f"{car.consistency_score:<6.3f}"
            )
        print("\nDriver performance details:")
        for car in self.sorted_by_total():
            print(
                f"- {car.driver.name} ({car.team} {car.model}): skill={car.driver.skill:.2f}, "
                f"consistency={car.driver.consistency:.2f}, aggression={car.driver.aggression:.2f}",
            )
        print("\n" + "#" * 58 + "\n")


class RaceSimulator:
    def __init__(self, seed: Optional[int] = 0):
        self.random = random.Random(seed)

    def generate_grid(self) -> List[Car]:
        driver_profiles = [
            Driver(name="Ava", skill=0.92, consistency=0.88, aggression=0.65),
            Driver(name="Leo", skill=0.84, consistency=0.93, aggression=0.55),
            Driver(name="Mia", skill=0.78, consistency=0.80, aggression=0.75),
            Driver(name="Noah", skill=0.88, consistency=0.82, aggression=0.70),
            Driver(name="Zoe", skill=0.81, consistency=0.90, aggression=0.60),
        ]

        car_specs = [
            ("Falcon GT", "Red Arrow"),
            ("Stealth R", "Blue Horizon"),
            ("Vortex X", "Silver Pulse"),
            ("Cyclone Z", "Green Thunder"),
            ("Comet S", "Black Stallion"),
        ]

        return [Car(model=model, team=team, driver=driver) for driver, (model, team) in zip(driver_profiles, car_specs)]

    def simulate_race(self, race_number: int, laps: int = 8, base_lap: float = 75.0) -> RaceResult:
        cars = self.generate_grid()
        for car in cars:
            car.lap_times.clear()
            for lap in range(1, laps + 1):
                lap_time = self.simulate_lap(car, base_lap, lap)
                car.add_lap_time(round(lap_time, 3))
        return RaceResult(race_number=race_number, cars=cars)

    def simulate_lap(self, car: Car, base_lap: float, lap_index: int) -> float:
        driver = car.driver
        target = base_lap * driver.performance_modifier()

        drift = self.random.gauss(0.0, 0.8 * (1.0 - driver.consistency))
        aggression_adjust = (driver.aggression - 0.5) * self.random.uniform(-1.2, 1.2)
        fatigue_penalty = 0.15 * max(0, lap_index - 4)

        lap_time = target + drift - aggression_adjust + fatigue_penalty
        lap_time = max(lap_time, 60.0)
        return lap_time


class RaceAnalyzer:
    @staticmethod
    def analyze_driver_influence(result: RaceResult) -> None:
        print("Driver influence analysis")
        print("-" * 40)

        sorted_cars = result.sorted_by_total()
        winner = sorted_cars[0]
        best_skill = max(result.cars, key=lambda c: c.driver.skill)
        best_consistency = max(result.cars, key=lambda c: c.driver.consistency)
        best_aggression = max(result.cars, key=lambda c: c.driver.aggression)

        print(f"Race winner: {winner.driver.name} with total time {winner.total_time:.3f}s")
        print(f"Highest skill driver: {best_skill.driver.name} (skill={best_skill.driver.skill:.2f})")
        print(f"Most consistent driver: {best_consistency.driver.name} (consistency={best_consistency.driver.consistency:.2f})")
        print(f"Most aggressive driver: {best_aggression.driver.name} (aggression={best_aggression.driver.aggression:.2f})")

        for car in result.cars:
            driver = car.driver
            print(
                f"{driver.name}: total={car.total_time:.3f}s, best={car.best_lap:.3f}s, "
                f"skill={driver.skill:.2f}, consistency={driver.consistency:.2f}, aggression={driver.aggression:.2f}"
            )
        print("\n")

    @staticmethod
    def summary(results: List[RaceResult]) -> None:
        print("Race series summary")
        print("=" * 40)
        overall_stats = {}

        for result in results:
            for position, car in enumerate(result.sorted_by_total(), start=1):
                overall = overall_stats.setdefault(car.driver.name, {"points": 0, "wins": 0, "total_time": 0.0})
                points = max(0, 11 - position)
                overall["points"] += points
                overall["wins"] += 1 if position == 1 else 0
                overall["total_time"] += car.total_time

        summary_list = [
            (driver, data["points"], data["wins"], data["total_time"])
            for driver, data in overall_stats.items()
        ]
        summary_list.sort(key=lambda item: (-item[1], item[3]))

        print(f"{'Driver':<12}{'Points':<8}{'Wins':<6}{'Total Time':<12}")
        for driver, points, wins, total_time in summary_list:
            print(f"{driver:<12}{points:<8}{wins:<6}{total_time:<12.3f}")
        print("\n")


if __name__ == "__main__":
    simulator = RaceSimulator(seed=42)
    series = [simulator.simulate_race(race_number=i, laps=8, base_lap=74.5 + i * 0.5) for i in range(1, 4)]

    for race_result in series:
        race_result.display()
        RaceAnalyzer.analyze_driver_influence(race_result)

    RaceAnalyzer.summary(series)
