from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="arxiv_fetcher",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A system that automatically fetches papers from arXiv for specific research fields",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/arxiv-paper-fetcher",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "src": ["templates/*.html", "static/css/*.css"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "arxiv-fetcher=main:main",
        ],
    },
)