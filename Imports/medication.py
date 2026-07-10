import random


def generate_vitals():
    return {
        "temperature": round(random.uniform(36.0, 40.5), 1),
        "heart_rate": random.randint(60, 120),
        "bp_systolic": random.randint(90, 180),
        "bp_diastolic": random.randint(50, 110),
        "oxygen_level": random.randint(90, 100),
        "respiratory_rate": random.randint(12, 24),
    }


def analyze_condition(vitals):
    temp = vitals["temperature"]
    hr = vitals["heart_rate"]
    systolic = vitals["bp_systolic"]
    diastolic = vitals["bp_diastolic"]
    oxygen = vitals["oxygen_level"]
    rr = vitals["respiratory_rate"]

    if oxygen < 92:
        return "Low oxygen", "Possible breathing problem or lung issue", "Seek urgent care and use oxygen support if prescribed"
    if temp >= 39 or (temp >= 38 and hr > 100):
        return "Fever / infection", "Likely viral or bacterial infection", "Rest and use paracetamol/acetaminophen if safe"
    if systolic >= 140 or diastolic >= 90:
        return "High blood pressure", "Stress, dehydration, or heart strain", "Rest and follow prescribed blood pressure treatment"
    if systolic <= 90 or diastolic <= 60:
        return "Low blood pressure", "Dehydration, blood loss, or shock", "Drink fluids and seek medical care if symptoms continue"
    if hr >= 100:
        return "High heart rate", "Stress, fever, or anxiety", "Rest and stay hydrated"
    if temp < 35.5:
        return "Low body temperature", "Exposure to cold or severe illness", "Warm up gently and get medical help if needed"
    if rr > 20:
        return "Breathing stress", "Possible mild respiratory irritation", "Rest and monitor breathing"
    return "Stable", "No major concern from these readings", "Maintain hydration and monitor regularly"


def main():
    vitals = generate_vitals()
    condition, cause, medicine = analyze_condition(vitals)

    print(f"Condition: {condition}")
    print(f"Possible cause: {cause}")
    print(f"Suggested medicine: {medicine}")


if __name__ == "__main__":
    main()
