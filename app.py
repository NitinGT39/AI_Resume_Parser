import streamlit as st
import pdfplumber
import docx2txt
import re
import spacy
import pandas as pd
import json
from io import BytesIO
from time import sleep

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# =========================
# FUNCTION DEFINITIONS
# =========================
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_text_from_docx(uploaded_file):
    return docx2txt.process(uploaded_file)

def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group() if match else "Not found"

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-()]{8,14}\d", text)
    return match.group() if match else "Not found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not found"

def extract_skills(text):
    skill_set = [
        "python", "java", "sql", "html", "css", "javascript", "c++", "c#", "excel",
        "project management", "time management", "public speaking", "conflict management",
        "data analytics", "communication skills", "team player", "leadership", "negotiation",
        "recruitment", "hr policies", "benefits", "payroll", "compliance", "training",
        "organizational skills", "analytical skills", "problem solving", "decision making",
        "microsoft office", "presentation", "employee engagement", "talent acquisition","design software","typography","UI/UX designer","print design","creative problem solving"
    ]

    found = []
    resume_text = text.lower()

    for skill in skill_set:
        if skill.lower() in resume_text:
            found.append(skill.title())

    return list(set(found))


def extract_education(text):
    education_keywords = [
        "bachelor", "master", "ph.d", "mba", "b.a", "m.a", "bsc", "msc", "bca", "mca"
    ]
    institute_keywords = ["university", "college", "institute", "school"]
    
    lines = text.lower().split("\n")
    results = []

    for i, line in enumerate(lines):
        if any(degree in line for degree in education_keywords):
            if any(inst in line for inst in institute_keywords):
                results.append(line.strip().title())
            elif i+1 < len(lines) and any(inst in lines[i+1] for inst in institute_keywords):
                results.append((line + " " + lines[i+1]).strip().title())

    return list(set(results))




# =========================
# STREAMLIT UI
# =========================

st.set_page_config(page_title="AI Resume Scanner", layout="wide")

# Header Section
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 30px 0 10px 0;
        background: linear-gradient(to right, #2e86de, #48c6ef);
        color: black;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .info-box {
        background-color: #f8f9fa;
        color: black;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #2e86de;
    }
    </style>
    <div class='main-header'>
        <h1>📄 Smart Resume AI Parser</h1>
        <p>Upload resumes and extract candidate data like a pro!</p>
    </div>
""", unsafe_allow_html=True)

# File Upload
st.subheader("📁 Upload Resumes")
uploaded_files = st.file_uploader(
    "Drop PDF or DOCX files below (Multiple files supported)", 
    type=["pdf", "docx"], 
    accept_multiple_files=True
)

# Process Files
if uploaded_files:
    all_parsed_data = []
    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):
        st.markdown(f"---\n#### 📑 **Processing:** `{file.name}`")

        file_type = file.name.split('.')[-1].lower()
        resume_text = extract_text_from_pdf(file) if file_type == "pdf" else extract_text_from_docx(file)

        st.subheader("📄 Raw Resume Text")
        st.text_area("Extracted Text", resume_text, height=300)

        name = extract_name(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        skills = extract_skills(resume_text)
        education = extract_education(resume_text)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='info-box'><b>👤 Name:</b> {name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><b>📧 Email:</b> {email}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><b>📞 Phone:</b> {phone}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='info-box'><b>💼 Skills:</b> {', '.join(skills) if skills else 'Not found'}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><b>🎓 Education:</b> {', '.join(education) if education else 'Not found'}</div>", unsafe_allow_html=True)

        parsed_data = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Skills": ', '.join(skills),
            "Education": ', '.join(education)
        }
        all_parsed_data.append(parsed_data)
        progress.progress((i + 1) / len(uploaded_files))
        sleep(0.1)

    st.success(f"✅ Successfully parsed {len(all_parsed_data)} resume(s)")

    # Export Section
    st.markdown("## 💾 Export Results")
    all_df = pd.DataFrame(all_parsed_data)

    col_csv, col_json, col_excel = st.columns(3)
    with col_csv:
        st.download_button("⬇️ CSV", all_df.to_csv(index=False), file_name="resumes.csv", mime="text/csv")
    with col_json:
        json_data = json.dumps(all_parsed_data, indent=2)
        st.download_button("⬇️ JSON", data=json_data, file_name="resumes.json", mime="application/json")
    with col_excel:
        excel_buffer = BytesIO()
        all_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button("⬇️ Excel", data=excel_buffer, file_name="resumes.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("👈 Please upload at least one resume to begin.")

# Footer
st.markdown("---")
st.markdown("<center><small>🛠️ Made with 💙 using Python & Streamlit</small></center>", unsafe_allow_html=True)