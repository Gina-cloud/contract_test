"""Text extraction from DOCX and PDF files."""
import io
from typing import Tuple
import fitz  # PyMuPDF
from docx import Document


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX file."""
    doc = Document(io.BytesIO(file_bytes))
    text_parts = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text.strip())
    return "\n".join(text_parts)


def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, bool]:
    """Extract text from PDF file. Returns (text, is_scanned)."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts = []
    total_chars = 0
    
    for page in doc:
        page_text = page.get_text()
        text_parts.append(page_text)
        total_chars += len(page_text.strip())
    
    doc.close()
    
    # 스캔 PDF 감지: 페이지당 평균 문자 수가 매우 적으면 스캔으로 판단
    is_scanned = total_chars < len(text_parts) * 50
    
    return "\n".join(text_parts), is_scanned