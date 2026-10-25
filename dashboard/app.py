import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BROKE | Student Money Analytics",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ============================================================
# 3. COLORS
# ============================================================

COLORS = {
    "background": "#0F1020",
    "card": "#1A1B2E",
    "purple": "#A78BFA",
    "mint": "#6EE7B7",
    "pink": "#F472B6",
    "white": "#F8FAFC"
}


# ============================================================
# 4. LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    expenses = pd.read_csv(
        DATA_DIR / "cleaned_student_expenses.csv",
        parse_dates=["date"]
    )

    students = pd.read_csv(
        DATA_DIR / "student_behavioral_summary.csv"
    )

    daily = pd.read_csv(
        DATA_DIR / "student_daily_spending.csv",
        parse_dates=["date"]
    )

    return expenses, students, daily


try:
    df, student_summary, student_daily = load_data()

except (FileNotFoundError, pd.errors.ParserError) as error:

    st.error(f"Unable to load project data: {error}")
    st.stop()


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def style_chart(fig, title):

    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center"
        },
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["background"],
        font=dict(
            color=COLORS["white"],
            family="Arial",
            size=13
        ),
        title_font_size=19,
        margin=dict(
            l=30,
            r=30,
            t=80,
            b=40
        )
    )

    return fig


def get_student_data(student_id):

    student_df = df[
        df["student_id"] == student_id
    ].copy()

    student_info = student_summary[
        student_summary["student_id"] == student_id
    ]

    if student_info.empty:
        st.error("Student information not found.")
        st.stop()

    return student_df, student_info.iloc[0]


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("💸 BROKE")

st.sidebar.markdown(
    "Your Wallet Has a Story. Let's Decode It."
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Financial Overview",
        "💳 Spending Habits",
        "🧠 Spending Personality",
        "🔮 Budget Simulator"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    ### About BROKE

    BROKE explores the spending habits of
    simulated Tunisian university students.

    **Technologies**
    - Python
    - Pandas
    - Plotly
    - Streamlit

    **Dataset:** Synthetic / Educational
    """
)


# ============================================================
# 7. PAGE 1 — FINANCIAL OVERVIEW
# ============================================================

if page == "🏠 Financial Overview":

    st.title("🏠 Financial Overview")

    st.write(
        "Understand where your money goes "
        "and how much of your budget remains."
    )

    st.divider()

    # --------------------------------------------------------
    # STUDENT SELECTION
    # --------------------------------------------------------

    selected_student = st.selectbox(
        "Select a student",
        sorted(df["student_id"].unique()),
        key="overview_student"
    )

    student_df, student_info = get_student_data(
        selected_student
    )

    # --------------------------------------------------------
    # FINANCIAL CALCULATIONS
    # --------------------------------------------------------

    total_spending = student_df["amount_tnd"].sum()

    monthly_budget = float(
        student_info["monthly_budget"]
    )

    remaining_budget = monthly_budget - total_spending

    budget_used = (
        total_spending / monthly_budget
    ) * 100

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Monthly Budget",
            f"{monthly_budget:,.2f} TND"
        )

    with col2:
        st.metric(
            "💸 Total Spending",
            f"{total_spending:,.2f} TND"
        )

    with col3:
        st.metric(
            "💵 Remaining Budget",
            f"{remaining_budget:,.2f} TND"
        )

    with col4:
        st.metric(
            "📊 Budget Used",
            f"{budget_used:.1f}%"
        )

    # --------------------------------------------------------
    # BUDGET PROGRESS
    # --------------------------------------------------------

    st.subheader("📊 Budget Consumption")

    progress_value = min(
        max(budget_used / 100, 0),
        1
    )

    st.progress(progress_value)

    st.caption(
        f"{budget_used:.1f}% of the monthly budget consumed."
    )

    # --------------------------------------------------------
    # BUDGET ALERT
    # --------------------------------------------------------

    if remaining_budget < 0:

        st.error(
            "🚨 This student has exceeded "
            "their monthly budget!"
        )

    elif budget_used >= 80:

        st.warning(
            "⚠️ More than 80% of the budget "
            "has been consumed."
        )

    else:

        st.success(
            "✅ Spending is currently "
            "within the monthly budget."
        )

    st.divider()

    # --------------------------------------------------------
    # SPENDING BY CATEGORY
    # --------------------------------------------------------

    category_spending = (
        student_df.groupby(
            "category",
            as_index=False
        )["amount_tnd"]
        .sum()
        .sort_values(
            "amount_tnd",
            ascending=False
        )
    )

    fig = px.bar(
        category_spending,
        x="category",
        y="amount_tnd",
        color="category",
        text="amount_tnd",
        labels={
            "amount_tnd": "Spending (TND)",
            "category": "Category"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False
    )

    fig = style_chart(
        fig,
        "💸 Where Does Your Money Go?"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # BUDGET SURVIVAL CURVE
    # --------------------------------------------------------

    st.subheader("📈 Budget Survival Curve")

    student_daily_data = student_daily[
        student_daily["student_id"] == selected_student
    ].copy()

    if not student_daily_data.empty:

        student_daily_data = (
            student_daily_data.sort_values("date")
        )

        fig_budget = go.Figure()

        fig_budget.add_trace(
            go.Scatter(
                x=student_daily_data["date"],
                y=student_daily_data["budget_used_pct"],
                mode="lines+markers",
                name="Budget Used",
                line=dict(
                    color=COLORS["purple"],
                    width=4
                )
            )
        )

        fig_budget.add_hline(
            y=100,
            line_dash="dash",
            line_color=COLORS["pink"],
            annotation_text="Budget Limit — 100%"
        )

        fig_budget.update_layout(
            xaxis_title="Date",
            yaxis_title="Budget Used (%)"
        )

        fig_budget = style_chart(
            fig_budget,
            "📈 Your Monthly Budget Journey"
        )

        st.plotly_chart(
            fig_budget,
            use_container_width=True
        )

    else:

        st.info(
            "No daily spending data available."
        )

    st.divider()

    # --------------------------------------------------------
    # TRANSACTION HISTORY
    # --------------------------------------------------------

    st.subheader("📋 Transaction History")

    st.dataframe(
        student_df[
            [
                "date",
                "category",
                "amount_tnd",
                "payment_method"
            ]
        ].sort_values(
            "date",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 8. PAGE 2 — SPENDING HABITS
# ============================================================

elif page == "💳 Spending Habits":

    st.title("💳 Spending Habits")

    st.write(
        "Discover how small daily purchases "
        "can accumulate over time."
    )

    st.divider()

    # --------------------------------------------------------
    # STUDENT SELECTION
    # --------------------------------------------------------

    selected_student = st.selectbox(
        "Select a student",
        sorted(df["student_id"].unique()),
        key="habits_student"
    )

    student_df, student_info = get_student_data(
        selected_student
    )

    # --------------------------------------------------------
    # SMALL EXPENSE THRESHOLD
    # --------------------------------------------------------

    threshold = st.slider(
        "What counts as a small expense? (TND)",
        min_value=2,
        max_value=30,
        value=10,
        step=1
    )

    small_expenses = student_df[
        student_df["amount_tnd"] < threshold
    ].copy()

    # --------------------------------------------------------
    # SMALL EXPENSE METRICS
    # --------------------------------------------------------

    small_total = small_expenses["amount_tnd"].sum()

    small_count = len(small_expenses)

    monthly_budget = float(
        student_info["monthly_budget"]
    )

    small_budget_share = (
        small_total / monthly_budget
    ) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "☕ Small Expenses",
            f"{small_total:.2f} TND"
        )

    with col2:
        st.metric(
            "🧾 Transactions",
            small_count
        )

    with col3:
        st.metric(
            "💰 Share of Budget",
            f"{small_budget_share:.1f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # CUMULATIVE SMALL EXPENSES
    # --------------------------------------------------------

    small_daily = (
        small_expenses.groupby(
            "date",
            as_index=False
        )["amount_tnd"]
        .sum()
        .sort_values("date")
    )

    if not small_daily.empty:

        small_daily["cumulative"] = (
            small_daily["amount_tnd"].cumsum()
        )

        fig = px.line(
            small_daily,
            x="date",
            y="cumulative",
            markers=True,
            labels={
                "date": "Date",
                "cumulative":
                    "Cumulative Spending (TND)"
            }
        )

        fig.update_traces(
            line_color=COLORS["mint"],
            line_width=4
        )

        fig = style_chart(
            fig,
            "☕ The Invisible Spending Effect"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No transactions match this threshold."
        )

    # --------------------------------------------------------
    # TOP SMALL EXPENSE CATEGORIES
    # --------------------------------------------------------

    st.subheader("🔍 Where Do Small Expenses Go?")

    if not small_expenses.empty:

        small_categories = (
            small_expenses.groupby(
                "category",
                as_index=False
            )["amount_tnd"]
            .sum()
        )

        fig_categories = px.pie(
            small_categories,
            names="category",
            values="amount_tnd",
            hole=0.5
        )

        fig_categories = style_chart(
            fig_categories,
            "Small Expense Breakdown"
        )

        st.plotly_chart(
            fig_categories,
            use_container_width=True
        )

    else:

        st.info(
            "No small expenses to analyze."
        )


# ============================================================
# 9. PAGE 3 — SPENDING PERSONALITY
# ============================================================

elif page == "🧠 Spending Personality":

    st.title("🧠 What's Your Spending Personality?")

    st.write(
        "Discover your spending profile "
        "based on your transaction history."
    )

    st.divider()

    # --------------------------------------------------------
    # STUDENT SELECTION
    # --------------------------------------------------------

    selected_student = st.selectbox(
        "Select a student",
        sorted(student_summary["student_id"].unique()),
        key="personality_student"
    )

    student_df, student_info = get_student_data(
        selected_student
    )

    personality = student_info["personality"]

    # --------------------------------------------------------
    # PERSONALITY DESCRIPTION
    # --------------------------------------------------------

    descriptions = {
        "Coffee Lover ☕":
            "Coffee takes a significant share "
            "of your spending.",

        "Foodie 🍔":
            "Food is one of your main "
            "spending priorities.",

        "Shopping Enthusiast 🛍️":
            "Shopping represents a large "
            "part of your expenses.",

        "Entertainment Lover 🎉":
            "Entertainment plays a major "
            "role in your spending.",

        "Balanced Spender 💰":
            "Your spending doesn't match "
            "the other predefined profiles."
    }

    st.markdown(
        f"## {personality}"
    )

    st.info(
        descriptions.get(
            personality,
            "Your spending profile is being analyzed."
        )
    )

    st.divider()

    # --------------------------------------------------------
    # SPENDING DNA
    # --------------------------------------------------------

    category_spending = (
        student_df.groupby(
            "category",
            as_index=False
        )["amount_tnd"]
        .sum()
    )

    fig = px.pie(
        category_spending,
        names="category",
        values="amount_tnd",
        hole=0.55
    )

    fig.update_traces(
        textinfo="percent"
    )

    fig = style_chart(
        fig,
        "🧬 Your Spending DNA"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # TOP SPENDING CATEGORY
    # --------------------------------------------------------

    top_category = (
        category_spending.sort_values(
            "amount_tnd",
            ascending=False
        ).iloc[0]
    )

    st.metric(
        "🏆 Your Top Spending Category",
        top_category["category"]
    )

    st.caption(
        "Spending personalities are rule-based "
        "descriptions, not psychological assessments."
    )


# ============================================================
# 10. PAGE 4 — BUDGET SIMULATOR
# ============================================================

elif page == "🔮 Budget Simulator":

    st.title("🔮 Will You Survive Until Month-End?")

    st.write(
        "Test your budget and discover "
        "how small changes can affect your savings."
    )

    st.divider()

    # --------------------------------------------------------
    # USER INPUTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        monthly_budget = st.number_input(
            "Monthly Budget (TND)",
            min_value=1.0,
            value=450.0,
            step=10.0
        )

        money_spent = st.number_input(
            "Money Already Spent (TND)",
            min_value=0.0,
            value=280.0,
            step=10.0
        )

    with col2:

        days_remaining = st.number_input(
            "Days Remaining",
            min_value=1,
            max_value=31,
            value=12
        )

        daily_spending = st.number_input(
            "Average Daily Spending (TND)",
            min_value=0.0,
            value=18.0,
            step=1.0
        )

    # --------------------------------------------------------
    # CALCULATIONS
    # --------------------------------------------------------

    remaining_budget = (
        monthly_budget - money_spent
    )

    daily_limit = (
        remaining_budget / days_remaining
    )

    projected_spending = (
        money_spent
        + daily_spending * days_remaining
    )

    projected_overspending = max(
        0,
        projected_spending - monthly_budget
    )

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    st.subheader("📊 Your Financial Forecast")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Remaining Budget",
            f"{remaining_budget:.2f} TND"
        )

    with col2:
        st.metric(
            "📅 Daily Spending Limit",
            f"{daily_limit:.2f} TND"
        )

    with col3:
        st.metric(
            "📊 Projected Spending",
            f"{projected_spending:.2f} TND"
        )

    # --------------------------------------------------------
    # BUDGET ALERT
    # --------------------------------------------------------

    if projected_overspending > 0:

        st.error(
            f"🚨 At this pace, you may exceed "
            f"your budget by "
            f"{projected_overspending:.2f} TND."
        )

    else:

        st.success(
            "✅ Your projected spending "
            "stays within your budget."
        )

    st.divider()

    # --------------------------------------------------------
    # WHAT-IF SIMULATOR
    # --------------------------------------------------------

    st.subheader(
        "💡 What If You Changed One Habit?"
    )

    st.write(
        "Explore how reducing a small daily "
        "expense can create long-term savings."
    )

    daily_savings = st.slider(
        "How much could you save per day? (TND)",
        min_value=0.0,
        max_value=20.0,
        value=2.0,
        step=0.5
    )

    weekly_savings = daily_savings * 7
    monthly_savings = daily_savings * 30
    yearly_savings = daily_savings * 365

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📅 7-Day Savings",
            f"{weekly_savings:.2f} TND"
        )

    with col2:
        st.metric(
            "🗓️ 30-Day Savings",
            f"{monthly_savings:.2f} TND"
        )

    with col3:
        st.metric(
            "📈 365-Day Savings",
            f"{yearly_savings:.2f} TND"
        )

    st.caption(
        "This is a deterministic scenario, "
        "not a machine-learning prediction. "
        "Savings assume the daily reduction "
        "is maintained throughout the period."
    )


# ============================================================
# 11. GLOBAL FOOTER
# ============================================================

st.divider()

st.caption(
    "BROKE Analytics 💸 | "
    "Built with Python, Pandas, Plotly & Streamlit | "
    "Synthetic Data — Educational Project"
)