from setuptools import setup, find_packages

setup(
    name="certbot-dns-spaceship",
    version="1.0.4",
    description="Spaceship DNS Authenticator plugin for Certbot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/version-two/certbot_dns_spaceship",
    author="Mario Chamuty",
    author_email="info@versiontwo.sk",
    license="Apache License 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "certbot>=1.0.0",
        "requests",
        "tldextract",
    ],
    entry_points={
        "certbot.plugins": [
            "dns-spaceship = certbot_dns_spaceship.authenticator:SpaceshipDNSAuthenticator",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
)
    