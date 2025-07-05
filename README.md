# 🧾 Document Workflow Tool

## 📌 Overview

This tool extracts tables from PDF and DOCX documents and visualizes the workflow from upload to export.

## 🚀 Features

- Upload PDFs or DOCX
- Table extraction (including OCR for scanned PDFs)
- Streamlit-based editing & exporting
- Visual workflow mockup

## 📦 Run Instructions

```bash
cd backend
uvicorn app:app --reload

cd ../streamlit_app
streamlit run app.py
