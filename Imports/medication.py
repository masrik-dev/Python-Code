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
        return "Low oxygen", "Possible breathing problem or lung issue", "Seek urgent care; oxygen support and prescribed inhalers or antibiotics may be needed"
    if temp >= 39 or (temp >= 38 and hr > 100):
        return "Fever / infection", "Likely viral or bacterial infection", "Rest; paracetamol/acetaminophen, ibuprofen, or antibiotics if prescribed"
    if systolic >= 140 or diastolic >= 90:
        return "High blood pressure", "Stress, dehydration, or heart strain", "Rest; prescribed antihypertensives such as amlodipine or lisinopril may be needed"
    if systolic <= 90 or diastolic <= 60:
        return "Low blood pressure", "Dehydration, blood loss, or shock", "Drink fluids; oral rehydration salts or IV fluids may be required"
    if hr >= 100:
        return "High heart rate", "Stress, fever, or anxiety", "Rest, stay hydrated, and use prescribed beta-blockers if advised"
    if temp < 35.5:
        return "Low body temperature", "Exposure to cold or severe illness", "Warm up gently; warm fluids and medical care if symptoms continue"
    if rr > 20:
        return "Breathing stress", "Possible mild respiratory irritation", "Rest; use prescribed bronchodilators or inhalers if needed"
    return "Stable", "No major concern from these readings", "Maintain hydration; paracetamol if needed for mild discomfort"


def main():
    vitals = generate_vitals()
    condition, cause, medicine = analyze_condition(vitals)

    print(f"Condition: {condition}")
    print(f"Possible cause: {cause}")
    print(f"Suggested medicine: {medicine}")


if __name__ == "__main__":
    main()
