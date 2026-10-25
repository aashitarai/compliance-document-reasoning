"""
Script to generate all 99 GDPR Rules into data/rules.json, preserving existing benchmark rules.
Each rule includes:
- rule_id: RULE-GDPR-001 through RULE-GDPR-099
- rule_title: Article Title
- chapter: Chapter 1 to 11
- section: Section name if applicable
- source_name: Regulation (EU) 2016/679 (GDPR)
- source_reference_or_url: https://gdpr-info.eu/art-X-gdpr/
- jurisdiction: European Union / Global
- legal_or_policy_category: GDPR - <Chapter Name>
- rule_text: Comprehensive statutory requirement
- required_action_or_control: Specific operational/contractual control
- evidence_requirements: List of typical audit artifacts
- severity: Critical / High / Medium
- synthetic_or_verified: VERIFIED
"""

import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(PROJECT_ROOT, "data", "rules.json")

# 99 GDPR Articles Metadata (Articles 1 - 99)
GDPR_ARTICLES = [
    # CHAPTER 1
    (1, "Chapter 1 General provisions", None, "Subject-matter and objectives",
     "Lays down rules relating to the protection of natural persons with regard to the processing of personal data and rules relating to the free movement of personal data.",
     "Establish organizational privacy governance protecting fundamental rights and freedoms of natural persons.",
     ["Data Protection Policy", "Privacy Governance Charter"], "Medium"),
    (2, "Chapter 1 General provisions", None, "Material scope",
     "Applies to the processing of personal data wholly or partly by automated means and to the processing other than by automated means which form part of a filing system.",
     "Determine whether processing falls within material scope; ensure exclusion of purely personal or household activities.",
     ["Scope Assessment Document", "Data Flow Inventory"], "Medium"),
    (3, "Chapter 1 General provisions", None, "Territorial scope",
     "Applies to processing of personal data in the context of an establishment of a controller or processor in the Union, or targeting individuals in the Union.",
     "Document territorial applicability including EU establishment or offering of goods/services or monitoring behavior within the EU.",
     ["Territorial Scope Evaluation", "Article 27 EU Representative Appointment"], "High"),
    (4, "Chapter 1 General provisions", None, "Definitions",
     "Establishes binding statutory definitions for personal data, processing, restriction, profiling, pseudonymisation, filing system, controller, processor, and recipient.",
     "Adopt statutory definitions in all corporate policies, DPAs, and vendor agreements.",
     ["Data Protection Definitions Appendix", "Corporate Data Glossary"], "Low"),

    # CHAPTER 2
    (5, "Chapter 2 Principles", None, "Principles relating to processing of personal data",
     "Personal data must be processed lawfully, fairly, and transparently, collected for specified explicit purposes, limited to what is necessary, accurate, kept only as long as necessary, and integrity/confidentiality guaranteed.",
     "Implement controls for lawfulness, purpose limitation, data minimisation, accuracy, storage limitation, and integrity/confidentiality (AES-256/TLS 1.3).",
     ["Privacy Policy", "Data Minimisation Guidelines", "Storage Retention Schedule", "Encryption Standard"], "Critical"),
    (6, "Chapter 2 Principles", None, "Lawfulness of processing",
     "Processing is lawful only if at least one legal basis applies: consent, contract performance, legal obligation, vital interests, public interest, or legitimate interests.",
     "Identify and record valid legal basis prior to commencing any personal data processing operation.",
     ["Record of Legal Basis for Processing", "Legitimate Interests Assessment (LIA)"], "Critical"),
    (7, "Chapter 2 Principles", None, "Conditions for consent",
     "Where processing is based on consent, the controller must be able to demonstrate that the data subject has consented; consent must be freely given, specific, informed, and unambiguous.",
     "Maintain auditable consent logs and provide clear mechanisms for data subjects to withdraw consent at any time without detriment.",
     ["Consent Management System Logs", "Opt-In Checkbox Documentation", "Withdrawal Mechanism Proof"], "High"),
    (8, "Chapter 2 Principles", None, "Conditions applicable to child’s consent in relation to information society services",
     "Processing of personal data of a child below the age of 16 years (or lower national age down to 13) is lawful only if consent is given or authorized by the holder of parental responsibility.",
     "Implement verifiable parental consent verification systems and age-gating mechanisms for information society services.",
     ["Age Verification System Architecture", "Parental Consent Verification Mechanism"], "High"),
    (9, "Chapter 2 Principles", None, "Processing of special categories of personal data",
     "Prohibits processing of personal data revealing racial or ethnic origin, political opinions, religious beliefs, genetic data, biometric data, health data, or sexual orientation unless strict Article 9(2) exceptions apply.",
     "Enforce heightened security, encryption, role-based access control, and explicit statutory exemptions for sensitive personal data.",
     ["Article 9 Exemption Documentation", "Special Category Data Registry", "Enhanced Access Control Logs"], "Critical"),
    (10, "Chapter 2 Principles", None, "Processing of personal data relating to criminal convictions and offences",
     "Processing of personal data relating to criminal convictions and offences shall be carried out only under the control of official authority or authorized by Union or Member State law.",
     "Ensure criminal record checks and background screenings are strictly conducted under authorized statutory frameworks.",
     ["Background Check Policy", "Statutory Authorization Documentation"], "High"),
    (11, "Chapter 2 Principles", None, "Processing which does not require identification",
     "If the purposes for which a controller processes personal data do not require the identification of a data subject, the controller shall not be obliged to maintain or acquire additional information.",
     "Ensure data subject rights are appropriately handled when processing pseudonymised or non-identifiable data.",
     ["De-Identification Policy", "Pseudonymisation Technical Standard"], "Medium"),

    # CHAPTER 3 - Section 1
    (12, "Chapter 3 Rights of the data subject", "Section 1 Transparency and modalities", "Transparent information, communication and modalities for the exercise of the rights of the data subject",
     "The controller shall take appropriate measures to provide any information in a concise, transparent, intelligible and easily accessible form, using clear and plain language.",
     "Publish accessible privacy notices and establish streamlined operational channels for data subjects to exercise rights free of charge within 1 month.",
     ["Data Subject Rights Request (DSR) Portal", "Transparency Communication Protocol"], "High"),

    # CHAPTER 3 - Section 2
    (13, "Chapter 3 Rights of the data subject", "Section 2 Information and access to personal data", "Information to be provided where personal data are collected from the data subject",
     "Where personal data are collected directly from the data subject, controller must provide identity, contact details of DPO, purposes, legal basis, recipients, and retention periods at collection time.",
     "Provide layered privacy disclosures at point of collection including identity, purpose, legal basis, recipients, and international transfers.",
     ["Point-of-Collection Privacy Notices", "Terms of Service Privacy Disclosures"], "High"),
    (14, "Chapter 3 Rights of the data subject", "Section 2 Information and access to personal data", "Information to be provided where personal data have not been obtained from the data subject",
     "Where personal data have not been obtained directly, controller must provide categories of data, source, and statutory disclosures within a reasonable period (maximum 1 month).",
     "Establish automated notification mechanisms for third-party or indirect data ingestion sources within 30 days.",
     ["Indirect Ingestion Privacy Notice", "Third-Party Data Source Registry"], "High"),
    (15, "Chapter 3 Rights of the data subject", "Section 2 Information and access to personal data", "Right of access by the data subject",
     "The data subject shall have the right to obtain confirmation as to whether personal data concerning him or her are being processed, and access to the personal data and supplementary details.",
     "Provide automated export tools or DSR workflows to furnish copy of processed personal data within 30 days.",
     ["DSR Access Request SOP", "Data Subject Export Logs"], "High"),

    # CHAPTER 3 - Section 3
    (16, "Chapter 3 Rights of the data subject", "Section 3 Rectification and erasure", "Right to rectification",
     "The data subject shall have the right to obtain from the controller without undue delay the rectification of inaccurate personal data.",
     "Provide self-service profile update portals or operational ticketing workflows to rectify inaccurate records across all databases.",
     ["Data Rectification SOP", "Database Update Audit Logs"], "Medium"),
    (17, "Chapter 3 Rights of the data subject", "Section 3 Rectification and erasure", "Right to erasure (‘right to be forgotten’)",
     "The data subject shall have the right to obtain from the controller the erasure of personal data without undue delay where grounds such as withdrawal of consent or obsolescence apply.",
     "Implement cryptographic deletion and database purge scripts cascading across backups, replicas, and sub-tier processors.",
     ["Erasure / Right-to-be-Forgotten Policy", "Automated Purge Scripts Verification", "Downstream Processor Erasure Notifications"], "Critical"),
    (18, "Chapter 3 Rights of the data subject", "Section 3 Rectification and erasure", "Right to restriction of processing",
     "The data subject shall have the right to obtain restriction of processing where accuracy is contested, processing is unlawful, or data is needed for legal claims.",
     "Implement database logical flags or segregated storage quarantine to freeze processing during dispute resolution.",
     ["Processing Restriction Mechanism", "Database Quarantine Schema"], "Medium"),
    (19, "Chapter 3 Rights of the data subject", "Section 3 Rectification and erasure", "Notification obligation regarding rectification or erasure of personal data or restriction of processing",
     "The controller shall communicate any rectification, erasure or restriction of processing to each recipient to whom the personal data have been disclosed.",
     "Establish automated notification webhooks and tracking logs notifying all downstream subprocessors of erasures or rectifications.",
     ["Subprocessor Erasure Notification Logs", "Third-Party Sync Webhook Architecture"], "High"),
    (20, "Chapter 3 Rights of the data subject", "Section 3 Rectification and erasure", "Right to data portability",
     "The data subject shall have the right to receive personal data concerning him or her in a structured, commonly used and machine-readable format (e.g. JSON, CSV, XML).",
     "Implement automated machine-readable export endpoints (JSON/CSV) permitting direct transmission to another controller.",
     ["Data Portability API Documentation", "Automated JSON/CSV Export Verification"], "High"),

    # CHAPTER 3 - Section 4
    (21, "Chapter 3 Rights of the data subject", "Section 4 Right to object and automated individual decision-making", "Right to object",
     "The data subject shall have the right to object at any time to processing of personal data concerning him or her based on legitimate interests or direct marketing.",
     "Provide one-click unsubscribe links for marketing and documented assessment procedures to cease processing upon legitimate objection.",
     ["One-Click Opt-Out Mechanism", "Objection Handling Protocol"], "High"),
    (22, "Chapter 3 Rights of the data subject", "Section 4 Right to object and automated individual decision-making", "Automated individual decision-making, including profiling",
     "The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her.",
     "Implement human-in-the-loop oversight, explainability mechanisms, and the right to contest automated underwriting or scoring algorithms.",
     ["AI Governance Charter", "Human-in-the-Loop Review SOP", "Automated Decision System Impact Assessment"], "Critical"),

    # CHAPTER 3 - Section 5
    (23, "Chapter 3 Rights of the data subject", "Section 5 Restrictions", "Restrictions",
     "Union or Member State law may restrict the scope of obligations and rights when necessary and proportionate to safeguard national security, defense, public security, or judicial proceedings.",
     "Document formal statutory exemptions or judicial mandates justifying any lawful restriction of data subject rights.",
     ["Legal Exception Register", "Judicial Order Response Protocol"], "Low"),

    # CHAPTER 4 - Section 1
    (24, "Chapter 4 Controller and processor", "Section 1 General obligations", "Responsibility of the controller",
     "The controller shall implement appropriate technical and organisational measures to ensure and to be able to demonstrate that processing is performed in accordance with this Regulation.",
     "Maintain an overarching information security management system (ISMS) and regular audit review schedules.",
     ["ISMS Framework Documentation", "Executive Compliance Verification Attestation"], "Critical"),
    (25, "Chapter 4 Controller and processor", "Section 1 General obligations", "Data protection by design and by default",
     "The controller shall implement appropriate technical and organisational measures, such as pseudonymisation and data minimisation, designed to implement data-protection principles effectively.",
     "Integrate privacy impact checks into CI/CD pipelines, enforce default private settings, and mandate automated data tokenization.",
     ["Privacy by Design Architectural Blueprint", "Default Privacy Configuration Audit", "Tokenization Architecture"], "High"),
    (26, "Chapter 4 Controller and processor", "Section 1 General obligations", "Joint controllers",
     "Where two or more controllers jointly determine the purposes and means of processing, they shall determine their respective responsibilities by means of an arrangement between them.",
     "Execute formal Joint Controller Agreements defining respective transparent disclosures and contact points.",
     ["Joint Controller Agreement (JCA)", "Article 26 Allocation Matrix"], "High"),
    (27, "Chapter 4 Controller and processor", "Section 1 General obligations", "Representatives of controllers or processors not established in the Union",
     "Controllers or processors not established in the Union must designate in writing a representative in the Union under Article 3(2) conditions.",
     "Execute formal mandate with an EU-established representative and list contact details in public privacy policies.",
     ["Article 27 EU Representative Mandate Agreement", "Supervisory Authority Contact Channel"], "High"),
    (28, "Chapter 4 Controller and processor", "Section 1 General obligations", "Processor",
     "Processing by a processor shall be governed by a contract (Data Processing Agreement) binding the processor to the controller with mandatory covenants under Article 28(3).",
     "Execute binding DPAs mandating instruction-based processing, confidentiality, security measures, subprocessor restrictions, audit rights, and post-termination erasure.",
     ["Data Processing Agreement (DPA)", "Article 28 Mandatory Terms Addendum", "Subprocessor Authorisation Protocol"], "Critical"),
    (29, "Chapter 4 Controller and processor", "Section 1 General obligations", "Processing under the authority of the controller or processor",
     "The processor and any person acting under the authority of the controller or of the processor shall not process those data except on instructions from the controller.",
     "Enforce role-based access control (RBAC), signed non-disclosure agreements (NDAs), and privileged session logging.",
     ["Employee Confidentiality Undertakings", "Access Control Policy", "Privileged Session Monitoring Logs"], "High"),
    (30, "Chapter 4 Controller and processor", "Section 1 General obligations", "Records of processing activities",
     "Each controller and processor shall maintain a record of processing activities under its responsibility (RoPA) containing purposes, categories, recipients, transfers, and security measures.",
     "Maintain an up-to-date central Record of Processing Activities (RoPA) covering all active data workflows.",
     ["Record of Processing Activities (RoPA) Registry", "Annual RoPA Review Audit"], "High"),
    (31, "Chapter 4 Controller and processor", "Section 1 General obligations", "Cooperation with the supervisory authority",
     "The controller and the processor and, where applicable, their representatives, shall cooperate, on request, with the supervisory authority in the performance of its tasks.",
     "Establish formal incident coordination protocols and designate regulatory liaison officers for Data Protection Authorities (DPAs).",
     ["Regulatory Inquiry Response Protocol", "Supervisory Liaison Workflow"], "Medium"),

    # CHAPTER 4 - Section 2
    (32, "Chapter 4 Controller and processor", "Section 2 Security of personal data", "Security of processing",
     "The controller and processor shall implement appropriate technical and organisational measures including pseudonymisation, AES-256 encryption, confidentiality, resilience, and regular vulnerability testing.",
     "Enforce AES-256 encryption at rest, TLS 1.3 in transit, automated vulnerability scanning, and annual penetration testing.",
     ["SOC 2 Type II Report", "Penetration Testing Audit Report", "Cryptographic Architecture Review", "ISO 27001 Certificate"], "Critical"),
    (33, "Chapter 4 Controller and processor", "Section 2 Security of personal data", "Notification of a personal data breach to the supervisory authority",
     "In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the competent supervisory authority.",
     "Establish automated breach detection and strictly enforce statutory 72-hour notification ceiling in vendor contracts and incident protocols.",
     ["Incident Response Plan (IRP)", "72-Hour Breach Escalation SLA", "Breach Notification Log", "Forensic Retrospective Audit"], "Critical"),
    (34, "Chapter 4 Controller and processor", "Section 2 Security of personal data", "Communication of a personal data breach to the data subject",
     "When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay.",
     "Draft emergency data subject breach notification templates and automated broadcast channels.",
     ["High-Risk Breach Assessment SOP", "Data Subject Breach Notification Template"], "High"),

    # CHAPTER 4 - Section 3
    (35, "Chapter 4 Controller and processor", "Section 3 Data protection impact assessment and prior consultation", "Data protection impact assessment",
     "Where processing is likely to result in a high risk, the controller shall, prior to processing, carry out a Data Protection Impact Assessment (DPIA).",
     "Mandate formal DPIA assessments prior to rolling out new AI models, biometrics, large-scale surveillance, or sensitive data systems.",
     ["Data Protection Impact Assessment (DPIA) Report", "Risk Treatment Plan"], "Critical"),
    (36, "Chapter 4 Controller and processor", "Section 3 Data protection impact assessment and prior consultation", "Prior consultation",
     "The controller shall consult the supervisory authority prior to processing where a DPIA indicates that the processing would result in a high risk in the absence of measures taken by the controller.",
     "Establish prior consultation workflow with lead supervisory authorities for residual high-risk operations.",
     ["Supervisory Prior Consultation Dossier", "Regulatory Guidance Records"], "High"),

    # CHAPTER 4 - Section 4
    (37, "Chapter 4 Controller and processor", "Section 4 Data protection officer", "Designation of the data protection officer",
     "The controller and processor shall designate a data protection officer (DPO) where processing is carried out by a public authority or core activities require regular systematic monitoring or large scale sensitive data.",
     "Designate a qualified DPO, notify relevant Data Protection Authorities, and publish DPO contact coordinates.",
     ["DPO Formal Appointment Letter", "Supervisory Authority DPO Registration Proof"], "High"),
    (38, "Chapter 4 Controller and processor", "Section 4 Data protection officer", "Position of the data protection officer",
     "The controller and processor shall ensure that the DPO is involved in all privacy matters, operates independently without conflict of interest, and reports directly to highest management.",
     "Guarantee organizational independence, direct executive reporting, and resource budget for the DPO function.",
     ["DPO Governance Charter", "Executive Reporting Lines Chart"], "Medium"),
    (39, "Chapter 4 Controller and processor", "Section 4 Data protection officer", "Tasks of the data protection officer",
     "The DPO shall inform and advise the controller/processor, monitor compliance with GDPR, provide advice on DPIAs, and act as contact point for supervisory authorities.",
     "Maintain records of DPO oversight audits, employee privacy trainings, and DPIA consultations.",
     ["Annual DPO Compliance Report", "Privacy Training Completion Logs"], "Medium"),

    # CHAPTER 4 - Section 5
    (40, "Chapter 4 Controller and processor", "Section 5 Codes of conduct and certification", "Codes of conduct",
     "Associations and other bodies representing categories of controllers or processors may prepare codes of conduct to facilitate effective GDPR application.",
     "Align sectoral data processing with approved industry codes of conduct (e.g. EU Cloud Code of Conduct).",
     ["Adherence to Approved Code of Conduct Certificate", "Annual Self-Assessment Report"], "Low"),
    (41, "Chapter 4 Controller and processor", "Section 5 Codes of conduct and certification", "Monitoring of approved codes of conduct",
     "A body which has an appropriate level of expertise may monitor compliance with a code of conduct after accreditation by the competent supervisory authority.",
     "Submit annual compliance evidence to accredited monitoring bodies.",
     ["Code of Conduct Monitoring Audit", "Accredited Body Review Letter"], "Low"),
    (42, "Chapter 4 Controller and processor", "Section 5 Codes of conduct and certification", "Certification",
     "Establishment of data protection certification mechanisms and data protection seals/marks for demonstrating compliance by controllers and processors.",
     "Obtain accredited GDPR compliance certification (e.g. Europrivacy) or ISO/IEC 27701 certification.",
     ["Europrivacy Certificate", "ISO/IEC 27701 Privacy Information Management System Certificate"], "Medium"),
    (43, "Chapter 4 Controller and processor", "Section 5 Codes of conduct and certification", "Certification bodies",
     "Certification bodies accredited by supervisory authorities or national accreditation bodies shall issue and renew data protection certifications.",
     "Verify that third-party certification bodies hold active accreditation under EN-ISO/IEC 17065 and Article 43 GDPR.",
     ["Certification Body Accreditation Proof", "Formal Audit Scope Statement"], "Low"),

    # CHAPTER 5
    (44, "Chapter 5 Transfers of personal data to third countries or international organisations", None, "General principle for transfers",
     "Any transfer of personal data to a third country or international organisation shall take place only if conditions laid down in Chapter V are complied with.",
     "Audit all egress traffic and cloud regions to ensure personal data transfers to non-EEA jurisdictions comply with Chapter V safeguards.",
     ["Cross-Border Data Transfer Inventory", "Transfer Impact Assessment (TIA)"], "Critical"),
    (45, "Chapter 5 Transfers of personal data to third countries or international organisations", None, "Transfers on the basis of an adequacy decision",
     "A transfer of personal data to a third country or international organisation may take place where the Commission has decided that the third country ensures an adequate level of protection.",
     "Verify and record applicable European Commission Adequacy Decisions (e.g. EU-US Data Privacy Framework, UK, Japan, Switzerland).",
     ["Adequacy Decision Verification Record", "EU-US Data Privacy Framework Certification"], "High"),
    (46, "Chapter 5 Transfers of personal data to third countries or international organisations", None, "Transfers subject to appropriate safeguards",
     "In the absence of an adequacy decision, transfer may occur only if controller/processor provides appropriate safeguards, such as Standard Contractual Clauses (SCCs).",
     "Execute European Commission Standard Contractual Clauses (SCCs 2021/914) with supplementary technical safeguards (encryption, zero-knowledge keys).",
     ["Executed Standard Contractual Clauses (SCCs)", "Supplementary Technical Safeguards Review"], "Critical"),
    (47, "Chapter 5 Transfers of personal data to third countries or international organisations", None, "Binding corporate rules",
     "Supervisory authorities shall approve binding corporate rules (BCRs) for multinational corporate groups transferring data globally.",
     "Maintain approved BCR policies for intra-group global data transfers with annual compliance audits.",
     ["Approved Binding Corporate Rules (BCR)", "Lead Supervisory Authority Approval Decision"], "High"),
    (48, "Chapter 5 Transfers of personal data to third countries or international organisations", None, "Transfers or disclosures not authorised by Union law",
     "Any judgment of a court or tribunal or decision of an administrative authority of a third country requiring disclosure may only be recognized if based on an international agreement (e.g. MLAT).",
     "Establish legal review protocols blocking extra-territorial third-country warrants absent formal mutual legal assistance treaties (MLATs).",
     ["Government Access Request Policy", "Third-Country Subpoena Protocol"], "High"),
    (49, "Chapter 5 Transfers of personal data to third countries or international organisations", None, "Derogations for specific situations",
     "In absence of adequacy decision or appropriate safeguards, transfer may occur only on specific derogations (explicit consent, contract performance, public interest, defense of claims).",
     "Document narrow legal grounds and explicit consent when relying on Article 49 exceptional derogations.",
     ["Article 49 Derogation Assessment", "Explicit Cross-Border Transfer Consent Log"], "Medium"),
    (50, "Chapter 5 Transfers of personal data to third countries or international organisations", None, "International cooperation for the protection of personal data",
     "Commission and supervisory authorities shall take appropriate steps to develop international cooperation mechanisms with third-country privacy authorities.",
     "Maintain regulatory liaison documentation for multi-jurisdictional compliance cooperation.",
     ["International Regulatory Protocol Documentation"], "Low"),

    # CHAPTER 6 - Section 1
    (51, "Chapter 6 Independent supervisory authorities", "Section 1 Independent status", "Supervisory authority",
     "Each Member State shall provide for one or more independent public authorities to be responsible for monitoring the application of this Regulation.",
     "Identify and record lead and concerned supervisory authorities across all EU operational jurisdictions.",
     ["Supervisory Authority Jurisdiction Mapping", "Lead DPA Designation Matrix"], "Low"),
    (52, "Chapter 6 Independent supervisory authorities", "Section 1 Independent status", "Independence",
     "Each supervisory authority shall act with complete independence in performing its tasks and exercising its powers in accordance with this Regulation.",
     "Respect complete independence of supervisory authority investigations and mandates.",
     ["Supervisory Cooperation Policy"], "Low"),
    (53, "Chapter 6 Independent supervisory authorities", "Section 1 Independent status", "General conditions for the members of the supervisory authority",
     "Member States shall provide for each member of their supervisory authorities to be appointed by transparent procedure by their parliament or government.",
     "Regulatory administrative knowledge; no direct corporate action required.",
     ["Regulatory Framework Notice"], "Low"),
    (54, "Chapter 6 Independent supervisory authorities", "Section 1 Independent status", "Rules on the establishment of the supervisory authority",
     "Each Member State shall provide by law for the establishment, qualifications, term of office, and rules governing supervisory authority members.",
     "Regulatory administrative knowledge; reference national implementing laws.",
     ["National GDPR Implementation Review"], "Low"),

    # CHAPTER 6 - Section 2
    (55, "Chapter 6 Independent supervisory authorities", "Section 2 Competence, tasks and powers", "Competence",
     "Each supervisory authority shall be competent for the performance of tasks and exercise of powers conferred on it on the territory of its own Member State.",
     "Direct jurisdictional inquiries and filings to the competent territorial supervisory authority.",
     ["Jurisdictional Competence Filing Register"], "Low"),
    (56, "Chapter 6 Independent supervisory authorities", "Section 2 Competence, tasks and powers", "Competence of the lead supervisory authority",
     "The supervisory authority of the main establishment or single establishment of the controller or processor shall be competent to act as lead supervisory authority for cross-border processing.",
     "Document main establishment criteria (place of central administration) to establish One-Stop-Shop lead supervisory authority status.",
     ["Main Establishment Assessment Dossier", "Lead Supervisory Authority Confirmation"], "High"),
    (57, "Chapter 6 Independent supervisory authorities", "Section 2 Competence, tasks and powers", "Tasks",
     "Each supervisory authority shall monitor and enforce application of GDPR, promote public awareness, advise national institutions, and handle complaints.",
     "Establish internal tracking for public guidance, opinions, and decisions issued by supervisory authorities.",
     ["Regulatory Guidance Monitoring Log"], "Medium"),
    (58, "Chapter 6 Independent supervisory authorities", "Section 2 Competence, tasks and powers", "Powers",
     "Supervisory authorities possess investigative powers (audits, access to premises), corrective powers (warnings, reprimands, processing bans, fines), and authorization powers.",
     "Establish regulatory audit readiness procedures facilitating inspector access, document production, and corrective action plans.",
     ["DPA Audit Readiness SOP", "Corrective Action Governance Plan"], "High"),
    (59, "Chapter 6 Independent supervisory authorities", "Section 2 Competence, tasks and powers", "Activity reports",
     "Each supervisory authority shall draw up an annual activity report on its activities, including violations and sanctions.",
     "Review supervisory authority annual activity reports to assess regulatory enforcement trends and fine benchmarks.",
     ["Annual Enforcement Benchmarking Report"], "Low"),

    # CHAPTER 7 - Section 1
    (60, "Chapter 7 Cooperation and consistency", "Section 1 Cooperation", "Cooperation between the lead supervisory authority and the other supervisory authorities concerned",
     "The lead supervisory authority shall cooperate with other concerned supervisory authorities in an endeavor to reach consensus under the One-Stop-Shop mechanism.",
     "Coordinate cross-border incident notifications through the designated lead supervisory authority.",
     ["Cross-Border Incident Dossier", "One-Stop-Shop Regulatory Submissions"], "Medium"),
    (61, "Chapter 6 Independent supervisory authorities", "Section 1 Cooperation", "Mutual assistance",
     "Supervisory authorities shall provide each other with relevant information and mutual assistance in order to implement and apply this Regulation in a consistent manner.",
     "Maintain unified records capable of being produced during multi-authority mutual assistance proceedings.",
     ["Multi-Jurisdictional Regulatory Audit Trail"], "Low"),
    (62, "Chapter 7 Cooperation and consistency", "Section 1 Cooperation", "Joint operations of supervisory authorities",
     "Supervisory authorities may conduct joint operations, including joint investigations and joint enforcement measures.",
     "Maintain corporate protocol for handling joint investigative actions across multiple EU Member State authorities.",
     ["Joint Investigative Protocol SOP"], "Medium"),

    # CHAPTER 7 - Section 2
    (63, "Chapter 7 Cooperation and consistency", "Section 2 Consistency", "Consistency mechanism",
     "Supervisory authorities shall contribute to the consistent application of GDPR throughout the Union through the consistency mechanism set out in this section.",
     "Track consistency mechanism opinions regarding cross-border binding corporate rules and standard contractual clauses.",
     ["Consistency Mechanism Tracking Registry"], "Low"),
    (64, "Chapter 7 Cooperation and consistency", "Section 2 Consistency", "Opinion of the Board",
     "The European Data Protection Board (EDPB) shall issue opinions on draft decisions concerning codes of conduct, BCRs, standard clauses, and high-risk processing lists.",
     "Ensure internal policies align with published EDPB opinions and Article 64 guidelines.",
     ["EDPB Opinion Compliance Review"], "Medium"),
    (65, "Chapter 7 Cooperation and consistency", "Section 2 Consistency", "Dispute resolution by the Board",
     "The EDPB shall adopt binding decisions to resolve disputes between supervisory authorities on cross-border processing cases.",
     "Monitor EDPB binding dispute resolution decisions impacting corporate processing categories.",
     ["EDPB Binding Decision Legal Analysis"], "Low"),
    (66, "Chapter 7 Cooperation and consistency", "Section 2 Consistency", "Urgency procedure",
     "In exceptional circumstances, where a supervisory authority considers urgent need to act to protect data subjects, it may immediately adopt provisional measures.",
     "Establish emergency incident response procedures to comply with provisional regulatory injunctions within 24 hours.",
     ["Emergency Regulatory Compliance Response SOP"], "High"),
    (67, "Chapter 7 Cooperation and consistency", "Section 2 Consistency", "Exchange of information",
     "The Commission and supervisory authorities shall supply each other with any information necessary to improve GDPR consistency.",
     "Maintain standardized information export workflows for regulatory submissions.",
     ["Regulatory Data Submission Portal"], "Low"),

    # CHAPTER 7 - Section 3
    (68, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "European Data Protection Board",
     "The European Data Protection Board (EDPB) is established as an independent body of the Union with legal personality.",
     "Recognize EDPB guidance as authoritative source for interpreting EU privacy law.",
     ["EDPB Regulatory Baseline Register"], "Low"),
    (69, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Independence",
     "The EDPB shall act independently when performing its tasks or exercising its powers.",
     "Administrative statutory recognition; ensure compliance with EDPB guidelines.",
     ["Regulatory Independence Acknowledgment"], "Low"),
    (70, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Tasks of the Board",
     "The EDPB shall advise the Commission, issue guidelines, promote cooperation, approve BCRs, and maintain public electronic registers.",
     "Adopt EDPB binding guidelines on breach notification, DPIAs, profiling, and international transfers.",
     ["EDPB Guidelines Alignment Audit", "Regulatory Best Practices Matrix"], "Medium"),
    (71, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Reports",
     "The EDPB shall draw up an annual public report on the protection of natural persons with regard to processing in the Union and third countries.",
     "Review EDPB annual report for strategic compliance benchmarking.",
     ["EDPB Annual Report Compliance Review"], "Low"),
    (72, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Procedure",
     "The EDPB shall take decisions by simple majority of its members, or two-thirds majority for binding decisions.",
     "Procedural knowledge; track voting outcomes on significant enforcement mechanisms.",
     ["EDPB Procedural Tracking Notice"], "Low"),
    (73, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Chair",
     "The EDPB shall elect a chair and two deputy chairs by a two-thirds majority of its members for a five-year term.",
     "Administrative knowledge.",
     ["Regulatory Registry Entry"], "Low"),
    (74, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Tasks of the Chair",
     "The Chair shall convene and preside over EDPB meetings, ensure timely performance of tasks, and represent the Board.",
     "Administrative knowledge.",
     ["Regulatory Registry Entry"], "Low"),
    (75, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Secretariat",
     "The EDPB shall have a secretariat provided by the European Data Protection Supervisor (EDPS).",
     "Administrative knowledge.",
     ["Regulatory Registry Entry"], "Low"),
    (76, "Chapter 7 Cooperation and consistency", "Section 3 European data protection board", "Confidentiality",
     "The discussions of the Board shall be confidential where the Board deems it necessary.",
     "Maintain strict confidentiality of ongoing EDPB dispute resolution proceedings involving the organization.",
     ["Confidentiality Agreement for Regulatory Proceedings"], "Medium"),

    # CHAPTER 8
    (77, "Chapter 8 Remedies, liability and penalties", None, "Right to lodge a complaint with a supervisory authority",
     "Every data subject shall have the right to lodge a complaint with a supervisory authority if they consider their GDPR rights have been infringed.",
     "Maintain internal dispute escalation procedures to resolve data subject concerns prior to formal supervisory authority complaints.",
     ["Customer Privacy Grievance Procedure", "Complaint Escalation SLA"], "Medium"),
    (78, "Chapter 8 Remedies, liability and penalties", None, "Right to an effective judicial remedy against a supervisory authority",
     "Natural or legal persons have the right to an effective judicial remedy against a legally binding decision of a supervisory authority concerning them.",
     "Establish litigation response workflows for judicial appeals against administrative decisions.",
     ["Administrative Appeal Legal Protocol"], "Low"),
    (79, "Chapter 8 Remedies, liability and penalties", None, "Right to an effective judicial remedy against a controller or processor",
     "Data subjects have the right to an effective judicial remedy where they consider their rights have been infringed as a result of unlawful processing.",
     "Ensure contractual dispute resolution clauses provide appropriate jurisdiction without obstructing data subject statutory remedies.",
     ["Litigation Management Protocol", "Contractual Jurisdiction Review"], "High"),
    (80, "Chapter 8 Remedies, liability and penalties", None, "Representation of data subjects",
     "The data subject shall have the right to mandate a non-profit body or organization to lodge complaints and exercise rights on their behalf.",
     "Establish operational procedures to verify legal mandates and credentials of representative privacy organizations.",
     ["Representative Mandate Verification Protocol", "Collective Action SOP"], "Medium"),
    (81, "Chapter 8 Remedies, liability and penalties", None, "Suspension of proceedings",
     "Where a court is informed of proceedings concerning the same subject matter pending in another Member State, it may suspend its proceedings.",
     "Track concurrent multi-jurisdictional proceedings to request coordination or stay of proceedings.",
     ["Multi-Jurisdiction Litigation Register"], "Low"),
    (82, "Chapter 8 Remedies, liability and penalties", None, "Right to compensation and liability",
     "Any person who has suffered material or non-material damage as a result of an infringement shall have the right to receive compensation from the controller or processor.",
     "Maintain comprehensive cyber liability insurance coverage and clear contractual indemnification allocations in vendor agreements.",
     ["Cyber Risk Insurance Policy", "Contractual Indemnity and Liability Clause Review"], "Critical"),
    (83, "Chapter 8 Remedies, liability and penalties", None, "General conditions for imposing administrative fines",
     "Imposition of administrative fines up to 20,000,000 EUR or 4% of total worldwide annual turnover, whichever is higher, for severe infringements.",
     "Conduct continuous executive compliance audits to eliminate systemic deficiencies subject to maximum statutory turnover fines.",
     ["Executive Risk Heatmap", "Turnover Exposure Assessment", "Continuous Compliance Audit Report"], "Critical"),
    (84, "Chapter 8 Remedies, liability and penalties", None, "Penalties",
     "Member States shall lay down rules on other penalties applicable to infringements, particularly for infringements not subject to administrative fines.",
     "Ensure compliance with national criminal and civil privacy sanctions in each Member State of operation.",
     ["National Penalties Compliance Matrix"], "Medium"),

    # CHAPTER 9
    (85, "Chapter 9 Provisions relating to specific processing situations", None, "Processing and freedom of expression and information",
     "Member States shall reconcile the right to protection of personal data with the right to freedom of expression and information (journalistic, academic, artistic).",
     "Implement journalistic and editorial exemption assessments for media publishing and public commentary operations.",
     ["Journalistic Exemption Policy", "Editorial Review Protocol"], "Low"),
    (86, "Chapter 9 Provisions relating to specific processing situations", None, "Processing and public access to official documents",
     "Personal data in official documents held by a public authority may be disclosed in accordance with Union or Member State law on public access.",
     "Establish public records disclosure protocols balancing freedom of information with privacy redaction.",
     ["Public Records Redaction Protocol"], "Low"),
    (87, "Chapter 9 Provisions relating to specific processing situations", None, "Processing of the national identification number",
     "Member States may determine the specific conditions for the processing of a national identification number or any other identifier of general application.",
     "Enforce strict tokenization, access restrictions, and legal basis verification for national IDs (SSN, National Insurance, Tax ID).",
     ["National ID Security and Tokenization Standard"], "High"),
    (88, "Chapter 9 Provisions relating to specific processing situations", None, "Processing in the context of employment",
     "Member States may provide for more specific rules to ensure the protection of rights and freedoms regarding the processing of employees' personal data in employment.",
     "Implement workplace privacy policies, employee monitoring notices, and works council consultation protocols.",
     ["Employee Privacy Notice", "Workplace Monitoring Protocol", "Works Council Agreement"], "High"),
    (89, "Chapter 9 Provisions relating to specific processing situations", None, "Safeguards and derogations relating to processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes",
     "Processing for archiving, scientific or historical research, or statistical purposes shall be subject to appropriate safeguards including pseudonymisation.",
     "Implement automated data pseudonymisation, aggregation, and research ethics board reviews for scientific and statistical datasets.",
     ["Research Data Pseudonymisation Standard", "Ethics Committee Approval Register"], "Medium"),
    (90, "Chapter 9 Provisions relating to specific processing situations", None, "Obligations of secrecy",
     "Member States may adopt specific rules to set out powers of supervisory authorities regarding secrecy obligations (medical, legal, banking).",
     "Enforce legal professional privilege and medical secrecy protections across corporate communication tools.",
     ["Statutory Secrecy Protocol", "Privilege Logging SOP"], "Medium"),
    (91, "Chapter 9 Provisions relating to specific processing situations", None, "Existing data protection rules of churches and religious associations",
     "Where churches and religious associations apply comprehensive rules for protection of natural persons, such rules may continue provided they are brought into conformity with GDPR.",
     "Assess religious organization exemption scope if operating religious or community association systems.",
     ["Religious Association Exemption Review"], "Low"),

    # CHAPTER 10
    (92, "Chapter 10 Delegated acts and implementing acts", None, "Exercise of the delegation",
     "The power to adopt delegated acts is conferred on the Commission subject to conditions laid down in this Article.",
     "Track Commission delegated acts impacting GDPR standard contractual clauses or certification criteria.",
     ["Delegated Act Monitoring Log"], "Low"),
    (93, "Chapter 10 Delegated acts and implementing acts", None, "Committee procedure",
     "The Commission shall be assisted by a committee. That committee shall be a committee within the meaning of Regulation (EU) No 182/2011.",
     "Administrative knowledge.",
     ["Regulatory Committee Registry"], "Low"),

    # CHAPTER 11
    (94, "Chapter 11 Final provisions", None, "Repeal of Directive 95/46/EC",
     "Directive 95/46/EC is repealed. References to the repealed Directive shall be construed as references to this Regulation.",
     "Update legacy contracts and agreements to replace references to Directive 95/46/EC with Regulation (EU) 2016/679.",
     ["Legacy Contract Remediation Audit"], "Medium"),
    (95, "Chapter 11 Final provisions", None, "Relationship with Directive 2002/58/EC",
     "This Regulation shall not impose additional obligations on natural or legal persons where they are subject to specific obligations in Directive 2002/58/EC (ePrivacy).",
     "Coordinate GDPR compliance with ePrivacy cookie consent and electronic marketing rules.",
     ["Cookie Consent Management Audit", "ePrivacy Electronic Communications Standard"], "High"),
    (96, "Chapter 11 Final provisions", None, "Relationship with previously concluded Agreements",
     "International agreements involving the transfer of personal data to third countries concluded prior to 24 May 2016 shall remain in force until amended or revoked.",
     "Verify status of pre-2016 bilateral international agreements governing data transfer obligations.",
     ["Legacy International Agreement Audit"], "Low"),
    (97, "Chapter 11 Final provisions", None, "Commission reports",
     "By 25 May 2020 and every four years thereafter, the Commission shall submit a report on the evaluation and review of this Regulation to the European Parliament and Council.",
     "Review European Commission four-year GDPR evaluation reports for upcoming statutory amendments.",
     ["Commission Four-Year GDPR Review Evaluation"], "Low"),
    (98, "Chapter 11 Final provisions", None, "Review of other Union legal acts on data protection",
     "The Commission shall submit legislative proposals to amend other Union legal acts on the protection of personal data to ensure uniform protection.",
     "Monitor alignment between GDPR, EU AI Act, Data Act, and Digital Services Act.",
     ["EU Digital Legislation Coherence Review"], "Medium"),
    (99, "Chapter 11 Final provisions", None, "Entry into force and application",
     "This Regulation entered into force on the twentieth day following publication and has applied since 25 May 2018. It is binding in its entirety and directly applicable in all Member States.",
     "Maintain enterprise-wide operational compliance with all applicable GDPR mandates.",
     ["Annual Comprehensive GDPR Compliance Dossier"], "High")
]


def build_all_rules():
    existing_rules = []
    if os.path.exists(RULES_PATH):
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            existing_rules = json.load(f)

    print(f"Loaded {len(existing_rules)} existing rules.")

    # Keep all existing non-GDPR-duplicate rules (e.g. RULE-SEC-001 through RULE-SEC-025)
    kept_rules = []
    for r in existing_rules:
        # Keep security / SOC 2 / ISO benchmark rules
        if not r.get("rule_id", "").startswith("RULE-GDPR-"):
            kept_rules.append(r)

    print(f"Preserving {len(kept_rules)} benchmark rules (RULE-SEC-XXX).")

    # Now add all 99 GDPR Articles
    gdpr_rules = []
    for item in GDPR_ARTICLES:
        art_num, chapter, section, title, desc, control, ev_reqs, severity = item
        rule_id = f"RULE-GDPR-{art_num:03d}"
        url = f"https://gdpr-info.eu/art-{art_num}-gdpr/"

        # Keywords for semantic search
        kw = [
            f"Article {art_num}", f"Art. {art_num}", "GDPR", title.lower(),
            chapter.lower()
        ]
        if section:
            kw.append(section.lower())
        kw.extend([w.lower() for w in title.split() if len(w) > 3])

        rule_obj = {
            "rule_id": rule_id,
            "rule_title": f"GDPR Article {art_num}: {title}",
            "rule_text": desc,
            "source_type": "verified_statutory_standard",
            "source_name": "Regulation (EU) 2016/679 (GDPR)",
            "source_reference_or_url": url,
            "jurisdiction": "European Union / Global",
            "legal_or_policy_category": f"GDPR - {chapter.split()[1] if len(chapter.split()) > 1 else 'General'}",
            "chapter": chapter,
            "section": section,
            "article_number": art_num,
            "applicable_entity_types": ["controller", "processor", "vendor", "cloud_provider"],
            "applicability_conditions": f"Processing of personal data within territorial or material scope under GDPR Article {art_num}.",
            "required_action_or_control": control,
            "evidence_requirements": ev_reqs,
            "validity_or_deadline_rules": "Continuous regulatory validity under EU law.",
            "exceptions": "Statutory exemptions under Article 2(2) (purely personal activities) or Article 23 (Member State restrictions).",
            "severity": severity,
            "effective_date": "2018-05-25",
            "expiry_or_superseded_date": None,
            "version": "2016/679 Final",
            "synthetic_or_verified": "VERIFIED",
            "source_verification_status": "Statutory Law",
            "keywords": kw
        }
        gdpr_rules.append(rule_obj)

    final_rules = kept_rules + gdpr_rules
    print(f"Total rules after adding 99 GDPR articles: {len(final_rules)}")

    with open(RULES_PATH, "w", encoding="utf-8") as f:
        json.dump(final_rules, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved {len(final_rules)} rules to {RULES_PATH}.")


if __name__ == "__main__":
    build_all_rules()
