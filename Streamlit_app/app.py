# # import streamlit as st
# # import requests
# # import pandas as pd

# # st.title("📄 Document Table Extractor")

# # uploaded_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"])
# # if uploaded_file:
# #     with open(f"sample_docs/{uploaded_file.name}", "wb") as f:
# #         f.write(uploaded_file.read())
# #     st.success("File uploaded successfully.")
    
# #     if st.button("🔍 Extract Table"):
# #         res = requests.get(f"http://localhost:8000/extract?filename={uploaded_file.name}")
# #         data = res.json()
# #         df = pd.DataFrame(data)
# #         st.dataframe(df)

# #         st.markdown("### ✏️ Edit Table Below")
# #         edited_df = st.data_editor(df)

# #         if st.button("⬇ Export CSV"):
# #             csv = edited_df.to_csv(index=False).encode('utf-8')
# #             st.download_button("Download CSV", csv, file_name="extracted_table.csv")

# #         if st.button("⬇ Export JSON"):
# #             json_data = edited_df.to_json(orient="records").encode('utf-8')
# #             st.download_button("Download JSON", json_data, file_name="extracted_table.json")

# # st.markdown("### 🔄 Workflow Canvas")
# # st.image("frontend/mockups.png", caption="Drag-and-Drop Workflow")


# import streamlit as st
# import pandas as pd
# import requests
# import os

# st.set_page_config(page_title="Document Table Extractor", layout="wide")

# st.title("📄 Document Table Extractor")

# # -----------------------------------------------
# # 1. List existing PDFs/DOCX in the sample_docs/ folder
# # -----------------------------------------------
# sample_docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_docs"))
# doc_files = [f for f in os.listdir(sample_docs_path) if f.endswith((".pdf", ".docx"))]

# if doc_files:
#     selected_file = st.selectbox("📂 Select a file from sample_docs/", doc_files)

#     if st.button("🔍 Extract Table"):
#         # Call backend extract API
#         r = requests.get(f"http://localhost:8000/extract?filename={selected_file}")
#         if r.status_code == 200:
#             table = r.json()
#             df = pd.DataFrame(table)

#             st.dataframe(df, use_container_width=True)
#             st.markdown("### ✏️ Edit Table Below")
#             edited_df = st.data_editor(df)

#             # Download buttons
#             csv = edited_df.to_csv(index=False).encode('utf-8')
#             st.download_button("Download CSV", csv, f"{selected_file}_table.csv")

#             json_data = edited_df.to_json(orient="records").encode('utf-8')
#             st.download_button("Download JSON", json_data, f"{selected_file}_table.json")
#         else:
#             st.error(f"Extraction failed: {r.text}")

# else:
#     st.warning("No documents found in sample_docs/. Please upload PDFs or DOCX files.")

# # Optional: Upload new file into the folder
# st.markdown("---")
# st.markdown("### 📤 Or Upload a New File")
# uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
# if uploaded_file:
#     with open(os.path.join(sample_docs_path, uploaded_file.name), "wb") as f:
#         f.write(uploaded_file.read())
#     st.success(f"{uploaded_file.name} uploaded successfully! Refresh dropdown to see it.")

# # Optional: Canvas image
# st.markdown("### 🔄 Workflow Canvas View")

import streamlit as st
import pandas as pd
from helpers import upload_document, extract_table

st.set_page_config(page_title="📄 Document Table Extractor", layout="wide")

st.title("📄 Document Table Extractor")

st.header("📤 Upload Document")
file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if file:
    # Upload file to backend
    upload_response = upload_document(file)
    filename = upload_response.get("filename")
    st.success(f"✅ Uploaded: {filename}")

    st.header("🔍 Extract Table")
    response = extract_table(filename)

    # Extract actual tables from the response
    tables = response.get("tables", [])

    if tables and isinstance(tables, list) and len(tables) > 0:
        raw_table = tables[0]  # Only process first table

        if isinstance(raw_table, list) and len(raw_table) > 1:
            # Convert to DataFrame
            headers = list(raw_table[0].values())
            rows = [list(row.values()) for row in raw_table[1:]]
            df = pd.DataFrame(rows, columns=headers)

            st.subheader("📋 Extracted Table")
            st.dataframe(df, use_container_width=True)

            st.subheader("✏️ Edit Table Below")
            edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

            st.subheader("⬇ Export Edited Table")
            export_format = st.selectbox("Select export format", ["csv", "json"])
            if st.button("Download"):
                if export_format == "csv":
                    csv = edited_df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download CSV", csv, file_name="edited_table.csv")
                else:
                    json_data = edited_df.to_json(orient="records").encode("utf-8")
                    st.download_button("Download JSON", json_data, file_name="edited_table.json")
        else:
            st.warning("⚠️ Extracted table is empty or invalid.")
    else:
        st.warning("⚠️ No tables found in the document. Please try another file.")

    st.header("🔄 Workflow View")
    image_path = "../Frontend/mockups.png"
    st.image(image_path, caption="Document Processing Workflow")