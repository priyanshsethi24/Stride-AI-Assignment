import pdfplumber
import pandas as pd
import camelot
import os
from docx import Document

def extract_from_pdf(file_path):
    try:
        tables = camelot.read_pdf(file_path, pages='all')
        result = []
        for table in tables:
            df = table.df
            result.append(df.to_dict(orient='records'))
        return result
    except Exception:
        with pdfplumber.open(file_path) as pdf:
            all_tables = []
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table)
                    all_tables.append(df.to_dict(orient='records'))
        return all_tables

def extract_from_docx(file_path):
    doc = Document(file_path)
    tables = doc.tables
    result = []
    for table in tables:
        data = []
        for row in table.rows:
            data.append([cell.text.strip() for cell in row.cells])
        df = pd.DataFrame(data)
        result.append(df.to_dict(orient='records'))
    return result

def get_extracted_file_path(filename: str, format: str, extracted_dir: str = "extracted_output") -> str:
    """
    Returns the absolute path to the extracted file in the requested format.
    """
    clean_name = filename.replace(".pdf", "").replace(".docx", "")
    return os.path.join(extracted_dir, f"{clean_name}.{format}")



