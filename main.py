import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import random

class RockPaperScissorsGame:
    def __init__(self):
        self.window = ThemedTk(theme="equilux")  # Using the Equilux theme
        self.window.title("Rock-Paper-Scissors Game")

        self.user_score = 0
        self.computer_score = 0

        self.choice_icons = {
            "rock": "🪨",
            "paper": "📄",
            "scissors": "✂️",
        }

        self.create_widgets()

    def create_widgets(self):
        self.window.configure(background="#263238")  # Set background color

        ttk.Label(self.window, text="Choose Rock, Paper, or Scissors:", background="#263238", foreground="#ffffff").pack(pady=10)

        for choice in self.choice_icons:
            ttk.Button(self.window, text=self.choice_icons[choice], command=lambda c=choice: self.play(c),
                       style="GameButton.TButton").pack(pady=5)

        self.result_label = ttk.Label(self.window, text="", background="#263238", foreground="#ffffff")
        self.result_label.pack(pady=10)

        self.scores_label = ttk.Label(self.window, text="Score: User {} - {} Computer".format(self.user_score, self.computer_score),
                                      background="#263238", foreground="#ffffff")
        self.scores_label.pack(pady=5)

        ttk.Button(self.window, text="Play Again", command=self.reset_game, style="GameButton.TButton").pack(pady=10)

        self.window.style = ttk.Style()
        self.window.style.configure("GameButton.TButton", font=('Helvetica', 12), background="#546e7a", foreground="#ffffff")

    def play(self, user_choice):
        choices = list(self.choice_icons.keys())
        computer_choice = random.choice(choices)

        result = self.determine_winner(user_choice, computer_choice)

        self.result_label.config(text="User: {} | Computer: {} | Result: {}".format(
            self.choice_icons[user_choice], self.choice_icons[computer_choice], result))
        self.update_scores(result)
        self.update_scores_label()

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a Tie!"
        elif (
            (user_choice == "rock" and computer_choice == "scissors") or
            (user_choice == "paper" and computer_choice == "rock") or
            (user_choice == "scissors" and computer_choice == "paper")
        ):
            return "You Win!"
        else:
            return "You Lose!"

    def update_scores(self, result):
        if result == "You Win!":
            self.user_score += 1
        elif result == "You Lose!":
            self.computer_score += 1

    def update_scores_label(self):
        self.scores_label.config(text="Score: User {} - {} Computer".format(self.user_score, self.computer_score))

    def reset_game(self):
        self.result_label.config(text="")
        self.user_score = 0
        self.computer_score = 0
        self.update_scores_label()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.window.mainloop()
