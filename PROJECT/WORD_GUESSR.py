import random as r
import colorama
from colorama import Fore
import sqlite3


def get_5_letter_words(file_name):
    five_letter_words = []
    with open(file_name, 'r') as file:
        for word in file:
            word = word.strip().lower()
            if len(word) == 5 and word.isalpha():
                five_letter_words.append(word)

    return five_letter_words


words_list = get_5_letter_words('words.txt')


def game():
    colorama.init(autoreset=True)
    random_word = r.choice(words_list)
    print(random_word)

    print("YOU HAVE A TOTAL OF FIVE ATTEMPTS!")

    for j in range(5):
        print(f"\nATTEMPT {j + 1}!\n")
        while True:
            guess = input("Enter guess: ").lower()
            if guess not in words_list:
                print("Guess must be a valid 5-letter word from the word list!")
                continue
            if len(guess) == 5:
                break

        if guess == random_word:
            points = 5 - j
            print(Fore.GREEN + f"{guess.upper()} is correct!")
            return points, True

        for i in range(5):
            if guess[i] == random_word[i]:
                print(Fore.GREEN + f"{guess[i]} ", end="")
            elif guess[i] in random_word:
                print(Fore.YELLOW + f"{guess[i]} ", end="")
            else:
                print(Fore.RED + f"{guess[i]} ", end="")
        print()

    print("\nYOU LOST")
    print(f"The word was: {random_word.upper()}")
    return 0, False


def show_leaderboard():
    conn = sqlite3.connect("WORD_GUESSR.db")
    cursor = conn.cursor()
    cursor.execute("SELECT NAME, LEVEL, SCORE FROM LEADERBOARD ORDER BY score DESC LIMIT 10")
    scores = cursor.fetchall()
    conn.close()

    print("\nLEADERBOARD:")
    print("+-----------------+--------+-------+")
    print("| Name            | Level  | Score |")
    print("+-----------------+--------+-------+")
    for row in scores:
        print(f"| {row[0].ljust(15)} | {str(row[1]).ljust(6)} | {str(row[2]).ljust(5)} |")
    print("+-----------------+--------+-------+")


def save_score(name, level, score):
    conn = sqlite3.connect("WORD_GUESSR.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SCORE FROM LEADERBOARD WHERE NAME = ?", (name,))
    existing_score = cursor.fetchone()

    if existing_score:
        if score > existing_score[0]:
            cursor.execute("UPDATE LEADERBOARD SET LEVEL = ?, SCORE = ? WHERE NAME = ?", (level, score, name))
    else:
        cursor.execute("INSERT INTO LEADERBOARD (NAME, LEVEL, SCORE) VALUES (?, ?, ?)", (name, level, score))

    conn.commit()
    cursor.execute("DELETE FROM LEADERBOARD WHERE id NOT IN (SELECT id FROM LEADERBOARD ORDER BY SCORE DESC LIMIT 10)")
    conn.commit()
    conn.close()


def main():
    while True:

        choice = int(input("\n1. PLAY  2. LEADERBOARD  3. EXIT\nEnter your choice: "))

        if choice == 1:
            name = input("ENTER YOUR NAME: ")
            level = 1
            total_score = 0

            while True:
                print(f"\nLevel: {level}, Total Score: {total_score}")

                points, guessed_correctly = game()
                total_score += points

                if guessed_correctly:
                    level += 1
                else:
                    print(f"\nFinal Score: {total_score}, Reached Level: {level}")
                    save_score(name, level, total_score)
                    break
        elif choice == 2:
            show_leaderboard()
        elif choice == 3:
            print("THANK YOU FOR PLAYING!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


main()
