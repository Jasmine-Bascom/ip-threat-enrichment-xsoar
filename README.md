# IP Threat Enrichment for Cortex XSOAR

This project simulates a basic Cortex XSOAR playbook and integration that enriches IP addresses using a public threat intelligence API.

- Uses the XSOAR SDK format for structure.
- Validates inputs to prevent unintended downstream effects.
- Leverages `keyring` for secure API key storage.
- Enriches data from AbuseIPDB.
- Includes a `main()` function for compatibility with XSOAR or local CLI testing.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Jasmine-Bascom/ip-threat-enrichment-xsoar.git
cd ip-threat-enrichment-xsoar
```

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Store Your AbuseIPDB API Key Securely

```bash
python -c "import keyring; keyring.set_password('xsoar', 'abuseipdb_api_key', 'your-api-key')"
```

---

## Local Testing

Run the enrichment manually from the command line:

```bash
python ./Integrations/IPThreatEnrichment/IPThreatEnrichment.py 8.8.8.8
```

You should see JSON-style enrichment output for the IP address.

If no key is set, you'll see:

```
Error: API key not found. Please set it using keyring.
```

---

## Using in Cortex XSOAR

This script uses a format compatible with XSOAR custom integrations:

- `main()` expects input arguments using `demisto.args()`
- Uses `CommandResults` and `return_results()` for structured XSOAR output
- Outputs include IP, RiskScore, Country, ISP, and Domain

To adapt fully into XSOAR:

1. Replace `sys.argv` with `demisto.args()`
2. Use the `CommonServerPython` import and utilities
3. Register the integration and test it via XSOAR UI with `!ip-enrich ip=8.8.8.8`

---

## File Structure

```
ip-threat-enrichment-xsoar/
├── Integrations/
│   └── IPThreatEnrichment/
│       └── IPThreatEnrichment.py
├── Local-Simulation/
│   └── mockPlaybook.yml
├── Playbooks/
│   ├── playbookBatchIPEnrichment.yml
│   ├── playbookIPEnrichment.yml
│   └── playbookMaliciousIPDecision.yml
├── README.md
├── requirements.txt
└── venv/
    ├── bin/
    ├── include/
    ├── lib/
    └── pyvenv.cfg

```

---

## Future Expansion with XSOAR Access

This demo was developed without access to a full Cortex XSOAR instance, but it follows official development patterns outlined in xsoar.pan.dev, including Python-based automation, modular structure, and API integration.

With access to a production XSOAR environment, I would expand this project by:

- Packaging the script as a full custom integration using XSOAR’s integration framework

- Creating a visual playbook to automate IP enrichment and incident handling

- Connecting to live data sources (e.g., SIEM, EDR) to trigger the enrichment automatically

- Storing results in incident fields and tracking enrichment metrics

- Supporting full end-to-end testing in the XSOAR UI

This project demonstrates my understanding of SOAR principles and readiness to build scalable automations in a production environment.

---

## Security Note

This project avoids hardcoded credentials. API keys are stored and retrieved using `keyring` for secure local development. Inputs for the CLI version are validated using `ipaddress`.

---

## Playbooks Overview

This project includes several YAML-formatted playbooks that simulate how threat enrichment workflows could be automated within Cortex XSOAR:

- Playbooks/playbookIPEnrichment.yml

This playbook represents a basic automation sequence for enriching a single IP address. It calls the IPThreatEnrichment integration and saves the result. Useful for small-scale testing or a manual trigger on specific indicators.

- Playbooks/playbookBatchIPEnrichment.yml

Designed for bulk processing, this playbook takes a list of IP addresses and iteratively enriches each one. It's suitable for use cases where multiple IOCs (Indicators of Compromise) are ingested at once—e.g., from a SIEM alert or an external feed.

- Playbooks/playbookMaliciousIPDecision.yml

This playbook builds on the enrichment logic to include conditional decision-making. After enrichment, it evaluates the threat score or threat intelligence returned and performs an action (e.g., escalate, notify, or block) if the IP is deemed malicious. This mirrors real-world SOAR decision logic.

- Local-Simulation/mockPlaybook.yml

A simplified simulation of a playbook that demonstrates how input validation and enrichment could be chained together in a local test environment. This is useful for showcasing the structure and logic of a playbook even outside of XSOAR.