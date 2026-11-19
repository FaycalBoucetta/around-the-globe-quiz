"""
Around the Globe Quiz
A geography quiz game using Python, Pandas, NumPy, and Matplotlib.
"""

from datetime import datetime
import json
import os
import random

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.environ.get("TEMP", "."), "matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_geography_data(filepath="geography_data.json"):
    """
    Load country geography data from a JSON file with basic error handling.

    Parameters:
        filepath (str): Path to the JSON file.

    Returns:
        list: List of country dictionaries, or None if loading fails.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list) or len(data) < 5:
            print(f"Error: '{filepath}' does not contain enough country data.")
            return None

        return data

    except FileNotFoundError:
        print(f"Error: Could not find '{filepath}'. Please ensure the file exists in the project folder.")
        return None
    except json.JSONDecodeError:
        print(f"Error: '{filepath}' is not a valid JSON file. Please check its formatting.")
        return None


def generate_capital_question(data, difficulty, target=None):
    """
    Generate a multiple-choice question for a country's capital based on difficulty.

    Parameters:
        data (list): List of country dictionaries.
        difficulty (str): 'Easy', 'Medium', or 'Hard'.
        target (dict, optional): Specific country dictionary. If None, picks randomly.

    Returns:
        dict: Question dictionary with question text, options A-D, and correct answer letter.
    """
    if target is None:
        target = random.choice(data)

    correct_capital = target["capital"]
    target_continent = target["continent"]
    target_region = target["region"]

    wrong_capitals = []

    if difficulty == "Easy":
        candidates = []
        for item in data:
            if item["continent"] != target_continent:
                candidates.append(item["capital"])

        if len(candidates) < 3:
            for item in data:
                if item["capital"] != correct_capital and item["capital"] not in candidates:
                    candidates.append(item["capital"])

        wrong_capitals = random.sample(candidates, 3)

    elif difficulty == "Medium":
        same_continent = []
        for item in data:
            if item["continent"] == target_continent and item["capital"] != correct_capital:
                same_continent.append(item["capital"])

        if len(same_continent) >= 3:
            wrong_capitals = random.sample(same_continent, 3)
        else:
            wrong_capitals = list(same_continent)

            other_capitals = []
            for item in data:
                if item["capital"] != correct_capital and item["capital"] not in wrong_capitals:
                    other_capitals.append(item["capital"])

            needed = 3 - len(wrong_capitals)
            wrong_capitals.extend(random.sample(other_capitals, needed))

    else:
        same_region = []
        for item in data:
            if item["region"] == target_region and item["capital"] != correct_capital:
                same_region.append(item["capital"])

        if len(same_region) >= 3:
            wrong_capitals = random.sample(same_region, 3)
        else:
            wrong_capitals = list(same_region)

            same_continent = []
            for item in data:
                if item["continent"] == target_continent and item["capital"] != correct_capital:
                    if item["capital"] not in wrong_capitals:
                        same_continent.append(item["capital"])

            needed = 3 - len(wrong_capitals)
            if len(same_continent) >= needed:
                wrong_capitals.extend(random.sample(same_continent, needed))
            else:
                wrong_capitals.extend(same_continent)

                needed = 3 - len(wrong_capitals)
                other_capitals = []
                for item in data:
                    if item["capital"] != correct_capital and item["capital"] not in wrong_capitals:
                        other_capitals.append(item["capital"])
                wrong_capitals.extend(random.sample(other_capitals, needed))

    options = [correct_capital] + wrong_capitals
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
    Display three separate performance charts using Matplotlib.

    Parameters:
        history_df (DataFrame): DataFrame containing past quiz records.
        diff_averages (Series): Average accuracy per difficulty level.
        diff_counts (Series): Count of games played per difficulty level.
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

    pie_labels = []
    pie_counts = []
    pie_colors = []
    color_map = {"Easy": "#66bb6a", "Medium": "#ffa726", "Hard": "#ef5350"}

    for d in difficulties:
        if d in diff_counts and diff_counts[d] > 0:
            pie_labels.append(d)
            pie_counts.append(diff_counts[d])
            pie_colors.append(color_map[d])

    plt.figure()
    plt.pie(pie_counts, labels=pie_labels, autopct="%1.1f%%", startangle=90, colors=pie_colors)
    plt.title("Games Played by Difficulty")
    plt.show()


def play_quiz():
    """
    Run the interactive Around the Globe Quiz.
    """
    geography_data = load_geography_data("geography_data.json")
    if geography_data is None:
        print("Cannot start quiz because geography data is missing or invalid. ")
        return

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
    print("Let's begin!\n")

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

    try:
        file_exists = os.path.exists(history_file)
        new_record.to_csv(history_file, mode="a", header=not file_exists, index=False)
        print("Quiz result saved to history.")
    except OSError as error:
        print(f"Warning: Could not save quiz result to file ({error}).")

    try:
        history_df = pd.read_csv(history_file)

        if history_df.empty:
            print("\nQuiz history is empty.")
            return

        print("\n" + "=" * 40)
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

        for diff_name in ["Easy", "Medium", "Hard"]:
            if diff_name in diff_counts:
                games = diff_counts[diff_name]
                avg = diff_averages[diff_name]
                print(f"  {diff_name:<6} -> Games played: {games} | Average accuracy: {avg:.2f}%")

        print("=" * 40)

        display_quiz_charts(history_df, diff_averages, diff_counts)

    except FileNotFoundError:
        print("\nNo quiz history file found to display.")
    except pd.errors.EmptyDataError:
        print("\nQuiz history file is empty.")
    except (pd.errors.ParserError, OSError) as error:
        print(f"\nWarning: Could not load quiz history ({error}).")


if __name__ == "__main__":
    play_quiz()
