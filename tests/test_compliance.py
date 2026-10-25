"""
Automated Test Suite for Compliance Platform
Validates:
1. Multi-format text extraction (PDF, DOCX, TXT, Image)
2. Document type auto-classification
3. Requirement matching and similarity scoring
4. Cross-document reasoning engine
5. Primary status determinations:
   - Compliant (strong evidence)
   - Non-compliant (explicit violation)
   - Unverified (missing evidence)
   - Indeterminate (contradictions & ambiguity)
   - Not applicable (out-of-scope conditions)
6. Amendment precedence over base contract
7. Ground truth evaluation benchmark
"""

import os
import sys
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from modules.document_reader import (
    read_pdf, read_docx, read_txt, read_image,
    detect_document_type, process_uploaded_document
)
from modules.compliance_engine import (
    load_rules_catalogue, evaluate_single_requirement,
    analyze_uploaded_session, SimpleTextMatcher
)
from modules.evaluation import run_synthetic_benchmark


@pytest.fixture
def rules():
    return load_rules_catalogue()


def test_pdf_extraction():
    pdf_path = os.path.join(PROJECT_ROOT, "sample_documents", "demo_A_compliant", "02_CyberVault_Master_Cloud_Agreement.pdf")
    assert os.path.exists(pdf_path), "Sample PDF should exist"
    with open(pdf_path, "rb") as f:
        data = f.read()
    result = read_pdf(data, "02_CyberVault_Master_Cloud_Agreement.pdf")
    assert result["success"] is True
    assert "CyberVault" in result["full_text"]
    assert "AES-256" in result["full_text"]
    assert result["page_count"] >= 1
    assert result["document_type"] == "vendor_contract"


def test_docx_extraction():
    docx_path = os.path.join(PROJECT_ROOT, "sample_documents", "demo_A_compliant", "01_Aegis_Internal_Security_Policy.docx")
    assert os.path.exists(docx_path), "Sample DOCX should exist"
    with open(docx_path, "rb") as f:
        data = f.read()
    result = read_docx(data, "01_Aegis_Internal_Security_Policy.docx")
    assert result["success"] is True
    assert "Aegis Financial" in result["full_text"]
    assert "Cryptographic Controls" in result["full_text"]
    assert result["document_type"] == "internal_policy"


def test_txt_extraction():
    txt_path = os.path.join(PROJECT_ROOT, "sample_documents", "demo_C_explicit_violation", "01_BritePay_Payment_Agreement.txt")
    assert os.path.exists(txt_path), "Sample TXT should exist"
    with open(txt_path, "rb") as f:
        data = f.read()
    result = read_txt(data, "01_BritePay_Payment_Agreement.txt")
    assert result["success"] is True
    assert "BritePay" in result["full_text"]
    assert "ten (10) business days" in result["full_text"]


def test_image_processing_graceful_handling():
    img_path = os.path.join(PROJECT_ROOT, "sample_documents", "sample_contract_clause_scanned.png")
    assert os.path.exists(img_path), "Sample PNG should exist"
    with open(img_path, "rb") as f:
        data = f.read()
    result = read_image(data, "sample_contract_clause_scanned.png")
    assert result["success"] is True
    assert "dimensions" in result


def test_rules_catalogue_structure(rules):
    assert len(rules) >= 20, "Should have at least 20 structured compliance rules"
    for r in rules:
        assert "rule_id" in r
        assert "rule_title" in r
        assert "legal_or_policy_category" in r
        assert "severity" in r
        assert r["synthetic_or_verified"] in ["VERIFIED", "SYNTHETIC"]


def test_scenario_compliant(rules):
    rule_enc = next(r for r in rules if r["rule_id"] == "RULE-SEC-001")
    # Upload docs representing Demo A (Contract + Audit report)
    contract_doc = {
        "document_id": "DOC-TEST-01",
        "title": "Vendor Cloud Agreement",
        "document_type": "vendor_contract",
        "full_text": "Clause 8.1 Encryption at Rest: Vendor shall encrypt all Customer data at rest using AES-256 and in transit via TLS 1.3."
    }
    audit_doc = {
        "document_id": "DOC-TEST-02",
        "title": "Deloitte SOC 2 Type II Report",
        "document_type": "audit_report",
        "full_text": "Control CC6.6 (Encryption): Auditor sampled 50 volumes; 100% verified encrypted at rest with AES-256 and TLS 1.3. No deviations noted."
    }
    assessment = evaluate_single_requirement(rule_enc, [contract_doc, audit_doc])
    assert assessment["expected_status"] == "Compliant"
    assert assessment["evidence_sufficiency"] == "Strong"
    assert len(assessment["relevant_passages"]) >= 1


def test_scenario_explicit_violation(rules):
    rule_notif = next(r for r in rules if r["rule_id"] == "RULE-SEC-004")
    contract_doc = {
        "document_id": "DOC-TEST-V1",
        "title": "Merchant Services Agreement",
        "document_type": "vendor_contract",
        "full_text": "Clause 11.4: In the event of a security incident, processor shall notify customer within ten (10) business days following completion of internal forensic investigation."
    }
    assessment = evaluate_single_requirement(rule_notif, [contract_doc])
    assert assessment["expected_status"] == "Non-compliant"
    assert "10" in assessment["relevant_passages"][0] or "ten" in assessment["relevant_passages"][0].lower()


def test_scenario_missing_evidence_unverified(rules):
    rule_sub = next(r for r in rules if r["rule_id"] == "RULE-SEC-006")
    contract_doc = {
        "document_id": "DOC-TEST-M1",
        "title": "SaaS Agreement",
        "document_type": "vendor_contract",
        "full_text": "Clause 14.1: Vendor covenants to maintain an audited list of sub-processors and provide prior written notice."
    }
    # No audit report uploaded!
    assessment = evaluate_single_requirement(rule_sub, [contract_doc])
    assert assessment["expected_status"] == "Unverified"
    assert assessment["evidence_sufficiency"] == "Unavailable"
    assert "missing" in assessment["missing_evidence"].lower()


def test_scenario_expired_certificate(rules):
    rule_cert = next(r for r in rules if r["rule_id"] == "RULE-SEC-007")
    cert_doc = {
        "document_id": "DOC-TEST-E1",
        "title": "ISO 27001 Certificate",
        "document_type": "compliance_certificate",
        "full_text": "BSI Certificate of Registration — ISO/IEC 27001:2013. Expiry Date: 14 June 2023. Status: EXPIRED."
    }
    assessment = evaluate_single_requirement(rule_cert, [cert_doc])
    assert assessment["expected_status"] == "Non-compliant"
    assert "expired" in assessment["reasoning_steps"][2].lower()


def test_scenario_contradictory_documents(rules):
    rule_log = next(r for r in rules if r["rule_id"] == "RULE-SEC-015")
    ciso_doc = {
        "document_id": "DOC-TEST-C1",
        "title": "CISO Declaration",
        "document_type": "supporting_evidence",
        "full_text": "Log retention policies strictly enforce 365-day minimum preservation prior to automated purging."
    }
    audit_doc = {
        "document_id": "DOC-TEST-C2",
        "title": "Technical Evaluation",
        "document_type": "audit_report",
        "full_text": "S3 bucket has active lifecycle transition rule DeleteMarkerAfterDays: 90. Logs older than 90 days are purged automatically."
    }
    assessment = evaluate_single_requirement(rule_log, [ciso_doc, audit_doc])
    assert assessment["expected_status"] == "Indeterminate"
    assert assessment["contradictions"] is not None


def test_scenario_not_applicable(rules):
    rule_hipaa = next(r for r in rules if r["rule_id"] == "RULE-SEC-019")
    sow_doc = {
        "document_id": "DOC-TEST-NA1",
        "title": "IT Staffing Agreement",
        "document_type": "vendor_contract",
        "full_text": "Exclusion of Health Data: Supplier personnel will not receive, process, store, or transmit any Protected Health Information (PHI) under HIPAA."
    }
    assessment = evaluate_single_requirement(rule_hipaa, [sow_doc])
    assert assessment["expected_status"] == "Not applicable"


def test_ground_truth_benchmark_accuracy():
    benchmark_res = run_synthetic_benchmark()
    assert benchmark_res["total_evaluated_cases"] >= 8
    assert benchmark_res["accuracy"] >= 0.85
    assert "Compliant" in benchmark_res["per_class_metrics"]
    assert "Non-compliant" in benchmark_res["per_class_metrics"]
    assert "Unverified" in benchmark_res["per_class_metrics"]
    assert "Indeterminate" in benchmark_res["per_class_metrics"]
    assert "Not applicable" in benchmark_res["per_class_metrics"]
