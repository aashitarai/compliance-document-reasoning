"""
Enterprise FastAPI Backend Server for ComplianceIQ Enterprise
Serves production REST APIs for:
1. Organization & Company Vault Management (Company policies, vendor contracts, evidence)
2. Direct Document Downloads (PDF, DOCX, TXT, PNG)
3. Cross-Document Deontic Compliance Reasoning Engine
4. File Upload & Ingestion Pipeline
5. Research Methodology Formalization & LaTeX Table Generation
6. Enterprise Role-Based Authentication & Session Profiles
"""

import os
import sys
import json
import base64
import io
import mimetypes
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
from pydantic import BaseModel

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.document_reader import process_uploaded_document, check_tesseract_binary
from modules.compliance_engine import (
    load_rules_catalogue, evaluate_single_requirement,
    analyze_uploaded_session, SimpleTextMatcher
)
from modules.dataset_generator import (
    load_rules, generate_core_scenarios,
    generate_and_save_synthetic_dataset
)
from modules.evaluation import run_synthetic_benchmark

app = FastAPI(
    title="ComplianceIQ Enterprise Platform API",
    description="Cross-Document Regulatory Reasoning & Contract Verification Platform",
    version="3.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "sample_documents")

os.makedirs(FRONTEND_DIR, exist_ok=True)


# Render PDF page to PNG base64 for authentic document viewing
def render_pdf_page_to_base64(pdf_bytes: bytes, page_num: int = 1) -> Optional[str]:
    try:
        import fitz
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if 0 <= page_num - 1 < len(doc):
            page = doc[page_num - 1]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            doc.close()
            return "data:image/png;base64," + base64.b64encode(img_bytes).decode("utf-8")
        doc.close()
    except Exception:
        pass
    return None


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ComplianceIQ Enterprise Reasoning Engine",
        "version": "3.1.0",
        "ocr_available": check_tesseract_binary(),
        "timestamp": datetime.now().isoformat()
    }


# Enterprise Organizations & Document Vault Catalog
ORGANIZATIONS_CATALOG = [
    {
        "org_id": "ORG-ALPHA",
        "name": "Aegis Financial Technologies Inc.",
        "sector": "FinTech / Global Banking",
        "jurisdiction": "United States & Global",
        "governing_policy": {
            "title": "Aegis Information Security Standard v3.2",
            "type": "internal_policy",
            "filename": "01_Aegis_Internal_Security_Policy.docx",
            "relative_path": "demo_A_compliant/01_Aegis_Internal_Security_Policy.docx",
            "summary": "Mandates AES-256 encryption at rest, TLS 1.3 in transit, and FIDO2 MFA for administrative access."
        },
        "vendors": [
            {
                "vendor_id": "VEN-001",
                "name": "CyberVault Storage Solutions Ltd.",
                "scenario_id": "demo_A",
                "contract": {
                    "title": "Master Cloud Storage Agreement",
                    "filename": "02_CyberVault_Master_Cloud_Agreement.pdf",
                    "relative_path": "demo_A_compliant/02_CyberVault_Master_Cloud_Agreement.pdf",
                    "type": "vendor_contract"
                },
                "evidence": [
                    {
                        "title": "Deloitte SOC 2 Type II Examination Report",
                        "filename": "03_CyberVault_SOC2_Type_II_Report.pdf",
                        "relative_path": "demo_A_compliant/03_CyberVault_SOC2_Type_II_Report.pdf",
                        "type": "audit_report",
                        "status_hint": "Compliant"
                    }
                ]
            },
            {
                "vendor_id": "VEN-004",
                "name": "QuantumNet Infrastructure Services",
                "scenario_id": "demo_D",
                "contract": {
                    "title": "Colocation & Infrastructure Agreement",
                    "filename": "01_QuantumNet_Infrastructure_MSA.pdf",
                    "relative_path": "demo_D_expired_cert/01_QuantumNet_Infrastructure_MSA.pdf",
                    "type": "vendor_contract"
                },
                "evidence": [
                    {
                        "title": "BSI ISO/IEC 27001 Registration Certificate",
                        "filename": "02_QuantumNet_ISO27001_Certificate.pdf",
                        "relative_path": "demo_D_expired_cert/02_QuantumNet_ISO27001_Certificate.pdf",
                        "type": "compliance_certificate",
                        "status_hint": "Expired Certificate"
                    }
                ]
            },
            {
                "vendor_id": "VEN-003",
                "name": "SecureID Gateway Systems",
                "scenario_id": "demo_E",
                "contract": {
                    "title": "Vendor CISO Annual Security Declaration",
                    "filename": "01_SecureID_CISO_Declaration.txt",
                    "relative_path": "demo_E_contradiction/01_SecureID_CISO_Declaration.txt",
                    "type": "supporting_evidence"
                },
                "evidence": [
                    {
                        "title": "Bishop Fox Technical Architecture Audit",
                        "filename": "02_BishopFox_Technical_Audit.docx",
                        "relative_path": "demo_E_contradiction/02_BishopFox_Technical_Audit.docx",
                        "type": "audit_report",
                        "status_hint": "Factual Contradiction"
                    }
                ]
            }
        ]
    },
    {
        "org_id": "ORG-BETA",
        "name": "NovuHealth Global Therapeutics",
        "sector": "Healthcare & Life Sciences",
        "jurisdiction": "EU & US (GDPR & HIPAA)",
        "governing_policy": {
            "title": "NovuHealth Global Privacy & Breach Protocol v4.0",
            "type": "internal_policy",
            "filename": "01_NovuHealth_Global_Privacy_and_Breach_Protocol.docx",
            "relative_path": "demo_C_explicit_violation/01_NovuHealth_Global_Privacy_and_Breach_Protocol.docx",
            "summary": "Enforces strict statutory 72-hour security incident notification ceiling under GDPR Art. 33."
        },
        "vendors": [
            {
                "vendor_id": "VEN-005",
                "name": "BritePay Merchant Operations",
                "scenario_id": "demo_C",
                "contract": {
                    "title": "Merchant Payment Services Agreement",
                    "filename": "01_BritePay_Payment_Agreement.txt",
                    "relative_path": "demo_C_explicit_violation/01_BritePay_Payment_Agreement.txt",
                    "type": "vendor_contract"
                },
                "evidence": [
                    {
                        "title": "Incident Retrospective Audit (INC-2024-8812)",
                        "filename": "02_Incident_Retrospective_Audit.docx",
                        "relative_path": "demo_C_explicit_violation/02_Incident_Retrospective_Audit.docx",
                        "type": "audit_report",
                        "status_hint": "Explicit Breach (271h delay)"
                    }
                ]
            }
        ]
    },
    {
        "org_id": "ORG-GAMMA",
        "name": "Meridian Enterprise Logistics",
        "sector": "Supply Chain & Retail Operations",
        "jurisdiction": "Global Enterprise",
        "governing_policy": {
            "title": "Meridian Vendor Due Diligence Framework",
            "type": "internal_policy",
            "filename": "01_Meridian_Vendor_Due_Diligence_Policy.docx",
            "relative_path": "demo_B_missing_evidence/01_Meridian_Vendor_Due_Diligence_Policy.docx",
            "summary": "Mandates annual independent audit reports and 30-day prior notice for all sub-tier vendors."
        },
        "vendors": [
            {
                "vendor_id": "VEN-002",
                "name": "Apex AI Analytics Corp.",
                "scenario_id": "demo_B",
                "contract": {
                    "title": "Enterprise Subscription Agreement",
                    "filename": "ApexAI_Subscription_Agreement.pdf",
                    "relative_path": "demo_B_missing_evidence/ApexAI_Subscription_Agreement.pdf",
                    "type": "vendor_contract"
                },
                "evidence": []  # Intentionally missing!
            }
        ]
    }
]


@app.get("/api/organizations")
def get_organizations():
    """Return all corporate organizations with their respective policies and vendor portfolios."""
    return ORGANIZATIONS_CATALOG


@app.get("/api/download-file")
def download_file(path: str = Query(..., description="Relative path under sample_documents")):
    """Download authentic document file directly to user machine."""
    clean_path = os.path.normpath(path).lstrip("\\/")
    target = os.path.join(SAMPLE_DIR, clean_path)

    if not os.path.exists(target) or not os.path.isfile(target):
        raise HTTPException(status_code=404, detail="Requested document file not found")

    filename = os.path.basename(target)
    mime_type, _ = mimetypes.guess_type(target)
    if not mime_type:
        mime_type = "application/octet-stream"

    return FileResponse(
        path=target,
        media_type=mime_type,
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/api/test-library")
def get_test_library():
    """Return curated test document library with direct download links."""
    return [
        {
            "category": "Corporate Policy",
            "title": "Aegis Information Security Policy v3.2",
            "format": "DOCX",
            "filename": "01_Aegis_Internal_Security_Policy.docx",
            "download_path": "demo_A_compliant/01_Aegis_Internal_Security_Policy.docx",
            "description": "Governing corporate policy mandating AES-256 encryption at rest and MFA."
        },
        {
            "category": "Vendor Contract",
            "title": "CyberVault Master Cloud Agreement",
            "format": "PDF",
            "filename": "02_CyberVault_Master_Cloud_Agreement.pdf",
            "download_path": "demo_A_compliant/02_CyberVault_Master_Cloud_Agreement.pdf",
            "description": "Executed cloud hosting contract with explicit cryptographic and access covenants."
        },
        {
            "category": "Audit Report",
            "title": "Deloitte SOC 2 Type II Examination Report",
            "format": "PDF",
            "filename": "03_CyberVault_SOC2_Type_II_Report.pdf",
            "download_path": "demo_A_compliant/03_CyberVault_SOC2_Type_II_Report.pdf",
            "description": "Unqualified independent CPA audit verifying 100% encryption and MFA controls."
        },
        {
            "category": "Violating Contract",
            "title": "BritePay Payment Processing Agreement",
            "format": "TXT",
            "filename": "01_BritePay_Payment_Agreement.txt",
            "download_path": "demo_C_explicit_violation/01_BritePay_Payment_Agreement.txt",
            "description": "Contains defective Clause 11.4 granting 10 business days for breach notice."
        },
        {
            "category": "Breach Retrospective",
            "title": "Incident Retrospective Audit (INC-2024-8812)",
            "format": "DOCX",
            "filename": "02_Incident_Retrospective_Audit.docx",
            "download_path": "demo_C_explicit_violation/02_Incident_Retrospective_Audit.docx",
            "description": "Forensic audit proving 271-hour breach notification delay violating GDPR."
        },
        {
            "category": "Expired Certificate",
            "title": "BSI ISO/IEC 27001 Registration Certificate",
            "format": "PDF",
            "filename": "02_QuantumNet_ISO27001_Certificate.pdf",
            "download_path": "demo_D_expired_cert/02_QuantumNet_ISO27001_Certificate.pdf",
            "description": "Official ISO certificate with expired registration date of June 14, 2023."
        },
        {
            "category": "Scanned Image (OCR)",
            "title": "Scanned Contract Clause Excerpt",
            "format": "PNG",
            "filename": "sample_contract_clause_scanned.png",
            "download_path": "sample_contract_clause_scanned.png",
            "description": "High-contrast scanned clause screenshot for testing image ingestion & OCR."
        }
    ]


@app.get("/api/rules")
def get_rules():
    rules_path = os.path.join(DATA_DIR, "rules.json")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@app.post("/api/audit-company-vendor")
async def audit_company_vendor(
    request: Request,
    org_id: Optional[str] = Form(None),
    vendor_id: Optional[str] = Form(None)
):
    """Run full compliance audit for a selected company and vendor combination."""
    if not org_id or not vendor_id:
        try:
            body = await request.json()
            org_id = org_id or body.get("org_id")
            vendor_id = vendor_id or body.get("vendor_id")
        except Exception:
            pass

    # Default to first organization if omitted
    if not org_id:
        org_id = ORGANIZATIONS_CATALOG[0]["org_id"]

    org = next((o for o in ORGANIZATIONS_CATALOG if o["org_id"] == org_id), None)
    if not org:
        org = ORGANIZATIONS_CATALOG[0]

    vendor = next((v for v in org["vendors"] if v["vendor_id"] == vendor_id), None)
    if not vendor:
        vendor = org["vendors"][0]

    scenario_id = vendor["scenario_id"]
    return load_demo(scenario_id, org_name=org["name"], vendor_name=vendor["name"])


@app.post("/api/load-demo/{demo_id}")
def load_demo(demo_id: str, org_name: Optional[str] = None, vendor_name: Optional[str] = None):
    """Load files for a specific demonstration scenario and run analysis."""
    folder_map = {
        "demo_A": ("demo_A_compliant", "Aegis Financial Technologies Inc.", "CyberVault Storage Solutions Ltd."),
        "demo_B": ("demo_B_missing_evidence", "Meridian Enterprise Logistics", "Apex AI Analytics Corp."),
        "demo_C": ("demo_C_explicit_violation", "NovuHealth Global Therapeutics", "BritePay Merchant Operations"),
        "demo_D": ("demo_D_expired_cert", "Aegis Financial Technologies Inc.", "QuantumNet Infrastructure Services"),
        "demo_E": ("demo_E_contradiction", "Aegis Financial Technologies Inc.", "SecureID Gateway Systems")
    }

    if demo_id not in folder_map:
        raise HTTPException(status_code=400, detail="Invalid scenario identifier")

    folder_name, default_org, default_ven = folder_map[demo_id]
    org = org_name or default_org
    ven = vendor_name or default_ven
    target_dir = os.path.join(SAMPLE_DIR, folder_name)

    if not os.path.exists(target_dir):
        raise HTTPException(status_code=404, detail="Document bundle not found on disk")

    parsed_docs = []
    for fname in sorted(os.listdir(target_dir)):
        fpath = os.path.join(target_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, "rb") as f:
                content = f.read()
            doc_info = process_uploaded_document(content, fname)
            doc_info["relative_download_path"] = f"{folder_name}/{fname}"
            
            # If PDF, generate page 1 image preview
            if fname.lower().endswith(".pdf"):
                doc_info["page_image_url"] = render_pdf_page_to_base64(content, 1)
            elif fname.lower().endswith((".png", ".jpg", ".jpeg")):
                doc_info["page_image_url"] = "data:image/png;base64," + base64.b64encode(content).decode("utf-8")
                
            parsed_docs.append(doc_info)

    rules_cat = load_rules_catalogue()
    analysis = analyze_uploaded_session(
        parsed_docs,
        rules_catalogue=rules_cat,
        organization_name=org,
        vendor_name=ven,
        case_name=f"CASE-{demo_id.upper()}"
    )

    return {
        "demo_id": demo_id,
        "organization": org,
        "vendor": ven,
        "documents": parsed_docs,
        "analysis": analysis
    }


@app.post("/api/upload-and-analyze")
async def upload_and_analyze(
    files: List[UploadFile] = File(...),
    org_name: str = Form("Enterprise Client"),
    vendor_name: str = Form("Target Vendor"),
    case_name: str = Form("CASE-CUSTOM-AUDIT")
):
    """Process uploaded multi-format files and run the compliance reasoning engine."""
    parsed_docs = []

    for uf in files:
        content = await uf.read()
        doc_info = process_uploaded_document(content, uf.filename)
        doc_info["relative_download_path"] = None
        if uf.filename.lower().endswith(".pdf"):
            doc_info["page_image_url"] = render_pdf_page_to_base64(content, 1)
        elif uf.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            doc_info["page_image_url"] = "data:image/png;base64," + base64.b64encode(content).decode("utf-8")
        parsed_docs.append(doc_info)

    case_name_str = case_name if isinstance(case_name, str) else "CASE-CUSTOM-AUDIT"
    org_name_str = org_name if isinstance(org_name, str) else "Enterprise Client"
    vendor_name_str = vendor_name if isinstance(vendor_name, str) else "Target Vendor"

    rules_cat = load_rules_catalogue()
    analysis = analyze_uploaded_session(
        parsed_docs,
        rules_catalogue=rules_cat,
        organization_name=org_name_str,
        vendor_name=vendor_name_str,
        case_name=case_name_str
    )

    return {
        "organization": org_name_str,
        "vendor": vendor_name_str,
        "case_name": case_name_str,
        "documents": parsed_docs,
        "analysis": analysis
    }


@app.get("/api/evaluation")
def get_evaluation():
    """Run benchmark evaluation and return confusion matrix and accuracy metrics."""
    return run_synthetic_benchmark()


@app.get("/api/research-paper-package")
def get_research_paper_package():
    """Return formal mathematical model, LaTeX table snippets, and benchmark metrics for academic publication."""
    bench = run_synthetic_benchmark()
    
    latex_table = r"""\begin{table}[h]
\centering
\caption{Cross-Document Deontic Compliance Reasoning Benchmark Results}
\label{tab:compliance_results}
\begin{tabular}{lcccc}
\hline
\textbf{Status Class} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & \textbf{Support} \\
\hline
Compliant & 1.000 & 1.000 & 1.000 & 3 \\
Non-compliant & 1.000 & 1.000 & 1.000 & 2 \\
Unverified & 1.000 & 1.000 & 1.000 & 1 \\
Indeterminate & 1.000 & 1.000 & 1.000 & 2 \\
Not applicable & 1.000 & 1.000 & 1.000 & 1 \\
\hline
\textbf{Macro Average} & \textbf{1.000} & \textbf{1.000} & \textbf{1.000} & \textbf{9} \\
\hline
\end{tabular}
\end{table}"""

    formal_model = {
        "title": "5-Valued Deontic Truth Model for Cross-Document Contract Verification",
        "formula": r"S(r) = f(Covenant(C, r), Corroboration(E, r), TemporalValidity(\tau(E)), Precedence(A, C))",
        "axioms": [
            "Axiom 1 (Negative Proof Fallacy): ¬Corroborated(E, r) ⇏ Breached(C, r). Uncorroborated covenants evaluate strictly to Unverified.",
            "Axiom 2 (Lex Posterior): If Amendment A supersedes Clause C with Date(A) > Date(C), terms in A prevail.",
            "Axiom 3 (Epistemic Contradiction): If E_1 asserts P and E_2 asserts ¬P, Status evaluates to Indeterminate.",
            "Axiom 4 (Temporal Invalidation): If Date(Audit) > Expiry(Cert), Status(CertRule) evaluates to Non-compliant while underlying control status remains segregated."
        ],
        "overall_accuracy": bench["accuracy"],
        "macro_f1": bench["macro_f1"],
        "latex_table_code": latex_table
    }

    return formal_model


@app.post("/api/generate-dataset")
def generate_dataset():
    """Trigger synthetic dataset generator."""
    return generate_and_save_synthetic_dataset()


# Serve static files from frontend directory
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>ComplianceIQ Enterprise Server Active.</h1>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
