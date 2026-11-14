from datetime import datetime
import json
import os
import random

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.environ.get("TEMP", "."), "matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


with open("geography_data.json", "r", encoding="utf-8") as file:
    geography_data = json.load(file)


def generate_capital_question(data, difficulty, target=None):
    """
    Generate a multiple-choice question for a country's capital.

    Parameters:
        data (list): List of country dictionaries with geography details.
        difficulty (str): 'Easy', 'Medium', or 'Hard'.
        target (dict, optional): Specific country dictionary. If None, picks randomly.

    Returns:
        dict: A question dictionary with question text, options A-D, and correct answer letter.
    """
    if target is None:
        target = random.choice(data)
    correct_capital = target["capital"]
    target_continent = target["continent"]
    target_region = target["region"]

    candidates = []

    if difficulty == "Easy":
        for item in data:
            if item["continent"] != target_continent:
                candidates.append(item["capital"])

        if len(candidates) < 3:
            for item in data:
                if item["capital"] != correct_capital and item["capital"] not in candidates:
                    candidates.append(item["capital"])

    elif difficulty == "Medium":
        for item in data:
            if item["continent"] == target_continent and item["capital"] != correct_capital:
                candidates.append(item["capital"])

        if len(candidates) < 3:
            for item in data:
                if item["capital"] != correct_capital and item["capital"] not in candidates:
                    candidates.append(item["capital"])

    else:
        for item in data:
            if item["region"] == target_region and item["capital"] != correct_capital:
                candidates.append(item["capital"])

        if len(candidates) < 3:
            for item in data:
                if item["continent"] == target_continent and item["capital"] != correct_capital:
                    if item["capital"] not in candidates:
                        candidates.append(item["capital"])

        if len(candidates) < 3:
            for item in data:
                if item["capital"] != correct_capital and item["capital"] not in candidates:
                    candidates.append(item["capital"])

    wrong_capitals = random.sample(candidates, 3)

    options = [correct_capital, wrong_capitals[0], wrong_capitals[1], wrong_capitals[2]]
    random.shuffle(options)

    if options[0] == correct_capital:
        correct_letter = "A"
    elif options[1] == correct_capital:
        correct_letter = "B"
    elif options[2] == correct_capital:
        correct_letter = "C"
    else:
        correct_letter = "D"

    return {
        "question": f"What is the capital of {target['country']}?",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": correct_letter
    }


def display_quiz_charts(history_df, diff_averages, diff_counts):
    """
    Display three separate performance charts using Matplotlib:
    1. Bar chart: Average accuracy by difficulty.
    2. Line chart: Accuracy across games over time.
    3. Pie chart: Share of games played at each difficulty.

    Parameters:
        history_df (DataFrame): Pandas DataFrame containing past quiz records.
        diff_averages (Series): Pandas Series with average accuracy per difficulty.
        diff_counts (Series): Pandas Series with game counts per difficulty.
    """
    if len(history_df) == 0:
        print("\nNo quiz history available to display charts.")
        return

    print("\nDisplaying performance charts...")

    difficulties = ["Easy", "Medium", "Hard"]
    avg_accuracies = []
    for d in difficulties:
        if d in diff_averages:
            avg_accuracies.append(diff_averages[d])
        else:
            avg_accuracies.append(0.0)

    plt.figure()
    plt.bar(difficulties, avg_accuracies, color=["green", "orange", "red"])
    plt.title("Average Accuracy by Difficulty")
    plt.xlabel("Difficulty Level")
    plt.ylabel("Average Accuracy (%)")
    plt.ylim(0, 100)
    plt.show()

    game_numbers = list(range(1, len(history_df) + 1))
    plt.figure()
    plt.plot(game_numbers, history_df["accuracy_pct"], marker="o", color="blue")
    plt.title("Accuracy Over Time")
    plt.xlabel("Game Number")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 105)
    plt.grid(True)
    plt.show()

    played_labels = list(diff_counts.index)
    played_counts = list(diff_counts.values)
    plt.figure()
    plt.pie(played_counts, labels=played_labels, autopct="%1.1f%%", startangle=90)
    plt.title("Games Played by Difficulty")
    plt.show()


score = 0
incorrect_answers = []
points_per_difficulty = {"Easy": 1, "Medium": 2, "Hard": 3}

print("=" * 40)
print("   Welcome to Around the Globe Quiz!")
print("=" * 40)
print()

print("Select your difficulty level:")
print("  1 - Easy")
print("  2 - Medium")
print("  3 - Hard")

difficulty_choice = input("Enter 1, 2 or 3: ").strip()

while difficulty_choice not in ["1", "2", "3"]:
    print("Invalid input. Please enter 1, 2 or 3.")
    difficulty_choice = input("Enter 1, 2 or 3: ").strip()

if difficulty_choice == "1":
    difficulty = "Easy"
elif difficulty_choice == "2":
    difficulty = "Medium"
else:
    difficulty = "Hard"

selected_countries = random.sample(geography_data, 5)

questions = []
for country in selected_countries:
    new_question = generate_capital_question(geography_data, difficulty, country)
    questions.append(new_question)

points = points_per_difficulty[difficulty]
max_points = points * len(questions)

print(f"\nYou selected: {difficulty} ({points} point(s) per correct answer)")
print(f"Let's begin!\n")

for i in range(len(questions)):
    q = questions[i]
    print(f"Question {i + 1} of {len(questions)}")
    print(q["question"])
    print(f"  A) {q['A']}")
    print(f"  B) {q['B']}")
    print(f"  C) {q['C']}")
    print(f"  D) {q['D']}")

    player_answer = input("Your answer (A/B/C/D): ").strip().upper()

    while player_answer not in ["A", "B", "C", "D"]:
        print("Invalid input. Please enter A, B, C or D.")
        player_answer = input("Your answer (A/B/C/D): ").strip().upper()

    if player_answer == q["answer"]:
        print(f"Correct! +{points} point(s)\n")
        score = score + points
    else:
        print(f"Wrong! The correct answer was {q['answer']} ({q[q['answer']]}).\n")
        incorrect_answers.append({
            "question": q["question"],
            "your_answer": f"{player_answer} ({q[player_answer]})",
            "correct_answer": f"{q['answer']} ({q[q['answer']]})",
        })

print("=" * 40)
print(f"Quiz complete! Your score: {score} out of {max_points} points")

percentage = (score / max_points) * 100
print(f"Accuracy: {percentage:.2f}%")

if percentage >= 80:
    print("Excellent!")
elif percentage >= 60:
    print("Good job!")
elif percentage >= 40:
    print("Not bad! Keep practising.")
else:
    print("Keep practising!")
print("=" * 40)

print()
if len(incorrect_answers) == 0:
    print("Congratulations! You made no mistakes!")
else:
    print("Review Your Mistakes:")
    print("-" * 40)
    for item in incorrect_answers:
        print(f"  Q: {item['question']}")
        print(f"  Your answer: {item['your_answer']}")
        print(f"  Correct answer: {item['correct_answer']}")
        print()

current_result = {
    "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "difficulty": difficulty,
    "score": score,
    "max_score": max_points,
    "accuracy_pct": round(percentage, 2)
}

new_record = pd.DataFrame([current_result])

history_file = "quiz_history.csv"
file_exists = os.path.exists(history_file)
new_record.to_csv(history_file, mode="a", header=not file_exists, index=False)

history_df = pd.read_csv(history_file)

print("=" * 40)
print("           QUIZ HISTORY")
print("=" * 40)
print(history_df.to_string(index=False))
print("-" * 40)

total_games = len(history_df)
average_accuracy = np.mean(history_df["accuracy_pct"])
highest_accuracy = history_df["accuracy_pct"].max()

print(f"Total games played: {total_games}")
print(f"Average accuracy:   {average_accuracy:.2f}% (NumPy mean)")
print(f"Highest accuracy:   {highest_accuracy:.2f}% (Pandas max)")

print("\nPerformance by Difficulty (Pandas):")
diff_counts = history_df.groupby("difficulty")["accuracy_pct"].count()
diff_averages = history_df.groupby("difficulty")["accuracy_pct"].mean()

for diff in ["Easy", "Medium", "Hard"]:
    if diff in diff_counts:
        games = diff_counts[diff]
        avg = diff_averages[diff]
        print(f"  {diff:<6} -> Games played: {games} | Average accuracy: {avg:.2f}%")

print("=" * 40)

display_quiz_charts(history_df, diff_averages, diff_counts)
