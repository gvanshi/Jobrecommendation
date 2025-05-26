from fpdf import FPDF

def generate_roadmap_pdf(name, job_role, roadmap_steps, missing_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Career Roadmap for {name}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=f"Target Job: {job_role}", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Roadmap Steps:", ln=True)
    for i, step in enumerate(roadmap_steps, 1):
        pdf.multi_cell(0, 10, txt=f"{i}. {step}")

    pdf.ln(5)
    if missing_skills:
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Skills You Still Need:", ln=True)
        pdf.set_font("Arial", size=12)
        for skill in missing_skills:
            pdf.cell(200, 10, txt=f"- {skill}", ln=True)

    return pdf.output(dest='S').encode('latin-1')
