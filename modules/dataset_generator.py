"""
Synthetic Compliance Dataset Generator Module
Generates interconnected synthetic compliance cases, document families, 
explicit relationship graphs, and ground-truth compliance assessments.

Supports 12 explicit scenarios:
1. Fully Compliant with valid evidence
2. Explicit Violation with direct evidence
3. Missing Evidence (contract promise present, but proof absent)
4. Expired Certificate / Outdated Evidence
5. Contradictory Evidence across documents
6. Conditional Obligations (Not Applicable if condition unmet)
7. Contractual or Policy Exceptions
8. Ambiguous Wording (Indeterminate)
9. Non-Applicable Requirements (Entity/Data out of scope)
10. Superseded Contract Clauses (Amendment precedence)
11. Conflicting Dates / Retention Deadlines
12. Multi-Document Complex Reasoning (>= 3 documents)
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_rules(rules_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load the structured rules catalogue from JSON."""
    if not rules_path:
        rules_path = os.path.join(DATA_DIR, "rules.json")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# Standard fictional organizations and vendors
ORGANIZATIONS = [
    {"org_id": "ORG-ALPHA", "name": "Aegis Financial Technologies Inc.", "sector": "FinTech / Banking", "region": "North America"},
    {"org_id": "ORG-BETA", "name": "NovuHealth Global Therapeutics", "sector": "Healthcare / Life Sciences", "region": "EU & US"},
    {"org_id": "ORG-GAMMA", "name": "Meridian Enterprise Logistics", "sector": "Supply Chain & Retail", "region": "Global"},
    {"org_id": "ORG-DELTA", "name": "Vanguard Cloud Intelligence Corp", "sector": "SaaS Platform", "region": "EU"}
]

VENDORS = [
    {"vendor_id": "VEN-001", "name": "CyberVault Storage Solutions Ltd.", "type": "Cloud Storage & Database Host", "tier": "Tier-1 Critical"},
    {"vendor_id": "VEN-002", "name": "Apex AI Analytics Corp.", "type": "Machine Learning SaaS", "tier": "Tier-2 Operational"},
    {"vendor_id": "VEN-003", "name": "SecureID Gateway Systems", "type": "Identity & Access Provider", "tier": "Tier-1 Critical"},
    {"vendor_id": "VEN-004", "name": "QuantumNet Infrastructure Services", "type": "Data Center & Hosting", "tier": "Tier-1 Critical"},
    {"vendor_id": "VEN-005", "name": "BritePay Merchant Operations", "type": "Payment Processor", "tier": "Tier-1 Critical"},
    {"vendor_id": "VEN-006", "name": "Optima Talent Staffing Group", "type": "Staff Augmentation & Contractors", "tier": "Tier-3 Ancillary"}
]


def generate_core_scenarios(rules: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate rich, interconnected compliance cases with documents, relationships, and ground-truth assessments.
    Returns (documents, relationships, assessments).
    """
    rule_map = {r["rule_id"]: r for r in rules}

    documents = []
    relationships = []
    assessments = []

    # Helper to add relationship
    def add_rel(source_id: str, target_id: str, rel_type: str, desc: str):
        relationships.append({
            "rel_id": f"REL-{len(relationships) + 1:04d}",
            "source_id": source_id,
            "target_id": target_id,
            "relationship_type": rel_type, # implements, requires, satisfies, fails_to_satisfy, supports, contradicts, supersedes, exception_to, evidence_missing_for
            "description": desc
        })

    # =========================================================================
    # SCENARIO 1: CASE-001 (Fully Compliant: Data Encryption & MFA)
    # Vendor: VEN-001 (CyberVault) | Org: ORG-ALPHA (Aegis Financial)
    # Rules: RULE-SEC-001 (Encryption) & RULE-SEC-002 (MFA)
    # Status: COMPLIANT
    # =========================================================================
    case_1_id = "CASE-2024-001"
    
    # Doc 1: Internal Policy
    d1_1 = {
        "document_id": "DOC-C1-01",
        "case_id": case_1_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-001",
        "document_type": "internal_policy",
        "title": "Aegis Financial Vendor Information Security Policy v3.2",
        "source_type": "Synthetic Organizational Policy",
        "version": "3.2",
        "issue_date": "2023-01-15",
        "effective_date": "2023-02-01",
        "expiry_date": None,
        "full_text": """AEGIS FINANCIAL TECHNOLOGIES INC. — INTERNAL SECURITY POLICY
SECTION 4: THIRD-PARTY DATA SAFEGUARDS
4.1 Cryptographic Controls: All tier-1 cloud storage vendors must enforce hardware-accelerated AES-256 encryption for all data at rest and TLS 1.3 for all ingress/egress endpoints.
4.2 Administrative Access: Phishing-resistant multi-factor authentication (MFA) is strictly mandatory for 100% of vendor administrative consoles and support portals accessing customer databases.
4.3 Annual Audit Verification: Vendors must furnish an annual unqualified SOC 2 Type II examination report covering Trust Services Criteria CC6.1 and CC6.6.""",
        "related_document_ids": ["RULE-SEC-001", "RULE-SEC-002"]
    }
    documents.append(d1_1)
    add_rel(d1_1["document_id"], "RULE-SEC-001", "implements", "Policy Section 4.1 implements regulatory encryption rule")
    add_rel(d1_1["document_id"], "RULE-SEC-002", "implements", "Policy Section 4.2 implements regulatory MFA rule")

    # Doc 2: Vendor Contract (MSA)
    d1_2 = {
        "document_id": "DOC-C1-02",
        "case_id": case_1_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-001",
        "document_type": "vendor_contract",
        "title": "Master Cloud Hosting Agreement — CyberVault Storage Ltd.",
        "source_type": "Synthetic Contract",
        "version": "1.0",
        "issue_date": "2023-03-01",
        "effective_date": "2023-03-15",
        "expiry_date": "2026-03-15",
        "full_text": """MASTER CLOUD SERVICES AGREEMENT (MSA)
BETWEEN: Aegis Financial Technologies Inc. ('Customer') AND CyberVault Storage Solutions Ltd. ('Vendor')
EFFECTIVE DATE: March 15, 2023

CLAUSE 8. CONFIDENTIALITY AND SECURITY COVENANTS
8.1 Encryption at Rest and in Transit: Vendor covenants and warrants that Customer Data stored on CyberVault cloud volumes is continuously encrypted at rest using AES-256 bit encryption keys managed under FIPS 140-2 Level 3 HSM modules. All web interfaces and API endpoints mandate TLS 1.3 encryption.
8.2 Identity and Access Management: Vendor mandates Multi-Factor Authentication (MFA) utilizing FIDO2 security keys for all operational engineers and database administrators accessing production clusters.
8.3 Annual Audit Deliverable: Vendor covenants to supply Customer with an annual SOC 2 Type II report within forty-five (45) days of the conclusion of each examination cycle.""",
        "related_document_ids": ["DOC-C1-01"]
    }
    documents.append(d1_2)
    add_rel(d1_2["document_id"], d1_1["document_id"], "satisfies", "Contract Clause 8 binds vendor to policy requirements")

    # Doc 3: SOC 2 Type II Report (Valid Evidence)
    d1_3 = {
        "document_id": "DOC-C1-03",
        "case_id": case_1_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-001",
        "document_type": "audit_report",
        "title": "Independent Service Auditor Report on SOC 2 Type II (CyberVault)",
        "source_type": "Synthetic Evidence",
        "version": "2024 Final",
        "issue_date": "2024-04-10",
        "effective_date": "2023-10-01",
        "expiry_date": "2024-09-30",
        "full_text": """INDEPENDENT SERVICE AUDITOR'S REPORT (SOC 2 TYPE II)
SERVICE ORGANIZATION: CyberVault Storage Solutions Ltd.
PERIOD OF TESTING: October 1, 2023 to March 31, 2024
AUDITOR: Deloitte & Touche LLP (Accredited CPA Firm)
OPINION: Unqualified Clean Opinion

SECTION IV — AUDIT TESTING OF CONTROLS:
Control CC6.6 (Encryption):
- Testing Performed: Auditor inspected automated configuration scripts, AWS KMS key policies, and TLS cipher configurations.
- Auditor Finding: Sampled 50 production storage volumes; 100% verified encrypted at rest with AES-256. Sampled 30 API gateway endpoints; 100% enforced TLS 1.2 or TLS 1.3 with high-strength cipher suites. No deviations noted.

Control CC6.1 (Logical Access and Authentication):
- Testing Performed: Auditor sampled 45 administrative staff accounts across DevOps and Systems Engineering.
- Auditor Finding: 100% of sampled administrative accounts enforced mandatory hardware-based MFA (YubiKey/FIDO2). No administrative accounts were accessible via single-factor credentials. No deviations noted.""",
        "related_document_ids": ["DOC-C1-02"]
    }
    documents.append(d1_3)
    add_rel(d1_3["document_id"], "RULE-SEC-001", "supports", "Deloitte SOC 2 Section IV confirms AES-256 and TLS 1.3 controls")
    add_rel(d1_3["document_id"], "RULE-SEC-002", "supports", "Deloitte SOC 2 Section IV confirms 100% MFA compliance")

    # Assessment 1: RULE-SEC-001
    assessments.append({
        "assessment_id": "ASSESS-C1-001",
        "case_id": case_1_id,
        "rule_id": "RULE-SEC-001",
        "rule_title": "Data Encryption in Transit and at Rest",
        "expected_status": "Compliant",
        "applicability_result": "Applicable (Vendor stores and transmits sensitive financial data)",
        "relevant_document_ids": ["DOC-C1-01", "DOC-C1-02", "DOC-C1-03"],
        "relevant_passages": [
            "Contract Clause 8.1: 'Customer Data stored on CyberVault cloud volumes is continuously encrypted at rest using AES-256... All web interfaces and API endpoints mandate TLS 1.3 encryption.'",
            "SOC 2 Report Section IV Control CC6.6: 'Sampled 50 production storage volumes; 100% verified encrypted at rest with AES-256... Sampled 30 API gateway endpoints; 100% enforced TLS 1.2 or TLS 1.3... No deviations noted.'"
        ],
        "reasoning_steps": [
            "Step 1: Verified applicability — CyberVault hosts production database storage for financial client.",
            "Step 2: Identified policy mandate in Aegis Policy Section 4.1 requiring AES-256 and TLS 1.3.",
            "Step 3: Verified contract commitment in MSA Clause 8.1 binding vendor to these cryptographic controls.",
            "Step 4: Inspected independent SOC 2 Type II audit report (DOC-C1-03) covering period ending March 2024.",
            "Step 5: Auditor confirmed 100% encryption at rest with AES-256 and TLS 1.3 on sampled endpoints with zero deviations.",
            "Conclusion: Control is fully established by unexpired, accredited third-party examination."
        ],
        "evidence_sufficiency": "Strong",
        "missing_evidence": "None. Both contractual covenant and independent third-party examination report present.",
        "contradictions": "None observed.",
        "recommended_action": "Maintain monitoring; schedule next annual SOC 2 review by April 2025.",
        "review_notes": "Benchmark positive compliant example with unbroken chain of evidence."
    })

    # Assessment 2: RULE-SEC-002
    assessments.append({
        "assessment_id": "ASSESS-C1-002",
        "case_id": case_1_id,
        "rule_id": "RULE-SEC-002",
        "rule_title": "Multi-Factor Authentication (MFA) for Administrative Access",
        "expected_status": "Compliant",
        "applicability_result": "Applicable (Vendor personnel hold administrative access to production systems)",
        "relevant_document_ids": ["DOC-C1-01", "DOC-C1-02", "DOC-C1-03"],
        "relevant_passages": [
            "Contract Clause 8.2: 'Vendor mandates Multi-Factor Authentication (MFA) utilizing FIDO2 security keys for all operational engineers...'",
            "SOC 2 Report Section IV Control CC6.1: '100% of sampled administrative accounts enforced mandatory hardware-based MFA... No administrative accounts were accessible via single-factor credentials.'"
        ],
        "reasoning_steps": [
            "Step 1: Confirmed applicability under SOC 2 CC6.1 criteria for administrative access.",
            "Step 2: Contractual obligation explicitly present in MSA Clause 8.2.",
            "Step 3: Unqualified SOC 2 Type II audit report tested 45 administrative staff accounts and found 100% MFA enforcement with no deviations.",
            "Conclusion: Requirement is demonstrably satisfied."
        ],
        "evidence_sufficiency": "Strong",
        "missing_evidence": "None.",
        "contradictions": "None.",
        "recommended_action": "No remediation required. Next review in Q2 2025.",
        "review_notes": "Full compliance verified."
    })

    # =========================================================================
    # SCENARIO 2: CASE-002 (Explicit Violation: Incident Notification SLA)
    # Vendor: VEN-005 (BritePay) | Org: ORG-BETA (NovuHealth)
    # Rule: RULE-SEC-004 (72-Hour Security Incident Notification)
    # Status: NON-COMPLIANT
    # =========================================================================
    case_2_id = "CASE-2024-002"

    d2_1 = {
        "document_id": "DOC-C2-01",
        "case_id": case_2_id,
        "organization_id": "ORG-BETA",
        "vendor_id": "VEN-005",
        "document_type": "internal_policy",
        "title": "NovuHealth Global Privacy & Breach Management Protocol",
        "source_type": "Synthetic Organizational Policy",
        "version": "4.0",
        "issue_date": "2023-05-10",
        "effective_date": "2023-06-01",
        "expiry_date": None,
        "full_text": """NOVUHEALTH GLOBAL BREACH PROTOCOL
SECTION 3. VENDOR NOTIFICATION TIMELINES
In compliance with GDPR Article 33 and HIPAA Breach Notification Rule, any third-party payment processor or data vendor experiencing a confirmed security breach must notify NovuHealth in writing within seventy-two (72) hours of discovery. Notification terms exceeding 72 hours are strictly prohibited.""",
        "related_document_ids": ["RULE-SEC-004"]
    }
    documents.append(d2_1)
    add_rel(d2_1["document_id"], "RULE-SEC-004", "implements", "Implements GDPR Art. 33 notification mandate")

    # Contract containing explicit conflicting / violating clause
    d2_2 = {
        "document_id": "DOC-C2-02",
        "case_id": case_2_id,
        "organization_id": "ORG-BETA",
        "vendor_id": "VEN-005",
        "document_type": "vendor_contract",
        "title": "Merchant Payment Processing Agreement — BritePay Operations",
        "source_type": "Synthetic Contract",
        "version": "2.0",
        "issue_date": "2023-08-15",
        "effective_date": "2023-09-01",
        "expiry_date": "2025-09-01",
        "full_text": """MERCHANT PAYMENT SERVICES AGREEMENT
BETWEEN: NovuHealth Therapeutics ('Customer') AND BritePay Merchant Operations ('Processor')

SECTION 11. SECURITY INCIDENTS AND BREACH NOTIFICATION
11.4 Notification Period: In the event Processor confirms a verified security incident affecting Customer cardholder data or credentials, Processor shall exercise commercially reasonable efforts to notify Customer within ten (10) business days following completion of Processor's internal forensic investigation. In no event shall notice be required earlier than seven (7) business days from incident confirmation.""",
        "related_document_ids": ["DOC-C2-01"]
    }
    documents.append(d2_2)
    add_rel(d2_2["document_id"], "RULE-SEC-004", "fails_to_satisfy", "Clause 11.4 allows 10 business days, directly violating 72-hour ceiling")

    # Post-incident Audit Review confirming late notification
    d2_3 = {
        "document_id": "DOC-C2-03",
        "case_id": case_2_id,
        "organization_id": "ORG-BETA",
        "vendor_id": "VEN-005",
        "document_type": "audit_report",
        "title": "Incident Retrospective Audit Report — BritePay API Incident",
        "source_type": "Synthetic Evidence",
        "version": "1.0",
        "issue_date": "2024-02-20",
        "effective_date": "2024-02-01",
        "expiry_date": None,
        "full_text": """INDEPENDENT BREACH AUDIT RETROSPECTIVE
ORGANIZATION AUDITED: BritePay Merchant Operations
INCIDENT REF: INC-2024-8812 (Payment Token Leak)

FINDING SUMMARY:
- Breach Detection Date: January 12, 2024 (08:30 UTC)
- Customer Notification Sent: January 23, 2024 (16:15 UTC)
- Total Elapsed Time: 271 hours (11 calendar days / 8 business days)
- Root Cause of Delay: Vendor followed Section 11.4 internal forensic completion clause rather than statutory 72-hour notification.
- Compliance Assessment: Vendor breached GDPR Art. 33 and regulatory 72-hour ceiling.""",
        "related_document_ids": ["DOC-C2-02"]
    }
    documents.append(d2_3)
    add_rel(d2_3["document_id"], "RULE-SEC-004", "supports", "Audit evidence proves notification elapsed 271 hours vs 72-hour limit")

    assessments.append({
        "assessment_id": "ASSESS-C2-001",
        "case_id": case_2_id,
        "rule_id": "RULE-SEC-004",
        "rule_title": "Security Incident Notification Within 72 Hours",
        "expected_status": "Non-compliant",
        "applicability_result": "Applicable (Vendor processes sensitive patient payment records subject to GDPR/HIPAA)",
        "relevant_document_ids": ["DOC-C2-01", "DOC-C2-02", "DOC-C2-03"],
        "relevant_passages": [
            "Contract Clause 11.4: 'Processor shall exercise commercially reasonable efforts to notify Customer within ten (10) business days following completion of internal forensic investigation...'",
            "Audit Report Finding INC-2024-8812: 'Breach Detection Date: January 12, 2024... Customer Notification Sent: January 23, 2024... Total Elapsed Time: 271 hours (11 calendar days)... Vendor breached regulatory 72-hour ceiling.'"
        ],
        "reasoning_steps": [
            "Step 1: Rule RULE-SEC-004 mandates breach notification within 72 hours under GDPR Art. 33.",
            "Step 2: NovuHealth Internal Policy explicitly bars notification windows exceeding 72 hours.",
            "Step 3: Contract Section 11.4 grants vendor 10 business days, which on its face fails to satisfy the mandatory 72-hour legal ceiling.",
            "Step 4: Audit Retrospective (DOC-C2-03) provides empirical evidence of actual incident INC-2024-8812 where notification took 271 hours.",
            "Conclusion: Non-compliant. Explicit violation supported by both contractual deficiency and direct incident audit evidence."
        ],
        "evidence_sufficiency": "Strong",
        "missing_evidence": "None. Violation is established by direct proof.",
        "contradictions": "Contract Clause 11.4 contradicts statutory 72-hour requirement.",
        "recommended_action": "Execute urgent Contract Amendment reducing notification timeline to 72 hours; issue formal legal breach cure notice.",
        "review_notes": "Clear non-compliance scenario for empirical benchmark verification."
    })

    # =========================================================================
    # SCENARIO 3: CASE-003 (Missing Evidence: Subcontractor Due Diligence)
    # Vendor: VEN-002 (Apex AI) | Org: ORG-GAMMA (Meridian Logistics)
    # Rule: RULE-SEC-006 (Subcontractor Prior Written Notice and Vetting)
    # Status: UNVERIFIED
    # =========================================================================
    case_3_id = "CASE-2024-003"

    d3_1 = {
        "document_id": "DOC-C3-01",
        "case_id": case_3_id,
        "organization_id": "ORG-GAMMA",
        "vendor_id": "VEN-002",
        "document_type": "vendor_contract",
        "title": "SaaS Subscription Agreement — Apex AI Analytics",
        "source_type": "Synthetic Contract",
        "version": "1.1",
        "issue_date": "2023-11-01",
        "effective_date": "2023-11-15",
        "expiry_date": "2025-11-15",
        "full_text": """APEX AI ANALYTICS SUBSCRIPTION AGREEMENT
CLAUSE 14. SUB-PROCESSORS AND THIRD-PARTY SUBCONTRACTORS
14.1 Authorization and Registry: Vendor covenants that it maintains an audited list of approved sub-processors. Vendor shall provide Customer with thirty (30) days prior written notice before onboarding any new sub-processor.
14.2 Pass-Through Auditing: Vendor shall conduct annual security reviews of all sub-processors possessing access to Customer data and make copies of sub-processor security attestations available to Customer upon request.""",
        "related_document_ids": ["RULE-SEC-006"]
    }
    documents.append(d3_1)
    add_rel(d3_1["document_id"], "RULE-SEC-006", "requires", "Contract clause 14 promises subprocessor due diligence audit availability")

    # Notice: NO subprocessor registry or audit report uploaded for this case!
    add_rel("RULE-SEC-006", "DOC-C3-01", "evidence_missing_for", "Required subprocessor due diligence audit report and active subprocessor registry have not been supplied")

    assessments.append({
        "assessment_id": "ASSESS-C3-001",
        "case_id": case_3_id,
        "rule_id": "RULE-SEC-006",
        "rule_title": "Subcontractor Prior Written Notice and Vetting",
        "expected_status": "Unverified",
        "applicability_result": "Applicable (Vendor utilizes third-party infrastructure and sub-processors)",
        "relevant_document_ids": ["DOC-C3-01"],
        "relevant_passages": [
            "Contract Clause 14.1: 'Vendor covenants that it maintains an audited list of approved sub-processors...'",
            "Contract Clause 14.2: 'Vendor shall conduct annual security reviews... and make copies available upon request.'"
        ],
        "reasoning_steps": [
            "Step 1: Requirement mandates active subprocessor vetting and 30-day notice mechanism.",
            "Step 2: Contract Clause 14 contains an explicit contractual promise to perform reviews and provide documentation.",
            "Step 3: Verification check: No Subprocessor Registry, SOC 2 bridge letter, or third-party vetting report was provided in the submission family.",
            "Step 4: Distinguish absence of proof from proof of violation: The vendor may possess compliant subprocessor audits, but without inspecting them, fulfillment cannot be established.",
            "Conclusion: Unverified. Missing evidence prevents definitive determination."
        ],
        "evidence_sufficiency": "Unavailable",
        "missing_evidence": "Subprocessor Registry and Annual Subprocessor Due Diligence Audit Reports are missing from the case files.",
        "contradictions": "None observed in contract text.",
        "recommended_action": "Issue formal vendor compliance request requesting complete Subprocessor Registry and current SOC 2/ISO certifications for all listed subprocessors.",
        "review_notes": "Highlights core principle: Never label missing evidence as proof of non-compliance."
    })

    # =========================================================================
    # SCENARIO 4: CASE-004 (Expired Certificate: ISO 27001)
    # Vendor: VEN-004 (QuantumNet) | Org: ORG-ALPHA (Aegis Financial)
    # Rule: RULE-SEC-007 (ISO/IEC 27001 Certification Validity)
    # Status: NON-COMPLIANT for Certificate Rule / UNVERIFIED for underlying controls
    # =========================================================================
    case_4_id = "CASE-2024-004"

    d4_1 = {
        "document_id": "DOC-C4-01",
        "case_id": case_4_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-004",
        "document_type": "vendor_contract",
        "title": "Colocation & Infrastructure Agreement — QuantumNet",
        "source_type": "Synthetic Contract",
        "version": "1.0",
        "issue_date": "2021-04-01",
        "effective_date": "2021-05-01",
        "expiry_date": "2026-05-01",
        "full_text": """INFRASTRUCTURE MASTER SERVICES AGREEMENT
BETWEEN: Aegis Financial Technologies Inc. AND QuantumNet Infrastructure Services
SECTION 9. MANDATORY CERTIFICATIONS
9.1 Continuous ISO 27001 Maintenance: QuantumNet covenants that all tier-IV datacenter facilities shall maintain an active, unexpired ISO/IEC 27001 certification throughout the entire contract duration. Failure to renew certification prior to expiration constitutes a material compliance default.""",
        "related_document_ids": ["RULE-SEC-007"]
    }
    documents.append(d4_1)

    # Expired Certificate Document
    d4_2 = {
        "document_id": "DOC-C4-02",
        "case_id": case_4_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-004",
        "document_type": "compliance_certificate",
        "title": "Certificate of Registration — ISO/IEC 27001:2013 (QuantumNet)",
        "source_type": "Synthetic Evidence",
        "version": "Cert # IS-99412",
        "issue_date": "2020-06-15",
        "effective_date": "2020-06-15",
        "expiry_date": "2023-06-14",  # Expired!
        "full_text": """BSI CERTIFICATE OF REGISTRATION
INFORMATION SECURITY MANAGEMENT SYSTEM — ISO/IEC 27001:2013
This is to certify that: QuantumNet Infrastructure Services, Frankfurt Datacenter
Holds Certificate No: IS-99412
Original Cycle Start Date: 15 June 2020
Expiry Date: 14 June 2023
Status: EXPIRED. (No renewal certificate or surveillance audit extension letter on record for 2024).""",
        "related_document_ids": ["DOC-C4-01"]
    }
    documents.append(d4_2)
    add_rel(d4_2["document_id"], "RULE-SEC-007", "fails_to_satisfy", "Certificate expired on 2023-06-14; currently invalid")

    assessments.append({
        "assessment_id": "ASSESS-C4-001",
        "case_id": case_4_id,
        "rule_id": "RULE-SEC-007",
        "rule_title": "ISO/IEC 27001 Certification Validity",
        "expected_status": "Non-compliant",
        "applicability_result": "Applicable (Contract specifically mandates maintaining unexpired ISO 27001 certification)",
        "relevant_document_ids": ["DOC-C4-01", "DOC-C4-02"],
        "relevant_passages": [
            "Contract Clause 9.1: 'QuantumNet covenants that all tier-IV datacenter facilities shall maintain an active, unexpired ISO/IEC 27001 certification throughout the entire contract duration.'",
            "Certificate IS-99412: 'Expiry Date: 14 June 2023. Status: EXPIRED.'"
        ],
        "reasoning_steps": [
            "Step 1: Rule RULE-SEC-007 requires maintaining an active, unexpired ISO 27001 certificate.",
            "Step 2: Certificate DOC-C4-02 was inspected; its registered expiry date is June 14, 2023.",
            "Step 3: Temporal reasoning check: Current date exceeds June 2023; certificate has lapsed by over 9 months.",
            "Step 4: Distinguish certification validity from underlying controls: The underlying technical controls may still be functioning, but the specific legal requirement for an *active unexpired certificate* is explicitly breached.",
            "Conclusion: Non-compliant regarding certification validity."
        ],
        "evidence_sufficiency": "Strong",
        "missing_evidence": "Renewal ISO 27001:2022 certificate for the 2023-2026 cycle.",
        "contradictions": "Contract mandates continuous active certification, but uploaded document is expired.",
        "recommended_action": "Require vendor to provide recertification audit letter or 2024 ISO 27001 certificate within 15 calendar days.",
        "review_notes": "Carefully distinguishes expired certificate from automatic claim that technical controls are missing."
    })

    # =========================================================================
    # SCENARIO 5: CASE-005 (Contradictory Documents: Audit vs Vendor Declaration)
    # Vendor: VEN-003 (SecureID) | Org: ORG-ALPHA (Aegis Financial)
    # Rule: RULE-SEC-015 (Tamper-Evident Audit Logging & 1-Year Retention)
    # Status: INDETERMINATE
    # =========================================================================
    case_5_id = "CASE-2024-005"

    d5_1 = {
        "document_id": "DOC-C5-01",
        "case_id": case_5_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-003",
        "document_type": "vendor_contract",
        "title": "Identity Services Master Agreement — SecureID Gateway",
        "source_type": "Synthetic Contract",
        "version": "1.0",
        "issue_date": "2023-02-10",
        "effective_date": "2023-03-01",
        "expiry_date": "2026-03-01",
        "full_text": """SECUREID MASTER SERVICES AGREEMENT
CLAUSE 6. LOGGING AND AUDIT TRAIL PRESERVATION
6.2 Log Retention Window: SecureID covenants that all authentication event logs, administrative role changes, and API telemetry shall be retained in immutable cloud storage for a minimum duration of 365 calendar days.""",
        "related_document_ids": ["RULE-SEC-015"]
    }
    documents.append(d5_1)

    # Document 2: Vendor Self-Attestation claiming 365 days
    d5_2 = {
        "document_id": "DOC-C5-02",
        "case_id": case_5_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-003",
        "document_type": "supporting_evidence",
        "title": "Vendor Security Attestation Declaration (SecureID CISO)",
        "source_type": "Synthetic Evidence",
        "version": "2024 Annual",
        "issue_date": "2024-01-10",
        "effective_date": "2024-01-01",
        "expiry_date": None,
        "full_text": """SECUREID CISO ANNUAL SECURITY DECLARATION
I, Marcus Vance, Chief Information Security Officer of SecureID Systems, hereby certify that as of January 1, 2024:
1. All system event logs, authentication logs, and privileged administrative sessions are archived to immutable AWS S3 Glacier storage configured with Object Lock (Compliance Mode).
2. Log retention policies strictly enforce 365-day minimum preservation prior to automated purging.""",
        "related_document_ids": ["DOC-C5-01"]
    }
    documents.append(d5_2)

    # Document 3: Independent Technical Architecture Audit showing 90 days purge!
    d5_3 = {
        "document_id": "DOC-C5-03",
        "case_id": case_5_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-003",
        "document_type": "audit_report",
        "title": "Technical Architecture Assessment Report — Bishop Fox Security",
        "source_type": "Synthetic Evidence",
        "version": "1.0",
        "issue_date": "2024-03-05",
        "effective_date": "2024-02-15",
        "expiry_date": None,
        "full_text": """BISHOP FOX THIRD-PARTY TECHNICAL EVALUATION
TARGET: SecureID Gateway Production Telemetry Pipeline
DATE: February 2024
FINDING ID: SEC-LOG-04 (Lifecycle Configuration Mismatch)
The assessment team inspected live AWS CloudWatch and S3 bucket lifecycle configurations:
- Observed Configuration: S3 bucket 'secureid-prod-auth-logs' has an active lifecycle transition rule 'DeleteMarkerAfterDays: 90'.
- Log Analysis: Queries against log indexes older than 90 days returned zero results; logs from 2023 are purged automatically on day 91.
- Contradiction Note: This directly contradicts the vendor's declared 365-day retention policy and CISO annual declaration.""",
        "related_document_ids": ["DOC-C5-02"]
    }
    documents.append(d5_3)
    add_rel(d5_3["document_id"], d5_2["document_id"], "contradicts", "Technical audit observed 90-day automated purge contradicting CISO 365-day declaration")

    assessments.append({
        "assessment_id": "ASSESS-C5-001",
        "case_id": case_5_id,
        "rule_id": "RULE-SEC-015",
        "rule_title": "Comprehensive Audit Logging and 1-Year Retention",
        "expected_status": "Indeterminate",
        "applicability_result": "Applicable (Identity gateway handles authentication records)",
        "relevant_document_ids": ["DOC-C5-01", "DOC-C5-02", "DOC-C5-03"],
        "relevant_passages": [
            "Vendor CISO Declaration: 'Log retention policies strictly enforce 365-day minimum preservation prior to automated purging.'",
            "Bishop Fox Audit Finding SEC-LOG-04: 'Observed Configuration: S3 bucket... has active lifecycle transition rule DeleteMarkerAfterDays: 90... directly contradicts vendor declared 365-day retention.'"
        ],
        "reasoning_steps": [
            "Step 1: Rule RULE-SEC-015 requires 365 calendar days immutable log retention.",
            "Step 2: Vendor CISO signed a sworn declaration (DOC-C5-02) asserting compliance with 365-day retention.",
            "Step 3: Independent engineering evaluation (DOC-C5-03) conducted 6 weeks later observed live AWS configuration purging logs after 90 days.",
            "Step 4: Unresolved factual contradiction exists between vendor executive declaration and external technical finding. The platform cannot unilaterally determine whether the 90-day rule was a temporary staging anomaly or active non-compliance.",
            "Conclusion: Indeterminate. Documents contain direct unresolved contradictions requiring vendor clarification."
        ],
        "evidence_sufficiency": "Partial",
        "missing_evidence": "Reconciliation statement from SecureID explaining discrepancy between CISO declaration and Bishop Fox finding.",
        "contradictions": "Direct contradiction between CISO Declaration (365 days) and Bishop Fox Technical Inspection (90 days).",
        "recommended_action": "Freeze contract acceptance; issue formal request for clarification and demand live AWS S3 lifecycle rule export.",
        "review_notes": "Exemplary indeterminate contradiction case."
    })

    # =========================================================================
    # SCENARIO 6: CASE-006 (Conditional / Not Applicable Requirement)
    # Vendor: VEN-006 (Optima Staffing) | Org: ORG-ALPHA (Aegis Financial)
    # Rule: RULE-SEC-019 (HIPAA BAA and Health Data Safeguards)
    # Status: NOT APPLICABLE
    # =========================================================================
    case_6_id = "CASE-2024-006"

    d6_1 = {
        "document_id": "DOC-C6-01",
        "case_id": case_6_id,
        "organization_id": "ORG-ALPHA",
        "vendor_id": "VEN-006",
        "document_type": "vendor_contract",
        "title": "Professional IT Staff Augmentation Agreement — Optima Talent",
        "source_type": "Synthetic Contract",
        "version": "1.0",
        "issue_date": "2023-07-01",
        "effective_date": "2023-07-15",
        "expiry_date": "2025-07-15",
        "full_text": """PROFESSIONAL SERVICES MASTER AGREEMENT
BETWEEN: Aegis Financial Technologies Inc. ('Customer') AND Optima Talent Staffing Group ('Supplier')
STATEMENT OF WORK: IT Recruiting and Frontend Developer Staff Augmentation
EXCLUSION OF HEALTH DATA: Supplier personnel are assigned exclusively to internal financial analytics tools. Customer represents and warrants that Supplier personnel will not receive, process, store, or transmit any Protected Health Information (PHI) or electronic medical records governed by HIPAA 45 CFR §160/§164.""",
        "related_document_ids": ["RULE-SEC-019"]
    }
    documents.append(d6_1)

    assessments.append({
        "assessment_id": "ASSESS-C6-001",
        "case_id": case_6_id,
        "rule_id": "RULE-SEC-019",
        "rule_title": "Health Data Safeguards and HIPAA Business Associate Agreement",
        "expected_status": "Not applicable",
        "applicability_result": "Not applicable (Vendor does not receive or process Protected Health Information)",
        "relevant_document_ids": ["DOC-C6-01"],
        "relevant_passages": [
            "Contract SOW Exclusion: 'Customer represents and warrants that Supplier personnel will not receive, process, store, or transmit any Protected Health Information (PHI) or electronic medical records governed by HIPAA...'"
        ],
        "reasoning_steps": [
            "Step 1: Rule RULE-SEC-019 condition: Only applies when an entity processes Protected Health Information (PHI).",
            "Step 2: Inspecting Contract DOC-C6-01 reveals services are strictly limited to financial analytics frontend development.",
            "Step 3: Contract expressly disclaims transmission of any healthcare data or PHI.",
            "Conclusion: Not applicable under defined applicability conditions."
        ],
        "evidence_sufficiency": "Strong",
        "missing_evidence": "None (No PHI data flow exists).",
        "contradictions": "None.",
        "recommended_action": "Mark requirement as Not Applicable; no HIPAA Business Associate Agreement needed.",
        "review_notes": "Demonstrates proper conditional non-applicability evaluation."
    })

    # =========================================================================
    # SCENARIO 7: CASE-007 (Superseded Contract: Amendment Precedence)
    # Vendor: VEN-001 (CyberVault) | Org: ORG-DELTA (Vanguard Cloud)
    # Rule: RULE-SEC-004 (Incident Notification 72 Hours)
    # Status: COMPLIANT via Amendment Precedence (Original MSA said 14 days, Amendment 2 changed to 72 hours)
    # =========================================================================
    case_7_id = "CASE-2024-007"

    d7_1 = {
        "document_id": "DOC-C7-01",
        "case_id": case_7_id,
        "organization_id": "ORG-DELTA",
        "vendor_id": "VEN-001",
        "document_type": "vendor_contract",
        "title": "Master Cloud Agreement (Original 2021) — CyberVault",
        "source_type": "Synthetic Contract",
        "version": "1.0",
        "issue_date": "2021-01-10",
        "effective_date": "2021-02-01",
        "expiry_date": "2026-02-01",
        "full_text": """CYBERVAULT MASTER SERVICES AGREEMENT (2021 BASE)
CLAUSE 12. INCIDENT REPORTING
12.1 Vendor shall notify customer in writing within fourteen (14) calendar days following confirmation of any security incident affecting customer data.""",
        "related_document_ids": ["RULE-SEC-004"]
    }
    documents.append(d7_1)

    # Document 2: Executed Amendment superseding Clause 12.1
    d7_2 = {
        "document_id": "DOC-C7-02",
        "case_id": case_7_id,
        "organization_id": "ORG-DELTA",
        "vendor_id": "VEN-001",
        "document_type": "contract_amendment",
        "title": "Second Contract Amendment & GDPR Data Addendum",
        "source_type": "Synthetic Contract",
        "version": "Amendment No. 2",
        "issue_date": "2023-11-20",
        "effective_date": "2023-12-01",
        "expiry_date": None,
        "full_text": """SECOND AMENDMENT TO MASTER SERVICES AGREEMENT
BETWEEN: Vanguard Cloud Intelligence Corp AND CyberVault Storage Solutions Ltd.
EFFECTIVE DATE: December 1, 2023

WHEREAS the parties wish to align with EU General Data Protection Regulation requirements;
NOW THEREFORE:
1. Superseding Precedence: This Amendment amends and completely supersedes Clause 12.1 of the 2021 Base Agreement.
2. Revised Incident SLA: Clause 12.1 is hereby deleted in its entirety and replaced with the following:
   '12.1 Vendor shall notify Customer in writing without undue delay and in all cases within seventy-two (72) hours of becoming aware of any confirmed security incident, data breach, or unauthorized access.'
3. Ratification: In the event of any conflict between this Amendment No. 2 and the Base Agreement, the terms of this Amendment shall prevail.""",
        "related_document_ids": ["DOC-C7-01"]
    }
    documents.append(d7_2)
    add_rel(d7_2["document_id"], d7_1["document_id"], "supersedes", "Amendment No. 2 supersedes Clause 12.1 of 2021 Base Agreement")
    add_rel(d7_2["document_id"], "RULE-SEC-004", "satisfies", "Amended Clause 12.1 enforces 72-hour notification")

    assessments.append({
        "assessment_id": "ASSESS-C7-001",
        "case_id": case_7_id,
        "rule_id": "RULE-SEC-004",
        "rule_title": "Security Incident Notification Within 72 Hours",
        "expected_status": "Compliant",
        "applicability_result": "Applicable (Vendor processes EU cloud data)",
        "relevant_document_ids": ["DOC-C7-01", "DOC-C7-02"],
        "relevant_passages": [
            "Base Agreement Clause 12.1 (Superseded): 'notify customer in writing within fourteen (14) calendar days...'",
            "Amendment No. 2 Section 2: 'Clause 12.1 is hereby deleted in its entirety and replaced with: Vendor shall notify Customer in writing... within seventy-two (72) hours...'"
        ],
        "reasoning_steps": [
            "Step 1: Identified apparent initial conflict: Base Agreement 2021 allowed 14 days, which would be non-compliant.",
            "Step 2: Inspected subsequent document family; located executed Amendment No. 2 dated December 1, 2023.",
            "Step 3: Applied legal precedence rule (RULE-SEC-021): Subsequent executed amendment explicitly deleted and superseded original Clause 12.1.",
            "Step 4: Governing term in force is the amended 72-hour commitment.",
            "Conclusion: Compliant. The active governing contract terms fulfill the 72-hour requirement."
        ],
        "evidence_sufficiency": "Strong",
        "missing_evidence": "None.",
        "contradictions": "Base agreement contained 14-day clause, but was formally resolved and superseded by Amendment No. 2.",
        "recommended_action": "Archive Base 2021 clause; tag Amendment No. 2 as active governing covenant.",
        "review_notes": "Demonstrates multi-document amendment reasoning."
    })

    # =========================================================================
    # SCENARIO 8: CASE-008 (Ambiguous Wording: Indeterminate)
    # Vendor: VEN-002 (Apex AI) | Org: ORG-BETA (NovuHealth)
    # Rule: RULE-SEC-025 (AI Model Governance & Zero Training on Client Data)
    # Status: INDETERMINATE
    # =========================================================================
    case_8_id = "CASE-2024-008"

    d8_1 = {
        "document_id": "DOC-C8-01",
        "case_id": case_8_id,
        "organization_id": "ORG-BETA",
        "vendor_id": "VEN-002",
        "document_type": "vendor_contract",
        "title": "Enterprise AI Analytics Agreement — Apex AI",
        "source_type": "Synthetic Contract",
        "version": "1.0",
        "issue_date": "2024-01-15",
        "effective_date": "2024-02-01",
        "expiry_date": "2025-02-01",
        "full_text": """APEX AI ENTERPRISE MASTER AGREEMENT
CLAUSE 19. ARTIFICIAL INTELLIGENCE TRAINING AND MODEL IMPROVEMENT
19.3 Data Usage Rights: Customer acknowledges that Vendor may utilize aggregate customer telemetry, anonymized session patterns, and derived statistical embeddings to reasonably improve and optimize general model performance, provided that Customer's identifiable raw source records are not retained in public foundational weight distributions without appropriate technical filtering.""",
        "related_document_ids": ["RULE-SEC-025"]
    }
    documents.append(d8_1)

    assessments.append({
        "assessment_id": "ASSESS-C8-001",
        "case_id": case_8_id,
        "rule_id": "RULE-SEC-025",
        "rule_title": "AI Model Governance and Customer Data Isolation",
        "expected_status": "Indeterminate",
        "applicability_result": "Applicable (Vendor provides machine learning models processing customer inputs)",
        "relevant_document_ids": ["DOC-C8-01"],
        "relevant_passages": [
            "Contract Clause 19.3: 'Vendor may utilize aggregate customer telemetry, anonymized session patterns, and derived statistical embeddings to reasonably improve and optimize general model performance, provided that raw source records are not retained... without appropriate technical filtering.'"
        ],
        "reasoning_steps": [
            "Step 1: Rule RULE-SEC-025 strictly bars using customer confidential prompts and data to train or improve models without explicit opt-in.",
            "Step 2: Contract Clause 19.3 uses ambiguous legal phrasing: 'derived statistical embeddings to reasonably improve... model performance' and 'without appropriate technical filtering'.",
            "Step 3: Neither 'derived statistical embeddings' nor 'appropriate technical filtering' is defined with technical specificity.",
            "Step 4: It cannot be determined from this language whether customer confidential data is isolated from foundational model training or if latent representation learning violates the zero-training mandate.",
            "Conclusion: Indeterminate due to ambiguous contractual phrasing."
        ],
        "evidence_sufficiency": "Weak",
        "missing_evidence": "AI Data Isolation Technical Addendum specifying exact embedding retention and fine-tuning boundaries.",
        "contradictions": "Ambiguous clause blends improvement rights with filtering provisos.",
        "recommended_action": "Do not sign or accept without an explicit Zero-Data-Retention (ZDR) and No-Training Addendum.",
        "review_notes": "Highlights ambiguous wording detection."
    })

    return documents, relationships, assessments


def generate_and_save_synthetic_dataset(output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Generate the full dataset files and persist to JSON."""
    if not output_dir:
        output_dir = DATA_DIR

    os.makedirs(output_dir, exist_ok=True)
    rules = load_rules(os.path.join(output_dir, "rules.json"))
    
    docs, rels, assesses = generate_core_scenarios(rules)

    docs_file = os.path.join(output_dir, "documents.json")
    rels_file = os.path.join(output_dir, "relationships.json")
    assess_file = os.path.join(output_dir, "assessments.json")

    with open(docs_file, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

    with open(rels_file, "w", encoding="utf-8") as f:
        json.dump(rels, f, indent=2)

    with open(assess_file, "w", encoding="utf-8") as f:
        json.dump(assesses, f, indent=2)

    return {
        "status": "success",
        "rules_count": len(rules),
        "documents_count": len(docs),
        "relationships_count": len(rels),
        "assessments_count": len(assesses),
        "files_written": [docs_file, rels_file, assess_file]
    }


if __name__ == "__main__":
    res = generate_and_save_synthetic_dataset()
    print("Dataset generation result:", res)
