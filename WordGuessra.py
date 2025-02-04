import random as r
import colorama
from colorama import Back, Fore, Style

words = (
    "apple", "dance", "light", "stone", "green", "brush", "flame", "table", "earth", "peace",
    "chair", "water", "piano", "music", "sword", "clock", "cloud", "water", "sleep", "drive",
    "dream", "leafy", "horse", "shirt", "fruit", "grape", "carve", "brace", "swear", "laugh",
    "grasp", "vivid", "dears", "trunk", "light", "judge", "sweep", "trend", "tiger", "piano",
    "grasp", "crisp", "stone", "stage", "fancy", "laugh", "needy", "freed", "earth", "swoop",
    "creek", "vivid", "shout", "train", "purse", "chime", "sweep", "waste", "crisp", "brace",
    "whale", "horse", "clean", "sweep", "peace", "watch", "stone", "beads", "water", "lunar",
    "loose", "chart", "waste", "sweep", "trump", "bride", "glass", "sword", "piano", "drain",
    "quick", "pluck", "sweet", "gloom", "sword", "snake", "drove", "flock", "drive", "eager",
    "cider", "grape", "lapse", "stoic", "peace", "align", "torch", "loose", "wrist", "swear",
    "bench", "flute", "quilt", "stale", "creek", "swoop", "dawn", "grape", "roast", "drain",
    "bride", "pearl", "pride", "stone", "lunar", "dune", "swoop", "globe", "sweep", "blink",
    "thump", "flick", "chime", "grasp", "vivid", "tiger", "train", "plane", "piano", "crash",
    "trace", "spike", "trump", "swore", "sword", "sweep", "plume", "blink", "stone", "eagle",
    "lapse", "bloom", "grape", "guise", "brink", "tiger", "stone", "chime", "quick", "plume",
    "slate", "stone", "peace", "swoop", "scope", "spine", "align", "score", "piano", "bride",
    "ocean", "drove", "grape", "loose", "flute", "sweep", "peace", "wrack", "grasp", "plume",
    "shine", "noble", "brash", "sweep", "bride", "loose", "blaze", "stone", "pearl", "chime",
    "piano", "trace", "straw", "swoop", "flock", "cloud", "light", "stone", "bloom", "drive",
    "trunk", "quilt", "crisp", "glide", "shine", "brace", "flame", "glove", "swear", "trace",
    "sweet", "drain", "water", "beads", "peace", "bride", "stone", "piano", "gloom", "spike",
    "chime", "drive", "quick", "globe", "grape", "swoop", "brace", "flick", "flash", "stone",
    "align", "cloud", "plume", "clear", "spine", "crisp", "whale", "sweep", "pearl", "drove",
    "peace", "trace", "swear", "brush", "stone", "glass", "quick", "stone", "piano", "bride"
)


def game():
    temp = []
    colorama.init(autoreset=True)
    word = r.choice(words).upper()
    points = 0

    for i in word:
        if i in temp:
            continue
        else:
            print(word.count(i))
            temp.append(i)
    print(word)

    print("YOU HAVE TOTAL FIVE ATTEMPTS!")

    for j in range(0, 5):
        print()
        print(f"ATTEMPT {j + 1}!")
        print()
        while True:
            guess = input("Enter guess: ").upper()

            if len(guess) == 5:
                break
            else:
                print("GUESS HAS TO BE A 5 LETTER WORD")

        for i in range(0, 5):
            if guess == word:
                points = 5 - j
                print(f"The Guessed Word" + Fore.GREEN + f" {guess} ", end="")
                print("is correct.")
                return points, True
            else:
                if guess[i] == word[i]:
                    print(Fore.GREEN + f"{guess[i]} ", end="")
                elif guess[i] in word:
                    print(Fore.YELLOW + f"{guess[i]} ", end="")
                elif guess[i] not in word:
                    print(Fore.RED + f"{guess[i]} ", end="")
        print()

    print()
    print("YOU LOST")
    print(f"THE WORD WAS: {word}")
    return 0, False


level = 1
total_score = 0

while True:
    print(f"Level: {level}, Total Score: {total_score}")

    points, guessed_correctly = game()
    total_score = total_score + points

    if guessed_correctly == True:
        level = level + 1
    else:
        print(f"Final Score: {total_score}, Reached Level: {level}")
        break
