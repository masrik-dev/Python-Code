"""
cars_condition_bef_aft_race.py
Realistic race simulation: generates random car conditions before/after race.

Simulates actual race events: fuel consumption, tire degradation, engine stress,
collision damage, and pit stops to produce authentic tactical reports.
"""

from dataclasses import dataclass
from typing import List, Dict
import random
import json


@dataclass
class CarStatus:
	id: str
	driver: str
	fuel_before_l: float
	fuel_after_l: float
	tire_condition_before: str
	tire_condition_after: str
	engine_ok_before: bool
	engine_ok_after: bool
	damage_notes: str = ""
	laps_completed: int = 0
	pit_stops: int = 0
	tire_degradation_pct: float = 0.0
	engine_temp_before_c: float = 0.0
	engine_temp_after_c: float = 0.0


def evaluate_change(before: float, after: float) -> float:
	return before - after


def simulate_race(num_laps: int = 50, num_cars: int = 3) -> List[CarStatus]:
	"""Simulate a realistic race with fuel, tire, engine, and collision events."""
	results = []
	
	for car_num in range(1, num_cars + 1):
		car_id = f"{car_num:02d}"
		driver_names = ["Alice", "Bob", "Charlie", "Diana", "Eva", "Frank"]
		driver = random.choice(driver_names)
		
		# Starting conditions (realistic)
		fuel_start = random.uniform(70.0, 85.0)  # liters
		engine_temp_start = random.uniform(78.0, 88.0)  # Celsius
		
		# Fuel consumption: ~2.1-2.6 L/lap base, increased with aggression
		aggression = random.uniform(0.7, 1.3)  # 0.7=conservative, 1.3=aggressive
		fuel_per_lap = random.uniform(2.1, 2.6) * aggression
		
		# Pit stop logic: typically 1-2 stops in a 50-lap race
		pit_stops = 1 if random.random() < 0.6 else 2
		laps_per_stint = num_laps // (pit_stops + 1)
		
		# Calculate fuel after race (accounting for pit refueling)
		# Assume each pit refuels ~50L
		fuel_consumed = num_laps * fuel_per_lap
		fuel_end = max(5.0, fuel_start - fuel_consumed + (pit_stops * 50.0))
		if fuel_end > 100:  # Can't overfill
			fuel_end = random.uniform(15.0, 30.0)
		
		# Tire degradation: 0-100% where 0=fresh, 100=slicks
		tire_deg_per_lap = random.uniform(1.2, 2.0) * aggression
		tire_degradation = min(100.0, num_laps * tire_deg_per_lap)
		
		# Tire condition mapping
		def tire_condition(deg: float) -> str:
			if deg < 20: return "Fresh"
			elif deg < 40: return "Good"
			elif deg < 60: return "Worn"
			elif deg < 80: return "Very Worn"
			else: return "Critical"
		
		tire_before = "Fresh"
		tire_after = tire_condition(tire_degradation)
		
		# Engine temperature: rises with laps and aggression
		engine_temp_per_lap = random.uniform(0.8, 1.5) * aggression
		engine_temp_end = engine_temp_start + (num_laps * engine_temp_per_lap)
		engine_temp_end = min(135.0, engine_temp_end)  # Cap at critical
		
		engine_ok_before = True
		engine_ok_after = engine_temp_end < 120.0  # OK if below 120°C
		
		# Collision/damage events: small random chance per lap
		damage_events = []
		for lap in range(num_laps):
			if random.random() < 0.005 * aggression:  # ~0.5% per lap when aggressive
				damage_events.append(f"Contact lap {lap+1}")
		
		damage_notes = "; ".join(damage_events) if damage_events else "No incidents"
		
		status = CarStatus(
			id=car_id,
			driver=driver,
			fuel_before_l=round(fuel_start, 2),
			fuel_after_l=round(max(0.0, fuel_end), 2),
			tire_condition_before=tire_before,
			tire_condition_after=tire_after,
			engine_ok_before=engine_ok_before,
			engine_ok_after=engine_ok_after,
			damage_notes=damage_notes,
			laps_completed=num_laps,
			pit_stops=pit_stops,
			tire_degradation_pct=round(tire_degradation, 1),
			engine_temp_before_c=round(engine_temp_start, 1),
			engine_temp_after_c=round(engine_temp_end, 1),
		)
		results.append(status)
	
	return results


def summarize_car(status: CarStatus) -> Dict:
	fuel_used = evaluate_change(status.fuel_before_l, status.fuel_after_l)
	fuel_pct_used = None
	if status.fuel_before_l > 0:
		fuel_pct_used = round((fuel_used / status.fuel_before_l) * 100, 1)

	return {
		"id": status.id,
		"driver": status.driver,
		"laps": status.laps_completed,
		"pit_stops": status.pit_stops,
		"fuel_used_l": round(fuel_used, 2),
		"fuel_used_pct": fuel_pct_used,
		"fuel_before": status.fuel_before_l,
		"fuel_after": status.fuel_after_l,
		"tires": f"{status.tire_condition_before} -> {status.tire_condition_after} ({status.tire_degradation_pct}%)",
		"engine_temp": f"{status.engine_temp_before_c}°C -> {status.engine_temp_after_c}°C",
		"engine_before_ok": status.engine_ok_before,
		"engine_after_ok": status.engine_ok_after,
		"damage_notes": status.damage_notes,
	}


def generate_report(statuses: List[CarStatus]) -> Dict:
	report = {
		"race_stats": {
			"total_cars": len(statuses),
			"laps": statuses[0].laps_completed if statuses else 0,
		},
		"cars": [summarize_car(s) for s in statuses],
	}
	return report


def print_report(report: Dict) -> None:
	print(f"\n{'='*60}")
	print(f"RACE REPORT — {report['race_stats']['total_cars']} cars, {report['race_stats']['laps']} laps")
	print(f"{'='*60}\n")
	for c in report.get("cars", []):
		print(f"Car #{c['id']} — Driver: {c['driver']}")
		print(f"  Laps completed: {c['laps']} | Pit stops: {c['pit_stops']}")
		print(f"  Fuel: {c['fuel_before']}L -> {c['fuel_after']}L (used {c['fuel_used_l']}L / {c['fuel_used_pct']}%)")
		print(f"  Tires: {c['tires']}")
		print(f"  Engine: {c['engine_temp']} | Status: {'OK' if c['engine_after_ok'] else '[!] PROBLEM'}")
		print(f"  Incidents: {c['damage_notes']}")
		print(f"{'-'*60}\n")


if __name__ == "__main__":
	# Simulate a 50-lap race with 4 random cars
	statuses = simulate_race(num_laps=50, num_cars=4)
	rpt = generate_report(statuses)
	print_report(rpt)

