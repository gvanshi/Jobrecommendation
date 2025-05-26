import fitz  # PyMuPDF
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    """Extract raw text from uploaded resume PDF."""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_skills(text):
    """Extracts noun chunks and entities as skill-like words."""
    doc = nlp(text)
    keywords = set()

    # Grab common noun phrases and proper nouns
    for chunk in doc.noun_chunks:
        if len(chunk.text.strip()) > 2:
            keywords.add(chunk.text.strip())

    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'SKILL', 'WORK_OF_ART']:  # Add more if needed
            keywords.add(ent.text.strip())

    return list(keywords)
