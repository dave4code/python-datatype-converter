from setuptools import setup, find_packages

setup(
    name="data-conversion-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "pandas",
        "tabulate",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="API for converting between XML, JSON, and CSV formats",
    keywords="api, conversion, data, xml, json, csv",
    url="https://github.com/yourusername/data-conversion-api",
)