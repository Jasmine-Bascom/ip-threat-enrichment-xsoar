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

def call_abuseipdb(ip, api_key):
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def enrich_ip(ip):
    api_key = keyring.get_password("xsoar", "abuseipdb_api_key")
    if not api_key:
        raise ValueError("API key not found. Please set it using keyring.")
    if not is_valid_ip(ip):
        raise ValueError("Invalid IP address")
    result = call_abuseipdb(ip, api_key)
    # Process the response JSON to extract relevant fields
    data = result.get("data", {})
    enriched = {
        "IP": ip,
        "RiskScore": data.get("abuseConfidenceScore"),
        "Country": data.get("countryCode"),
        "ISP": data.get("isp"),
        "Domain": data.get("domain"),
    }
    return enriched

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
