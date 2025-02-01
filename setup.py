from setuptools import setup, find_packages

setup(
    name="simple_agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit>=1.32.0",
        "openai>=1.12.0",
        "python-dotenv>=1.0.1",
        "google-search-results>=2.4.2",
    ],
) 