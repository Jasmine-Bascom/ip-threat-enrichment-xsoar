import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Integrations.IPThreatEnrichment.IPThreatEnrichment import enrich_ip, is_valid_ip
from unittest.mock import patch

def test_valid_ip():
    assert is_valid_ip("8.8.8.8")
    assert is_valid_ip("1.1.1.1")
    assert not is_valid_ip("not-an-ip")
    assert not is_valid_ip("256.0.0.1")


@patch("Integrations.IPThreatEnrichment.IPThreatEnrichment.keyring.get_password")
@patch("Integrations.IPThreatEnrichment.IPThreatEnrichment.call_abuseipdb")
def test_enrich_ip(mock_call_abuseipdb, mock_get_password):
    mock_get_password.return_value = "fake_api_key"
    mock_call_abuseipdb.return_value = {
        "data": {
            "abuseConfidenceScore": 85,
            "countryCode": "US",
            "isp": "Google LLC",
            "domain": "google.com"
        }
    }

    result = enrich_ip("8.8.8.8")
    assert result["IP"] == "8.8.8.8"
    assert result["RiskScore"] == 85
    assert result["Country"] == "US"
    assert result["ISP"] == "Google LLC"
    assert result["Domain"] == "google.com"


@patch("Integrations.IPThreatEnrichment.IPThreatEnrichment.keyring.get_password")
def test_enrich_ip_invalid_ip(mock_get_password):
    mock_get_password.return_value = "fake_api_key"  # mock valid API key so IP validation runs
    with pytest.raises(ValueError, match="Invalid IP address"):
        enrich_ip("not-an-ip")

@patch("Integrations.IPThreatEnrichment.IPThreatEnrichment.keyring.get_password")
def test_enrich_ip_missing_api_key(mock_get_password):
    mock_get_password.return_value = None
    with pytest.raises(ValueError, match="API key not found. Please set it using keyring."):
        enrich_ip("8.8.8.8")
