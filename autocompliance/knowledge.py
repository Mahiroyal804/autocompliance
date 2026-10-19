"""Compliance knowledge base: GDPR + SOC 2 controls with assessment questions.

Each control: id, framework, category, title, why it matters,
questions (each with weight 1-3 and a concrete fix), and related documents.
"""

CONTROLS = [
    # ---------------- GDPR ----------------
    {
        "id": "GDPR-01", "framework": "GDPR", "category": "Lawful Basis",
        "title": "Documented lawful basis for every processing activity",
        "why": "GDPR Art. 6: you may only process personal data under one of six lawful bases (consent, contract, legal obligation, vital interests, public task, legitimate interests). No basis = unlawful processing.",
        "questions": [
            {"q": "Have you documented a specific lawful basis (Art. 6) for EACH type of personal data you process?", "weight": 3,
             "fix": "Create a data inventory mapping each data type -> purpose -> lawful basis. Template included in generated docs."},
            {"q": "If you rely on consent, is it freely given, specific, informed, and as easy to withdraw as to give?", "weight": 2,
             "fix": "Rebuild consent flows: no pre-ticked boxes, granular choices, one-click withdrawal."},
            {"q": "If you rely on legitimate interests, have you completed a Legitimate Interests Assessment (LIA)?", "weight": 2,
             "fix": "Complete an LIA for each legitimate-interest use case (purpose test, necessity test, balancing test)."},
        ],
        "docs": ["ropa", "lia_template"],
    },
    {
        "id": "GDPR-02", "framework": "GDPR", "category": "Transparency",
        "title": "Clear privacy notices at collection points",
        "why": "GDPR Art. 13/14: people must know who you are, why you process their data, their rights, and how to complain — at the moment you collect it.",
        "questions": [
            {"q": "Does every data-collection point (signup, checkout, contact form) link to an up-to-date privacy notice?", "weight": 3,
             "fix": "Publish a privacy notice covering identity, purposes, bases, retention, rights, and DPO contact. Generator included."},
            {"q": "Is your privacy notice written in plain language (no legal walls of text)?", "weight": 1,
             "fix": "Rewrite using layered notices: short summary up front, details behind expandable sections."},
        ],
        "docs": ["privacy_policy"],
    },
    {
        "id": "GDPR-03", "framework": "GDPR", "category": "Data Subject Rights",
        "title": "Working process for data subject requests (DSR)",
        "why": "GDPR Art. 12-22: access, rectification, erasure, portability, restriction, objection — you must respond within ONE month.",
        "questions": [
            {"q": "Can a user request a copy or deletion of their data through a defined channel (not just 'email us maybe')?", "weight": 3,
             "fix": "Define one intake channel (e.g. privacy@), assign an owner, and build a 30-day response workflow."},
            {"q": "Have you handled (or drill-tested) a DSR end-to-end in the last 12 months?", "weight": 2,
             "fix": "Run a tabletop exercise: fake DSR -> locate data across systems -> respond within 30 days."},
            {"q": "Can you actually DELETE a user's data from backups and third-party processors, not just your main DB?", "weight": 2,
             "fix": "Map data flows to processors; confirm deletion propagation in each DPA."},
        ],
        "docs": ["dsr_playbook"],
    },
    {
        "id": "GDPR-04", "framework": "GDPR", "category": "Security",
        "title": "Appropriate technical measures (encryption, access control)",
        "why": "GDPR Art. 32: encryption, pseudonymization, access control, and regular testing — proportional to risk.",
        "questions": [
            {"q": "Is personal data encrypted in transit (TLS) AND at rest (disk/DB encryption)?", "weight": 3,
             "fix": "Enable TLS everywhere; turn on at-rest encryption for databases and backups."},
            {"q": "Do employees get least-privilege access (they see only the data their job needs)?", "weight": 2,
             "fix": "Audit access quarterly; remove standing admin; require MFA for all staff."},
            {"q": "Is MFA enforced for all staff accounts, especially email, code, and cloud consoles?", "weight": 3,
             "fix": "Enforce MFA org-wide this week — the single highest-ROI security control."},
        ],
        "docs": ["security_policy"],
    },
    {
        "id": "GDPR-05", "framework": "GDPR", "category": "Breach Response",
        "title": "72-hour breach notification capability",
        "why": "GDPR Art. 33/34: notify the supervisory authority within 72 hours of becoming aware; notify affected people without undue delay if high risk.",
        "questions": [
            {"q": "Do you have a written incident response plan naming who decides, who notifies, and how?", "weight": 3,
             "fix": "Adopt the included incident response plan; assign roles (lead, comms, legal)."},
            {"q": "Would you DETECT a breach (logging, alerting) or only find out from a customer tweet?", "weight": 2,
             "fix": "Enable audit logging on auth, data access, and admin actions; set up alerts."},
        ],
        "docs": ["incident_response"],
    },
    {
        "id": "GDPR-06", "framework": "GDPR", "category": "Accountability",
        "title": "Records of processing (RoPA) maintained",
        "why": "GDPR Art. 30: most companies must maintain written records of processing activities — the first thing a regulator asks for.",
        "questions": [
            {"q": "Do you maintain a written Record of Processing Activities (purposes, categories, recipients, retention, security)?", "weight": 3,
             "fix": "Generate the RoPA template and fill it per data flow — 2-hour exercise."},
        ],
        "docs": ["ropa"],
    },
    {
        "id": "GDPR-07", "framework": "GDPR", "category": "Vendors",
        "title": "Data Processing Agreements with all processors",
        "why": "GDPR Art. 28: every vendor touching personal data (hosting, analytics, email, support) needs a signed DPA with required clauses.",
        "questions": [
            {"q": "Do you have signed DPAs with EVERY vendor that touches personal data (cloud, analytics, email, CRM, support)?", "weight": 3,
             "fix": "List all vendors; request DPAs from each; sign the generated DPA template where they lack one."},
            {"q": "For non-EU vendors, is there a valid transfer mechanism (SCCs, adequacy decision)?", "weight": 2,
             "fix": "Execute EU Standard Contractual Clauses with non-adequate-country vendors."},
        ],
        "docs": ["dpa_template", "vendor_register"],
    },
    {
        "id": "GDPR-08", "framework": "GDPR", "category": "Data Minimization",
        "title": "Data minimization and retention limits enforced",
        "why": "GDPR Art. 5(1)(c),(e): collect only what you need, keep it only as long as needed.",
        "questions": [
            {"q": "Do you have defined retention periods per data type (not 'keep forever')?", "weight": 2,
             "fix": "Set retention per category (e.g. logs 12 months, inactive accounts 24 months) and automate deletion."},
            {"q": "Do signup forms avoid collecting fields you don't use?", "weight": 1,
             "fix": "Remove every optional field you can't justify against a purpose."},
        ],
        "docs": ["retention_schedule"],
    },
    {
        "id": "GDPR-09", "framework": "GDPR", "category": "DPIA & DPO",
        "title": "DPIAs for high-risk processing; DPO designated if required",
        "why": "GDPR Art. 35/37: Data Protection Impact Assessments before high-risk processing; a DPO is mandatory for large-scale monitoring or public authorities.",
        "questions": [
            {"q": "Have you assessed whether any processing is 'high risk' (profiling, large-scale tracking, sensitive data)?", "weight": 2,
             "fix": "Run the DPIA screening checklist; complete a full DPIA where triggered."},
            {"q": "If required, is a DPO (internal or external) formally designated and published?", "weight": 1,
             "fix": "Designate a DPO and publish contact details in your privacy notice."},
        ],
        "docs": ["dpia_template"],
    },
    # ---------------- SOC 2 ----------------
    {
        "id": "SOC2-01", "framework": "SOC 2", "category": "Access Control",
        "title": "Logical access: joiner/mover/leaver process",
        "why": "SOC 2 CC6.1: access is provisioned on hire, changed on role change, and REVOKED on exit — promptly.",
        "questions": [
            {"q": "Is access revoked within 24 hours when someone leaves (including SaaS apps, not just email)?", "weight": 3,
             "fix": "Build an offboarding checklist covering every SaaS app; use SSO so one disable kills all sessions."},
            {"q": "Do you use SSO for all business apps (one identity, central control)?", "weight": 2,
             "fix": "Put every app behind SSO (Google Workspace / Okta / Entra); kill local passwords."},
            {"q": "Are admin/privileged accounts inventoried and reviewed quarterly?", "weight": 2,
             "fix": "List all admins; review quarterly; require approval for new grants."},
        ],
        "docs": ["access_policy"],
    },
    {
        "id": "SOC2-02", "framework": "SOC 2", "category": "Change Management",
        "title": "Tested, approved changes to production",
        "why": "SOC 2 CC8.1: changes are authorized, tested, and approved before hitting production.",
        "questions": [
            {"q": "Do production deploys require peer review / approval (no cowboy pushes)?", "weight": 3,
             "fix": "Require PR approval for main branch; protect the branch in GitHub/GitLab."},
            {"q": "Is there a staging/test environment where changes are verified first?", "weight": 2,
             "fix": "Stand up staging; make it a required deploy target before prod."},
            {"q": "Can you roll back a bad deploy quickly?", "weight": 1,
             "fix": "Document the rollback procedure; test it once per quarter."},
        ],
        "docs": ["change_policy"],
    },
    {
        "id": "SOC2-03", "framework": "SOC 2", "category": "Monitoring",
        "title": "Security monitoring and anomaly detection",
        "why": "SOC 2 CC7.2/CC7.3: you monitor system operations and detect anomalies — and someone actually looks.",
        "questions": [
            {"q": "Are security-relevant logs centralized and retained (auth, admin actions, data exports)?", "weight": 2,
             "fix": "Ship logs to one place; retain 12 months; alert on impossible logins and bulk exports."},
            {"q": "Is there an on-call rotation or named person who responds to security alerts?", "weight": 2,
             "fix": "Name the responder; document escalation; test with a fake alert."},
        ],
        "docs": ["security_policy", "incident_response"],
    },
    {
        "id": "SOC2-04", "framework": "SOC 2", "category": "Backups",
        "title": "Tested backups and recovery",
        "why": "SOC 2 CC7.2/A1.2: backups exist AND restore actually works when tested.",
        "questions": [
            {"q": "Are production databases backed up automatically (daily minimum)?", "weight": 3,
             "fix": "Enable automated daily backups with point-in-time recovery."},
            {"q": "Have you TESTED a restore in the last 6 months?", "weight": 3,
             "fix": "Do a restore drill to a sandbox; time it; document the runbook."},
        ],
        "docs": ["backup_runbook"],
    },
    {
        "id": "SOC2-05", "framework": "SOC 2", "category": "Vendor Management",
        "title": "Vendor risk reviews for critical suppliers",
        "why": "SOC 2 CC9.2: you assess the risks of the vendors your system depends on.",
        "questions": [
            {"q": "Do you review the security posture (SOC 2 report / questionnaire) of critical vendors annually?", "weight": 2,
             "fix": "Tier vendors by criticality; collect SOC 2 reports or security questionnaires yearly."},
        ],
        "docs": ["vendor_register"],
    },
    {
        "id": "SOC2-06", "framework": "SOC 2", "category": "Risk Assessment",
        "title": "Annual risk assessment performed",
        "why": "SOC 2 CC3: you identify, assess, and respond to risks to your objectives — at least annually.",
        "questions": [
            {"q": "Have you performed a documented risk assessment in the last 12 months?", "weight": 2,
             "fix": "Run the included risk assessment workshop template (assets, threats, likelihood, mitigations)."},
        ],
        "docs": ["risk_register"],
    },
    {
        "id": "SOC2-07", "framework": "SOC 2", "category": "Policies",
        "title": "Security policies published and acknowledged",
        "why": "SOC 2 CC2.2/CC5: expectations are communicated; people acknowledge them.",
        "questions": [
            {"q": "Do you have written information security policies staff have actually read and acknowledged?", "weight": 2,
             "fix": "Publish the generated security policy; collect written acknowledgment from all staff."},
            {"q": "Is there security awareness training at onboarding and annually?", "weight": 1,
             "fix": "30-minute onboarding module + annual phishing test."},
        ],
        "docs": ["security_policy"],
    },
]

FRAMEWORKS = {
    "GDPR": {
        "full": "EU General Data Protection Regulation (2016/679)",
        "applies": "You process personal data of people in the EU/EEA — almost certain if you have a website with EU visitors.",
        "fines": "Up to \u20ac20M or 4% of global turnover.",
    },
    "SOC 2": {
        "full": "SOC 2 Trust Services Criteria (AICPA)",
        "applies": "B2B SaaS selling to enterprises — customers increasingly demand a SOC 2 report before signing.",
        "fines": "No fines, but lost deals: enterprise procurement blocks vendors without SOC 2.",
    },
}
