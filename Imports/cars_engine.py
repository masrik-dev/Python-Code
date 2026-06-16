import random


class CarEngine:

    def __init__(self, model_name):
        self.model_name = model_name
        # Simulate a live engine snapshot with random values
        self.is_running = random.choices([True, False], weights=[95, 5])[0]

        if self.is_running:
            self.rpm = random.randint(800, 6500)  # Revolutions per minute
            self.temperature = round(
                random.uniform(75.0, 105.0), 1
            )  # Celsius
            self.oil_pressure = random.randint(20, 60)  # PSI
        else:
            self.rpm = 0
            self.temperature = round(
                random.uniform(20.0, 35.0), 1
            )  # Ambient temp
            self.oil_pressure = 0

    def display_status(self):
        status = "RUNNING" if self.is_running else "OFF"
        print(f"\n--- {self.model_name} Engine Snapshot ---")
        print(f"Status:       {status}")
        print(f"Engine Speed: {self.rpm} RPM")
        print(f"Temperature:  {self.temperature}°C")
        print(f"Oil Pressure: {self.oil_pressure} PSI")


def compare_engines(car1, car2):
    print("\n=========================================")
    print("           ENGINE COMPARISON             ")
    print("=========================================")

    # Compare RPM
    if car1.rpm == car2.rpm:
        print("RPM:          Both engines are spinning at the same speed.")
    else:
        faster_car = car1 if car1.rpm > car2.rpm else car2
        slower_car = car2 if car1.rpm > car2.rpm else car1
        diff_rpm = faster_car.rpm - slower_car.rpm
        print(
            f"RPM:          {faster_car.model_name} is running harder (+{diff_rpm} RPM)."
        )

    # Compare Temperature
    if car1.temperature == car2.temperature:
        print("Temperature:  Both engines are at the exact same temperature.")
    else:
        hotter_car = car1 if car1.temperature > car2.temperature else car2
        cooler_car = car2 if car1.temperature > car2.temperature else car1
        diff_temp = round(hotter_car.temperature - cooler_car.temperature, 1)
        print(
            f"Temperature:  {hotter_car.model_name} is running hotter (+{diff_temp}°C)."
        )

    # Compare Oil Pressure
    if car1.oil_pressure == car2.oil_pressure:
        print("Oil Pressure: Both engines have identical oil pressure.")
    else:
        higher_press = car1 if car1.oil_pressure > car2.oil_pressure else car2
        print(
            f"Oil Pressure: {higher_press.model_name} has higher lubricating pressure."
        )


# --- Execution ---
if __name__ == "__main__":
    # Generate random engine data for two cars
    car_a = CarEngine("Supercharged V8")
    car_b = CarEngine("Turbocharged I4")

    # Display individual stats
    car_a.display_status()
    car_b.display_status()

    # Compare the two snapshots
    compare_engines(car_a, car_b)