import requests
import configparser
from tldextract import extract  # Library for proper domain and TLD extraction

class SpaceshipClient:
    """Client to interact with the Spaceship DNS API."""

    def __init__(self, credentials_path: str) -> None:
        # Read the API credentials from the provided path
        config = configparser.ConfigParser()
        config.read(credentials_path)

        self.api_key = config.get("spaceship", "api_key")
        self.api_secret = config.get("spaceship", "api_secret")
        self.base_url = "https://spaceship.dev/api/v1"  # Base URL for Spaceship API

        if not self.api_key or not self.api_secret:
            raise ValueError("Spaceship credentials file is missing API key or secret")

    def _get_headers(self) -> dict:
        """Prepare API headers for authentication."""
        return {
            "X-Api-Key": self.api_key,
            "X-Api-Secret": self.api_secret,
        }

    def _get_main_domain(self, domain: str) -> str:
        """
        Extract the main domain (e.g., `acechange.io`) from a full domain name.
        Uses tldextract for accurate extraction of the domain and TLD.
        """
        extracted = extract(domain)
        if not extracted.domain or not extracted.suffix:
            raise ValueError(f"Unable to extract main domain from: {domain}")
        return f"{extracted.domain}.{extracted.suffix}"

    def add_txt_record(self, domain: str, name: str, content: str) -> None:
        """Create a TXT record for DNS-01 challenge."""
        main_domain = self._get_main_domain(domain)
        url = f"{self.base_url}/dns/records/{main_domain}"
        payload = {
            "type": "TXT",
            "name": name,
            "content": content,
        }

        try:
            # Make a POST request to create the TXT record
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error adding TXT record for {domain}: {e}")

    def remove_txt_record(self, domain: str, name: str, content: str) -> None:
        """Delete a TXT record for DNS-01 challenge."""
        main_domain = self._get_main_domain(domain)
        url = f"{self.base_url}/dns/records/{main_domain}"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            records = response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error retrieving DNS records for {domain}: {e}")

        # Find the record ID matching the name and content
        record_id = None
        for record in records:
            if (
                record["type"] == "TXT"
                and record["name"] == name
                and record["content"] == content
            ):
                record_id = record["id"]
                break

        if not record_id:
            raise ValueError(f"TXT record for {name} not found.")

        # Delete the specific DNS record
        delete_url = f"{url}/{record_id}"
        try:
            delete_response = requests.delete(delete_url, headers=self._get_headers())
            delete_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error removing TXT record for {domain}: {e}")
