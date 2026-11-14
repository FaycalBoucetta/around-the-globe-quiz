 Around the Globe Quiz


The game asks multiple-choice questions about world capitals. Questions are generated automatically from a dataset of 25 countries.

---

## 1. Main Features

- **Three difficulty levels:**
  - **Easy:** Wrong options come from different continents.
  - **Medium:** Wrong options come from the same continent.
  - **Hard:** Wrong options come from the same geographic region.
- **Dynamic questions:** Questions are created automatically using `geography_data.json`.
- **No repeated countries:** Every 5-question quiz uses five different countries.
- **Input check:** The game only accepts valid choices (`1`, `2`, `3` for difficulty; `A`, `B`, `C`, `D` for answers).
- **Review mistakes:** At the end of the quiz, missed questions are shown with their correct capital names.
- **Quiz history:** Every game is saved in `quiz_history.csv` with the date, difficulty, score, and accuracy percentage.
- **Data analysis:**
  - Calculates the average accuracy using NumPy.
  - Calculates games played and average accuracy by difficulty using Pandas.
- **Visual charts:** Displays three Matplotlib charts (average accuracy by difficulty, accuracy over time, and games played by difficulty).

---

## 2. Libraries Used

- **Python standard library:**
  - `json` (loads the geography data)
  - `random` (picks countries and shuffles answers)
  - `datetime` (saves game timestamps)
  - `os` (checks if history files exist)
- **External packages:**
  - `pandas` (saves and analyzes quiz history)
  - `numpy` (calculates average accuracy)
  - `matplotlib` (creates the performance charts)

---

## 3. Project Files

- `quiz.py`: The main script that runs the quiz in the terminal.
- `geography_data.json`: A JSON file with 25 countries, capitals, continents, and regions.
- `quiz_history.csv`: A CSV file where completed games are saved.
- `requirements.txt`: Lists the required Python packages (`pandas`, `numpy`, `matplotlib`).
- `Around_the_Globe_Quiz.ipynb`: A Jupyter Notebook demonstrating the data, analysis, and charts.
- `.gitignore`: Tells Git which temporary files to ignore.

---

## 4. Installation and How to Run

### Install dependencies
In your terminal, navigate to the project folder and run:

```bash
pip install -r requirements.txt
```

### Run the quiz
To play the quiz in the terminal, run:

```bash
python quiz.py
```

### Run the Jupyter Notebook
To open the presentation notebook, run:

```bash
jupyter notebook Around_the_Globe_Quiz.ipynb
```
(or open it directly in VS Code or any notebook editor).
