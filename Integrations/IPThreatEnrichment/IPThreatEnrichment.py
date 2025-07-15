#!/usr/bin/env python3
import requests
import keyring
import ipaddress

# For real XSOAR use, you'll need this SDK:
# from CommonServerPython import *  ← Normally imported in XSOAR

def is_valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def ip_enrich_command(ip: str):
    api_key = keyring.get_password("xsoar", "abuseipdb_api_key")
    if not api_key:
        raise ValueError("API key not found. Please set it using keyring.")

    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return {
        'IP': ip,
        'RiskScore': data['data']['abuseConfidenceScore'],
        'Country': data['data']['countryCode'],
        'Domain': data['data'].get('domain'),
        'ISP': data['data'].get('isp')
    }

# This would be your actual entry point in XSOAR
def main():
    try:
        # In XSOAR, use this:
        # args = demisto.args()
        # ip = args.get("ip")

        # For local testing, use this:
        import sys
        if len(sys.argv) < 2:
            print("Usage: python IPThreatEnrichment.py <IP_ADDRESS>")
            sys.exit(1)

        ip = sys.argv[1]

        if not is_valid_ip(ip):
            print(f"Error: '{ip}' is not a valid IP address.")
            sys.exit(1)

        result = ip_enrich_command(ip)

        # In XSOAR:
        # return_results(CommandResults(
        #     outputs_prefix="IPThreatEnrichment.Result",
        #     outputs_key_field="IP",
        #     outputs=result,
        #     readable_output=f"IP Enrichment:\n{result}"
        # ))

        print("Enrichment result:")
        print(result)

    except Exception as e:
        # In XSOAR:
        # return_error(f"Failed to enrich IP: {str(e)}")

        print(f"Error: {e}")

if __name__ == "__main__":
    main()
