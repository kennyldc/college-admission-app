# College Admission — Interactive simulation

Interactive web app to explore **fairness and college admission** in a simplified model with two groups (advantaged / disadvantaged) and probabilistic features.

---

## About this project

This repository is part of **Project 1** for **DCDS 8991 — Computational and Data Sciences Research Exploration**, Washington University in St. Louis. The app illustrates fairness concepts in decision algorithms (admission) through a visual simulation.

---

## What the app does

- **Two groups:** Group A (advantaged) and Group D (disadvantaged), with different base probabilities for having certain features (x₁, x₂).
- **Decision rule:** A simple rule (e.g. f = x₁ ∧ x₂) is used to simulate “admission”.
- **Visualization:** Scroll-style sections with Apple-like transitions, circle with group icons, person grid, speed controls, and replay button.
- **Probabilities:** P(x₁=1), P(x₂=1), and P(f=1) are shown per group so you can see how disparity in resources translates into disparity in outcomes.

The goal is to show intuitively how **inequality in feature probabilities** can lead to **inequality in admission rates** across groups, even with the same “group-blind” rule.

---

## How to run it locally

### Requirements

- Python 3.9+
- Dependencies in `requirements.txt`

### Steps

1. **Clone the repo** (or download and unzip):

   ```bash
   git clone <repo-url>
   cd college-admission-app
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**

   ```bash
   streamlit run app.py
   ```

   It will open in your browser (default `http://localhost:8501`).

---

## Requirements (requirements.txt)

- `numpy`
- `pandas`
- `streamlit`
- `plotly`

---

## Deploy to the cloud (Streamlit Community Cloud)

1. Fork or push this repo to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. “New app” → select this repository.
4. **Main file path:** `app.py`
5. Deploy. You’ll get a public URL to share.

---

## License and use

Educational project for DCDS 8991. If you reuse or adapt the code, please credit the course and project.
