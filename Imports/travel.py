# Top 5 travel destinations

destinations = [
    {
        "rank": 1,
        "place": "Paris",
        "country": "France",
        "highlight": "Eiffel Tower, art museums, and French cuisine",
    },
    {
        "rank": 2,
        "place": "Tokyo",
        "country": "Japan",
        "highlight": "Modern city life, temples, and sushi",
    },
    {
        "rank": 3,
        "place": "Bali",
        "country": "Indonesia",
        "highlight": "Beaches, rice terraces, and relaxing resorts",
    },
    {
        "rank": 4,
        "place": "Rome",
        "country": "Italy",
        "highlight": "Colosseum, Vatican City, and Italian food",
    },
    {
        "rank": 5,
        "place": "New York City",
        "country": "USA",
        "highlight": "Times Square, Central Park, and Broadway",
    },
]

futuristic_cities = [
    {
        "rank": 1,
        "place": "Dubai",
        "country": "UAE",
        "highlight": "Burj Khalifa, smart city tech, and desert futurism",
    },
    {
        "rank": 2,
        "place": "Singapore",
        "country": "Singapore",
        "highlight": "Gardens by the Bay, Marina Bay Sands, and smart urban design",
    },
    {
        "rank": 3,
        "place": "Seoul",
        "country": "South Korea",
        "highlight": "High-tech districts, K-culture, and digital city life",
    },
    {
        "rank": 4,
        "place": "Shanghai",
        "country": "China",
        "highlight": "Pudong skyline, bullet trains, and futuristic architecture",
    },
    {
        "rank": 5,
        "place": "Tokyo",
        "country": "Japan",
        "highlight": "Neon districts, robotics, and cutting-edge transit",
    },
]


def show_destinations(title, places):
    print(title)
    print("=" * 40)
    for d in places:
        print(f"\n#{d['rank']} {d['place']}, {d['country']}")
        print(f"   Why visit: {d['highlight']}")


show_destinations("Top 5 Travel Destinations", destinations)
print("\n")
show_destinations("Top 5 Futuristic City Destinations", futuristic_cities)
