# 💸 BROKE — The Tunisian Student Money Crisis

### Your Wallet Has a Story. Let's Decode It.

**BROKE** is an interactive data analytics project exploring how everyday spending habits can affect a university student's monthly budget.

From coffee breaks to shopping and transportation, small expenses can add up faster than expected.

This project transforms a synthetic dataset of Tunisian university student transactions into interactive visualizations, spending profiles, and budget simulations.

🌍 **[Explore the Live Dashboard](https://the-broke-student-analytics.streamlit.app/)**

---
![BROKE Dashboard Preview](images/dashboard_preview.png)

## 🎯 The Idea

University students often manage limited monthly budgets while balancing essential expenses and lifestyle choices.

But what happens when small daily purchases accumulate over an entire month?

BROKE explores questions such as:

- Where does most of a student's money go?
- How much of a monthly budget is consumed by small purchases?
- How quickly can a student exceed their budget?
- What spending patterns appear across different categories?
- How much could someone save by changing one daily habit?

The goal is to make spending patterns easier to understand through data analytics and interactive storytelling.

---

## 📊 Dataset

The project uses a **synthetic dataset** designed to simulate student spending behavior in Tunisia.

The dataset contains approximately 7,500 transactions representing 100 fictional university students during September 2026.

### Dataset features

| Feature | Description |
|---|---|
| `student_id` | Unique fictional student identifier |
| `date` | Transaction date |
| `category` | Expense category |
| `amount_tnd` | Transaction amount in Tunisian dinars |
| `payment_method` | Payment method |
| `is_essential` | Essential or non-essential expense |
| `monthly_budget` | Student's simulated monthly budget |
| `city` | Tunisian city |

Expense categories include Food, Coffee, Transport, Shopping, Entertainment, and Education.

**Important:** All records are artificially generated for educational purposes. They do not represent real students or measured spending behavior in Tunisia. Any patterns observed are specific to the simulation.

---

## 🔍 Data Analytics Workflow

### 1. Data Generation

Created a synthetic dataset containing student budgets, spending categories, transaction amounts, and dates.

### 2. Data Cleaning

Prepared the dataset using Pandas, including date processing, validation, and feature engineering.

### 3. Exploratory Data Analysis

Explored spending distributions, budget consumption, expense categories, and differences between simulated student profiles.

### 4. Behavioral Analytics

Developed rule-based indicators to explore:

- Small recurring expenses
- Budget consumption
- Cumulative spending
- Budget overruns
- Spending personality categories

### 5. Data Visualization

Created visualizations to communicate spending patterns and budget-related insights.

### 6. Interactive Dashboard

Developed a Streamlit application that allows users to explore student transactions and test different budget scenarios.

---

## 🖥️ Dashboard Features

### 🏠 Financial Overview

Explore an individual student's simulated financial situation.

Features include monthly budget indicators, total spending, remaining budget, category breakdowns, and transaction history.

### 💳 Spending Habits

Investigate how small purchases accumulate.

Users can adjust the threshold defining a small expense and explore cumulative spending over time.

### 🧠 Spending Personality

Explore a rule-based spending profile based on transaction categories.

Profiles include Coffee Lover, Foodie, Shopping Enthusiast, Entertainment Lover, and Balanced Spender.

These labels are descriptive rules, not psychological assessments or machine-learning classifications.

### 🔮 Budget Simulator

Experiment with different financial scenarios.

Users can adjust their monthly budget, current spending, remaining days, and expected daily expenses.

The simulator estimates future spending and illustrates how daily savings could accumulate over time.

These calculations are deterministic scenarios, not predictive machine-learning models.

---

## 📈 Data Visualizations

The analysis includes visualizations covering:

- Spending by category
- The accumulation of small expenses
- Monthly budget consumption
- Weekend spending patterns
- Spending personality distributions

### Spending by Category

![Spending by Category](images/spending_categories.png)

### The Invisible Spending Effect

![Small Expenses](images/invisible_spending.png)

### Budget Survival

![Budget Survival](images/budget_survival.png)

### Weekend Spending

![Weekend Spending](images/weekend_effect.png)

### Spending Personalities

![Spending Personalities](images/spending_personalities.png)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive data visualization |
| Streamlit | Interactive web dashboard |
| Jupyter Notebook | Exploratory analysis |
| Git & GitHub | Version control and project hosting |

---

## 🚀 Run the Project Locally

Clone the repository:

```bash
git clone https://github.com/asmalimayem/The-Broke-Student-Analytics
cd The-Broke-Student-Analytics
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the dashboard:

```bash
python -m streamlit run dashboard/app.py
```

Open the local address displayed in the terminal.

---

## ⚠️ Limitations

This project is an educational demonstration based entirely on simulated data.

The findings should not be generalized to Tunisian university students.

The spending personalities are rule-based, and the budget simulator uses arithmetic projections rather than machine-learning predictions.

Future versions could incorporate anonymized real-world data collected with appropriate consent, more realistic simulation assumptions, and additional statistical validation.

---

## 🌱 Future Improvements

Potential next steps include:

- More realistic spending simulations
- Advanced statistical analysis
- Personalized budget recommendations
- Additional interactive visualizations
- Comparison between different spending scenarios
- Improved mobile responsiveness

---

## 👩‍💻 Author

**Asma Limayem**

Computer Engineering Student | Data Science & AI

*Built as part of my Data Science learning journey.*

---

### 💸 BROKE

**Your Wallet Has a Story. Let's Decode It.**