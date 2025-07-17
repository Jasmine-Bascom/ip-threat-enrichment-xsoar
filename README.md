# IP Threat Enrichment for Cortex XSOAR

This project simulates a basic Cortex XSOAR playbook and integration that enriches IP addresses using a public threat intelligence API.

- Follows the XSOAR SDK integration format.
- Validates inputs to guard against unexpected behavior.
- Leverages `keyring` for secure API key storage.
- Enriches data from AbuseIPDB.
- Supports both local CLI testing and compatibility with XSOAR’s `main()` structure.

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

## Testing

This project includes a set of automated tests using pytest to verify core functionality of the integration code.

### Test Highlights
- Input validation and API interaction logic are tested.
- Tests mock external dependencies (like API key retrieval via `keyring`) to isolate and focus on functionality.
- For example, the API key retrieval is mocked in tests to ensure validation logic can be tested independently without requiring an actual API key.

### How to Run Tests

1. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Run tests with pytest:
    ```bash
    pytest
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
├── Integrations
│   ├── IPThreatEnrichment
│   ├── __init__.py
│   └── __pycache__
├── Local-Simulation
│   └── mockPlaybook.yml
├── Playbooks
│   ├── playbookBatchIPEnrichment.yml
│   ├── playbookIPEnrichment.yml
│   └── playbookMaliciousIPDecision.yml
├── README.md
├── requirements.txt
├── tests
│   ├── __init__.py
│   ├── __pycache__
│   └── test_ip_enrichment.py
└── venv
    ├── bin
    ├── include
    ├── lib
    └── pyvenv.cfg

```

---

## Security Note

This project avoids hardcoded credentials. API keys are stored and retrieved using `keyring` for secure local development. Inputs are validated using `ipaddress`.

---

## Playbooks Overview

This project includes several YAML-formatted playbooks that simulate how threat enrichment workflows could be automated within Cortex XSOAR:

- Playbooks/playbookIPEnrichment.yml

Enriches a single IP address via the custom integration. Ideal for small-scale testing or ad hoc enrichment of specific indicators.

- Playbooks/playbookBatchIPEnrichment.yml

Performs enrichment on a list of IP addresses, simulating ingestion from SIEM alerts or external feeds.

- Playbooks/playbookMaliciousIPDecision.yml

Extends the basic enrichment by evaluating risk scores and branching into actions such as blocklisting or alerting, modeling real-world SOAR workflows.

- Local-Simulation/mockPlaybook.yml

A simplified YAML structure for simulating playbook logic outside of XSOAR. Useful for understanding the basic flow of validation and enrichment in a CLI-friendly format.

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