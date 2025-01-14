
from setuptools import setup, find_packages

setup(
    name="certbot-dns-spaceship",
    version="0.1.0",
    description="Spaceship DNS Authenticator plugin for Certbot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/certbot-dns-spaceship",
    author="Your Name",
    author_email="your-email@example.com",
    license="Apache License 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "certbot>=1.0.0",
        "requests",
    ],
    entry_points={
        "certbot.plugins": [
            "dns-spaceship = certbot_dns_spaceship.authenticator:SpaceshipDNSAuthenticator",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
)
    