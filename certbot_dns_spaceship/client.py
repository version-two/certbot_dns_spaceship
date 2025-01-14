
import requests
import configparser

class SpaceshipClient:
    """Client to interact with the Spaceship DNS API."""

    def __init__(self, credentials_path: str) -> None:
        config = configparser.ConfigParser()
        config.read(credentials_path)

        self.api_key = config.get("spaceship", "api_key")
        self.api_secret = config.get("spaceship", "api_secret")
        self.base_url = "https://api.spaceship.com/v1/domains"

        if not self.api_key or not self.api_secret:
            raise ValueError("Spaceship credentials file is missing API key or secret")

    def add_txt_record(self, domain: str, name: str, content: str) -> None:
        """Create a TXT record for DNS-01 challenge."""
        url = f"{self.base_url}/{domain}/dns-records"
        headers = {
            "X-Api-Key": self.api_key,
            "X-Api-Secret": self.api_secret,
        }
        payload = {
            "type": "TXT",
            "name": name,
            "content": content,
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

    def remove_txt_record(self, domain: str, name: str, content: str) -> None:
        """Delete a TXT record for DNS-01 challenge."""
        url = f"{self.base_url}/{domain}/dns-records"
        headers = {
            "X-Api-Key": self.api_key,
            "X-Api-Secret": self.api_secret,
        }

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        