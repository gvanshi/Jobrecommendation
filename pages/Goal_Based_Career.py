import streamlit as st
from utils.roadmap import generate_roadmap, draw_roadmap
from utils.resume_parser import extract_text_from_pdf, extract_skills
from utils.pdf_generator import generate_roadmap_pdf
from utils.email_sender import send_email_with_pdf
import pandas as pd
import tempfile

# Initialize session keys
if "target_job" not in st.session_state:
    st.session_state["target_job"] = ""
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = ""
if "last_roadmap" not in st.session_state:
    st.session_state["last_roadmap"] = []

st.title("🧭 Goal-Based Career Roadmap")
st.markdown("### What job do you dream of? We’ll help you get there!")

target_job = st.text_input("🎯 Your Dream Job Role", placeholder="e.g., Data Analyst")
resume_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=['pdf'])

if target_job and resume_file:
    with st.spinner("Reading resume and analyzing..."):
        raw_text = extract_text_from_pdf(resume_file)
        resume_skills = extract_skills(raw_text)
        resume_skills_lower = [s.lower() for s in resume_skills]

        # Load roadmap data
        df = pd.read_csv("data/job_roadmap.csv")
        row = df[df['Job Role'].str.lower() == target_job.lower()]

        if not row.empty:
            required_raw = row.iloc[0]['Required Skills']
            required_cleaned = required_raw.replace("Beginner:", "").replace("Advanced:", "").strip()
            required_skills = [s.strip().lower() for s in required_cleaned.split(",")]

            missing = [s for s in required_skills if s not in resume_skills_lower]

            st.success("✅ Here’s what we found:")
            st.write("📌 **Skills You Already Have:**", ", ".join([s for s in required_skills if s in resume_skills_lower]))
            st.write("🚧 **Skills You Still Need:**", ", ".join(missing) if missing else "None! You’re all set.")
            
            st.markdown("---")
            st.subheader("📍 Your Personalized Roadmap")
            roadmap_steps = row.iloc[0]['Suggested Roadmap'].split(" → ")
            graph = draw_roadmap(roadmap_steps)
            st.graphviz_chart(graph.source)

            # Save session progress
            st.session_state["target_job"] = target_job
            st.session_state["resume_uploaded"] = resume_file.name
            st.session_state["last_roadmap"] = roadmap_steps

            # 🎁 BONUS INSIGHTS SECTION
            st.markdown("---")
            st.subheader("💼 Additional Career Insights")

            st.info("📜 **Recommended Certifications:** " + str(row.iloc[0]['Recommended Certifications']))
            st.info("🧰 **Tools You’ll Use:** " + str(row.iloc[0]['Real-World Tools']))
            st.info("📈 **Industry Demand:** " + str(row.iloc[0]['Industry Demand Level']))
            st.info("💰 **Average Salary:** " + str(row.iloc[0]['Average Salary (₹)']))
            st.info("📚 **Learning Resources:** " + str(row.iloc[0]['Best Learning Resources']))

            # 🎓 COURSE RECOMMENDER SECTION
            st.markdown("---")
            st.subheader("🎓 Suggested Courses for Missing Skills")
            try:
                course_df = pd.read_csv("data/courses_map.csv")
                matched_courses = []

                for skill in missing:
                    match = course_df[course_df['Skill'].str.lower() == skill.lower()]
                    if not match.empty:
                        course_link = match.iloc[0]['Course']
                        matched_courses.append(f"**{skill.title()}**: [Click here]({course_link})")

                if matched_courses:
                    for course in matched_courses:
                        st.markdown(f"✅ {course}")
                else:
                    st.info("No specific course links found for these skills yet.")

            except Exception as e:
                st.warning(f"⚠️ Could not load course suggestions: {e}")

            # 📥 PDF DOWNLOAD SECTION
            st.markdown("---")
            st.subheader("📥 Download Your Career Plan")

            pdf_bytes = generate_roadmap_pdf(
                name="User",
                job_role=target_job,
                roadmap_steps=roadmap_steps,
                missing_skills=missing
            )

            st.download_button(
                label="📄 Download Career Roadmap as PDF",
                data=pdf_bytes,
                file_name=f"{target_job}_roadmap.pdf",
                mime='application/pdf'
            )

            # 📧 EMAIL SECTION
            st.markdown("---")
            st.subheader("📧 Email This Roadmap to Yourself")

            email = st.text_input("Enter your email address")
            sender_email = st.secrets["EMAIL_USER"]
            sender_password = st.secrets["EMAIL_PASS"]

            if st.button("📨 Send to My Email"):
                if email and pdf_bytes:
                    with st.spinner("Sending email..."):
                        # Save PDF to a temporary file
                        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        tmp_file.write(pdf_bytes)
                        tmp_file.close()

                        sent, message = send_email_with_pdf(
                            recipient_email=email,
                            subject=f"Your Career Roadmap for {target_job}",
                            body_text="Hi,\n\nPlease find attached your personalized career roadmap.\n\nBest wishes!",
                            pdf_data=None,  # not needed anymore
                            filename=tmp_file.name,
                            sender_email=sender_email,
                            sender_password=sender_password
                        )
                    if sent:
                        st.success("✅ Email sent successfully!")
                    else:
                        st.error(f"❌ Failed to send email: {message}")
                else:
                    st.warning("Please enter a valid email.")

        else:
            st.error("❌ Sorry! This job role is not found in our roadmap database.")

# 🕒 Progress Tracker at the bottom
st.markdown("---")
st.subheader("🕒 Your Session Progress")

st.write(f"🎯 Last Target Job: **{st.session_state['target_job']}**")
st.write(f"📄 Last Resume: **{st.session_state['resume_uploaded']}**")

if st.session_state['last_roadmap']:
    st.markdown("🧭 Last Roadmap Steps:")
    for step in st.session_state['last_roadmap']:
        st.markdown(f"- {step}")
else:
    st.info("No roadmap generated yet.")


# 🕒 Feedback

st.markdown("---")
st.subheader("🗣️ We’d Love Your Feedback!")

rating = st.slider("⭐ How useful was this roadmap for you?", 1, 5)
comment = st.text_area("💬 Any suggestions or thoughts?")



if st.button("Submit Feedback"):
    import csv
    import datetime

    feedback_data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "job_role": target_job,
        "rating": rating,
        "comment": comment,
        "resume_name": resume_file.name
    }

    with open("data/feedback.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=feedback_data.keys())
        if f.tell() == 0:  # If file is empty, write header
            writer.writeheader()
        writer.writerow(feedback_data)

    st.success("✅ Thank you! Your feedback was recorded.")
