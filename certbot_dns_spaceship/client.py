import requests
import configparser

class SpaceshipClient:
    """Client to interact with the Spaceship DNS API."""

    def __init__(self, credentials_path: str) -> None:
        config = configparser.ConfigParser()
        config.read(credentials_path)

        self.api_key = config.get("spaceship", "api_key")
        self.api_secret = config.get("spaceship", "api_secret")
        self.base_url = "https://spaceship.dev/api/v1"  # Updated base URL

        if not self.api_key or not self.api_secret:
            raise ValueError("Spaceship credentials file is missing API key or secret")

    def _get_headers(self) -> dict:
        """Prepare API headers."""
        return {
            "X-Api-Key": self.api_key,
            "X-Api-Secret": self.api_secret,
        }

    def _get_domain_info(self, domain: str) -> dict:
        """
        Retrieve information about the specified domain.
        Tries the full domain first (e.g., `in.acechange.io`) and falls back to the main domain (e.g., `acechange.io`).
        """
        for domain_try in [domain, domain.split('.', 1)[-1]]:  # Try `in.acechange.io` then `acechange.io`
            url = f"{self.base_url}/domains/{domain_try}"
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                continue  # Try the fallback
            response.raise_for_status()

        raise ValueError(f"Neither {domain} nor its parent domain found in Spaceship account.")

    def add_txt_record(self, domain: str, name: str, content: str) -> None:
        """Create a TXT record for DNS-01 challenge."""
        domain_info = self._get_domain_info(domain)
        domain_id = domain_info.get("id")
        if not domain_id:
            raise ValueError(f"Domain ID for {domain} not found.")

        url = f"{self.base_url}/domains/{domain_id}/dns-records"
        payload = {
            "type": "TXT",
            "name": name,
            "content": content,
        }

        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()

    def remove_txt_record(self, domain: str, name: str, content: str) -> None:
        """Delete a TXT record for DNS-01 challenge."""
        domain_info = self._get_domain_info(domain)
        domain_id = domain_info.get("id")
        if not domain_id:
            raise ValueError(f"Domain ID for {domain} not found.")

        # Fetch existing DNS records to find the record ID
        url = f"{self.base_url}/domains/{domain_id}/dns-records"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        records = response.json()

        # Find the record ID matching the name and content
        record_id = None
        for record in records:
            if record["type"] == "TXT" and record["name"] == name and record["content"] == content:
                record_id = record["id"]
                break

        if not record_id:
            raise ValueError(f"TXT record for {name} not found.")

        # Delete the specific DNS record
        delete_url = f"{url}/{record_id}"
        delete_response = requests.delete(delete_url, headers=self._get_headers())
        delete_response.raise_for_status()
