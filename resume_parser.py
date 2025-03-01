import re
import pdfminer.high_level
from docx import Document

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    return pdfminer.high_level.extract_text(pdf_path)

def extract_text_from_docx(docx_path):
    """Extract text from DOCX file."""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_data(file_path):
    """Extracts structured data from a resume file."""
    text = ""
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    
    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text)
    }
    return data

def extract_name(text):
    """Dummy function to extract name (Can be improved with NLP)."""
    lines = text.split("\n")
    return lines[0] if len(lines) > 0 else "Unknown"

def extract_email(text):
    """Extracts email from text."""
    match = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", text)
    return match.group(0) if match else "Not Found"

def extract_phone(text):
    """Extracts phone number from text."""
    match = re.search(r"\+?\d[\d -]{8,}\d", text)
    return match.group(0) if match else "Not Found"

def extract_skills(text):
    """Extracts keywords that match known skills."""
    skills_db = ["Python", "Flask", "AI", "Machine Learning", "SQL", "Java", "JavaScript", "Docker"]
    skills_found = [skill for skill in skills_db if skill.lower() in text.lower()]
    return skills_found if skills_found else ["No Skills Found"]

def extract_experience(text):
    """Extracts years of experience (Basic estimation)."""
    match = re.search(r"(\d+)\s*years?", text, re.IGNORECASE)
    return match.group(1) if match else "Unknown"