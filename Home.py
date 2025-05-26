import streamlit as st

# OpenAI API Key
OPENAI_API_KEY = st.secrets["openai"]["api_key"]

# Email Credentials
EMAIL_USER = st.secrets["email"]["user"]
EMAIL_PASS = st.secrets["email"]["password"]

st.set_page_config(
    page_title="Career Recommendation System",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Career Recommendation System")

st.markdown("""
Welcome to the AI-powered platform that helps you:

- 🔍 Get personalized **career recommendations**
- 📈 See your **career roadmap**
- 📄 **Extract skills** from your resume
- 🚀 Prepare for your **dream job** using data-driven insights!

👉 Use the left sidebar to navigate through different tools.
""")

st.markdown("---")
