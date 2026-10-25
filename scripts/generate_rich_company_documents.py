"""
Generate authentic, detailed, multi-section corporate policies and vendor contracts
for NovuHealth, Meridian, QuantumNet, SecureID, and Aegis.
Replaces short or placeholder files with realistic multi-clause legal artifacts.
"""

import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "sample_documents")


def style_document(doc, title_text, org_name, ref_code):
    # Set standard margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Document Header
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_meta = p_meta.add_run(f"CONFIDENTIAL & PROPRIETARY • {ref_code}\nISSUING ENTITY: {org_name.upper()}")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(8.5)
    r_meta.font.color.rgb = RGBColor(100, 116, 139)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(title_text)
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("_______________________________________________________________________________")
    r_div.font.color.rgb = RGBColor(203, 213, 225)


def add_clause(doc, num_str, title_str, body_str):
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(12)
    p_h.paragraph_format.space_after = Pt(4)
    r_h = p_h.add_run(f"{num_str} {title_str.upper()}")
    r_h.font.name = "Calibri"
    r_h.font.size = Pt(11)
    r_h.font.bold = True
    r_h.font.color.rgb = RGBColor(30, 41, 59)

    p_b = doc.add_paragraph()
    p_b.paragraph_format.space_after = Pt(8)
    p_b.paragraph_format.line_spacing = 1.15
    r_b = p_b.add_run(body_str)
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(10)
    r_b.font.color.rgb = RGBColor(51, 65, 85)


# =============================================================================
# 1. NOVUHEALTH GOVERNING POLICY (.docx)
# =============================================================================
def generate_novuhealth_policy():
    target_dir = os.path.join(SAMPLE_DIR, "demo_C_explicit_violation")
    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, "01_NovuHealth_Global_Privacy_and_Breach_Protocol.docx")

    doc = docx.Document()
    style_document(doc, "GLOBAL PRIVACY, CLINICAL DATA PROTECTION & BREACH ESCALATION PROTOCOL",
                   "NovuHealth Global Therapeutics Inc.", "DOC-NH-POL-2024-V4")

    clauses = [
        ("SECTION 1.", "PURPOSE AND STATUTORY SCOPE",
         "NovuHealth Global Therapeutics Inc. ('NovuHealth') is a multinational biopharmaceutical and life sciences enterprise subject to Regulation (EU) 2016/679 (GDPR), the Health Insurance Portability and Accountability Act (HIPAA), and applicable Member State health data regulations. This standard establishes strict corporate mandates governing all external service providers, contract research organizations (CROs), and payment processors handling Protected Health Information (PHI) or personal data."),

        ("SECTION 2.", "MANDATORY 72-HOUR INCIDENT NOTIFICATION CEILING",
         "Pursuant to Article 33 of Regulation (EU) 2016/679 and 45 CFR § 164.410, any vendor, contractor, or data processor experiencing a suspected or confirmed security breach, unauthorized access, ransomware incident, or availability interruption affecting NovuHealth data MUST formally notify the NovuHealth Global Data Protection Office in writing within seventy-two (72) hours of initial detection. Any contractual clause, SLA, or vendor policy purporting to provide notification terms exceeding seventy-two (72) hours (such as 5, 7, 10, or 14 business days) is strictly unlawful, constitutes an irremediable breach of contract, and shall be grounds for immediate contract termination with cause."),

        ("SECTION 3.", "CRYPTOGRAPHIC SAFEGUARDS FOR CLINICAL AND FINANCIAL RECORDS",
         "All customer personal data, cardholder information, and clinical trial records must be protected at rest using hardware-accelerated AES-256 encryption keys managed under FIPS 140-2 Level 3 Hardware Security Modules. All telemetry, web applications, and API transmission channels must enforce TLS 1.3 encryption (or minimum TLS 1.2 with forward secrecy cipher suites). Ephemeral storage or caching of unencrypted cardholder data is expressly prohibited."),

        ("SECTION 4.", "DATA PROCESSOR OBLIGATIONS (GDPR ARTICLE 28)",
         "All downstream processors must enter into a formal Data Processing Agreement (DPA) incorporating European Commission Standard Contractual Clauses (SCCs). Processors shall process personal data solely on documented instructions from NovuHealth, ensure all personnel have committed themselves to confidentiality, assist NovuHealth in responding to data subject rights requests within fifteen (15) calendar days, and make available all documentation necessary to demonstrate compliance."),

        ("SECTION 5.", "SUBPROCESSOR AUTHORIZATION AND AUDIT RIGHTS",
         "Processors shall not engage any subprocessor without prior specific or general written authorization of NovuHealth. In the case of general written authorization, the processor must inform NovuHealth at least thirty (30) calendar days in advance of any intended changes concerning the addition or replacement of subprocessors, thereby giving NovuHealth the right to object."),

        ("SECTION 6.", "INDEPENDENT THIRD-PARTY AUDIT DELIVERABLES",
         "All Tier-1 and Tier-2 vendors must provide NovuHealth annually with an unqualified SOC 2 Type II examination report covering Trust Services Criteria Security, Confidentiality, and Availability, alongside an active PCI-DSS v4.0 Attestation of Compliance (AoC) where payment card telemetry is touched."),

        ("SECTION 7.", "DATA RETENTION AND SYSTEMIC PURGING",
         "Clinical trial data and incident logs must be retained for a mandatory statutory period of three hundred and sixty-five (365) days from generation. Automated lifecycle rules purging records prior to 365 days without explicit DPO waiver are strictly forbidden.")
    ]

    for num, title, body in clauses:
        add_clause(doc, num, title, body)

    doc.save(out_path)
    print(f"Generated: {out_path}")


# =============================================================================
# 2. BRITEPAY PAYMENT AGREEMENT (.docx and .txt)
# =============================================================================
def generate_britepay_contract():
    target_dir = os.path.join(SAMPLE_DIR, "demo_C_explicit_violation")
    out_docx = os.path.join(target_dir, "01_BritePay_Payment_Agreement.docx")
    out_txt = os.path.join(target_dir, "01_BritePay_Payment_Agreement.txt")

    doc = docx.Document()
    style_document(doc, "MASTER PAYMENT PROCESSING SERVICES AGREEMENT",
                   "BritePay Merchant Operations Ltd.", "MSA-BP-NH-2023-88")

    clauses = [
        ("RECITALS & PREAMBLE", "",
         "This Master Payment Processing Services Agreement ('Agreement') is entered into as of October 14, 2023 ('Effective Date') by and between NovuHealth Global Therapeutics Inc., an enterprise corporation ('Customer'), and BritePay Merchant Operations Ltd., a merchant acquiring and settlement processor ('Processor' or 'Vendor'). WHEREAS Customer operates global clinical therapies and patient billing systems, and Processor provides automated merchant gateway routing and cardholder processing."),

        ("SECTION 1.", "DEFINITIONS AND APPLICABILITY",
         "1.1 'Customer Data' means all personal, cardholder, clinical account, or financial telemetry transmitted to Processor.\n1.2 'Security Incident' means any confirmed unauthorized access, exfiltration, or modification of Customer Data residing on Processor infrastructure."),

        ("SECTION 4.", "DATA SECURITY AND CRYPTOGRAPHIC STANDARDS",
         "4.1 Processor covenants that all payment transaction streams shall be transmitted using TLS 1.3 encryption. Stored cardholder credentials and merchant authorization tokens shall be encrypted at rest using AES-256 bit encryption keys.\n4.2 Processor warrants compliance with PCI-DSS Level 1 service provider standards."),

        ("SECTION 11.", "SECURITY INCIDENTS AND BREACH NOTIFICATION (DEFECTIVE SLA)",
         "11.1 Incident Mitigation: Processor shall maintain automated anomaly detection across all payment gateway endpoints.\n11.2 Forensic Investigation: Following any suspected breach, Processor's internal incident response team shall conduct a preliminary triage within seventy-two (72) hours.\n11.3 Forensic Determination: Processor shall compile a comprehensive forensic dossier prior to issuing any external corporate disclosures.\n11.4 Notification Period: In the event Processor confirms a verified security incident affecting Customer cardholder data or credentials, Processor shall exercise commercially reasonable efforts to notify Customer within ten (10) business days following completion of internal forensic investigation. In no event shall notice be required earlier than seven (7) business days from incident confirmation.\n11.5 Scope of Disclosure: Notification shall include the preliminary nature of incident, volume of records affected, and remediation patch schedules."),

        ("SECTION 14.", "AUDIT AND REGULATORY COOPERATION",
         "14.1 Processor shall provide Customer with an annual executive summary of its PCI-DSS Attestation of Compliance.\n14.2 On-site technical inspections by Customer auditors shall be limited to one inspection per thirty-six (36) month period with sixty (60) days prior written notice."),

        ("SECTION 18.", "GOVERNING LAW AND JURISDICTION",
         "18.1 This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to conflict of law principles.\n18.2 In witness whereof, the parties hereto have executed this Agreement by their duly authorized representatives.")
    ]

    txt_content = []
    for num, title, body in clauses:
        add_clause(doc, num, title, body)
        header_line = f"{num} {title}".strip()
        txt_content.append(f"{header_line}\n{body}\n")

    doc.save(out_docx)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n\n".join(txt_content))

    print(f"Generated: {out_docx} and {out_txt}")


# =============================================================================
# 3. MERIDIAN DUE DILIGENCE POLICY & APEX AI CONTRACT (.docx and .txt)
# =============================================================================
def generate_meridian_documents():
    target_dir = os.path.join(SAMPLE_DIR, "demo_B_missing_evidence")
    os.makedirs(target_dir, exist_ok=True)
    out_pol = os.path.join(target_dir, "01_Meridian_Vendor_Due_Diligence_Policy.docx")
    out_con = os.path.join(target_dir, "02_ApexAI_Subscription_Agreement.docx")
    out_txt = os.path.join(target_dir, "ApexAI_Subscription_Agreement.txt")

    # Policy
    doc_pol = docx.Document()
    style_document(doc_pol, "GLOBAL SUPPLY CHAIN VENDOR DUE DILIGENCE & SUBPROCESSOR OBLIGATIONS STANDARD",
                   "Meridian Enterprise Logistics Inc.", "MER-VDP-2023-V2")
    
    p_clauses = [
        ("SECTION 1.", "THIRD-PARTY LOGISTICS DATA SAFEGUARDS",
         "Meridian Enterprise Logistics Inc. ('Meridian') oversees critical supply chain, inventory, and automated tracking networks. Any SaaS provider, cloud host, or predictive routing vendor handling freight routing, bill-of-lading records, or enterprise credentials must demonstrate unbroken compliance with Meridian's Tier-1 data protection criteria."),

        ("SECTION 2.", "SUBPROCESSOR TRANSPARENCY AND WRITTEN NOTICE",
         "Pursuant to corporate governance and international data standards, vendors must maintain an exhaustive, accredited registry of all downstream subprocessors, infrastructure hosts, and analytics providers. Vendors shall provide at least thirty (30) days prior written notice before onboarding any new subprocessor, and must provide audited SOC 2 Type II or ISO 27001 proof confirming sub-tier compliance."),

        ("SECTION 3.", "INDEPENDENT AUDIT EVIDENCE MANDATE",
         "Under no circumstances shall contractual promises or self-declarations suffice for vendor compliance verification. Every vendor must furnish within forty-five (45) days of contract execution an unqualified SOC 2 Type II report conducted by an accredited CPA firm or an active ISO/IEC 27001 certification with unbroken surveillance audit records. Failure to provide such evidence results in automatic classification as 'Unverified' with contract suspension triggers.")
    ]
    for num, title, body in p_clauses:
        add_clause(doc_pol, num, title, body)
    doc_pol.save(out_pol)
    print(f"Generated: {out_pol}")

    # Apex AI Contract
    doc_con = docx.Document()
    style_document(doc_con, "ENTERPRISE AI LOGISTICS SUBSCRIPTION AGREEMENT",
                   "Apex AI Analytics Corp.", "AGR-APX-MER-2023-01")

    c_clauses = [
        ("PREAMBLE", "",
         "This Enterprise SaaS Agreement is entered into by and between Meridian Enterprise Logistics Inc. ('Customer') and Apex AI Analytics Corp. ('Vendor'), regarding the deployment of predictive freight analytics and generative routing optimization models."),

        ("CLAUSE 6.", "DATA ENCRYPTION AND TELEMETRY CONTROLS",
         "6.1 Vendor covenants that all supply chain telemetry ingested into the Apex Neural Engine is encrypted at rest using AES-256 and in transit via TLS 1.3.\n6.2 Multi-factor authentication (MFA) is enforced for all administrative portals."),

        ("CLAUSE 14.", "SUBPROCESSOR VETTING AND AUDIT OBLIGATIONS",
         "14.1 Vendor covenants and warrants that it maintains an audited list of subprocessors and cloud providers.\n14.2 Vendor shall provide Customer with prior written notice of thirty (30) days regarding any changes to its subprocessor fleet.\n14.3 Vendor covenants to supply an annual independent SOC 2 Type II audit examination report upon completion of its annual audit cycle."),

        ("CLAUSE 19.", "AI MODEL ISOLATION AND STATISTICAL EMBEDDINGS",
         "19.1 Customer retains all proprietary title and copyright in Customer prompts, dispatch orders, and manifest logs.\n19.2 Vendor shall isolate customer inference requests from public model training weights.\n19.3 Notwithstanding Section 19.2, Vendor may retain derived statistical embeddings without appropriate technical filtering solely to reasonably improve and optimize core routing weights.")
    ]

    txt_apex = []
    for num, title, body in c_clauses:
        add_clause(doc_con, num, title, body)
        txt_apex.append(f"{num} {title}\n{body}\n")

    doc_con.save(out_con)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n\n".join(txt_apex))

    print(f"Generated: {out_con} and {out_txt}")


# =============================================================================
# 4. SECUREID CISO DECLARATION (.docx and .txt)
# =============================================================================
def generate_secureid_declaration():
    target_dir = os.path.join(SAMPLE_DIR, "demo_E_contradiction")
    out_docx = os.path.join(target_dir, "01_SecureID_CISO_Declaration.docx")
    out_txt = os.path.join(target_dir, "01_SecureID_CISO_Declaration.txt")

    doc = docx.Document()
    style_document(doc, "ANNUAL EXECUTIVE SECURITY AND AUDIT TRAIL DECLARATION",
                   "SecureID Gateway Systems Inc.", "DEC-SEC-CISO-2024")

    clauses = [
        ("OFFICIAL DECLARATION OF CHIEF INFORMATION SECURITY OFFICER", "",
         "I, Marcus Vance, serving in the official capacity of Chief Information Security Officer (CISO) of SecureID Gateway Systems Inc., hereby issue this formal declaration regarding our enterprise identity authentication gateway and access logging systems:"),

        ("ARTICLE 1.", "IMMUTABLE AUDIT TRAIL LOGGING ARCHITECTURE",
         "All enterprise authentication events, single sign-on (SSO) exchanges, privileged identity modifications, and API access tokens are captured in real-time across our distributed microservices architecture. Logs are cryptographically signed using SHA-256 HMAC and streamed continuously to hardened AWS S3 storage buckets."),

        ("ARTICLE 2.", "MANDATORY 365-DAY RETENTION GUARANTEE",
         "In strict compliance with statutory financial audit standards and Customer security requirements, SecureID corporate log retention policies strictly enforce a mandatory three hundred and sixty-five (365) day minimum preservation period prior to any automated archival transition or purging. All logs remain hot-searchable for 365 consecutive calendar days to facilitate forensic investigations."),

        ("ARTICLE 3.", "CONFIDENTIALITY AND ACCESS CONTROLS",
         "Administrative access to production log volumes is restricted strictly to Level-3 security engineers utilizing hardware FIDO2 MFA tokens. No customer data or access logs are accessible via single-factor credentials.")
    ]

    txt_content = []
    for num, title, body in clauses:
        add_clause(doc, num, title, body)
        txt_content.append(f"{num} {title}\n{body}\n")

    doc.save(out_docx)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n\n".join(txt_content))

    print(f"Generated: {out_docx} and {out_txt}")


# =============================================================================
# 5. QUANTUMNET COLOCATION AGREEMENT (.docx and .txt)
# =============================================================================
def generate_quantumnet_documents():
    target_dir = os.path.join(SAMPLE_DIR, "demo_D_expired_cert")
    out_docx = os.path.join(target_dir, "01_QuantumNet_Infrastructure_MSA.docx")
    out_txt = os.path.join(target_dir, "01_QuantumNet_Infrastructure_MSA.txt")

    doc = docx.Document()
    style_document(doc, "COLOCATION AND INFRASTRUCTURE MASTER SERVICES AGREEMENT",
                   "QuantumNet Infrastructure Services AG", "QN-MSA-2022-771")

    clauses = [
        ("SECTION 1.", "INFRASTRUCTURE SERVICES AND DATA CENTER TIERS",
         "QuantumNet Infrastructure Services AG ('Vendor') covenants to provide Aegis Financial Technologies Inc. ('Customer') with dedicated Tier-IV data center colocation, private cage hosting, and dual redundant power feeds across its Frankfurt and Zurich facilities."),

        ("SECTION 5.", "SECURITY CERTIFICATION COVENANTS",
         "Vendor covenants that all operational hosting centers, physical perimeters, and biometric entry controls shall at all times maintain an active, unexpired ISO/IEC 27001:2013 certification issued by an accredited registrar (such as BSI or TÜV Rheinland). Vendor covenants to furnish Customer with renewed certificates within thirty (30) days of certificate expiration."),

        ("SECTION 8.", "INCIDENT NOTIFICATION AND ACCESS CONTROL",
         "Vendor enforces two-factor biometric access controls for all data hall entry points. Security incident notification shall be issued within 24 hours of any perimeter security breach.")
    ]

    txt_content = []
    for num, title, body in clauses:
        add_clause(doc, num, title, body)
        txt_content.append(f"{num} {title}\n{body}\n")

    doc.save(out_docx)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n\n".join(txt_content))

    print(f"Generated: {out_docx} and {out_txt}")


if __name__ == "__main__":
    generate_novuhealth_policy()
    generate_britepay_contract()
    generate_meridian_documents()
    generate_secureid_declaration()
    generate_quantumnet_documents()
    print("All rich corporate and contract documents successfully generated.")
