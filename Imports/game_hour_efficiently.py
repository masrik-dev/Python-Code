import random
import math

game_name = input("Enter the game name you played most: ")
hour = int(input("Enter how many hours you play the game: "))

if hour < 30:
    print("You are still a noob!")
else:
    user = random.randint(100, 1000)

    ef = math.log(hour/30)/math.log(2000/30)
    ef = max(0, min(1, ef))

    efficiency = ef * 100

    print("\nGame:", game_name)
    print("Player ID:", user)
    print("Game Time:", hour, "hours")
print("Efficiency:", round(efficiency, 2), "%")
