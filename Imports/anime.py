"""Anime recommendation module with direct genre lookup."""

anime_recommendations = {
    "action": [
        "Attack on Titan",
        "My Hero Academia",
        "One Punch Man",
        "Demon Slayer"
    ],
    "adventure": [
        "Fullmetal Alchemist: Brotherhood",
        "Hunter x Hunter",
        "Made in Abyss",
        "Magi: The Labyrinth of Magic"
    ],
    "comedy": [
        "KonoSuba",
        "Gintama",
        "Ouran High School Host Club",
        "The Devil is a Part-Timer!"
    ],
    "drama": [
        "Your Lie in April",
        "Clannad: After Story",
        "Anohana: The Flower We Saw That Day",
        "Violet Evergarden"
    ],
    "fantasy": [
        "Re:Zero",
        "Fate/Zero",
        "The Rising of the Shield Hero",
        "Mushoku Tensei"
    ],
    "slice of life": [
        "Barakamon",
        "March Comes in Like a Lion",
        "Laid-Back Camp",
        "Honey and Clover"
    ],
    "sports": [
        "Haikyuu!!",
        "Kuroko's Basketball",
        "Yuri!!! on Ice",
        "Free!"
    ],
    "romance": [
        "Toradora!",
        "Your Name",
        "Fruits Basket",
        "Kimi ni Todoke"
    ],
    "sci-fi": [
        "Steins;Gate",
        "Psycho-Pass",
        "Cowboy Bebop",
        "Ghost in the Shell"
    ],
    "mystery": [
        "Death Note",
        "Erased",
        "Monster",
        "The Promised Neverland"
    ],
    "thriller": [
        "Parasyte",
        "Tokyo Ghoul",
        "Death Note",
        "Made in Abyss"
    ],
    "horror": [
        "Another",
        "Tokyo Ghoul",
        "Parasyte",
        "Shiki"
    ],
    "isekai": [
        "Konosuba",
        "Overlord",
        "The Rising of the Shield Hero",
        "That Time I Got Reincarnated as a Slime"
    ],
    "mecha": [
        "Neon Genesis Evangelion",
        "Gurren Lagann",
        "Code Geass",
        "Aldnoah.Zero"
    ],
    "supernatural": [
        "Mob Psycho 100",
        "Blue Exorcist",
        "Natsume's Book of Friends",
        "Darker than Black"
    ],
    "psychological": [
        "Perfect Blue",
        "Serial Experiments Lain",
        "Monster",
        "Paprika"
    ]
}

synonyms = {
    "sliceoflife": "slice of life",
    "scifi": "sci-fi",
    "science fiction": "sci-fi",
    "action/adventure": "adventure",
    "supernatural thriller": "supernatural",
    "school": "slice of life",
    "love": "romance",
    "romance comedy": "romance"
}


def normalize_genre(raw_genre: str) -> str:
    genre = raw_genre.strip().lower()
    genre = genre.replace("-", " ")
    genre = " ".join(genre.split())

    if genre in anime_recommendations:
        return genre
    if genre in synonyms:
        return synonyms[genre]

    for known in anime_recommendations:
        if genre == known or genre in known:
            return known
    return ""


def recommend_anime(genre: str):
    """Return a list of anime recommendations for a given genre."""
    normalized = normalize_genre(genre)
    return anime_recommendations.get(normalized, [])


def print_recommendations(genre: str):
    normalized = normalize_genre(genre)
    recommendations = recommend_anime(genre)

    if not normalized:
        print(f"Genre '{genre}' is not recognized. Available genres are:")
        print(", ".join(sorted(anime_recommendations.keys())))
        return

    print(f"Recommendations for '{normalized}':")
    for index, title in enumerate(recommendations, start=1):
        print(f"{index}. {title}")
    print()


if __name__ == "__main__":
    # Direct recommendation output without interactive input.
    print_recommendations("action")
    print_recommendations("fantasy")
    print_recommendations("slice of life")
    print_recommendations("sci-fi")
