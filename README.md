# 🛡️ AutoCompliance

**GDPR + SOC 2 compliance autopilot for small businesses.**

Compliance consultants charge $5,000–$50,000. AutoCompliance does the first 80% free, in 10 minutes:

```bash
pip install autocompliance
autocompliance assess --company "Acme Inc" --email privacy@acme.com
```

Answer ~40 yes/no questions. Get:

- 📊 **Compliance grade** (A–F) with per-framework scores
- 🎯 **Prioritized fix list** — critical → high → medium, each with a concrete remedy
- 📄 **14 document templates** — privacy policy, DPA, RoPA, incident response plan, security policy, DSR playbook, vendor register, retention schedule, and more
- 🖼️ **Client-ready HTML report** — show customers and auditors where you stand

## Why

- **GDPR fines** reach €20M or 4% of global turnover. Most SMBs have no idea where they stand.
- **SOC 2** is the #1 enterprise procurement blocker — no report, no deal.
- Existing tools are expensive, consultant-led, and built for enterprises. SMBs get nothing.

AutoCompliance is the open-source self-serve alternative: assess yourself, fix the gaps, generate the paperwork.

## Commands

```bash
# Full interactive assessment (GDPR + SOC 2)
autocompliance assess --company "Acme Inc" --email privacy@acme.com

# GDPR only
autocompliance assess --company "Acme Inc" --frameworks GDPR

# Just generate the document templates
autocompliance docs --company "Acme Inc" --email privacy@acme.com

# List all 16 controls
autocompliance controls
```

## What's inside

| Framework | Controls | Checks |
|---|---|---|
| GDPR | 9 (lawful basis, transparency, DSR, security, breach, RoPA, vendors, minimization, DPIA/DPO) | 22 |
| SOC 2 | 7 (access, change, monitoring, backups, vendors, risk, policies) | 18 |

## Roadmap

- [ ] Web UI + hosted SaaS version
- [ ] Evidence collection (auto-check TLS, DNS, headers)
- [ ] ISO 27001 module
- [ ] Auditor export pack

## Disclaimer

Templates are starting points, not legal advice. Have a lawyer review before relying on them.

## License

MIT — make compliance boring. 🛡️
