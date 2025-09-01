"""Test period extraction with realistic sample."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.services.extractor import extract_text_from_docx
from ui.streamlit_app import extract_document_info

# Test with realistic sample
with open("sample_docs/realistic_sample.docx", "rb") as f:
    file_bytes = f.read()

text = extract_text_from_docx(file_bytes)
print("Extracted text:")
print(text)
print("\n" + "="*50 + "\n")

doc_info = extract_document_info(text)
print("Document info:")
for key, value in doc_info.items():
    print(f"{key}: {value}")