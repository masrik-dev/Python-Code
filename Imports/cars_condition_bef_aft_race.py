"""
cars_condition_bef_aft_race.py
Simple tactical report generator for car conditions before and after a race.

Usage: run the script; it prints a sample report. Import functions for programmatic use.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict
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


def evaluate_change(before: float, after: float) -> float:
	return before - after


def summarize_car(status: CarStatus) -> Dict:
	fuel_used = evaluate_change(status.fuel_before_l, status.fuel_after_l)
	fuel_pct_used = None
	if status.fuel_before_l > 0:
		fuel_pct_used = round((fuel_used / status.fuel_before_l) * 100, 1)

	return {
		"id": status.id,
		"driver": status.driver,
		"fuel_used_l": round(fuel_used, 2),
		"fuel_used_pct": fuel_pct_used,
		"tire_before": status.tire_condition_before,
		"tire_after": status.tire_condition_after,
		"engine_before_ok": status.engine_ok_before,
		"engine_after_ok": status.engine_ok_after,
		"damage_notes": status.damage_notes,
	}


def generate_report(statuses: List[CarStatus]) -> Dict:
	report = {
		"total_cars": len(statuses),
		"cars": [summarize_car(s) for s in statuses],
	}
	return report


def print_report(report: Dict) -> None:
	print(json.dumps(report, indent=2))


if __name__ == "__main__":
	sample = [
		CarStatus(
			id="01",
			driver="Alice",
			fuel_before_l=60.0,
			fuel_after_l=22.5,
			tire_condition_before="New",
			tire_condition_after="Worn",
			engine_ok_before=True,
			engine_ok_after=True,
			damage_notes="Front wing scuffed",
		),
		CarStatus(
			id="02",
			driver="Bob",
			fuel_before_l=60.0,
			fuel_after_l=15.0,
			tire_condition_before="Used",
			tire_condition_after="Flat",
			engine_ok_before=True,
			engine_ok_after=False,
			damage_notes="Engine misfire after lap 34",
		),
	]

	rpt = generate_report(sample)
	print_report(rpt)

