"""
Sample Documents Generator
Generates sample PDF, DOCX, TXT, and Image files for the 5 demonstration scenarios:
- Demo A: Fully Compliant (PDF contract, DOCX policy, PDF audit report)
- Demo B: Missing Evidence (PDF contract without audit evidence)
- Demo C: Explicit Violation (DOCX breach report & TXT contract)
- Demo D: Expired Certificate (PDF expired ISO 27001 certificate)
- Demo E: Conflicting Evidence (PDF CISO declaration vs DOCX audit finding)
"""

import os
import io
import fitz # pymupdf
import docx
from PIL import Image, ImageDraw, ImageFont

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_documents")


def create_pdf_document(filepath: str, title: str, paragraphs: list):
    """Generate a clean multi-page or single-page PDF using PyMuPDF."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842) # A4
    
    # Title
    page.insert_text((50, 60), title, fontsize=16, fontname="helv", color=(0.1, 0.2, 0.4))
    page.draw_line((50, 75), (545, 75), color=(0.7, 0.7, 0.7), width=1)
    
    y = 100
    for p in paragraphs:
        if y > 780:
            page = doc.new_page(width=595, height=842)
            y = 60
        
        # Check if heading
        if p.startswith("SECTION") or p.startswith("CLAUSE") or p.startswith("Control") or p.startswith("FINDING"):
            page.insert_text((50, y), p, fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 24
        else:
            # Wrap text roughly
            rect = fitz.Rect(50, y, 545, y + 100)
            rc = page.insert_textbox(rect, p, fontsize=10, fontname="helv", color=(0.25, 0.25, 0.25))
            y += abs(rc) + 18
            
    doc.save(filepath)
    doc.close()


def create_docx_document(filepath: str, title: str, sections: list):
    """Generate a formatted DOCX document using python-docx."""
    doc = docx.Document()
    doc.add_heading(title, level=0)
    
    for s_title, s_text in sections:
        if s_title:
            doc.add_heading(s_title, level=1)
        doc.add_paragraph(s_text)
        
    doc.save(filepath)


def create_txt_document(filepath: str, text: str):
    """Generate plain text document."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)


def create_sample_clause_image(filepath: str, title: str, clause_text: str):
    """Generate an image containing legal clause text for OCR demonstration."""
    img = Image.new("RGB", (900, 350), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Header border
    draw.rectangle([(20, 20), (880, 330)], outline=(180, 180, 180), width=2)
    draw.text((40, 40), title, fill=(20, 40, 80))
    draw.line([(40, 65), (860, 65)], fill=(200, 200, 200), width=1)
    
    # Paragraph text
    y = 85
    lines = [
        clause_text[:75],
        clause_text[75:150],
        clause_text[150:225],
        clause_text[225:300]
    ]
    for line in lines:
        if line.strip():
            draw.text((40, y), line.strip(), fill=(40, 40, 40))
            y += 25
            
    img.save(filepath)


def build_all_demo_files():
    """Build all sample files into sample_documents subdirectories."""
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    # Demo A: Compliant
    dir_a = os.path.join(SAMPLE_DIR, "demo_A_compliant")
    os.makedirs(dir_a, exist_ok=True)
    
    create_docx_document(
        os.path.join(dir_a, "01_Aegis_Internal_Security_Policy.docx"),
        "Aegis Financial Technologies — Internal Security Policy v3.2",
        [
            ("SECTION 4: THIRD-PARTY DATA SAFEGUARDS", 
             "4.1 Cryptographic Controls: All tier-1 cloud storage vendors must enforce hardware-accelerated AES-256 encryption for all data at rest and TLS 1.3 for all ingress/egress endpoints.\n4.2 Administrative Access: Phishing-resistant multi-factor authentication (MFA) is strictly mandatory for 100% of vendor administrative consoles.")
        ]
    )
    
    create_pdf_document(
        os.path.join(dir_a, "02_CyberVault_Master_Cloud_Agreement.pdf"),
        "Master Cloud Services Agreement — CyberVault Ltd.",
        [
            "BETWEEN: Aegis Financial Technologies Inc. ('Customer') AND CyberVault Storage Solutions Ltd. ('Vendor')",
            "EFFECTIVE DATE: March 15, 2023",
            "CLAUSE 8. CONFIDENTIALITY AND SECURITY COVENANTS",
            "8.1 Encryption at Rest and in Transit: Vendor covenants and warrants that Customer Data stored on CyberVault cloud volumes is continuously encrypted at rest using AES-256 bit encryption keys managed under FIPS 140-2 Level 3 HSM modules. All web interfaces and API endpoints mandate TLS 1.3 encryption.",
            "8.2 Identity and Access Management: Vendor mandates Multi-Factor Authentication (MFA) utilizing FIDO2 security keys for all operational engineers and database administrators accessing production clusters.",
            "8.3 Annual Audit Deliverable: Vendor covenants to supply Customer with an annual SOC 2 Type II report within forty-five (45) days of the conclusion of each examination cycle."
        ]
    )
    
    create_pdf_document(
        os.path.join(dir_a, "03_CyberVault_SOC2_Type_II_Report.pdf"),
        "Deloitte Independent Auditor Report (SOC 2 Type II)",
        [
            "SERVICE ORGANIZATION: CyberVault Storage Solutions Ltd.",
            "AUDIT PERIOD: October 1, 2023 to March 31, 2024",
            "OPINION: Unqualified Clean Opinion",
            "Control CC6.6 (Encryption at Rest and Transit):",
            "Testing Performed: Auditor inspected AWS KMS key policies and TLS configurations. Sampled 50 production storage volumes; 100% verified encrypted at rest with AES-256. Sampled 30 API gateway endpoints; 100% enforced TLS 1.2 or TLS 1.3 with high-strength cipher suites. No deviations noted.",
            "Control CC6.1 (Logical Access and Authentication):",
            "Testing Performed: Sampled 45 administrative staff accounts across DevOps. 100% of sampled administrative accounts enforced mandatory hardware-based MFA (FIDO2). No deviations noted."
        ]
    )

    # Demo B: Missing Evidence
    dir_b = os.path.join(SAMPLE_DIR, "demo_B_missing_evidence")
    os.makedirs(dir_b, exist_ok=True)
    
    create_pdf_document(
        os.path.join(dir_b, "ApexAI_Subscription_Agreement.pdf"),
        "Apex AI Analytics — Enterprise Subscription Agreement",
        [
            "CLAUSE 14. SUB-PROCESSORS AND THIRD-PARTY SUBCONTRACTORS",
            "14.1 Authorization and Registry: Vendor covenants that it maintains an audited list of approved sub-processors. Vendor shall provide Customer with thirty (30) days prior written notice before onboarding any new sub-processor.",
            "14.2 Pass-Through Auditing: Vendor shall conduct annual security reviews of all sub-processors possessing access to Customer data and make copies of sub-processor security attestations available to Customer upon request.",
            "(NOTE FOR REVIEWER: Notice that this case upload contains NO sub-processor registry or third-party audit reports. Expected compliance status: UNVERIFIED.)"
        ]
    )

    # Demo C: Explicit Violation
    dir_c = os.path.join(SAMPLE_DIR, "demo_C_explicit_violation")
    os.makedirs(dir_c, exist_ok=True)
    
    create_txt_document(
        os.path.join(dir_c, "01_BritePay_Payment_Agreement.txt"),
        """MERCHANT PAYMENT SERVICES AGREEMENT
BETWEEN: NovuHealth Therapeutics ('Customer') AND BritePay Merchant Operations ('Processor')
SECTION 11. SECURITY INCIDENTS AND BREACH NOTIFICATION
11.4 Notification Period: In the event Processor confirms a verified security incident affecting Customer cardholder data or credentials, Processor shall exercise commercially reasonable efforts to notify Customer within ten (10) business days following completion of internal forensic investigation. In no event shall notice be required earlier than seven (7) business days from incident confirmation."""
    )
    
    create_docx_document(
        os.path.join(dir_c, "02_Incident_Retrospective_Audit.docx"),
        "Incident Retrospective Audit — BritePay Incident INC-2024-8812",
        [
            ("FINDING SUMMARY",
             "Breach Detection Date: January 12, 2024 (08:30 UTC)\nCustomer Notification Sent: January 23, 2024 (16:15 UTC)\nTotal Elapsed Time: 271 hours (11 calendar days / 8 business days)\nRoot Cause: Vendor followed Section 11.4 internal forensic completion clause rather than statutory 72-hour notification.\nCompliance Finding: Explicit breach of statutory 72-hour ceiling.")
        ]
    )

    # Demo D: Expired Certificate
    dir_d = os.path.join(SAMPLE_DIR, "demo_D_expired_cert")
    os.makedirs(dir_d, exist_ok=True)
    
    create_pdf_document(
        os.path.join(dir_d, "01_QuantumNet_Infrastructure_MSA.pdf"),
        "QuantumNet Infrastructure Services — MSA",
        [
            "SECTION 9. MANDATORY CERTIFICATIONS",
            "9.1 Continuous ISO 27001 Maintenance: QuantumNet covenants that all tier-IV datacenter facilities shall maintain an active, unexpired ISO/IEC 27001 certification throughout the entire contract duration. Failure to renew certification prior to expiration constitutes a material compliance default."
        ]
    )
    
    create_pdf_document(
        os.path.join(dir_d, "02_QuantumNet_ISO27001_Certificate.pdf"),
        "BSI Certificate of Registration — ISO/IEC 27001:2013",
        [
            "ORGANIZATION: QuantumNet Infrastructure Services, Frankfurt Datacenter",
            "Certificate No: IS-99412",
            "Original Cycle Start Date: 15 June 2020",
            "Expiry Date: 14 June 2023",
            "Status: EXPIRED. (No surveillance extension letter or 2024 renewal certificate available)."
        ]
    )

    # Demo E: Contradictory Evidence
    dir_e = os.path.join(SAMPLE_DIR, "demo_E_contradiction")
    os.makedirs(dir_e, exist_ok=True)
    
    create_txt_document(
        os.path.join(dir_e, "01_SecureID_CISO_Declaration.txt"),
        """SECUREID CISO ANNUAL SECURITY DECLARATION
I, Marcus Vance, Chief Information Security Officer of SecureID Systems, hereby certify that:
1. All system event logs, authentication logs, and privileged administrative sessions are archived to immutable AWS S3 Glacier storage.
2. Log retention policies strictly enforce 365-day minimum preservation prior to automated purging."""
    )
    
    create_docx_document(
        os.path.join(dir_e, "02_BishopFox_Technical_Audit.docx"),
        "Bishop Fox Technical Architecture Evaluation — SecureID",
        [
            ("FINDING ID: SEC-LOG-04 (Lifecycle Configuration Mismatch)",
             "The assessment team inspected live AWS CloudWatch and S3 bucket lifecycle configurations:\n- S3 bucket 'secureid-prod-auth-logs' has active lifecycle transition rule 'DeleteMarkerAfterDays: 90'.\n- Logs from 2023 are purged automatically on day 91.\n- Contradiction Note: This directly contradicts the vendor's declared 365-day retention policy and CISO annual declaration.")
        ]
    )

    # Demo F: Sample Clause Image (OCR)
    create_sample_clause_image(
        os.path.join(SAMPLE_DIR, "sample_contract_clause_scanned.png"),
        "EXCERPT: CONFIDENTIALITY AND DATA ENCRYPTION",
        "The Vendor shall encrypt all Customer personal data at rest using AES-256 and in transit using TLS 1.3 protocol standards."
    )

    print("All demo files created in:", SAMPLE_DIR)


if __name__ == "__main__":
    build_all_demo_files()
