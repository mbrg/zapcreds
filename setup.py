from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

with open("var.txt", "r") as fp:
    ver = fp.read()

setup(
    name="zapcreds",
    version=ver,
    author="Zenity",
    author_email="hello@zenity.io",
    description="Recon tool to harvest credentials from Zapier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbrg/zapcreds",
    keywords="Zapier Recon Reconnaissance AppSec Zenity Security LowCode NoCode",
    project_urls={
        "Bug Tracker": "https://github.com/mbrg/zapcreds/issues",
        "Source": "https://github.com/mbrg/zapcreds",
        "Zenity": "https://zenity.io",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=["python=^3.10", "pandas=^1.4.1", "requests=^2.27.1"],
    entry_points={"console_scripts": ["zapcreds=zapcreds.main:main"]},
)
