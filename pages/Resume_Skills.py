import streamlit as st
from utils.resume_parser import extract_text_from_pdf, extract_skills

st.title("📄 Resume Skills Extractor")
st.write("Upload your resume and extract the key skills mentioned automatically.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])

if uploaded_file:
    with st.spinner("⏳ Reading and analyzing resume..."):
        text = extract_text_from_pdf(uploaded_file)

        if text.startswith("Error"):
            st.error(text)
        else:
            skills = extract_skills(text)
            if not skills:
                st.warning("⚠️ No significant skill terms found.")
            else:
                st.success("✅ Skills Extracted:")
                st.write(", ".join(skills))

                # Optional download
                st.download_button("📥 Download Skills List", "\n".join(skills), file_name="skills.txt")
