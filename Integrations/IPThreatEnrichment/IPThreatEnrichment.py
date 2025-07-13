import requests
import keyring

# For real XSOAR use, you'll need this SDK:
# from CommonServerPython import *  ← Normally imported in XSOAR

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
        ip = sys.argv[1] if len(sys.argv) > 1 else None

        if not ip:
            raise ValueError("Missing IP address argument.")

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
