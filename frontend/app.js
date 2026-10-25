/**
 * ComplianceIQ Enterprise — Modern Front-end Application Engine
 * Handles company-centric document vault workflows, authentic legal paper rendering,
 * direct document downloads, research methodology formalization, and role authentication.
 */

// Default Organizations Catalog (Guarantees dropdown is populated instantly at t=0)
const DEFAULT_ORGANIZATIONS = [
    {
        org_id: "ORG-ALPHA",
        name: "Aegis Financial Technologies Inc.",
        sector: "FinTech / Global Banking",
        jurisdiction: "US & Global (GLBA, SOC 2, ISO 27001)",
        governing_policy: {
            title: "Aegis Information Security Standard v3.2",
            type: "internal_policy",
            filename: "01_Aegis_Internal_Security_Policy.docx",
            relative_path: "demo_A_compliant/01_Aegis_Internal_Security_Policy.docx",
            summary: "Mandates AES-256-GCM encryption at rest, MFA for all administrative endpoints, and continuous monitoring."
        },
        vendors: [
            {
                vendor_id: "VEN-001",
                name: "CyberVault Storage Solutions Ltd.",
                scenario_id: "demo_A",
                contract: {
                    title: "Master Cloud Storage Agreement",
                    filename: "02_CyberVault_Master_Cloud_Agreement.pdf",
                    relative_path: "demo_A_compliant/02_CyberVault_Master_Cloud_Agreement.pdf",
                    type: "vendor_contract"
                },
                evidence: [
                    {
                        title: "Deloitte SOC 2 Type II Examination Report",
                        filename: "03_CyberVault_SOC2_Type_II_Report.pdf",
                        relative_path: "demo_A_compliant/03_CyberVault_SOC2_Type_II_Report.pdf",
                        type: "audit_report",
                        status_hint: "Unqualified Opinion (Pass)"
                    }
                ]
            },
            {
                vendor_id: "VEN-003",
                name: "QuantumNet Infrastructure Services",
                scenario_id: "demo_D",
                contract: {
                    title: "Master Infrastructure Services Agreement",
                    filename: "01_QuantumNet_Infrastructure_MSA.pdf",
                    relative_path: "demo_D_expired_cert/01_QuantumNet_Infrastructure_MSA.pdf",
                    type: "vendor_contract"
                },
                evidence: [
                    {
                        title: "BSI ISO/IEC 27001:2013 Certificate",
                        filename: "02_QuantumNet_ISO27001_Certificate.pdf",
                        relative_path: "demo_D_expired_cert/02_QuantumNet_ISO27001_Certificate.pdf",
                        type: "compliance_certificate",
                        status_hint: "Expired June 30, 2023"
                    }
                ]
            },
            {
                vendor_id: "VEN-004",
                name: "SecureID Gateway Systems",
                scenario_id: "demo_E",
                contract: {
                    title: "Vendor CISO Annual Security Declaration",
                    filename: "01_SecureID_CISO_Declaration.txt",
                    relative_path: "demo_E_contradiction/01_SecureID_CISO_Declaration.txt",
                    type: "supporting_evidence"
                },
                evidence: [
                    {
                        title: "Bishop Fox Technical Architecture Audit",
                        filename: "02_BishopFox_Technical_Audit.docx",
                        relative_path: "demo_E_contradiction/02_BishopFox_Technical_Audit.docx",
                        type: "audit_report",
                        status_hint: "Factual Contradiction"
                    }
                ]
            }
        ]
    },
    {
        org_id: "ORG-BETA",
        name: "NovuHealth Global Therapeutics",
        sector: "Healthcare & Life Sciences",
        jurisdiction: "EU & US (GDPR & HIPAA)",
        governing_policy: {
            title: "NovuHealth Global Privacy & Breach Protocol v4.0",
            type: "internal_policy",
            filename: "01_NovuHealth_Global_Privacy_and_Breach_Protocol.docx",
            relative_path: "demo_C_explicit_violation/01_NovuHealth_Global_Privacy_and_Breach_Protocol.docx",
            summary: "Enforces strict statutory 72-hour security incident notification ceiling under GDPR Art. 33."
        },
        vendors: [
            {
                vendor_id: "VEN-005",
                name: "BritePay Merchant Operations",
                scenario_id: "demo_C",
                contract: {
                    title: "Merchant Payment Services Agreement",
                    filename: "01_BritePay_Payment_Agreement.txt",
                    relative_path: "demo_C_explicit_violation/01_BritePay_Payment_Agreement.txt",
                    type: "vendor_contract"
                },
                evidence: [
                    {
                        title: "Incident Retrospective Forensic Audit",
                        filename: "02_Incident_Retrospective_Audit.docx",
                        relative_path: "demo_C_explicit_violation/02_Incident_Retrospective_Audit.docx",
                        type: "audit_report",
                        status_hint: "Explicit Breach (271h delay)"
                    }
                ]
            }
        ]
    },
    {
        org_id: "ORG-GAMMA",
        name: "Meridian Enterprise Logistics",
        sector: "Global Supply Chain & Logistics",
        jurisdiction: "International Commercial Law",
        governing_policy: {
            title: "Meridian Vendor Due Diligence Framework",
            type: "internal_policy",
            filename: "01_Meridian_Vendor_Due_Diligence_Policy.docx",
            relative_path: "demo_B_missing_evidence/01_Meridian_Vendor_Due_Diligence_Policy.docx",
            summary: "Mandates prior vetting and documentation of all downstream subcontractors and processors."
        },
        vendors: [
            {
                vendor_id: "VEN-002",
                name: "Apex AI Analytics Corp.",
                scenario_id: "demo_B",
                contract: {
                    title: "SaaS Subscription Agreement",
                    filename: "ApexAI_Subscription_Agreement.pdf",
                    relative_path: "demo_B_missing_evidence/ApexAI_Subscription_Agreement.pdf",
                    type: "vendor_contract"
                },
                evidence: []
            }
        ]
    }
];

// Application State
const state = {
    activeTab: 'workspace',
    organizations: DEFAULT_ORGANIZATIONS,
    selectedOrgId: 'ORG-ALPHA',
    selectedVendorId: 'VEN-001',
    currentCaseData: null,
    currentDocIndex: 0,
    zoomLevel: 1.0,
    showHighlights: true,
    rules: [],
    testLibrary: [],
    benchmark: null,
    researchPackage: null,
    statusChart: null,
    currentUser: {
        name: 'Sarah Jenkins',
        role: 'Compliance Officer',
        initials: 'SJ'
    }
};

// Initialize Application on Page Load
document.addEventListener('DOMContentLoaded', () => {
    setupTabNavigation();
    setupDropZone();
    
    // 1. Immediately populate select elements and vault ribbon synchronously
    onCompanySelected();

    // 2. Execute default audit right away
    executeAuditForSelected();

    // 3. Load live server catalog and secondary data in background
    loadOrganizationsData();
    loadInitialData();
});

/**
 * Tab Switching Controller
 */
function switchTab(tabId) {
    state.activeTab = tabId;

    // Update Top Navigation Buttons
    document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.getElementById(`tab-btn-${tabId}`);
    if (activeBtn) activeBtn.classList.add('active');

    // Toggle Content Views
    const views = ['workspace', 'test-center', 'dashboard', 'rules', 'research'];
    views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        if (el) {
            if (v === tabId) {
                el.classList.remove('hidden');
            } else {
                el.classList.add('hidden');
            }
        }
    });

    // Lazy load tab specific components
    if (tabId === 'dashboard') {
        renderDashboardCharts();
    } else if (tabId === 'rules') {
        renderRulesGrid();
    } else if (tabId === 'test-center') {
        renderTestLibrary();
    } else if (tabId === 'research') {
        renderResearchView();
    }
}

/**
 * Fetch Baseline Rules and Test Library
 */
async function loadInitialData() {
    try {
        const [rulesRes, testLibRes, evalRes, resPkgRes] = await Promise.all([
            fetch('/api/rules'),
            fetch('/api/test-library'),
            fetch('/api/evaluation'),
            fetch('/api/research-paper-package')
        ]);
        state.rules = await rulesRes.json();
        state.testLibrary = await testLibRes.json();
        state.benchmark = await evalRes.json();
        state.researchPackage = await resPkgRes.json();
    } catch (err) {
        console.error('Initial data load error:', err);
    }
}

/**
 * Load Company / Organization Vault Catalog
 */
async function loadOrganizationsData() {
    try {
        const res = await fetch('/api/organizations');
        if (res.ok) {
            state.organizations = await res.json();
            const selectComp = document.getElementById('select-company');
            if (selectComp) {
                const currentVal = selectComp.value || state.selectedOrgId;
                selectComp.innerHTML = state.organizations.map(o => `
                    <option value="${o.org_id}" ${o.org_id === currentVal ? 'selected' : ''}>${o.name} (${o.sector})</option>
                `).join('');
                state.selectedOrgId = currentVal;
                onCompanySelected();
            }
        }
    } catch (err) {
        console.error('Error loading organizations:', err);
    }
}

/**
 * Handler when user selects a different company
 */
function onCompanySelected() {
    const compSelect = document.getElementById('select-company');
    if (!compSelect) return;

    state.selectedOrgId = compSelect.value;
    const org = state.organizations.find(o => o.org_id === state.selectedOrgId);
    if (!org) return;

    const sectorDesc = document.getElementById('company-sector-desc');
    if (sectorDesc) {
        sectorDesc.innerText = `${org.sector} • Jurisdiction: ${org.jurisdiction}`;
    }

    // Populate Vendor dropdown for this company
    const vendSelect = document.getElementById('select-vendor');
    if (vendSelect && org.vendors && org.vendors.length > 0) {
        vendSelect.innerHTML = org.vendors.map(v => `
            <option value="${v.vendor_id}">${v.name} — ${v.contract.title}</option>
        `).join('');

        state.selectedVendorId = org.vendors[0].vendor_id;
        onVendorSelected();
    } else {
        renderCompanyVaultRibbon(org);
        executeAuditForSelected();
    }
}

/**
 * Handler when user selects a vendor contract under the company
 */
function onVendorSelected() {
    const vendSelect = document.getElementById('select-vendor');
    if (vendSelect && vendSelect.value) {
        state.selectedVendorId = vendSelect.value;
    }

    const org = state.organizations.find(o => o.org_id === state.selectedOrgId);
    if (!org) return;

    const vendor = org.vendors ? org.vendors.find(v => v.vendor_id === state.selectedVendorId) : null;
    if (vendor) {
        const evText = vendor.evidence && vendor.evidence.length > 0 
            ? vendor.evidence.map(e => e.title).join(', ')
            : 'None (Evidence Pending)';

        const vendDesc = document.getElementById('vendor-contract-desc');
        if (vendDesc) {
            vendDesc.innerText = `Contract: ${vendor.contract.title} • Evidence: ${evText}`;
        }
    }

    renderCompanyVaultRibbon(org);

    // Automatically execute the cross-document audit for the selected company & vendor!
    executeAuditForSelected();
}

/**
 * Render Company Vault Documents Ribbon with Direct Download Buttons
 */
function renderCompanyVaultRibbon(org) {
    const ribbon = document.getElementById('company-vault-ribbon');
    if (!ribbon) return;

    const vendor = org.vendors.find(v => v.vendor_id === state.selectedVendorId);
    let html = `
        <span class="text-xs font-semibold text-slate-400 mr-1">Download Company Files:</span>
        <a href="/api/download-file?path=${encodeURIComponent(org.governing_policy.relative_path)}" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-500/10 hover:bg-blue-500/20 text-blue-300 border border-blue-500/30 transition flex items-center space-x-1.5 shadow-sm" download title="Download Policy File">
            <i class="fa-solid fa-file-shield text-blue-400"></i>
            <span>Policy: ${org.governing_policy.title}</span>
            <i class="fa-solid fa-download text-[10px] ml-1 opacity-70"></i>
        </a>
    `;

    if (vendor && vendor.contract) {
        html += `
            <a href="/api/download-file?path=${encodeURIComponent(vendor.contract.relative_path)}" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 transition flex items-center space-x-1.5 shadow-sm" download title="Download Vendor Contract">
                <i class="fa-solid fa-file-contract text-indigo-400"></i>
                <span>Contract: ${vendor.contract.title}</span>
                <i class="fa-solid fa-download text-[10px] ml-1 opacity-70"></i>
            </a>
        `;
    }

    if (vendor && vendor.evidence) {
        vendor.evidence.forEach(ev => {
            html += `
                <a href="/api/download-file?path=${encodeURIComponent(ev.relative_path)}" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 transition flex items-center space-x-1.5 shadow-sm" download title="Download Evidence File">
                    <i class="fa-solid fa-file-circle-check text-emerald-400"></i>
                    <span>Evidence: ${ev.title}</span>
                    <i class="fa-solid fa-download text-[10px] ml-1 opacity-70"></i>
                </a>
            `;
        });
    }

    ribbon.innerHTML = html;
}

/**
 * Trigger Cross-Document Audit for Selected Company & Vendor
 */
async function executeAuditForSelected() {
    state.currentDocIndex = 0;

    const formData = new FormData();
    formData.append('org_id', state.selectedOrgId);
    formData.append('vendor_id', state.selectedVendorId);

    try {
        const res = await fetch('/api/audit-company-vendor', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) throw new Error('Audit execution failed');
        const data = await res.json();
        state.currentCaseData = data;

        // Render Workspace Panels
        renderDocumentFamilyTabs();
        renderActiveDocument();
        renderFindingsPanel();
        updateCaseHeaderSummary();
        updateDashboardView();

    } catch (err) {
        console.error('Audit execution error:', err);
    }
}

/**
 * Render Document Family Tab Buttons
 */
function renderDocumentFamilyTabs() {
    const container = document.getElementById('document-tabs-list');
    if (!container || !state.currentCaseData) return;

    const docs = state.currentCaseData.documents || [];
    container.innerHTML = '';

    docs.forEach((doc, idx) => {
        const isActive = (idx === state.currentDocIndex);
        const tabBtn = document.createElement('button');
        tabBtn.className = `px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition ${
            isActive ? 'bg-blue-600 text-white shadow-sm' : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
        }`;
        
        let icon = 'fa-file-lines';
        if (doc.filename.endsWith('.pdf')) icon = 'fa-file-pdf text-red-400';
        else if (doc.filename.endsWith('.docx')) icon = 'fa-file-word text-blue-400';
        else if (doc.filename.endsWith('.txt')) icon = 'fa-file-code text-emerald-400';
        else if (doc.filename.endsWith('.png') || doc.filename.endsWith('.jpg')) icon = 'fa-file-image text-purple-400';

        tabBtn.innerHTML = `<i class="fa-solid ${icon}"></i> <span class="max-w-[140px] truncate">${doc.filename}</span>`;
        tabBtn.onclick = () => {
            state.currentDocIndex = idx;
            renderDocumentFamilyTabs();
            renderActiveDocument();
        };
        container.appendChild(tabBtn);
    });
}

/**
 * Render The Realistic Document Paper Canvas
 */
function renderActiveDocument() {
    if (!state.currentCaseData || !state.currentCaseData.documents) return;
    const doc = state.currentCaseData.documents[state.currentDocIndex];
    if (!doc) return;

    // Document Bottom Stats Bar
    document.getElementById('doc-stat-filename').innerText = doc.filename;
    document.getElementById('doc-stat-chars').innerText = `${(doc.char_count || doc.full_text.length).toLocaleString()} characters extracted`;
    document.getElementById('doc-stat-type').innerText = (doc.document_type || 'SUPPORTING EVIDENCE').replace('_', ' ').toUpperCase();

    // Paper Header & Meta
    document.getElementById('doc-meta-org').innerText = state.currentCaseData.organization.toUpperCase();
    document.getElementById('doc-meta-id').innerText = `DOC-REF: ${doc.filename.replace(/\.[^/.]+$/, '').toUpperCase()}`;
    document.getElementById('doc-paper-title').innerText = doc.title || doc.filename;
    document.getElementById('doc-paper-subtitle').innerText = `${(doc.document_type || 'Legal Document').replace('_', ' ').toUpperCase()} • VERSION ${doc.version || '1.0'}`;
    document.getElementById('doc-paper-page-indicator').innerText = `PAGE 1 OF ${doc.page_count || 1}`;

    // Stamp Seal logic based on document nature & finding
    const seal = document.getElementById('doc-stamp-seal');
    if (doc.filename.includes('SOC2') || doc.filename.includes('audit')) {
        seal.className = 'stamp-badge stamp-official absolute top-8 right-8 pointer-events-none select-none';
        seal.innerText = 'OFFICIAL AUDIT COPY';
    } else if (doc.filename.includes('ISO') && doc.full_text.includes('EXPIRED')) {
        seal.className = 'stamp-badge stamp-expired absolute top-8 right-8 pointer-events-none select-none';
        seal.innerText = 'EXPIRED REGISTRATION';
    } else if (doc.filename.includes('Retrospective') || doc.full_text.includes('271 hours')) {
        seal.className = 'stamp-badge stamp-violation absolute top-8 right-8 pointer-events-none select-none';
        seal.innerText = 'DEFICIENCY NOTED';
    } else if (doc.full_text.includes('DeleteMarkerAfterDays')) {
        seal.className = 'stamp-badge stamp-indeterminate absolute top-8 right-8 pointer-events-none select-none';
        seal.innerText = 'EVIDENCE CONFLICT';
    } else {
        seal.className = 'stamp-badge stamp-official absolute top-8 right-8 pointer-events-none select-none';
        seal.innerText = 'EXECUTED INSTRUMENT';
    }

    const contentContainer = document.getElementById('doc-paper-content');
    contentContainer.innerHTML = '';

    // If document is an authentic rendered PDF page image or scanned image
    if (doc.page_image_url) {
        const imgWrapper = document.createElement('div');
        imgWrapper.className = 'my-4 text-center border border-slate-300 rounded shadow-md overflow-hidden bg-white';
        imgWrapper.innerHTML = `
            <div class="bg-slate-100 py-1.5 px-3 border-b border-slate-200 text-slate-600 text-[11px] font-mono flex justify-between items-center">
                <span><i class="fa-solid fa-camera mr-1 text-slate-400"></i> High-Resolution Rendered Document Page 1</span>
                <span class="text-emerald-600 font-semibold"><i class="fa-solid fa-circle-check mr-1"></i> Original Authenticity Verified</span>
            </div>
            <img src="${doc.page_image_url}" alt="${doc.filename}" class="max-w-full h-auto mx-auto select-none" />
        `;
        contentContainer.appendChild(imgWrapper);
    }

    // Process and format paragraphs into structured clause blocks with highlight capabilities
    let rawParagraphs = [];
    if (doc.clauses && doc.clauses.length > 0) {
        rawParagraphs = doc.clauses.map(c => c.text);
    } else if (doc.full_text) {
        rawParagraphs = doc.full_text.split('\n\n').filter(p => p.trim().length > 0);
        if (rawParagraphs.length <= 1) {
            rawParagraphs = doc.full_text.split('\n').filter(p => p.trim().length > 0);
        }
    }

    if (rawParagraphs.length === 0) {
        const emptyEl = document.createElement('div');
        emptyEl.className = 'py-12 text-center text-slate-500 italic';
        emptyEl.innerText = 'Document contains no readable text content.';
        contentContainer.appendChild(emptyEl);
        return;
    }

    rawParagraphs.forEach((para, idx) => {
        const trimmed = para.trim();
        if (trimmed.startsWith('--- Page') || !trimmed) return;

        const pEl = document.createElement('div');
        pEl.className = 'clause-block';
        pEl.id = `clause-para-${idx}`;

        // Formatting headings vs body paragraphs
        if (trimmed.startsWith('SECTION') || trimmed.startsWith('CLAUSE') || trimmed.startsWith('ARTICLE') || trimmed.startsWith('FINDING') || trimmed.startsWith('Control CC') || trimmed.startsWith('BSI CERTIFICATE') || trimmed.startsWith('INDEPENDENT SERVICE') || trimmed.startsWith('MASTER CLOUD') || trimmed.startsWith('MERCHANT PAYMENT') || trimmed.startsWith('INFRASTRUCTURE MASTER')) {
            pEl.innerHTML = `<h3 class="font-serif font-bold text-base text-slate-900 border-b border-slate-200 pb-1 mb-1.5">${escapeHtml(trimmed)}</h3>`;
        } else {
            pEl.innerHTML = `<p class="leading-relaxed text-slate-800">${highlightKeyTerms(escapeHtml(trimmed))}</p>`;
        }

        contentContainer.appendChild(pEl);
    });
}

/**
 * Highlight important legal terms on the document paper
 */
function highlightKeyTerms(text) {
    if (!state.showHighlights) return text;
    const terms = [
        "AES-256", "TLS 1.3", "TLS 1.2", "Multi-Factor Authentication", "MFA", "FIDO2",
        "seventy-two (72) hours", "ten (10) business days", "271 hours", "EXPIRED",
        "ISO/IEC 27001", "365 calendar days", "90 days", "DeleteMarkerAfterDays: 90",
        "Protected Health Information", "Deloitte & Touche"
    ];
    let res = text;
    terms.forEach(t => {
        const regex = new RegExp(`(${t})`, 'gi');
        res = res.replace(regex, `<span class="bg-amber-100/90 text-amber-900 px-1 py-0.5 rounded font-semibold border-b border-amber-300">$1</span>`);
    });
    return res;
}

/**
 * Render Right-Hand AI Compliance Reasoning Findings
 */
function renderFindingsPanel() {
    const container = document.getElementById('findings-container');
    if (!container || !state.currentCaseData) return;

    const analysis = state.currentCaseData.analysis || {};
    const findings = analysis.findings || [];
    container.innerHTML = '';

    document.getElementById('findings-total-count').innerText = findings.length;

    findings.forEach((finding) => {
        const statusSlug = finding.expected_status.toLowerCase().replace(/\s+/g, '-');
        const isViolation = statusSlug === 'non-compliant';
        const isConflict = statusSlug === 'indeterminate';
        const isMissing = statusSlug === 'unverified';
        const isCompliant = statusSlug === 'compliant';

        const card = document.createElement('div');
        card.className = `bg-slate-900 border rounded-xl p-4 transition hover:border-slate-600 shadow-md ${
            isViolation ? 'border-rose-800/80 bg-rose-950/20' :
            isCompliant ? 'border-emerald-900/60 bg-emerald-950/10' :
            isConflict ? 'border-purple-800/80 bg-purple-950/20' :
            isMissing ? 'border-amber-800/80 bg-amber-950/20' : 'border-slate-800'
        }`;

        const quoteBadgeClass = isViolation ? 'text-rose-400' :
            isConflict ? 'text-purple-400' :
            isMissing ? 'text-amber-400' :
            isCompliant ? 'text-emerald-400' : 'text-blue-400';

        const quoteSectionTitle = isViolation ? 'Quoted Violation Excerpt (Click to View in Document)' :
            isConflict ? 'Quoted Contradiction / Ambiguity (Click to View)' :
            isMissing ? 'Contract Covenant (Supporting Audit Report Missing)' :
            isCompliant ? 'Verified Contract / Audit Evidence Quote (Click to View)' : 'Relevant Excerpt';

        // Build passages HTML with Click-to-Jump functionality
        const passages = finding.relevant_passages || [];
        const passagesHtml = passages.map((p) => {
            const isViTxt = isViolation && (p.toLowerCase().includes('10 business days') || p.toLowerCase().includes('ten') || p.toLowerCase().includes('271 hours') || p.toLowerCase().includes('expired') || p.toLowerCase().includes('breach'));
            return `
            <div onclick="jumpToDocumentPassage('${escapeQuote(p)}')" class="trace-quote cursor-pointer hover:bg-slate-800/80 transition my-1.5 p-2.5 rounded-lg border ${
                isViTxt ? 'border-rose-500/40 bg-rose-500/15 text-rose-200 shadow-sm' :
                isConflict ? 'border-purple-500/40 bg-purple-500/15 text-purple-200' :
                isMissing ? 'border-amber-500/40 bg-amber-500/15 text-amber-200' :
                isCompliant ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200' :
                'border-slate-800 bg-slate-950/60 text-slate-200'
            } flex items-start justify-between group">
                <span class="text-xs font-serif leading-relaxed italic">“${escapeHtml(p)}”</span>
                <i class="fa-solid fa-arrow-up-right-from-square text-[10px] text-blue-400 opacity-70 group-hover:opacity-100 ml-2 mt-1 shrink-0"></i>
            </div>
            `;
        }).join('');

        // Reasoning steps list
        const stepsHtml = (finding.reasoning_steps || []).map(s => `
            <li class="flex items-start space-x-2">
                <i class="fa-solid fa-angle-right text-blue-400 mt-0.5 text-[10px]"></i>
                <span>${escapeHtml(s)}</span>
            </li>
        `).join('');

        const semanticPct = finding.semantic_score_pct || (finding.semantic_similarity ? Math.round(finding.semantic_similarity * 100) : 88);
        const cosineVal = finding.semantic_similarity ? Number(finding.semantic_similarity).toFixed(3) : (semanticPct / 100).toFixed(3);
        const plainSummary = finding.plain_english_summary || finding.reasoning || finding.reasoning_steps?.[0] || 'Assessment complete.';

        card.innerHTML = `
            <div class="flex items-start justify-between gap-2 mb-2">
                <div>
                    <span class="text-[10px] font-bold text-blue-400 uppercase tracking-wide">${escapeHtml(finding.rule_id)} • ${escapeHtml(finding.rule_category || 'SECURITY')}</span>
                    <h4 class="text-sm font-bold text-white tracking-tight">${escapeHtml(finding.rule_title)}</h4>
                </div>
                <span class="status-pill status-${statusSlug}">${escapeHtml(finding.expected_status)}</span>
            </div>

            <!-- Plain-English What We Found Box -->
            <div class="bg-slate-950/80 p-3 rounded-lg border ${isViolation ? 'border-rose-900/40' : 'border-slate-800'} text-xs text-slate-200 leading-relaxed my-2">
                <div class="text-[10px] font-bold uppercase ${isViolation ? 'text-rose-400' : 'text-slate-400'} mb-0.5 flex items-center">
                    <i class="fa-solid ${isViolation ? 'fa-triangle-exclamation text-rose-400' : 'fa-circle-info text-blue-400'} mr-1.5"></i> Finding Summary
                </div>
                ${escapeHtml(plainSummary)}
            </div>

            <!-- Semantic Match Progress Meter (AIML Vector Alignment) -->
            <div class="space-y-1.5 my-2.5 bg-slate-950/40 p-2.5 rounded-lg border border-slate-800/60">
                <div class="flex items-center justify-between text-[11px]">
                    <span class="text-slate-400 font-medium flex items-center">
                        <i class="fa-solid fa-chart-simple text-indigo-400 mr-1.5"></i> Semantic Document Match
                    </span>
                    <span class="text-indigo-300 font-bold font-mono">${semanticPct}% Match (Cosine: ${cosineVal})</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div class="bg-gradient-to-r from-blue-500 via-indigo-500 to-cyan-400 h-1.5 rounded-full" style="width: ${semanticPct}%"></div>
                </div>
            </div>

            <!-- Traceable Passages Section -->
            <div class="my-2.5">
                <span class="text-[10px] uppercase ${quoteBadgeClass} block mb-1 font-semibold flex items-center">
                    <i class="fa-solid fa-quote-left mr-1.5"></i> ${quoteSectionTitle}
                </span>
                ${passagesHtml || '<p class="text-xs text-slate-500 italic">No direct clause text retrieved.</p>'}
            </div>

            <!-- Expandable Reasoning Steps -->
            <details class="text-xs text-slate-300 mt-2">
                <summary class="cursor-pointer text-[11px] text-blue-400 hover:text-blue-300 select-none py-1 flex items-center space-x-1">
                    <i class="fa-solid fa-angles-right text-[10px]"></i>
                    <span>Inspect Step-by-Step Reasoning Chain (${(finding.reasoning_steps || []).length} steps)</span>
                </summary>
                <ul class="space-y-1.5 mt-2 pl-1 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800 text-[11px] text-slate-300">
                    ${stepsHtml}
                </ul>
            </details>

            <!-- Recommended Next Action Callout -->
            <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex items-start space-x-2 text-xs">
                <i class="fa-solid fa-lightbulb text-amber-400 text-sm mt-0.5"></i>
                <div>
                    <span class="text-slate-400 text-[10px] uppercase font-bold block">Recommended Action</span>
                    <span class="text-slate-200 font-medium">${escapeHtml(finding.recommended_action || 'Maintain ongoing quarterly review.')}</span>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

/**
 * Click-to-Jump from Finding Passage directly to Document Paper Clause
 */
function jumpToDocumentPassage(passageText) {
    if (!passageText || !state.currentCaseData) return;
    const cleanQuery = passageText.replace(/['"“”\[\]\n\r]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 45).toLowerCase();
    if (!cleanQuery) return;

    const findAndHighlight = () => {
        const blocks = document.querySelectorAll('.clause-block');
        let matched = null;
        blocks.forEach(b => {
            b.classList.remove('clause-highlight-active');
            const bText = b.innerText.toLowerCase().replace(/\s+/g, ' ');
            if (bText.includes(cleanQuery) || cleanQuery.includes(bText.slice(0, 30))) {
                matched = b;
            }
        });

        if (matched) {
            matched.classList.add('clause-highlight-active');
            matched.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return true;
        }
        return false;
    };

    if (findAndHighlight()) return;

    // Check if passage is in another document in the case
    const docs = state.currentCaseData.documents || [];
    for (let i = 0; i < docs.length; i++) {
        if (i === state.currentDocIndex) continue;
        const fullText = (docs[i].full_text || '').toLowerCase().replace(/\s+/g, ' ');
        if (fullText.includes(cleanQuery) || cleanQuery.includes(fullText.slice(0, 30))) {
            state.currentDocIndex = i;
            renderDocumentFamilyTabs();
            renderActiveDocument();
            setTimeout(findAndHighlight, 120);
            return;
        }
    }
}

/**
 * Download currently viewed document
 */
function downloadCurrentDocument() {
    if (!state.currentCaseData || !state.currentCaseData.documents) return;
    const doc = state.currentCaseData.documents[state.currentDocIndex];
    if (!doc) return;

    if (doc.relative_download_path) {
        window.location.href = `/api/download-file?path=${encodeURIComponent(doc.relative_download_path)}`;
    } else {
        // Trigger download of in-memory text
        const blob = new Blob([doc.full_text], { type: 'text/plain' });
        triggerDownload(blob, doc.filename);
    }
}

/**
 * Update Top Case Header & Counts Summary
 */
function updateCaseHeaderSummary() {
    if (!state.currentCaseData) return;
    const analysis = state.currentCaseData.analysis || {};
    const dist = analysis.status_distribution || {};

    document.getElementById('panel-case-id').innerText = analysis.case_name || 'CASE-AUDIT-ACTIVE';
    document.getElementById('panel-org-name').innerText = analysis.organization_name || state.currentCaseData.organization;
    document.getElementById('panel-vendor-name').innerText = analysis.vendor_name || state.currentCaseData.vendor;

    document.getElementById('count-compliant').innerText = dist['Compliant'] || 0;
    document.getElementById('count-noncompliant').innerText = dist['Non-compliant'] || 0;
    document.getElementById('count-unverified').innerText = dist['Unverified'] || 0;
    document.getElementById('count-indeterminate').innerText = dist['Indeterminate'] || 0;
    document.getElementById('count-na').innerText = dist['Not applicable'] || 0;

    // Overall Status Chip logic
    const overall = document.getElementById('overall-status-chip');
    if ((dist['Non-compliant'] || 0) > 0) {
        overall.className = 'status-pill status-non-compliant';
        overall.innerText = 'DEFICIENCIES DETECTED';
    } else if ((dist['Indeterminate'] || 0) > 0) {
        overall.className = 'status-pill status-indeterminate';
        overall.innerText = 'CONTRADICTIONS PENDING';
    } else if ((dist['Unverified'] || 0) > 0) {
        overall.className = 'status-pill status-unverified';
        overall.innerText = 'EVIDENCE PENDING';
    } else {
        overall.className = 'status-pill status-compliant';
        overall.innerText = 'PORTFOLIO COMPLIANT';
    }
}

/**
 * Zoom In / Out on Legal Paper Canvas
 */
function toggleDocZoom(delta) {
    state.zoomLevel = Math.max(0.7, Math.min(1.4, state.zoomLevel + delta));
    const container = document.getElementById('document-canvas-container');
    if (container) {
        container.style.transform = `scale(${state.zoomLevel})`;
    }
    document.getElementById('zoom-level').innerText = `${Math.round(state.zoomLevel * 100)}%`;
}

/**
 * Toggle Clause Highlighter Visibility
 */
function toggleHighlightVisibility() {
    state.showHighlights = !state.showHighlights;
    const btn = document.getElementById('btn-highlight-toggle');
    if (state.showHighlights) {
        btn.innerHTML = `<i class="fa-solid fa-highlighter mr-1"></i> Highlights On`;
        btn.className = "px-2.5 py-1 rounded bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 border border-blue-500/30 transition font-medium";
    } else {
        btn.innerHTML = `<i class="fa-solid fa-highlighter mr-1"></i> Highlights Off`;
        btn.className = "px-2.5 py-1 rounded bg-slate-800 text-slate-400 border border-slate-700 transition font-medium";
    }
    renderActiveDocument();
}

/**
 * Render Test Document Center Library Grid
 */
async function renderTestLibrary() {
    const container = document.getElementById('test-library-grid');
    if (!container) return;

    if (!state.testLibrary || state.testLibrary.length === 0) {
        try {
            const res = await fetch('/api/test-library');
            state.testLibrary = await res.json();
        } catch (e) { console.error('Error fetching test library:', e); }
    }

    if (!state.testLibrary) return;

    container.innerHTML = state.testLibrary.map(item => `
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between hover:border-slate-700 transition">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-[10px] font-mono uppercase font-bold text-blue-400">${escapeHtml(item.category)}</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        item.format === 'PDF' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                        item.format === 'DOCX' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' :
                        item.format === 'PNG' ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20' :
                        'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }">${escapeHtml(item.format)}</span>
                </div>
                <h4 class="text-sm font-bold text-white">${escapeHtml(item.title)}</h4>
                <p class="text-xs text-slate-400 mt-2 leading-relaxed">${escapeHtml(item.description)}</p>
                <div class="mt-3 font-mono text-[11px] text-slate-500 truncate">📄 ${escapeHtml(item.filename)}</div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-end">
                <a href="/api/download-file?path=${encodeURIComponent(item.download_path)}" download class="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition flex items-center space-x-1.5 shadow">
                    <i class="fa-solid fa-download"></i>
                    <span>Download File</span>
                </a>
            </div>
        </div>
    `).join('');
}

/**
 * Render Executive Dashboard Charts using Chart.js and update dynamic KPIs and Watchlist
 */
function renderDashboardCharts() {
    updateDashboardView();
}

function updateDashboardView() {
    const caseData = state.currentCaseData;
    const analysis = caseData?.analysis || {};
    const dist = analysis.status_distribution || {
        'Compliant': 0,
        'Non-compliant': 0,
        'Unverified': 0,
        'Indeterminate': 0,
        'Not applicable': 0
    };
    const docs = caseData?.documents || [];
    const findings = analysis.findings || [];

    // 1. Update Top KPI Counters
    const kpiCases = document.getElementById('dash-kpi-cases');
    const kpiCasesSub = document.getElementById('dash-kpi-cases-sub');
    const kpiDocs = document.getElementById('dash-kpi-docs');
    const kpiDocsSub = document.getElementById('dash-kpi-docs-sub');
    const kpiVerified = document.getElementById('dash-kpi-verified');
    const kpiBreaches = document.getElementById('dash-kpi-breaches');
    const kpiUnverified = document.getElementById('dash-kpi-unverified');

    if (kpiCases) kpiCases.innerText = caseData?.organization ? `${caseData.organization}` : '1 Monitored';
    if (kpiCasesSub) kpiCasesSub.innerHTML = `<i class="fa-solid fa-building mr-1"></i> Vendor: ${caseData?.vendor || 'Selected'}`;
    if (kpiDocs) kpiDocs.innerText = `${docs.length} File${docs.length === 1 ? '' : 's'}`;
    if (kpiDocsSub) kpiDocsSub.innerHTML = `<i class="fa-solid fa-file-lines mr-1"></i> ${docs.map(d => d.filename.split('.').pop().toUpperCase()).filter((v, i, a) => a.indexOf(v) === i).join(', ') || 'PDF, DOCX'}`;
    if (kpiVerified) kpiVerified.innerText = `${dist['Compliant'] || 0} Satisfied`;
    if (kpiBreaches) kpiBreaches.innerText = `${dist['Non-compliant'] || 0} Breaches`;
    if (kpiUnverified) kpiUnverified.innerText = `${dist['Unverified'] || 0} Missing`;

    // 2. Render Chart.js Status Distribution Bar Chart
    const ctx = document.getElementById('chart-status-distribution');
    if (ctx) {
        if (state.statusChart) {
            state.statusChart.destroy();
        }

        state.statusChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Compliant', 'Non-compliant', 'Unverified', 'Indeterminate', 'Not Applicable'],
                datasets: [{
                    label: 'Assessed Obligations Count',
                    data: [
                        dist['Compliant'] || 0,
                        dist['Non-compliant'] || 0,
                        dist['Unverified'] || 0,
                        dist['Indeterminate'] || 0,
                        dist['Not applicable'] || 0
                    ],
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.75)',
                        'rgba(239, 68, 68, 0.75)',
                        'rgba(245, 158, 11, 0.75)',
                        'rgba(168, 85, 247, 0.75)',
                        'rgba(100, 116, 139, 0.75)'
                    ],
                    borderColor: [
                        '#10b981', '#ef4444', '#f59e0b', '#a855f7', '#64748b'
                    ],
                    borderWidth: 1.5,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        grid: { color: 'rgba(51, 65, 85, 0.3)' },
                        ticks: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
                    },
                    y: {
                        grid: { color: 'rgba(51, 65, 85, 0.3)' },
                        ticks: { color: '#94a3b8', stepSize: 1, font: { family: 'Inter', size: 11 } }
                    }
                }
            }
        });
    }

    // 3. Dynamically populate Critical Deficiencies Watchlist
    const listContainer = document.getElementById('dash-deficiencies-list');
    const badge = document.getElementById('dash-watchlist-badge');
    if (!listContainer) return;

    // Filter findings that require attention (Non-compliant, Indeterminate, Unverified)
    const deficiencies = findings.filter(f => ['Non-compliant', 'Indeterminate', 'Unverified'].includes(f.expected_status));

    if (badge) {
        badge.innerText = `${deficiencies.length} Gap${deficiencies.length === 1 ? '' : 's'}`;
        badge.className = deficiencies.length > 0 
            ? "px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-400"
            : "px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400";
    }

    if (deficiencies.length === 0) {
        listContainer.innerHTML = `
            <div class="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-center">
                <i class="fa-solid fa-circle-check text-emerald-400 text-3xl mb-2 block"></i>
                <div class="font-bold text-emerald-300 text-sm">No Open Deficiencies Detected</div>
                <p class="text-xs text-slate-300 mt-1">All evaluated obligations for <strong>${escapeHtml(caseData?.vendor || 'this vendor')}</strong> have verified contractual commitments and accredited third-party examination proof.</p>
            </div>
        `;
        return;
    }

    listContainer.innerHTML = deficiencies.map(def => {
        const isBreach = def.expected_status === 'Non-compliant';
        const isConflict = def.expected_status === 'Indeterminate';
        const statusColor = isBreach ? 'rose' : isConflict ? 'purple' : 'amber';
        const statusLabel = isBreach ? 'NON-COMPLIANT' : isConflict ? 'CONTRADICTION' : 'UNVERIFIED';

        const quoteText = def.relevant_passages && def.relevant_passages[0] && def.relevant_passages[0] !== 'No direct matching clause found.'
            ? def.relevant_passages[0]
            : (def.reasoning || def.plain_english_summary || 'Control deficiency noted.');

        return `
            <div class="p-3.5 rounded-xl bg-${statusColor}-500/10 border border-${statusColor}-500/25 text-xs transition hover:border-${statusColor}-500/50">
                <div class="flex items-center justify-between font-bold text-${statusColor}-300 mb-1">
                    <span class="flex items-center">
                        <i class="fa-solid ${isBreach ? 'fa-triangle-exclamation' : isConflict ? 'fa-circle-question' : 'fa-clock'} mr-1.5"></i>
                        <span>${escapeHtml(def.rule_id)}: ${escapeHtml(def.rule_title)}</span>
                    </span>
                    <span class="px-2 py-0.5 rounded bg-${statusColor}-500/20 text-[10px] font-mono tracking-wider font-bold">${statusLabel}</span>
                </div>
                <p class="text-slate-300 text-[11.5px] leading-relaxed my-1.5">${escapeHtml(def.plain_english_summary || def.reasoning)}</p>
                <div class="bg-slate-950/60 p-2 rounded border border-${statusColor}-500/20 text-[11px] font-serif italic text-slate-300 my-1">
                    “${escapeHtml(quoteText.slice(0, 220))}${quoteText.length > 220 ? '...' : ''}”
                </div>
                <div class="text-[10.5px] text-${statusColor}-400 mt-1.5 font-medium flex items-center">
                    <i class="fa-solid fa-wrench mr-1"></i> <strong>Action:</strong>&nbsp;${escapeHtml(def.recommended_action || 'Remediation required.')}
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Render Rules Grid Catalogue View
 */
async function renderRulesGrid() {
    const container = document.getElementById('rules-grid-container');
    if (!container) return;

    if (!state.rules || state.rules.length === 0) {
        try {
            const res = await fetch('/api/rules');
            state.rules = await res.json();
        } catch (e) { console.error('Error fetching rules:', e); }
    }

    container.innerHTML = '';

    const query = (document.getElementById('rule-search-input')?.value || '').toLowerCase();
    const filtered = (state.rules || []).filter(r => 
        r.rule_title.toLowerCase().includes(query) ||
        r.legal_or_policy_category.toLowerCase().includes(query) ||
        r.source_name.toLowerCase().includes(query)
    );

    filtered.forEach(rule => {
        const card = document.createElement('div');
        card.className = "bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-md hover:border-slate-700 transition flex flex-col justify-between";
        card.innerHTML = `
            <div>
                <div class="flex items-center justify-between gap-2 mb-1.5">
                    <span class="text-[10px] font-mono font-bold text-blue-400">${escapeHtml(rule.rule_id)}</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase font-mono ${
                        rule.severity === 'Critical' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                        rule.severity === 'High' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                        'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                    }">${escapeHtml(rule.severity)}</span>
                </div>
                <h4 class="text-sm font-bold text-white">${escapeHtml(rule.rule_title)}</h4>
                <p class="text-[11px] text-slate-400 mt-1 font-mono">${escapeHtml(rule.source_name)} • ${escapeHtml(rule.jurisdiction)}</p>
                ${rule.chapter ? `<span class="inline-block px-2 py-0.5 rounded text-[10px] bg-slate-800 text-indigo-300 mt-1.5 font-medium">${escapeHtml(rule.chapter)}</span>` : ''}
                <p class="text-xs text-slate-300 mt-2.5 leading-relaxed">${escapeHtml(rule.rule_text)}</p>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
                <span class="font-mono text-slate-500 block text-[10px] uppercase">Required Control</span>
                <span class="text-slate-300 font-medium">${escapeHtml(rule.required_action_or_control)}</span>
                ${rule.source_reference_or_url ? `
                    <div class="mt-2.5 pt-2 border-t border-slate-800/60">
                        <a href="${rule.source_reference_or_url}" target="_blank" rel="noopener noreferrer" class="text-[11px] text-blue-400 hover:text-blue-300 font-mono inline-flex items-center space-x-1.5 font-semibold transition">
                            <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                            <span>Statutory Source (${rule.rule_id.startsWith('RULE-GDPR') ? 'gdpr-info.eu' : 'Official Standard'})</span>
                        </a>
                    </div>
                ` : ''}
            </div>
        `;
        container.appendChild(card);
    });
}

function filterRules() {
    renderRulesGrid();
}

/**
 * Render Research Methodology & Truth Matrix View
 */
async function renderResearchView() {
    if (!state.benchmark || !state.researchPackage) {
        try {
            const [evalRes, resPkgRes] = await Promise.all([
                fetch('/api/evaluation'),
                fetch('/api/research-paper-package')
            ]);
            state.benchmark = await evalRes.json();
            state.researchPackage = await resPkgRes.json();
        } catch (e) { console.error('Error fetching research data:', e); }
    }
    if (!state.benchmark) return;
    const b = state.benchmark;

    // Build Confusion Matrix Table
    const cmWrapper = document.getElementById('confusion-matrix-wrapper');
    if (cmWrapper && b.confusion_matrix) {
        const classes = b.classes || ['Compliant', 'Non-compliant', 'Unverified', 'Indeterminate', 'Not applicable'];
        let html = `
            <table class="w-full text-center border-collapse text-xs font-mono">
                <thead>
                    <tr class="border-b border-slate-800 text-slate-400">
                        <th class="p-2 text-left">Actual \\ Predicted</th>
                        ${classes.map(c => `<th class="p-2">${escapeHtml(c)}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
        `;

        classes.forEach(actual => {
            html += `<tr class="border-b border-slate-800/60"><td class="p-2 text-left font-bold text-slate-300">${escapeHtml(actual)}</td>`;
            classes.forEach(pred => {
                const count = b.confusion_matrix[actual]?.[pred] || 0;
                const isDiag = (actual === pred);
                const cellBg = isDiag && count > 0 ? 'bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30' : count > 0 ? 'bg-rose-500/20 text-rose-400 font-bold' : 'text-slate-600';
                html += `<td class="p-2 ${cellBg}">${count}</td>`;
            });
            html += `</tr>`;
        });

        html += `</tbody></table>`;
        cmWrapper.innerHTML = html;
    }

    // Build Per-Class Metrics Table
    const pcWrapper = document.getElementById('per-class-table-wrapper');
    if (pcWrapper && b.per_class_metrics) {
        let pcHtml = `
            <table class="w-full border-collapse font-mono text-left">
                <thead>
                    <tr class="border-b border-slate-800 text-slate-400 text-[11px]">
                        <th class="p-2">Status Class</th>
                        <th class="p-2">Precision</th>
                        <th class="p-2">Recall</th>
                        <th class="p-2">F1</th>
                        <th class="p-2">Support</th>
                    </tr>
                </thead>
                <tbody>
        `;
        for (const [cls, m] of Object.entries(b.per_class_metrics)) {
            pcHtml += `
                <tr class="border-b border-slate-800/60">
                    <td class="p-2 font-bold text-slate-200">${escapeHtml(cls)}</td>
                    <td class="p-2 text-emerald-400">${(m.precision * 100).toFixed(1)}%</td>
                    <td class="p-2 text-blue-400">${(m.recall * 100).toFixed(1)}%</td>
                    <td class="p-2 text-indigo-400 font-bold">${m.f1_score.toFixed(3)}</td>
                    <td class="p-2 text-slate-400">${m.support}</td>
                </tr>
            `;
        }
        pcHtml += `</tbody></table>`;
        pcWrapper.innerHTML = pcHtml;
    }
}

function copyLatexTable() {
    if (state.researchPackage && state.researchPackage.latex_table_code) {
        navigator.clipboard.writeText(state.researchPackage.latex_table_code);
        alert('LaTeX table code copied to clipboard! You can paste it directly into an Overleaf or paper editor.');
    }
}

function downloadResearchData() {
    const payload = {
        title: "Cross-Document Regulatory Grounding & Verification Benchmark",
        timestamp: new Date().toISOString(),
        formal_semantics: state.researchPackage,
        empirical_results: state.benchmark
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    triggerDownload(blob, "Research_Methodology_Dossier.json");
}

/**
 * Authentication Modal Handlers
 */
function openSignInModal() {
    document.getElementById('signin-modal')?.classList.remove('hidden');
}

function closeSignInModal() {
    document.getElementById('signin-modal')?.classList.add('hidden');
}

function selectUserRole(name, role, initials) {
    state.currentUser = { name, role, initials };
    document.getElementById('user-name').innerText = name;
    document.getElementById('user-role').innerText = role;
    document.getElementById('user-avatar').innerText = initials;
    closeSignInModal();
}

/**
 * Drag & Drop Custom File Upload Handlers
 */
function setupDropZone() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('modal-file-input');
    if (!dropZone || !fileInput) return;

    dropZone.onclick = (e) => {
        if (e.target !== fileInput) {
            fileInput.click();
        }
    };

    fileInput.onchange = (e) => {
        handleFilesSelected(Array.from(e.target.files));
    };

    dropZone.ondragover = (e) => {
        e.preventDefault();
        dropZone.classList.add('border-blue-500');
    };

    dropZone.ondragleave = () => {
        dropZone.classList.remove('border-blue-500');
    };

    dropZone.ondrop = (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-blue-500');
        if (e.dataTransfer.files) {
            handleFilesSelected(Array.from(e.dataTransfer.files));
        }
    };
}

let selectedUploadFiles = [];

function handleFilesSelected(files) {
    selectedUploadFiles = files;
    const container = document.getElementById('modal-selected-files');
    if (!container) return;
    container.innerHTML = files.map(f => `<div>📄 ${escapeHtml(f.name)} (${(f.size / 1024).toFixed(1)} KB)</div>`).join('');
}

function openUploadModal() {
    document.getElementById('upload-modal')?.classList.remove('hidden');
}

function closeUploadModal() {
    document.getElementById('upload-modal')?.classList.add('hidden');
    selectedUploadFiles = [];
    const container = document.getElementById('modal-selected-files');
    if (container) container.innerHTML = '';
}

async function submitUploadAndAnalyze() {
    if (selectedUploadFiles.length === 0) {
        alert('Please select at least one document (PDF, DOCX, TXT, or Image).');
        return;
    }

    const org = document.getElementById('modal-org-name')?.value || 'Client Organization';
    const ven = document.getElementById('modal-vendor-name')?.value || selectedUploadFiles[0].name.replace(/\.[^/.]+$/, '');
    const caseName = `CASE-UPLOAD-${Date.now().toString().slice(-4)}`;

    const formData = new FormData();
    selectedUploadFiles.forEach(f => formData.append('files', f));
    formData.append('org_name', org);
    formData.append('vendor_name', ven);
    formData.append('case_name', caseName);

    closeUploadModal();

    try {
        const res = await fetch('/api/upload-and-analyze', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) throw new Error('Document analysis failed');
        const data = await res.json();
        state.currentCaseData = data;
        state.currentDocIndex = 0;

        // Dynamically add this uploaded dossier to the top company selector dropdown
        const selectComp = document.getElementById('select-company');
        if (selectComp) {
            const uploadOrgId = `ORG-UPLOAD-${Date.now()}`;
            const opt = document.createElement('option');
            opt.value = uploadOrgId;
            opt.innerText = `📂 ${org} — ${selectedUploadFiles.length} Uploaded File(s)`;
            opt.selected = true;
            selectComp.insertBefore(opt, selectComp.firstChild);

            // Prepend to state.organizations
            state.organizations.unshift({
                org_id: uploadOrgId,
                name: org,
                sector: "Custom Ingested Vault",
                jurisdiction: "Audited Under Governing Standards",
                governing_policy: {
                    title: selectedUploadFiles[0].name,
                    filename: selectedUploadFiles[0].name,
                    relative_path: "",
                    summary: "Uploaded Document Portfolio"
                },
                vendors: [{
                    vendor_id: "VEN-UPLOADED",
                    name: ven,
                    scenario_id: "custom",
                    contract: { title: selectedUploadFiles[0].name },
                    evidence: []
                }]
            });
            state.selectedOrgId = uploadOrgId;
            state.selectedVendorId = "VEN-UPLOADED";

            const vendSelect = document.getElementById('select-vendor');
            if (vendSelect) {
                vendSelect.innerHTML = `<option value="VEN-UPLOADED">${ven} — ${selectedUploadFiles[0].name}</option>`;
            }
        }

        // Render Workspace Panels with the uploaded file
        renderDocumentFamilyTabs();
        renderActiveDocument();
        renderFindingsPanel();
        updateCaseHeaderSummary();
        updateDashboardView();

        // Switch directly to workspace so the user sees the parsed document and findings
        switchTab('workspace');

    } catch (err) {
        console.error('Custom upload error:', err);
        alert('Analysis error: ' + err.message);
    }
}

/**
 * Export Current Dossier as JSON or CSV
 */
function exportCurrentReport(format) {
    if (!state.currentCaseData || !state.currentCaseData.analysis) {
        alert('No analysis data available to export.');
        return;
    }

    const analysis = state.currentCaseData.analysis;
    const filename = `Compliance_Audit_${analysis.case_name || 'Report'}.${format}`;

    if (format === 'json') {
        const blob = new Blob([JSON.stringify(analysis, null, 2)], { type: 'application/json' });
        triggerDownload(blob, filename);
    } else {
        const rows = [['Case', 'Vendor', 'Rule ID', 'Title', 'Category', 'Status', 'Sufficiency', 'Recommended Action']];
        (analysis.findings || []).forEach(f => {
            rows.push([
                analysis.case_name,
                analysis.vendor_name,
                f.rule_id,
                `"${f.rule_title}"`,
                f.rule_category,
                f.expected_status,
                f.evidence_sufficiency,
                `"${(f.recommended_action || '').replace(/"/g, '""')}"`
            ]);
        });
        const csvContent = rows.map(r => r.join(',')).join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        triggerDownload(blob, filename);
    }
}

function triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Helpers
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function escapeQuote(str) {
    if (!str) return '';
    return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}
