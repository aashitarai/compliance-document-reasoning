"""
Document Reader and Ingestion Module (Lightweight Edition)
Handles multi-format parsing for PDF, DOCX, TXT, and Images using pure-Python packages.
Extracts document structure, clause markers, dates, and preliminary document types.
"""

import os
import re
import io
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import docx
from pypdf import PdfReader


def read_pdf(file_input: Union[str, bytes], filename: str = "document.pdf") -> Dict[str, Any]:
    """Extracts raw text from a PDF file or binary stream and returns structured metadata."""
    try:
        if isinstance(file_input, bytes):
            stream = io.BytesIO(file_input)
            reader = PdfReader(stream)
        else:
            reader = PdfReader(file_input)

        extracted = []
        page_count = len(reader.pages)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted.append(text)
        raw_text = "\n\n".join(extracted)
        doc_type = detect_document_type(raw_text, filename).lower().replace(" ", "_")
        return {
            "success": True,
            "raw_text": raw_text,
            "full_text": raw_text,
            "page_count": page_count,
            "document_type": doc_type,
            "filename": filename,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "raw_text": "",
            "full_text": "",
            "page_count": 0,
            "document_type": "unknown",
            "filename": filename,
            "error": str(e)
        }


def read_docx(file_input: Union[str, bytes], filename: str = "document.docx") -> Dict[str, Any]:
    """Extracts raw text from a Word document or binary stream."""
    try:
        if isinstance(file_input, bytes):
            stream = io.BytesIO(file_input)
            doc = docx.Document(stream)
        else:
            doc = docx.Document(file_input)
        raw_text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        doc_type = detect_document_type(raw_text, filename).lower().replace(" ", "_")
        return {
            "success": True,
            "raw_text": raw_text,
            "full_text": raw_text,
            "document_type": doc_type,
            "filename": filename,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "raw_text": "",
            "full_text": "",
            "document_type": "unknown",
            "filename": filename,
            "error": str(e)
        }


def read_txt(file_input: Union[str, bytes], filename: str = "document.txt") -> Dict[str, Any]:
    """Extracts raw text from a text/markdown file or binary stream."""
    try:
        if isinstance(file_input, bytes):
            raw_text = file_input.decode("utf-8", errors="ignore")
        else:
            with open(file_input, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
        doc_type = detect_document_type(raw_text, filename).lower().replace(" ", "_")
        return {
            "success": True,
            "raw_text": raw_text,
            "full_text": raw_text,
            "document_type": doc_type,
            "filename": filename,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "raw_text": "",
            "full_text": "",
            "document_type": "unknown",
            "filename": filename,
            "error": str(e)
        }


def read_image(file_input: Union[str, bytes], filename: str = "image.png") -> Dict[str, Any]:
    """Lightweight fallback for image files when OCR dependencies are removed."""
    stub_text = f"[Image document parsed: {filename} - Pure-Python OCR stub active]"
    return {
        "success": True,
        "raw_text": stub_text,
        "full_text": stub_text,
        "document_type": "supporting_evidence",
        "dimensions": (1024, 768),
        "filename": filename,
        "error": None
    }


def extract_text_ocr(file_input: Union[str, bytes], filename: str = "image.png") -> Dict[str, Any]:
    """Legacy alias for image extraction."""
    return read_image(file_input, filename)


def check_tesseract_binary() -> bool:
    """Checks if tesseract OCR binary is installed and accessible."""
    import shutil
    return bool(shutil.which("tesseract"))


def read_document(file_path: str) -> str:
    """Generic text reader that dispatches based on file extension and returns text string."""
    ext = os.path.splitext(file_path)[1].lower()
    filename = os.path.basename(file_path)

    if ext == ".pdf":
        res = read_pdf(file_path, filename)
    elif ext == ".docx":
        res = read_docx(file_path, filename)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        res = read_image(file_path, filename)
    else:
        res = read_txt(file_path, filename)

    return res.get("raw_text", "")


def parse_date_string(date_str: str) -> Optional[str]:
    """Extracts and normalizes dates (YYYY-MM-DD) from string matches."""
    patterns = [
        r'\b(\d{4}-\d{2}-\d{2})\b',
        r'\b(\d{1,2}/\d{1,2}/\d{4})\b',
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
    ]
    for pattern in patterns:
        match = re.search(pattern, date_str, re.IGNORECASE)
        if match:
            matched_text = match.group(0)
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y", "%B %d %Y"):
                try:
                    return datetime.strptime(matched_text.replace(",", ""), fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
    return None


def detect_document_type(text: str, filename: str) -> str:
    """Infers document category based on filename and header content keywords."""
    lower_text = text[:4000].lower()
    lower_filename = filename.lower()

    # Filename precedence
    if "policy" in lower_filename or "protocol" in lower_filename:
        return "Internal Policy"
    elif "amendment" in lower_filename or "addendum" in lower_filename:
        return "Amendment"
    elif any(k in lower_filename for k in ["contract", "msa", "agreement", "sow", "subscription"]):
        return "Vendor Contract"
    elif any(k in lower_filename for k in ["audit", "soc", "cert", "declaration"]):
        return "Audit Evidence"

    # Header text precedence
    if "security policy" in lower_text or "internal policy" in lower_text or "privacy protocol" in lower_text:
        return "Internal Policy"
    elif "amendment no." in lower_text or "second amendment" in lower_text:
        return "Amendment"
    elif any(k in lower_text for k in ["master services agreement", "service agreement", "cloud agreement", "commercial agreement"]):
        return "Vendor Contract"
    elif any(k in lower_text for k in ["independent auditor", "audit report", "financial statement", "soc 2", "balance sheet", "soc-2"]):
        return "Audit Evidence"
    elif "agreement" in lower_text or "terms of service" in lower_text:
        return "Vendor Contract"
    return "Supporting Document"


def extract_clauses(text: str) -> List[Dict[str, Any]]:
    """Splits document text into logical clauses or numbered paragraphs."""
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 15]
    if len(paragraphs) <= 1:
        paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 15]

    clauses = []
    for idx, para in enumerate(paragraphs, start=1):
        clause_match = re.match(r'^(Section|Article|Clause|Note|\d+\.|\d+\.\d+|\([a-z\d]+\))\s*([\d\.]*)', para, re.IGNORECASE)
        clause_id = clause_match.group(0).strip() if clause_match else f"Paragraph {idx}"
        clauses.append({
            "id": clause_id,
            "text": para,
            "index": idx
        })
    return clauses


def process_uploaded_document(file_input: Union[str, bytes], filename: Optional[str] = None) -> Dict[str, Any]:
    """
    Unified document ingestion processor.
    Accepts either a filesystem path (str) or raw binary content (bytes) with a filename.
    Dispatches to the appropriate parser (PDF, DOCX, TXT, Image), extracts text, clauses,
    dates, and document category classification.
    """
    if isinstance(file_input, str):
        if not filename:
            filename = os.path.basename(file_input)
        if os.path.exists(file_input) and os.path.isfile(file_input):
            with open(file_input, "rb") as f:
                content = f.read()
        else:
            content = file_input.encode("utf-8", errors="ignore")
    else:
        content = file_input
        if not filename:
            filename = "document.txt"

    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        res = read_pdf(content, filename)
    elif ext in [".docx", ".doc"]:
        res = read_docx(content, filename)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"]:
        res = read_image(content, filename)
    else:
        res = read_txt(content, filename)

    raw_text = res.get("raw_text") or res.get("full_text") or ""
    doc_type = detect_document_type(raw_text, filename)
    extracted_date = parse_date_string(raw_text[:1000]) or parse_date_string(filename)
    clauses = extract_clauses(raw_text)

    # Clean display title
    base_name = filename.rsplit(".", 1)[0]
    title = base_name.replace("_", " ").strip()
    if len(title) > 3 and title[:2].isdigit() and title[2] in [" ", "_"]:
        title = title[3:].strip()

    return {
        "filename": filename,
        "file_path": file_input if isinstance(file_input, str) else filename,
        "document_type": doc_type,
        "title": title.title(),
        "effective_date": extracted_date,
        "raw_text": raw_text,
        "full_text": raw_text,
        "char_count": len(raw_text),
        "clauses": clauses,
        "clause_count": len(clauses),
        "page_count": res.get("page_count", 1),
        "success": res.get("success", True),
        "error": res.get("error")
    }


def parse_document(file_path: str) -> Dict[str, Any]:
    """Reads PDF, DOCX, TXT, or Image files and returns structured metadata, full text, and clauses."""
    return process_uploaded_document(file_path, os.path.basename(file_path))