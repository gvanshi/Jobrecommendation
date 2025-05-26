import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Research Insights Dashboard", layout="wide")
st.title("📊 Key Research Insights")
st.markdown("Visualizing the most critical insights from real survey data.")

# --- Load All CSV Files ---
students = pd.read_csv("data/students_data.csv", on_bad_lines='skip')
industry = pd.read_csv("data/industry_data.csv")
feedback = pd.read_csv("data/feedback.csv")
roadmap = pd.read_csv("data/job_roadmap.csv")

# --- 🎓 STUDENTS INSIGHTS ---
import plotly.express as px

st.header("🎓 Student Survey Analysis")

# 1. Confidence by Year of Study
try:
    st.subheader("📈 Student Confidence vs Year")
    students['Confidence'] = pd.to_numeric(
        students["How confident are you in your ability to apply academic knowledge to an industry job?"],
        errors="coerce"
    )

    def normalize_year(year):
        year = str(year).lower().strip()
        mapping = {
            "1": "1st year", "first year": "1st year",
            "2": "2nd year", "second year": "2nd year",
            "3": "3rd year", "third year": "3rd year",
            "4": "4th year", "fourth year": "4th year",
        }
        return mapping.get(year, year)

    students['Year of Study'] = students['Year of Study'].apply(normalize_year)
    conf_chart = students.groupby("Year of Study")["Confidence"].mean().dropna()
    order = ["1st year", "2nd year", "3rd year", "4th year"]
    conf_chart = conf_chart.reindex(order).dropna()

    # Plotly Bar Chart with y-axis range
    fig = px.bar(
        conf_chart.reset_index(),
        x="Year of Study",
        y="Confidence",
        color="Year of Study",
        title="Confidence to Work in Industry by Year",
        range_y=[0, 5],
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Confidence chart error: {e}")


# 2. Programming Languages Learned
st.subheader("💻 Programming Languages Taught in Curriculum")
langs_series = pd.Series(
    [lang.strip() for row in students["Which programming languages have you learned in your academic curriculum?"].dropna()
     for lang in str(row).split(",")]
)
st.bar_chart(langs_series.value_counts())

# --- 🏭 INDUSTRY INSIGHTS ---
st.header("🏭 Industry Expert Insights")

# 1. Key Skill Gaps
st.subheader("🧠 Skill Gaps in Fresh Graduates (As per Industry)")
gaps = industry["What are the key knowledge gaps that you notice in recent graduates entering your industry? (Select all that apply)"].dropna()
gap_words = pd.Series([s.strip() for row in gaps for s in str(row).split(",")])
st.bar_chart(gap_words.value_counts())

# 2. Expert Curriculum Suggestions
st.subheader("💡 What Industry Wants Colleges to Improve")

# Load & clean suggestions
suggestions = industry["What is the single most important change that academic institutions can make to better prepare students for roles in your industry?"].dropna()

# Bar chart of counts
suggestion_counts = suggestions.value_counts().sort_values(ascending=False)
st.bar_chart(suggestion_counts)

# Show table of unique suggestions (optional)
st.markdown("### 📝 List of Unique Suggestions")
st.dataframe(suggestion_counts.reset_index().rename(columns={
    "index": "Suggestion",
    "count": "Number of Mentions"
}))


# --- 💰 JOB ROADMAP INSIGHTS ---
st.header("🗺️ Job Roles vs Average Salary")

try:
    st.subheader("💸 Top Paying Job Roles")
    roadmap["Salary Cleaned"] = roadmap["Average Salary (₹)"].str.replace(",", "").str.extract(r'(\d+)').astype(float)
    st.bar_chart(
        roadmap[["Job Role", "Salary Cleaned"]]
        .set_index("Job Role")
        .dropna()
        .sort_values(by="Salary Cleaned", ascending=False)
        .head(10)
    )
except:
    st.warning("Salary info is not in correct format.")

st.success("✅ Dashboard loaded with the most important insights for academic & industry gap analysis.")
