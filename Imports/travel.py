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

print("Top 5 Travel Destinations")
print("=" * 40)

for d in destinations:
    print(f"\n#{d['rank']} {d['place']}, {d['country']}")
    print(f"   Why visit: {d['highlight']}")
