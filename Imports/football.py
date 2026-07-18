import random

# 32-team World Cup-style tournament simulation
teams = {
    "Argentina": 91,
    "Brazil": 90,
    "France": 89,
    "Germany": 88,
    "Spain": 87,
    "England": 86,
    "Italy": 84,
    "Netherlands": 83,
    "Portugal": 83,
    "Uruguay": 82,
    "Belgium": 82,
    "Croatia": 81,
    "Denmark": 80,
    "USA": 79,
    "Mexico": 78,
    "Japan": 77,
    "South Korea": 76,
    "Senegal": 76,
    "Morocco": 75,
    "Egypt": 74,
    "Nigeria": 74,
    "Algeria": 73,
    "Cameroon": 73,
    "Ghana": 72,
    "Serbia": 72,
    "Sweden": 71,
    "Austria": 70,
    "Switzerland": 70,
    "Colombia": 71,
    "Chile": 70,
    "Peru": 69,
    "Costa Rica": 68,
}

# Predefined historical-style edge values.
# Positive values favor the first team; negative values favor the second team.
history_edge = {
    ("Argentina", "Brazil"): 0.06,
    ("Brazil", "Argentina"): -0.06,
    ("Germany", "France"): -0.04,
    ("France", "Germany"): 0.04,
    ("Spain", "Germany"): 0.03,
    ("Germany", "Spain"): -0.03,
    ("Italy", "France"): -0.02,
    ("France", "Italy"): 0.02,
    ("England", "Germany"): 0.02,
    ("Germany", "England"): -0.02,
    ("Netherlands", "Spain"): -0.01,
    ("Spain", "Netherlands"): 0.01,
    ("Brazil", "Germany"): 0.04,
    ("Germany", "Brazil"): -0.04,
    ("Argentina", "Germany"): 0.03,
    ("Germany", "Argentina"): -0.03,
    ("France", "Brazil"): 0.01,
    ("Brazil", "France"): -0.01,
}


def calculate_win_probability(team_a, team_b):
    rating_a = teams[team_a]
    rating_b = teams[team_b]
    base_probability = 0.5 + (rating_a - rating_b) / 200
    edge = history_edge.get((team_a, team_b), 0.0)
    probability = base_probability + edge
    return max(0.05, min(0.95, probability))


def simulate_match(team_a, team_b):
    probability = calculate_win_probability(team_a, team_b)
    return team_a if random.random() < probability else team_b


def make_groups(team_list):
    shuffled = team_list[:]
    random.shuffle(shuffled)
    return [shuffled[i:i + 4] for i in range(0, len(shuffled), 4)]


def play_group_stage(groups):
    qualified = []
    print("Group Stage")
    print("-----------")

    for index, group in enumerate(groups, start=1):
        points = {team: 0 for team in group}
        for i in range(4):
            for j in range(i + 1, 4):
                team_a = group[i]
                team_b = group[j]
                winner = simulate_match(team_a, team_b)
                points[winner] += 3

        ranked = sorted(points.items(), key=lambda item: (-item[1], -teams[item[0]]))
        first = ranked[0][0]
        second = ranked[1][0]
        qualified.extend([first, second])
        print(f"Group {index}: {', '.join(group)}")
        print(f"  Qualifiers: {first}, {second}")

    return qualified


def play_knockout_round(teams_in_round, round_name):
    winners = []
    print(f"\n{round_name}")
    print("-" * len(round_name))

    for i in range(0, len(teams_in_round), 2):
        team_a = teams_in_round[i]
        team_b = teams_in_round[i + 1]
        winner = simulate_match(team_a, team_b)
        print(f"{team_a} vs {team_b} -> {winner}")
        winners.append(winner)

    return winners


def simulate_tournament():
    print("World Cup-style Tournament Prediction")
    print("====================================")

    all_teams = list(teams.keys())
    groups = make_groups(all_teams)

    qualified_teams = play_group_stage(groups)

    random.shuffle(qualified_teams)
    round_of_16 = qualified_teams
    winners_16 = play_knockout_round(round_of_16, "Round of 16")

    winners_8 = play_knockout_round(winners_16, "Quarterfinal")
    winners_4 = play_knockout_round(winners_8, "Semifinal")
    champion = play_knockout_round(winners_4, "Final")[0]

    print("\nPredicted Champion:")
    print(champion)


if __name__ == "__main__":
    simulate_tournament()
