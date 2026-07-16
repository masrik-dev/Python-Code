import random

# Simple World Cup prediction model
teams = {
    "Argentina": {"attack": 91, "defense": 86, "form": 90},
    "Brazil": {"attack": 89, "defense": 84, "form": 88},
    "France": {"attack": 88, "defense": 87, "form": 87},
    "Germany": {"attack": 85, "defense": 86, "form": 83},
    "Spain": {"attack": 86, "defense": 85, "form": 85},
    "England": {"attack": 84, "defense": 82, "form": 84},
    "Netherlands": {"attack": 82, "defense": 84, "form": 83},
    "Portugal": {"attack": 83, "defense": 81, "form": 84},
}


def team_rating(team_name):
    stats = teams[team_name]
    return (stats["attack"] + stats["defense"] + stats["form"]) / 3


def predict_match(team_a, team_b):
    rating_a = team_rating(team_a)
    rating_b = team_rating(team_b)
    difference = rating_a - rating_b

    # Higher-rated teams are more likely to win
    win_probability = 1 / (1 + 10 ** (-difference / 12))
    return team_a if random.random() < win_probability else team_b


def simulate_tournament():
    groups = {
        "Group A": ["Argentina", "Brazil", "France", "Germany"],
        "Group B": ["Spain", "England", "Netherlands", "Portugal"],
    }

    group_winners = []
    for group_name, members in groups.items():
        winner = max(members, key=team_rating)
        group_winners.append(winner)
        print(f"{group_name}: {winner} is predicted to win the group")

    semifinal_1 = predict_match(group_winners[0], group_winners[1])
    semifinal_2 = predict_match(group_winners[1], group_winners[0])
    final = predict_match(semifinal_1, semifinal_2)

    print("\nPredicted knockout results:")
    print(f"Semi-final 1: {semifinal_1}")
    print(f"Semi-final 2: {semifinal_2}")
    print(f"Predicted World Cup winner: {final}")


if __name__ == "__main__":
    simulate_tournament()
