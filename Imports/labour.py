def worker_pay(hours, rate):
    """Return the pay for a worker given hours worked and hourly rate."""
    return hours * rate


import random


def department_amounts(department_name, worker_count=5):
    """Simulate medium-company revenue and worker pay for a department."""
    print(f"\n--- {department_name} Department ---")
    revenue = random.uniform(1_000_000, 2_500_000)
    workers = []

    for i in range(1, worker_count + 1):
        hours = random.uniform(160, 220)
        rate = random.uniform(35, 80)
        pay = worker_pay(hours, rate)
        workers.append(pay)
        print(f"  Worker {i} pay: ${pay:,.2f} ({hours:.1f}h @ ${rate:.2f}/h)")

    total_salary = sum(workers)
    net_earnings = revenue - total_salary

    print(f"{department_name} revenue: ${revenue:,.2f}")
    print(f"{department_name} total salary cost: ${total_salary:,.2f}")
    print(f"{department_name} net earnings after salaries: ${net_earnings:,.2f}")

    return {
        "department": department_name,
        "revenue": revenue,
        " salary_cost": total_salary,
        "net_earnings": net_earnings,
        "worker_pays": workers,
    }


def main():
    departments = ["Planning", "Administration", "Supply Chain Management"]
    results = []

    for department in departments:
        results.append(department_amounts(department))

    company_revenue = sum(item["revenue"] for item in results)
    company_salary = sum(item[" salary_cost"] for item in results)
    company_net = sum(item["net_earnings"] for item in results)

    print("\n=== Company Summary ===")
    print(f"Total company revenue: ${company_revenue:.2f}")
    print(f"Total company salary cost: ${company_salary:.2f}")
    print(f"Total company net earnings after salaries: ${company_net:.2f}")


if __name__ == "__main__":
    main()

