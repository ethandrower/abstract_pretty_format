"""
Setup configuration for abstract-format package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r') as f:
        requirements = [
            line.strip() for line in f.readlines() 
            if line.strip() and not line.startswith('#') and not line.startswith('http')
        ]
else:
    requirements = ["spacy>=3.4.0"]

setup(
    name="abstract-format",
    version="0.1.0",
    author="CiteMed Team",
    author_email="contact@citemed.ai",
    description="Transform dense scientific abstracts into readable, well-formatted text using advanced NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/citemed/abstract-format",
    project_urls={
        "Bug Reports": "https://github.com/citemed/abstract-format/issues",
        "Source": "https://github.com/citemed/abstract-format",
        "Documentation": "https://abstract-format.readthedocs.io",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing :: Linguistic", 
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0", 
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "build>=0.8.0",
            "twine>=4.0.0"
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "abstract-format=abstract_format.cli:main",
        ],
    },
    keywords=[
        "nlp", "scientific-text", "abstract", "formatting", 
        "text-processing", "spacy", "scientific-literature"
    ],
    include_package_data=True,
    zip_safe=False,
)