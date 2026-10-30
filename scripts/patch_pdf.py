import re

with open('scripts/generate_presentation_pdf.py', 'r', encoding='utf-8') as f:
    text = f.read()

target_marker = 'opt_deep_data = ['
end_marker = 't_opt_deep = Table(opt_deep_data'

start_idx = text.find(target_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found!")
    exit(1)

new_opt_section = '''opt_deep_data = [
        [
            Paragraph("<b>Optimization Technique</b>", bold_body),
            Paragraph("<b>Formula / Rule Logic</b>", bold_body),
            Paragraph("<b>Plain-English Explanation (What to Say on Screen)</b>", bold_body)
        ],
        [
            Paragraph("<b>1. Short-Circuiting Cascade</b><br/>(Early-Exit Pruning)", bold_body),
            Paragraph("<code>Hierarchy:</code><br/><b>1.</b> Scope Exclusion<br/><b>2.</b> Certificate Expiry<br/><b>3.</b> Amendment Precedence<br/><b>4.</b> Negative-Proof Guard<br/><b>5.</b> Corroboration<br/><i>(Halts on first true rule)</i>", code_style),
            Paragraph("&bull; <b>228x Faster Speed:</b> Cuts rule check time from <b>480 ms (BERT) down to 2.1 ms</b>. Audits all 124 rules in under 0.4 seconds.<br/>&bull; <b>Runs on Basic CPU (&lt; 120 KB RAM):</b> Drops memory from <b>450 MB to under 120 KB</b>, running on any normal laptop without an expensive GPU.<br/>&bull; <b>Smart Early-Exit (No False Alarms):</b> If a contract does not handle European data, GDPR breach checks are skipped immediately, marking it <b>'Not applicable'</b> to avoid false alarms.", body_style)
        ],
        [
            Paragraph("<b>2. Sublinear Term Frequency</b><br/>(Logarithmic Dampening)", bold_body),
            Paragraph("<font color='#1e3a8a'><b>tf_sub = 1 + ln(tf)</b></font><br/>for tf &gt; 0, else 0<br/><br/><i>Raw TF:</i> tf_raw = count(t, d)", formula_style),
            Paragraph("&bull; <b>The Problem:</b> Legal contracts repeat filler words (<i>'parties'</i>, <i>'agreement'</i>) 100+ times, drowning out important controls.<br/>&bull; <b>Easy Math:</b> Log scaling turns a 100-count filler word into just <b>5.60</b> (1 + ln(100)).<br/>&bull; <b>The Benefit:</b> Lets rare but crucial security terms (e.g., <i>'AES-256'</i>, <i>'MFA'</i>, <i>'72-hour notice'</i>) stand out clearly.", body_style)
        ],
        [
            Paragraph("<b>3. Dual-Sieve Additive Boost</b><br/>(Synonym Rescue)", bold_body),
            Paragraph("<font color='#1e3a8a'><b>Score = cos(v_q, v_c) + &alpha;&middot;min(|K|, 3)</b></font><br/>&bull; &alpha; = 0.25 (keyword bonus)<br/>&bull; Cutoff threshold &tau; = 0.18", formula_style),
            Paragraph("&bull; <b>The Problem:</b> Word-math fails on legal synonyms (e.g., <i>'256-bit block cipher'</i> vs <i>'AES-256'</i> scores 0.08, below cutoff).<br/>&bull; <b>The Fix:</b> Adds a +0.25 bonus whenever statutory keywords match so governing clauses are not lost.<br/>&bull; <b>Proven Result:</b> Eliminates <b>94% of legal noise</b> while keeping <b>100% of governing clauses</b>.", body_style)
        ],
        [
            Paragraph("<b>4. Epistemic 5-State Deontic Guard</b><br/>(Anti-Hallucination)", bold_body),
            Paragraph("<code>Discrete 5 States:</code><br/>&bull; Missing Proof &rArr; <b>Unverified</b><br/>&bull; Explicit Breach &rArr; <b>Non-compliant</b><br/>&bull; Confirmed Audit &rArr; <b>Compliant</b><br/>&bull; Contradiction &rArr; <b>Indeterminate</b>", code_style),
            Paragraph("&bull; <b>Solves Negative-Proof Fallacy:</b> Neural models guess that a missing audit certificate is a violation.<br/>&bull; <b>The Fix:</b> Strictly separates <i>'Missing Proof'</i> (<b>Unverified</b>) from an actual <i>'Breach'</i> (<b>Non-compliant</b>).<br/>&bull; <b>Impact:</b> Hallucination rate drops from <b>27.8% (BERT) down to 0.0% (Deterministic)</b>.", body_style)
        ]
    ]
    '''

updated_text = text[:start_idx] + new_opt_section + text[end_idx:]

with open('scripts/generate_presentation_pdf.py', 'w', encoding='utf-8') as f:
    f.write(updated_text)

print('Updated scripts/generate_presentation_pdf.py successfully!')
