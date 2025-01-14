import requests
import configparser

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

    def _get_domain_info(self, domain: str) -> dict:
        """
        Retrieve information about the specified domain.
        Tries the full domain first (e.g., `in.acechange.io`) and falls back to the main domain (e.g., `acechange.io`).
        """
        tried_domains = [domain, domain.split('.', 1)[-1]]  # Try `in.acechange.io`, then `acechange.io`
        errors = []  # Collect errors for all attempts

        for domain_try in tried_domains:
            url = f"{self.base_url}/domains/{domain_try}"
            try:
                # Attempt to fetch domain information
                response = requests.get(url, headers=self._get_headers())
                if response.status_code == 200:
                    return response.json()  # Successfully found domain
                elif response.status_code == 404:
                    errors.append(f"Domain not found: {domain_try}")
                else:
                    errors.append(f"Unexpected response for {domain_try}: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                # Catch network or request-related errors
                errors.append(f"Request error for {domain_try}: {str(e)}")

        # Raise a descriptive error if no domains were found
        error_message = (
            f"Unable to find domain information. Tried the following domains: {', '.join(tried_domains)}. "
            f"Errors encountered: {', '.join(errors)}"
        )
        raise ValueError(error_message)

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

        try:
            # Make a POST request to create the TXT record
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error adding TXT record for {domain}: {e}")

    def remove_txt_record(self, domain: str, name: str, content: str) -> None:
        """Delete a TXT record for DNS-01 challenge."""
        domain_info = self._get_domain_info(domain)
        domain_id = domain_info.get("id")
        if not domain_id:
            raise ValueError(f"Domain ID for {domain} not found.")

        # Fetch existing DNS records to find the record ID
        url = f"{self.base_url}/domains/{domain_id}/dns-records"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            records = response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error retrieving DNS records for {domain}: {e}")

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
        try:
            delete_response = requests.delete(delete_url, headers=self._get_headers())
            delete_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error removing TXT record for {domain}: {e}")
