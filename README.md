# Around the Globe Quiz

The game presents multiple-choice questions about world capitals. Questions and options are generated dynamically using a structured geography dataset. Completed games are logged to a CSV file for statistical analysis with Pandas and NumPy, and visualized with Matplotlib.

----


## 1. Project Purpose

The purpose of this project is to build an interactive, data-driven console quiz application while applying core principles of Python programming, external data ingestion, numerical computation, and data visualization.

Specifically, the project demonstrates:

- Clean, procedural Python code with input validation and beginner-friendly error handling.
- External data loading from JSON and tabular logging to CSV.
- Exploratory data analysis and summary statistics using **Pandas** and **NumPy**.
- Clear graphical data visualization using **Matplotlib**.
- An interactive presentation and code walkthrough prepared in a **Jupyter Notebook**.

---

## 2. Main Features

- **Dynamic Question Generation:** Questions and answer options are constructed dynamically at runtime from `geography_data.json` instead of relying on a static question list.
- **Three Adaptive Difficulty Levels:** The relationship between incorrect answer options (distractors) and the correct capital changes based on the selected difficulty.
- **No Repeated Countries:** Each 5-question game randomly selects five distinct countries, ensuring variety.
- **Robust Input Validation:** Re-prompts the user if an invalid menu option or answer letter is entered, preventing unexpected crashes.
- **Mistake Review:** Displays missed questions at the end of the game alongside the user's answer and the correct capital city.
- **Persistent Game History:** Appends every finished game (timestamp, difficulty, score, maximum score, and accuracy percentage) to `quiz_history.csv`.
- **Statistical Summaries:** Computes overall average accuracy via NumPy and summarizes performance per difficulty via Pandas `.groupby()`.
- **Visual Performance Plots:** Displays three separate Matplotlib figures (bar chart, line chart, pie chart).
- **Presentation Notebook:** A self-contained Jupyter Notebook (`Around_the_Globe_Quiz.ipynb`) that runs all analyses and showcases the project.

---

## 3. Difficulty Levels and Distractor Generation

The quiz features three difficulty levels that adjust how difficult it is to spot the correct capital:

- **Easy (Intercontinental Distractors):**
  - Distractor capitals are chosen from countries located on **different continents** from the target country.
  - _Fallback:_ If fewer than 3 different-continent countries are available, any remaining non-target capitals are used.
- **Medium (Intracontinental Distractors):**
  - Distractor capitals are chosen from countries on the **same continent** as the target country.
  - _Fallback:_ If fewer than 3 same-continent countries exist (e.g. Australia in Oceania), all available same-continent capitals are chosen first, and the remaining spots are filled from other continents.
- **Hard (Regional Distractors with Prioritized Fallback):**
  - Distractor capitals are prioritized from countries within the **exact same geographic region** (e.g. Western Europe, Southern Europe).
  - _Fallback:_ If the target country's region has fewer than 3 other countries in the dataset, the algorithm takes **all available same-region capitals first**, fills remaining spots from other countries on the **same continent**, and only uses other continents if still fewer than 3 distractors are found.

In all cases, the correct capital is combined with the three distractors and shuffled, guaranteeing four unique options with an unpredictable correct answer position (A, B, C, or D).

---

## 4. Scoring System

Before the quiz begins, the player selects a difficulty level for the entire 5-question game:

- **Easy:** 1 point per correct answer (Maximum score: 5 points).
- **Medium:** 2 points per correct answer (Maximum score: 10 points).
- **Hard:** 3 points per correct answer (Maximum score: 15 points).

Accuracy is calculated at the end of the quiz using:
$$\text{Accuracy (\%)} = \left(\frac{\text{Score}}{\text{Maximum Score}}\right) \times 100$$

This design keeps the scoring rules simple and intuitive while directly rewarding the player for answering harder questions and normalizing performance across all difficulty levels to a standard 0–100% scale.

---

## 5. Dataset Explanation

The project uses `geography_data.json`, a starter dataset of 25 countries created specifically for this quiz. Each entry contains:

- `country`: Country name (e.g., "France", "Japan", "Brazil").
- `capital`: Official capital city (e.g., "Paris", "Tokyo", "Brasilia").
- `continent`: Continent name (e.g., "Europe", "Asia", "Americas", "Africa", "Oceania").
- `region`: Geographic sub-region based on UN M49 classifications (e.g., "Western Europe", "Eastern Asia", "South America").

The dataset is stored locally in standard JSON format and loaded using Python's built-in `json` module. No external APIs, web scrapers, or third-party database connections are used, making the application fully self-contained and reproducible offline.

---

## 6. Technologies and Libraries Used

- **Python Standard Library:**
  - `json`: Loads and parses `geography_data.json`.
  - `random`: Randomly samples countries and shuffles answer options.
  - `datetime`: Generates timestamps for completed quiz attempts.
  - `os`: Manages file paths and environment variables.
- **Third-Party Libraries:**
  - `pandas`: Reads, writes, filters, and groups quiz history.
  - `numpy`: Computes numerical statistics such as overall mean accuracy.
  - `matplotlib`: Generates the three performance charts.
  - `notebook`: Provides the interactive Jupyter Notebook environment.

---

## 7. Project Structure

```text
pythonProject/
├── quiz.py                    # Main interactive quiz script
├── geography_data.json        # Dataset of 25 countries, capitals, continents, and regions
├── quiz_history.csv           # Persistent history log of completed quizzes
├── Around_the_Globe_Quiz.ipynb# Jupyter Notebook for presentation and analysis
├── requirements.txt           # Python library dependencies with version bounds
├── README.md                  # Comprehensive project documentation
└── .gitignore                 # Files and folders ignored by Git
```

---

## 8. Installation Instructions

### 1. Clone or download the repository

Open a terminal in the project directory:

```bash
cd pythonProject
```

### 2. Install dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

---

## 9. How to Run the Quiz

Run `quiz.py` from your terminal:

```bash
python quiz.py
```

Follow the prompts:

1. Select difficulty level (`1` for Easy, `2` for Medium, `3` for Hard).
2. Answer each of the 5 questions by entering `A`, `B`, `C`, or `D`.
3. View your final score, percentage, mistake review, updated history table, and performance charts.

---

## 10. How to Open and Run the Jupyter Notebook

To launch the project presentation in your browser:

```bash
jupyter notebook Around_the_Globe_Quiz.ipynb
```

You can also open `Around_the_Globe_Quiz.ipynb` directly in VS Code or JupyterLab. Select **Kernel $\rightarrow$ Restart & Run All** to execute all code cells and display the tables and charts.
