# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse, FileResponse
# from fastapi.encoders import jsonable_encoder

# from extractor import extract_from_pdf, extract_from_docx, export_data
# import shutil
# import os

# app = FastAPI()

# # Define base paths using absolute locations
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# SAMPLE_DOCS_DIR = os.path.join(BASE_DIR, "sample_docs")
# OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# # Ensure directories exist
# os.makedirs(SAMPLE_DOCS_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# @app.post("/upload")
# async def upload(file: UploadFile = File(...)):
#     filepath = os.path.join(SAMPLE_DOCS_DIR, file.filename)
#     with open(filepath, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {"filename": file.filename}

# @app.get("/extract")
# @app.get("/extract")
# def extract(filename: str):
#     path = f"sample_docs/{filename}"
#     if not os.path.exists(path):
#         return JSONResponse({"error": f"File '{filename}' not found."}, status_code=404)

#     if filename.endswith('.pdf'):
#         data = extract_from_pdf(path)
#     elif filename.endswith('.docx'):
#         data = extract_from_docx(path)
#     else:
#         return JSONResponse({"error": "Unsupported file type"}, status_code=400)

#     if not data or not data[0]:
#         return JSONResponse({"error": f"No tables found in {filename}."}, status_code=204)

#     export_data(data, "extracted_table")

#     # Safely encode and limit output to first 100 rows
#     safe_table = jsonable_encoder(data[0][:100])
#     return JSONResponse(content=safe_table)

# @app.get("/download")
# def download(format: str = "csv"):
#     file_path = os.path.join(OUTPUT_DIR, f"extracted_table.{format}")
#     if not os.path.exists(file_path):
#         return JSONResponse({"error": f"No {format} file found."}, status_code=404)
#     return FileResponse(file_path, filename=f"extracted_table.{format}")

from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.responses import JSONResponse, FileResponse
from extractor import extract_from_pdf, extract_from_docx
from extractor import get_extracted_file_path
from file_manager import get_download_file
import os
import uuid
import pandas as pd

app = FastAPI()
UPLOAD_DIR = "uploaded_docs"
EXTRACTED_DIR = "extracted_output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACTED_DIR, exist_ok=True)

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"filename": file.filename}

@app.get("/extract")
def extract(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})

    if filename.endswith(".pdf"):
        tables = extract_from_pdf(file_path)
    elif filename.endswith(".docx"):
        tables = extract_from_docx(file_path)
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file format"})

    if not tables or len(tables) == 0:
        return JSONResponse(
            status_code=200,
            content={
                "message": "No tables extracted",
                "data": []
            }
        )

    try:
        df = pd.DataFrame(tables[0])
        json_path = os.path.join(EXTRACTED_DIR, f"{filename}.json")
        df.to_csv(json_path.replace(".json", ".csv"), index=False)
        return {"tables": tables}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# @app.get("/extract")
# def extract(filename: str):
#     file_path = os.path.join(UPLOAD_DIR, filename)
#     if filename.endswith(".pdf"):
#         tables = extract_from_pdf(file_path)
#     elif filename.endswith(".docx"):
#         tables = extract_from_docx(file_path)
#     else:
#         return JSONResponse(status_code=400, content={"error": "Unsupported file format"})

#     json_path = os.path.join(EXTRACTED_DIR, f"{filename}.json")
#     pd.DataFrame(tables[0]).to_csv(json_path.replace('.json', '.csv'), index=False)
#     return tables

@app.get("/download")
# def download(filename: str = Query(...), format: str = Query("csv")):
#     """
#     Allows the user to download the extracted table
#     in either CSV or JSON format as a downloadable file.
#     """

#     # Get correct file path using reusable component
#     file_path = get_extracted_file_path(filename, format)

#     if not os.path.exists(file_path):
#         return JSONResponse(status_code=404, content={"error": f"Extracted file not found: {file_path}"})

#     media_type = "text/csv" if format == "csv" else "application/json"
#     output_name = os.path.basename(file_path)

#     return FileResponse(
#         path=file_path,
#         media_type=media_type,
#         filename=output_name
#     )
def download(filename: str = Query(...), format: str = Query("csv")):
    """
    Return extracted table as downloadable CSV or JSON file.
    """

    # Construct file path using helper
    file_path = get_extracted_file_path(filename, format)

    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": f"File not found: {file_path}"})

    # Determine media type
    media_type = "text/csv" if format == "csv" else "application/json"

    # Force browser to download instead of displaying text
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=f"{filename.replace('.pdf','').replace('.docx','')}.{format}",
        headers={"Content-Disposition": f"attachment; filename={filename.replace('.pdf','').replace('.docx','')}.{format}"}
    )


