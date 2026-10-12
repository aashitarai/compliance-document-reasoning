"""
Document Reader and Ingestion Module
Handles multi-format parsing for PDF, DOCX, TXT, and Images (with OCR support and graceful fallback).
Extracts document structure, clause markers, dates, and preliminary document types.
"""

import io
import re
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

# Optional PyMuPDF (fitz) or pypdf
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# python-docx
try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

# Pillow and pytesseract
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False


def check_tesseract_binary() -> bool:
    """Check if the tesseract OCR engine binary is accessible."""
    if not HAS_PYTESSERACT:
        return False
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        # Common Windows paths check
        default_win_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe")
        ]
        for p in default_win_paths:
            if os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
                try:
                    pytesseract.get_tesseract_version()
                    return True
                except Exception:
                    pass
        return False


def detect_document_type(text: str, filename: str) -> str:
    """
    Classify document type using structural signals, legal markers, and content headers.
    Returns one of:
      - 'regulation'
      - 'internal_policy'
      - 'vendor_contract'
      - 'contract_amendment'
      - 'audit_report'
      - 'compliance_certificate'
      - 'supporting_evidence'
      - 'unknown'
    """
    lower_name = filename.lower()
    lower_text = text.lower()[:3000]

    # Explicit filename cues
    if "amend" in lower_name or "addendum" in lower_name:
        return "contract_amendment"
    if "cert" in lower_name or "iso27001" in lower_name or "soc2_cert" in lower_name:
        return "compliance_certificate"
    if "policy" in lower_name or "vrm" in lower_name or "sop" in lower_name:
        return "internal_policy"
    if "audit" in lower_name or "soc2" in lower_name or "pentest" in lower_name:
        return "audit_report"
    if "contract" in lower_name or "msa" in lower_name or "agreement" in lower_name or "dpa" in lower_name:
        return "vendor_contract"
    if "rule" in lower_name or "regulation" in lower_name or "gdpr" in lower_name or "hipaa" in lower_name:
        return "regulation"

    # Content-based classification
    if any(k in lower_text for k in ["amendment no", "first amendment", "amends the agreement", "addendum to"]):
        return "contract_amendment"
    if any(k in lower_text for k in ["certificate of registration", "this is to certify that", "certificate no", "valid through", "expiration date:"]):
        return "compliance_certificate"
    if any(k in lower_text for k in ["report on controls", "independent service auditor", "system and organization controls", "penetration testing report", "vulnerability scan results"]):
        return "audit_report"
    if any(k in lower_text for k in ["master services agreement", "data processing addendum", "vendor agreement", "this agreement is entered into", "terms of service", "standard contractual clauses"]):
        return "vendor_contract"
    if any(k in lower_text for k in ["information security policy", "internal policy", "standard operating procedure", "employee handbook", "corporate governance policy"]):
        return "internal_policy"
    if any(k in lower_text for k in ["article ", "45 cfr", "statute", "directive (eu)", "regulatory authority", "pursuant to regulation"]):
        return "regulation"

    return "supporting_evidence"


def extract_dates(text: str) -> List[str]:
    """Find ISO and natural language dates in document text."""
    date_patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",                                           # 2024-05-18
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b", # May 18, 2024
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",   # 18 May 2024
        r"\b\d{1,2}/\d{1,2}/\d{4}\b"                                        # 05/18/2024
    ]
    found = []
    for pat in date_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            d_str = m.group(0)
            if d_str not in found:
                found.append(d_str)
    return found


def extract_clauses_and_sections(text: str) -> List[Dict[str, Any]]:
    """Detect numbered clauses or headings for granular traceability."""
    lines = text.split("\n")
    clauses = []
    clause_pat = re.compile(r"^(?:Section|Clause|Article|Schedule)?\s*(\d+(?:\.\d+)*)\.?\s+(.+)$", re.IGNORECASE)

    current_title = "Preamble / General Terms"
    current_lines = []

    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        match = clause_pat.match(cleaned)
        if match and len(cleaned) < 120:
            if current_lines:
                clauses.append({
                    "clause_identifier": current_title,
                    "content": "\n".join(current_lines).strip()
                })
                current_lines = []
            current_title = f"{match.group(1)} {match.group(2)}"
        else:
            current_lines.append(cleaned)

    if current_lines:
        clauses.append({
            "clause_identifier": current_title,
            "content": "\n".join(current_lines).strip()
        })

    return clauses


def read_pdf(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Extract text page-by-page from digital or scanned PDF files."""
    pages_text = []
    warnings = []
    ocr_applied = False
    tesseract_available = check_tesseract_binary()

    if HAS_PYMUPDF:
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text").strip()

                # If digital text is missing/scanty, attempt OCR if tesseract is configured
                if len(text) < 30:
                    if tesseract_available and HAS_PIL:
                        try:
                            pix = page.get_pixmap(dpi=200)
                            img = Image.open(io.BytesIO(pix.tobytes("png")))
                            ocr_text = pytesseract.image_to_string(img).strip()
                            if len(ocr_text) > len(text):
                                text = ocr_text
                                ocr_applied = True
                        except Exception as e:
                            warnings.append(f"Page {page_num + 1}: OCR attempted but failed: {str(e)}")
                    else:
                        warnings.append(f"Page {page_num + 1}: Low text density ({len(text)} chars). OCR engine not installed or unavailable.")

                pages_text.append({"page": page_num + 1, "text": text})
            doc.close()
        except Exception as e:
            return {
                "success": False,
                "error": f"PyMuPDF could not read '{filename}': {str(e)}",
                "filename": filename
            }
    elif HAS_PYPDF:
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page_num, page in enumerate(reader.pages):
                text = (page.extract_text() or "").strip()
                if len(text) < 30:
                    warnings.append(f"Page {page_num + 1}: Scanned or image-only page detected. Install Tesseract OCR to extract image text.")
                pages_text.append({"page": page_num + 1, "text": text})
        except Exception as e:
            return {
                "success": False,
                "error": f"pypdf failed to read '{filename}': {str(e)}",
                "filename": filename
            }
    else:
        return {
            "success": False,
            "error": "No PDF library available. Please install PyMuPDF or pypdf.",
            "filename": filename
        }

    full_text = "\n\n".join([f"--- Page {p['page']} ---\n{p['text']}" for p in pages_text])
    doc_type = detect_document_type(full_text, filename)
    clauses = extract_clauses_and_sections(full_text)
    dates = extract_dates(full_text)

    return {
        "success": True,
        "filename": filename,
        "document_type": doc_type,
        "page_count": len(pages_text),
        "pages": pages_text,
        "full_text": full_text,
        "clauses": clauses,
        "dates_found": dates,
        "warnings": warnings,
        "ocr_applied": ocr_applied,
        "char_count": len(full_text)
    }


def read_docx(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Extract paragraphs, headings, and table cells from DOCX files."""
    if not HAS_DOCX:
        return {
            "success": False,
            "error": "python-docx is not installed.",
            "filename": filename
        }

    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = []
        for p in doc.paragraphs:
            if p.text.strip():
                paragraphs.append(p.text.strip())

        # Also extract table text
        table_lines = []
        for t_idx, table in enumerate(doc.tables):
            table_lines.append(f"\n[Table {t_idx + 1}]")
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    table_lines.append(" | ".join(row_cells))

        full_text = "\n\n".join(paragraphs)
        if table_lines:
            full_text += "\n\n" + "\n".join(table_lines)

        doc_type = detect_document_type(full_text, filename)
        clauses = extract_clauses_and_sections(full_text)
        dates = extract_dates(full_text)

        return {
            "success": True,
            "filename": filename,
            "document_type": doc_type,
            "page_count": max(1, len(paragraphs) // 15),
            "pages": [{"page": 1, "text": full_text}],
            "full_text": full_text,
            "clauses": clauses,
            "dates_found": dates,
            "warnings": [],
            "ocr_applied": False,
            "char_count": len(full_text)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed reading DOCX '{filename}': {str(e)}",
            "filename": filename
        }


def read_txt(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Decode raw text file using UTF-8, latin-1, or cp1252."""
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    text = ""
    used_enc = None

    for enc in encodings:
        try:
            text = file_bytes.decode(enc)
            used_enc = enc
            break
        except UnicodeDecodeError:
            continue

    if not text and file_bytes:
        return {
            "success": False,
            "error": f"Could not decode text file '{filename}' with standard encodings.",
            "filename": filename
        }

    doc_type = detect_document_type(text, filename)
    clauses = extract_clauses_and_sections(text)
    dates = extract_dates(text)

    return {
        "success": True,
        "filename": filename,
        "document_type": doc_type,
        "page_count": 1,
        "pages": [{"page": 1, "text": text}],
        "full_text": text,
        "clauses": clauses,
        "dates_found": dates,
        "warnings": [] if used_enc == "utf-8" else [f"Decoded using fallback encoding '{used_enc}'"],
        "ocr_applied": False,
        "char_count": len(text)
    }


def read_image(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Perform OCR extraction on PNG, JPG, or JPEG images."""
    if not HAS_PIL:
        return {
            "success": False,
            "error": "Pillow (PIL) is not installed for image processing.",
            "filename": filename
        }

    try:
        img = Image.open(io.BytesIO(file_bytes))
        width, height = img.size
    except Exception as e:
        return {
            "success": False,
            "error": f"Invalid image file '{filename}': {str(e)}",
            "filename": filename
        }

    tesseract_available = check_tesseract_binary()
    warnings = []
    text = ""

    if not tesseract_available:
        warnings.append("Tesseract OCR is not installed on this system. Image loaded, but text could not be extracted automatically. Please install Tesseract-OCR or upload a text-based document (PDF, DOCX, TXT).")
    else:
        try:
            text = pytesseract.image_to_string(img).strip()
            if not text:
                warnings.append("OCR completed, but no legible text was recognized from the image (check resolution and contrast).")
        except Exception as e:
            warnings.append(f"Tesseract OCR execution error: {str(e)}")

    doc_type = detect_document_type(text, filename) if text else "supporting_evidence"
    clauses = extract_clauses_and_sections(text) if text else []
    dates = extract_dates(text) if text else []

    return {
        "success": True,
        "filename": filename,
        "document_type": doc_type,
        "page_count": 1,
        "pages": [{"page": 1, "text": text}],
        "full_text": text,
        "clauses": clauses,
        "dates_found": dates,
        "warnings": warnings,
        "ocr_applied": tesseract_available,
        "char_count": len(text),
        "dimensions": f"{width}x{height}"
    }


def process_uploaded_document(arg1: Any, arg2: Any) -> Dict[str, Any]:
    """
    Unified entrypoint dispatching by file extension.
    Accepts either (file_bytes, filename) or (filename, file_bytes).
    """
    if isinstance(arg1, (bytes, bytearray)) and isinstance(arg2, str):
        file_bytes = bytes(arg1)
        filename = arg2
    elif isinstance(arg1, str) and isinstance(arg2, (bytes, bytearray)):
        filename = arg1
        file_bytes = bytes(arg2)
    elif isinstance(arg1, str) and hasattr(arg2, "read"):
        filename = arg1
        file_bytes = arg2.read()
    elif hasattr(arg1, "read") and isinstance(arg2, str):
        file_bytes = arg1.read()
        filename = arg2
    else:
        # Fallback cast
        file_bytes = bytes(arg1) if isinstance(arg1, (bytes, bytearray)) else str(arg1).encode('utf-8', errors='ignore')
        filename = str(arg2)

    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return read_pdf(file_bytes, filename)
    elif ext == ".docx":
        return read_docx(file_bytes, filename)
    elif ext in [".txt", ".json", ".csv", ".md"]:
        return read_txt(file_bytes, filename)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return read_image(file_bytes, filename)
    else:
        return {
            "success": False,
            "error": f"Unsupported file extension '{ext}'. Supported formats: PDF, DOCX, TXT, PNG, JPG, JPEG.",
            "filename": filename
        }
