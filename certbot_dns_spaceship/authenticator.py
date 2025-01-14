import logging
from typing import Any, Callable, Optional

import requests
from certbot.plugins.dns_common import DNSAuthenticator

logger = logging.getLogger(__name__)

class SpaceshipDNSAuthenticator(DNSAuthenticator):
    """Spaceship DNS Authenticator for Certbot"""

    description = "Obtain certificates using a DNS TXT record (DNS-01 challenge) for Spaceship DNS."

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[str] = None

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None]) -> None:
        super().add_parser_arguments(add)
        add("credentials", help="Path to Spaceship API credentials INI file")

    def _setup_credentials(self) -> None:
        self.credentials = self.conf("credentials")
        if not self.credentials:
            raise ValueError("Credentials file is required for Spaceship DNS plugin")

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_spaceship_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_spaceship_client().remove_txt_record(domain, validation_name, validation)

    def _get_spaceship_client(self) -> "SpaceshipClient":
        from .client import SpaceshipClient
        return SpaceshipClient(self.credentials)
