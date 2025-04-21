import random
import sqlite3
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

table = None
class WordGuessrGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Guessr")
        self.root.geometry("810x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.words_list = self.get_5_letter_words('words.txt')
        self.random_word = ""
        self.current_attempt = 0
        self.max_attempts = 5
        self.name = ""
        self.level = 1
        self.total_score = 0
        self.letter_frames = []
        self.letter_labels = []

        self.setup_database()

        self.show_main_menu()

    def setup_database(self):
        conn = sqlite3.connect("WORD_GUESSR.db")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LEADERBOARD (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            LEVEL INTEGER,
            SCORE INTEGER
        )
        ''')
        conn.commit()
        conn.close()

    def get_5_letter_words(self, file_name):
            five_letter_words = []
            with open(file_name, 'r') as file:
                for word in file:
                    word = word.strip().lower()
                    if len(word) == 5 and word.isalpha():
                        five_letter_words.append(word)
            return five_letter_words


    def word_meaning(self, word):
        url = f"https://api.dictionaryapi.dev/api/v1/entries/en/{word}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            meanings = []
            for meaning_type in data[0].get("meaning", {}):
                if meaning_type in ["noun", "verb"]:
                    for entry in data[0]["meaning"][meaning_type]:
                        meanings.append(f"{meaning_type.capitalize()}: {entry['definition']}")
                        if len(meanings) >= 2:
                            return "\n".join(meanings)

            if meanings:
                return "\n".join(meanings)
            return "No definition found."

        except Exception as e:
            return "Meaning not found."

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        title_label = tk.Label(main_frame, text="WORD GUESSR", font=("Helvetica", 36, "bold"), bg="#f0f0f0",
                               fg="#333333")
        title_label.pack(pady=30)

        button_style = {"font": ("Helvetica", 16), "width": 15, "height": 2, "cursor": "hand2"}

        play_button = tk.Button(main_frame, text="PLAY", command=self.start_game_setup, bg="#4CAF50", fg="white",
                                **button_style)
        play_button.pack(pady=10)

        leaderboard_button = tk.Button(main_frame, text="LEADERBOARD", command=self.show_leaderboard, bg="#2196F3",
                                       fg="white", **button_style)
        leaderboard_button.pack(pady=10)

        exit_button = tk.Button(main_frame, text="EXIT", command=self.root.quit, bg="#F44336", fg="white",
                                **button_style)
        exit_button.pack(pady=10)

    def start_game_setup(self):
        self.clear_window()

        setup_frame = tk.Frame(self.root, bg="#f0f0f0")
        setup_frame.pack(expand=True, fill="both", padx=50, pady=50)

        title_label = tk.Label(setup_frame, text="Enter Your Name", font=("Helvetica", 24, "bold"), bg="#f0f0f0",
                               fg="#333333")
        title_label.pack(pady=30)

        name_var = tk.StringVar()
        name_entry = tk.Entry(setup_frame, textvariable=name_var, font=("Helvetica", 16), width=20)
        name_entry.pack(pady=20)
        name_entry.focus()

        start_button = tk.Button(
            setup_frame,
            text="START GAME",
            command=lambda: self.set_player_name(name_var.get()),
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            width=15,
            height=2,
            cursor="hand2"
        )
        start_button.pack(pady=20)

        back_button = tk.Button(
            setup_frame,
            text="BACK",
            command=self.show_main_menu,
            bg="#F44336",
            fg="white",
            font=("Helvetica", 12),
            width=10,
            cursor="hand2"
        )
        back_button.pack(pady=10)

    def set_player_name(self, name):
        if not name.strip():
            messagebox.showwarning("Warning", "Please enter your name!")
            return

        self.name = name
        self.level = 1
        self.total_score = 0
        self.start_game()

    def start_game(self):
        self.clear_window()
        self.current_attempt = 0
        self.random_word = random.choice(self.words_list)
        print(self.words_list)
        print(f"Random word: {self.random_word}")

        game_frame = tk.Frame(self.root, bg="#f0f0f0")
        game_frame.pack(expand=True, fill="both", padx=20, pady=20)

        info_frame = tk.Frame(game_frame, bg="#f0f0f0")
        info_frame.pack(fill="x", pady=10)

        player_label = tk.Label(info_frame, text=f"Player: {self.name}", font=("Helvetica", 14), bg="#f0f0f0")
        player_label.pack(side="left", padx=10)

        level_label = tk.Label(info_frame, text=f"Level: {self.level}", font=("Helvetica", 14), bg="#f0f0f0")
        level_label.pack(side="left", padx=10)

        score_label = tk.Label(info_frame, text=f"Score: {self.total_score}", font=("Helvetica", 14), bg="#f0f0f0")
        score_label.pack(side="left", padx=10)

        attempts_label = tk.Label(info_frame, text=f"Attempt: {self.current_attempt + 1}/{self.max_attempts}",
                                  font=("Helvetica", 14), bg="#f0f0f0")
        attempts_label.pack(side="right", padx=10)

        instructions = tk.Label(
            game_frame,
            text="Guess the 5-letter word. Green = correct position, Yellow = correct letter but wrong position, Red = wrong letter.",
            font=("Helvetica", 10),
            bg="#f0f0f0",
            wraplength=550
        )
        instructions.pack(pady=10)

        grid_frame = tk.Frame(game_frame, bg="#f0f0f0")
        grid_frame.pack(pady=20)

        self.letter_frames = []
        self.letter_labels = []

        for row in range(self.max_attempts):
            row_frames = []
            row_labels = []
            for col in range(5):
                letter_frame = tk.Frame(grid_frame, width=60, height=60, bg="#ffffff", highlightbackground="#000000",
                                        highlightthickness=1)
                letter_frame.grid(row=row, column=col, padx=5, pady=5)
                letter_frame.pack_propagate(False)

                letter_label = tk.Label(letter_frame, text="", font=("Helvetica", 24, "bold"), bg="#ffffff")
                letter_label.pack(expand=True)

                row_frames.append(letter_frame)
                row_labels.append(letter_label)

            self.letter_frames.append(row_frames)
            self.letter_labels.append(row_labels)

        input_frame = tk.Frame(game_frame, bg="#f0f0f0")
        input_frame.pack(pady=20)

        guess_var = tk.StringVar()
        guess_entry = tk.Entry(input_frame, textvariable=guess_var, font=("Helvetica", 16), width=10)
        guess_entry.pack(side="left", padx=10)
        guess_entry.focus()

        submit_button = tk.Button(
            input_frame,
            text="SUBMIT",
            command=lambda: self.check_guess(guess_var, guess_entry, attempts_label),
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 14),
            cursor="hand2"
        )
        submit_button.pack(side="left", padx=10)

        guess_entry.bind("<Return>", lambda event: self.check_guess(guess_var, guess_entry, attempts_label))

    def check_guess(self, guess_var, guess_entry, attempts_label):
        guess = guess_var.get().lower().strip()
        letter = ""
        if len(guess) != 5:
            messagebox.showwarning("Invalid Guess", "Your guess must be exactly 5 letters!")
            guess_entry.delete(0, tk.END)
            return

        if not guess.isalpha():
            messagebox.showwarning("Invalid Guess", "Your guess must contain only letters!")
            guess_entry.delete(0, tk.END)
            return

        if guess not in self.words_list:
            messagebox.showwarning("Invalid Guess", "Your guess must be a valid word from the word list!")
            guess_entry.delete(0, tk.END)
            return

        for i in range(5):
            letter += guess[i]
            self.letter_labels[self.current_attempt][i].config(text=guess[i].upper())

            if guess[i] == self.random_word[i]:
                self.letter_frames[self.current_attempt][i].config(bg="#4CAF50")  # Green
                self.letter_labels[self.current_attempt][i].config(bg="#4CAF50", fg="white")
            elif guess[i] in self.random_word:
                if self.random_word.count(guess[i]) >= letter.count(guess[i]):
                    self.letter_frames[self.current_attempt][i].config(bg="#FFC107")  # Yellow
                    self.letter_labels[self.current_attempt][i].config(bg="#FFC107")
                else:
                    self.letter_frames[self.current_attempt][i].config(bg="#F44336")  # Red
                    self.letter_labels[self.current_attempt][i].config(bg="#F44336", fg="white")
            else:
                self.letter_frames[self.current_attempt][i].config(bg="#F44336")  # Red
                self.letter_labels[self.current_attempt][i].config(bg="#F44336", fg="white")

        if guess == self.random_word:
            points = self.max_attempts - self.current_attempt
            self.total_score += points
            meaning = self.word_meaning(self.random_word)

            self.show_round_result(True, meaning, points)
            return

        self.current_attempt += 1
        attempts_label.config(text=f"Attempt: {self.current_attempt + 1}/{self.max_attempts}")

        if self.current_attempt >= self.max_attempts:
            meaning = self.word_meaning(self.random_word)
            self.show_round_result(False, meaning, 0)
            return

        guess_entry.delete(0, tk.END)
        guess_entry.focus()

    def show_round_result(self, won, meaning, points):
        result_window = tk.Toplevel(self.root)
        result_window.title("Round Result")
        result_window.geometry("600x750")
        result_window.transient(self.root)
        result_window.grab_set()

        result_frame = tk.Frame(result_window, padx=20, pady=20)
        result_frame.pack(expand=True, fill="both")

        if won:
            result_label = tk.Label(
                result_frame,
                text=f"Congratulations! You guessed the word!",
                font=("Helvetica", 14, "bold"),
                fg="#4CAF50"
            )
            points_label = tk.Label(
                result_frame,
                text=f"You earned {points} points!",
                font=("Helvetica", 12)
            )
            points_label.pack(pady=10)
        else:
            result_label = tk.Label(
                result_frame,
                text=f"Sorry! You ran out of attempts.",
                font=("Helvetica", 14, "bold"),
                fg="#F44336"
            )

        result_label.pack(pady=10)

        word_label = tk.Label(
            result_frame,
            text=f"The word was: {self.random_word.upper()}",
            font=("Helvetica", 16)
        )
        word_label.pack(pady=10)

        meaning_frame = tk.Frame(result_frame)
        meaning_frame.pack(pady=10, fill="both", expand = True)

        meaning_label = tk.Label(
            meaning_frame,
            text=f"Definition:",
            font=("Helvetica", 12, "bold")
        )
        meaning_label.pack(anchor="w")

        meaning_text = tk.Label(
            meaning_frame,
            text=meaning,
            font=("Helvetica", 10),
            justify="left",
            wraplength=350
        )
        meaning_text.pack(pady=5, anchor="w")

        button_frame = tk.Frame(result_frame)
        button_frame.pack(pady=20)

        if won:
            next_level_button = tk.Button(
                button_frame,
                text="Next Level",
                command=lambda: self.next_level(result_window),
                bg="#4CAF50",
                fg="white",
                font=("Helvetica", 12),
                cursor="hand2"
            )
            next_level_button.pack(side="left", padx=10)
        else:
            self.save_score(self.name, self.level, self.total_score)
            # After 5 wrong guesses, automatically return to main menu after showing the meaning
            result_window.after(3000, lambda: self.return_to_menu(result_window))

    def next_level(self, result_window):
        self.level += 1
        result_window.destroy()
        self.start_game()

    def return_to_menu(self, result_window):
        result_window.destroy()
        self.show_main_menu()

    def confirm_exit_game(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit the game? Your progress will be lost."):
            self.show_main_menu()

    def save_score(self, name, level, score):
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
        cursor.execute(
            "DELETE FROM LEADERBOARD WHERE id NOT IN (SELECT id FROM LEADERBOARD ORDER BY SCORE DESC LIMIT 10)")
        conn.commit()
        conn.close()

    def show_leaderboard(self):
        self.clear_window()
        global table
        leaderboard_frame = tk.Frame(self.root, bg="#f0f0f0")
        leaderboard_frame.pack(fill="both")

        title_label = tk.Label(leaderboard_frame, text="LEADERBOARD", font=("Arial", 24, "bold"), bg="#f0f0f0",
                               fg="#333333")
        title_label.pack(pady=20)

        table = tk.ttk.Treeview(leaderboard_frame, columns =('0','1','2','3'),show= "headings")
        
        table.heading('0', text = "Rank")
        table.heading('1', text = "Name")
        table.heading('2', text = "Level")
        table.heading('3', text = "Score")
        table.pack()
        
        conn = sqlite3.connect("WORD_GUESSR.db")
        cursor = conn.cursor()
        cursor.execute("SELECT NAME, LEVEL, SCORE FROM LEADERBOARD ORDER BY SCORE DESC LIMIT 10")
        scores = cursor.fetchall()
        
        for i, row in enumerate(scores, 1):
            table.insert("", tk.END, values=(i, *row))
        if not scores:
            no_scores_label = tk.Label(leaderboard_frame,text="No scores yet. Play the game to get on the leaderboard!",
                     font=("Helvetica", 12), bg="white")
            no_scores_label.pack(fill="x", pady=20)
        conn.close()
        back_button = tk.Button(
            leaderboard_frame,
            text="BACK TO MENU",
            command=self.show_main_menu,
            bg="#F44336",
            fg="white",
            font=("Helvetica", 12),
            width=15,
            cursor="hand2"
        )
        back_button.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordGuessrGame(root)
    root.mainloop()