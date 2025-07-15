# IP Threat Enrichment for Cortex XSOAR

This project simulates a basic Cortex XSOAR playbook and integration that enriches IP addresses using a public threat intelligence API.

- Uses the XSOAR SDK format for structure.
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
Integrations/
└── IPThreatEnrichment/
    ├── IPThreatEnrichment.py      # Main logic and CLI-compatible main()
    └── IPThreatEnrichment.yml     # XSOAR integration metadata
Playbooks/
└── ThreatEnrichmentPlaybook.yml  # Simulated playbook calling the integration
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