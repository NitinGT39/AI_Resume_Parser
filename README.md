🚀 Smart Resume Parser | Internship Project @ Pinnacle Labs

An intelligent resume parsing web app created during my internship at Pinnacle Labs, designed to extract essential candidate details from PDF and DOCX resumes using advanced AI and NLP techniques.

🧰 Tech Stack
Python 3

Streamlit – Web app frontend

spaCy – Natural language processing

pdfplumber / docx2txt – Resume content extraction

Pandas – Data manipulation and structuring

OpenPyXL – Excel file generation and export

🔍 Key Highlights
Supports upload of multiple resumes (PDF/DOCX)

Extracts the following candidate data:

👤 Full Name

📧 Email

📱 Phone Number

💼 Skills

🎓 Educational Background

Shows real-time progress during parsing

Export parsed data into:

📥 Excel (.xlsx)

📥 JSON

📥 CSV (auto-saved locally)

Modern and user-friendly interface

⚙️ Getting Started
Clone the Repository

bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/Smart-Resume-Parser.git
cd Smart-Resume-Parser
Create Virtual Environment

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # For Windows
Install Required Libraries

bash
Copy
Edit
pip install -r requirements.txt
python -m spacy download en_core_web_sm
Launch the App

bash
Copy
Edit
streamlit run app.py
🚧 Roadmap & Enhancements (Coming Soon)
🔠 OCR integration for image-based resumes

🏢 Work Experience extraction (company, role, duration)

🤖 Smarter skill recognition via ML models

📊 Candidate scoring based on job description match

💾 Integration with backend database for data persistence