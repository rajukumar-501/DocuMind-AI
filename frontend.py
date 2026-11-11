import os

import requests
import streamlit as st

st.set_page_config(page_title="DocuMind AI", page_icon="📚", layout="centered")
st.title("📚 DocuMind AI")
st.caption("Upload a PDF and ask questions grounded in its content.")

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
TIMEOUT = 120

with st.sidebar:
    st.subheader("Uploaded documents")
    if st.button("Refresh document list"):
        try:
            response = requests.get(f"{API_URL}/upload/metadata/", timeout=15)
            response.raise_for_status()
            documents = response.json()
            if not documents:
                st.info("No documents uploaded yet.")
            for doc in documents:
                st.markdown(f"**{doc['filename']}**")
                st.caption(f"ID: {doc['document_id']} · {doc['num_chunks']} chunks")
        except requests.RequestException:
            st.error("Could not connect to the API. Check that the backend is running.")

st.header("1. Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF (maximum 10 MB)", type=["pdf"])

if uploaded_file and st.button("Upload and index", type="primary"):
    with st.spinner("Extracting text and creating the search index..."):
        try:
            response = requests.post(
                f"{API_URL}/upload/",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            st.session_state["document_id"] = data["document_id"]
            st.success("PDF indexed successfully.")
            st.code(data["document_id"], language=None)
            st.caption(f"{data['chunk_count']} text chunks indexed.")
        except requests.RequestException as exc:
            detail = getattr(getattr(exc, "response", None), "text", str(exc))
            st.error(f"Upload failed: {detail}")

st.header("2. Ask a question")
document_id = st.text_input(
    "Document ID",
    value=st.session_state.get("document_id", ""),
)
question = st.text_area("What would you like to know?")

if st.button("Get answer", type="primary", disabled=not (document_id.strip() and question.strip())):
    with st.spinner("Searching the document and generating an answer..."):
        try:
            response = requests.post(
                f"{API_URL}/query/",
                json={"document_id": document_id.strip(), "question": question.strip()},
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            st.markdown("### Answer")
            st.write(response.json().get("answer", "No answer returned."))
        except requests.RequestException as exc:
            detail = getattr(getattr(exc, "response", None), "text", str(exc))
            st.error(f"Query failed: {detail}")
