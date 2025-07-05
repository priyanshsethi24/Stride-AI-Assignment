import requests
import pandas as pd

API_URL = "http://localhost:8000"

def upload_document(file):
    files = {"file": file}
    response = requests.post(f"{API_URL}/upload", files=files)
    return response.json()

def extract_table(filename):
    response = requests.get(f"{API_URL}/extract", params={"filename": filename})
    return response.json()

def download_table(filename, format):
    response = requests.get(f"{API_URL}/download", params={"filename": filename, "format": format})
    return response.content