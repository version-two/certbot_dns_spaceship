import requests
import configparser
from tldextract import extract

class SpaceshipClient:
    """Client to interact with the Spaceship DNS API."""

    def __init__(self, credentials_path: str) -> None:
        config = configparser.ConfigParser()
        config.read(credentials_path)

        self.api_key = config.get("spaceship", "api_key")
        self.api_secret = config.get("spaceship", "api_secret")
        self.base_url = "https://spaceship.dev/api/v1"

        if not self.api_key or not self.api_secret:
            raise ValueError("Spaceship credentials file is missing API key or secret")

    def _get_headers(self) -> dict:
        return {
            "X-Api-Key": self.api_key,
            "X-Api-Secret": self.api_secret,
            "Content-Type": "application/json"
        }

    def _get_main_domain(self, domain: str) -> str:
        extracted = extract(domain)
        if not extracted.domain or not extracted.suffix:
            raise ValueError(f"Unable to extract main domain from: {domain}")
        return f"{extracted.domain}.{extracted.suffix}"

    def add_txt_record(self, domain: str, name: str, content: str) -> None:
        """Create a TXT record for DNS-01 challenge."""
        main_domain = self._get_main_domain(domain)
        url = f"{self.base_url}/dns/records/{main_domain}"
        payload = {
            "force": True,
            "items": [
                {
                    "type": "TXT",
                    "name": name,
                    "value": content  # Ensure this field is included
                }
            ]
        }

        try:
            response = requests.put(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to add TXT record: {response.json()}")

    def remove_txt_record(self, domain: str, name: str, content: str) -> None:
        """Delete a TXT record for DNS-01 challenge."""
        main_domain = self._get_main_domain(domain)
        url = f"{self.base_url}/dns/records/{main_domain}"
        payload = [
            {
                "type": "TXT",
                "name": name,
                "value": content  # Ensure the correct field name
            }
        ]

        try:
            response = requests.delete(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error removing TXT record for {domain}: {e}")

    def list_records(self, domain: str, take: int = 100, skip: int = 0) -> dict:
        main_domain = self._get_main_domain(domain)
        url = f"{self.base_url}/dns/records/{main_domain}?take={take}&skip={skip}"

        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f"Failed to list DNS records: {response.json()}")
