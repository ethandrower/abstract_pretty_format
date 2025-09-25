"""
Abstract Format - A Python library for making scientific abstracts readable.

This library provides tools to automatically format dense, unreadable scientific abstracts
into well-structured, readable text with proper paragraph breaks and highlighting of 
technical terms.

Main classes:
- AbstractFormatter: Basic formatter using regex patterns
- SpacyAbstractFormatter: Advanced formatter using spaCy NLP
- ScientificDocumentFormatter: Extensible framework for different document types
"""

__version__ = "0.1.0"
__author__ = "CiteMed Team"
__email__ = "contact@citemed.ai"

from .formatters import AbstractFormatter, SpacyAbstractFormatter
from .document_processor import ScientificDocumentFormatter, DocumentProcessor
from .analyzers import AbstractAnalyzer, SectionType

__all__ = [
    "AbstractFormatter",
    "SpacyAbstractFormatter", 
    "ScientificDocumentFormatter",
    "DocumentProcessor",
    "AbstractAnalyzer",
    "SectionType"
]