
# Certbot DNS Spaceship Plugin

This plugin integrates Certbot with the Spaceship DNS API to automate the DNS-01 challenge required for obtaining SSL/TLS certificates, including wildcard certificates.

## What This Plugin Does
This plugin simplifies the process of obtaining and renewing SSL/TLS certificates by automatically creating and removing the necessary DNS TXT records via the Spaceship DNS API. It is especially useful for domains requiring wildcard certificates (e.g., `*.example.com`).

## Features
- Automates the DNS-01 challenge for Spaceship-managed domains.
- Supports obtaining wildcard certificates.
- Integrates seamlessly with Certbot.

## Prerequisites
1. A valid Spaceship account.
2. API access enabled on your Spaceship account.
3. An API key and secret from Spaceship.

   - To create API keys, log in to your Spaceship account and navigate to the **API Manager** section. Follow the instructions to generate your API key and secret. (https://www.spaceship.com/application/api-manager/)

## Installation

1. Clone the repository or download the package:
   ```bash
   git clone https://github.com/version-two/certbot_dns_spaceship.git
   cd certbot-dns-spaceship
   ```

2. Install the plugin using pip:
   ```bash
   pip install .
   ```

## Configuration

1. Create a credentials file (e.g., `spaceship_credentials.ini`) and add your API key and secret:
   ```ini
   [spaceship]
   api_key = your_api_key
   api_secret = your_api_secret
   ```

   > **Important:** Secure your credentials file. Use file permissions to restrict access:
   > ```bash
   > chmod 600 spaceship_credentials.ini
   > ```

2. Test the credentials by ensuring you can query your Spaceship DNS zones via the API (optional).

## Usage

To obtain a wildcard SSL/TLS certificate for `example.com`:
```bash
certbot certonly   --authenticator dns-spaceship   --dns-spaceship-credentials /path/to/spaceship_credentials.ini   -d "*.example.com" -d "example.com"
```

### Renewing Certificates
Certbot automatically uses the plugin for renewal if it was used for the initial certificate request. To renew, simply run:
```bash
certbot renew
```

## API Rate Limits and Considerations
- The Spaceship API enforces rate limits (e.g., 300 requests per 300 seconds for listing domains).
- Ensure your API key has permissions to manage DNS records.

## Spaceship API Documentation
For more details about the Spaceship API, refer to the [Spaceship API Documentation](https://docs.spaceship.com).

## Development

1. Clone this repository:
   ```bash
   git clone https://github.com/version-two/certbot_dns_spaceship.git
   cd certbot-dns-spaceship
   ```

2. Install development dependencies:
   ```bash
   pip install -e .
   ```

3. Run tests to validate changes.

## Troubleshooting
- If you encounter authentication issues, verify your API key and secret.
- Ensure the `spaceship_credentials.ini` file is properly formatted and accessible.

## License

This plugin is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Support
For issues related to this plugin, create an issue in the [GitHub repository](https://github.com/your-username/certbot-dns-spaceship). For Spaceship account or API issues, contact [Spaceship Support](https://spaceship.com/support).
