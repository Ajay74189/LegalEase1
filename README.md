# ⚖️ LegalEase AI

## AI-Powered Legal Document Generator

LegalEase AI is an AI-powered application that generates structured legal document drafts based on user-provided information.

The application uses Google Gemini for AI-based document generation and provides a Streamlit interface for users to enter document details and download generated documents.

---

## ✨ Features

- AI-powered legal document draft generation
- Google Gemini integration
- Streamlit web interface
- FastAPI backend
- TXT document generation
- DOCX document generation
- PDF document generation
- Editable generated document preview
- API endpoint for document generation
- Automated tests using Pytest
- Environment-variable based API key configuration

---

## 🏗️ Project Structure

```text
LegalEase AI/
│
├── ai_core/
│   └── gemini_generator.py
│
├── backend/
│   ├── formatters/
│   │   ├── docx_formatter.py
│   │   ├── pdf_formatter.py
│   │   └── text_formatter.py
│   │
│   ├── utils/
│   │   └── text_utils.py
│   │
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   ├── test_api.py
│   ├── test_formatters.py
│   └── test_utils.py
│
├── .env
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt