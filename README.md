# About Document Table Extractor

An end-to-end document processing application built using **FastAPI** for backend processing and **Streamlit** for frontend UI. It allows users to:

- Upload PDF or DOCX documents
- Automatically extract tabular data
- View and edit extracted tables in an interactive interface
- Export tables in **CSV** or **JSON** formats

---

## 2. Project Structure
Stride AI Assignment/
├── backend/
│   ├── app.py                  # FastAPI backend
│   ├── extractor.py            # Table extraction logic (Camelot, OCR, etc.)
│   └── requirements.txt        # Backend dependencies
├── frontend/
│   ├── workflow_canvas/        # No-code or HTML-based workflow UI
│   └── mockups.png             # Workflow diagram or UI snapshot
├── streamlit_app/
│   ├── app.py                  # Streamlit front-end app
│   └── helpers.py              # API helper functions for Streamlit
├── sample_docs/
│   ├── invoice.pdf             # Test sample
│   └── report.docx             # Test sample
├── docs/
│   ├── flow_diagram.png        # Architecture flow diagram
│   └── test_run.gif            # Demo of the app in use
└── README.md                   # Main documentation

## 3. Environment Setup
#### 1. Install Python 3.10+

https://www.python.org/downloads/

#### a) Create and activate a virtual environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux

#### b) Install dependencies
bash
Copy
Edit
pip install -r backend/requirements.txt

## 4. Setup and running the App
#### 🔹 Start the FastAPI backend command
cd backend
uvicorn app:app --reload

By default, runs at:
http://127.0.0.1:8000

#### 🔹 Start the Streamlit frontend command
bash
Copy
Edit
cd streamlit_app
streamlit run app.py
This opens the UI at:
http://localhost:8501

## 5. Sample Usage

1. Upload a file (invoice.pdf or report.docx).

2. Click "Extract Tables".

3. Review and edit the extracted tables.

4. Choose export format: CSV / JSON / Word / PDF.

5. Download results.
