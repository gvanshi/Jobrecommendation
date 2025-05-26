import streamlit as st
from utils.roadmap import generate_roadmap, draw_roadmap

st.title("📊 Career Roadmap Generator")
st.write("Visualize the path to your dream job step-by-step.")

job = st.text_input("🎯 Enter Target Job Role", placeholder="e.g., Data Scientist")
experience = st.slider("📅 Your Experience Level", 0, 5, 0)

if st.button("Generate Roadmap"):
    steps = generate_roadmap(job, experience)
    if not steps:
        st.error("❌ No roadmap found for this job role.")
    else:
        st.success("✅ Roadmap Generated:")
        st.write(" → ".join(steps))

        graph = draw_roadmap(steps)
        if graph:
            st.graphviz_chart(graph.source)
