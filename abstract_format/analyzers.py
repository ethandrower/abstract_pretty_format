"""
Abstract analysis tools for identifying patterns and structure in scientific texts.
"""

import re
from enum import Enum
from typing import Dict, List, Tuple
from dataclasses import dataclass


class SectionType(Enum):
    """Enumeration of common scientific abstract section types."""
    BACKGROUND = "background"
    PURPOSE = "purpose"
    OBJECTIVE = "objective"
    METHODS = "methods"
    APPROACH = "approach"
    PROCEDURE = "procedure"
    RESULTS = "results"
    OUTCOMES = "outcomes"
    CONCLUSIONS = "conclusions"
    SIGNIFICANCE = "significance"
    UNKNOWN = "unknown"


@dataclass
class AbstractSection:
    """Represents a section within a scientific abstract."""
    section_type: SectionType
    content: str
    start_pos: int
    end_pos: int


class AbstractAnalyzer:
    """Analyzes scientific abstracts to identify structural patterns and content."""
    
    # Common section headers (case-insensitive)
    SECTION_PATTERNS = {
        SectionType.BACKGROUND: [r'\bBACKGROUND\b', r'\bINTRODUCTION\b'],
        SectionType.PURPOSE: [r'\bPURPOSE\b', r'\bAIM\b', r'\bAIMS\b'],
        SectionType.OBJECTIVE: [r'\bOBJECTIVE\b', r'\bOBJECTIVES\b'],
        SectionType.METHODS: [r'\bMETHODS\b', r'\bMETHODOLOGY\b', r'\bMATERIALS AND METHODS\b'],
        SectionType.APPROACH: [r'\bAPPROACH\b'],
        SectionType.PROCEDURE: [r'\bPROCEDURE\b', r'\bPROCEDURES\b'],
        SectionType.RESULTS: [r'\bRESULTS\b', r'\bFINDINGS\b', r'\bMAIN RESULTS\b'],
        SectionType.OUTCOMES: [r'\bOUTCOMES\b'],
        SectionType.CONCLUSIONS: [r'\bCONCLUSION\b', r'\bCONCLUSIONS\b'],
        SectionType.SIGNIFICANCE: [r'\bSIGNIFICANCE\b', r'\bIMPLICATIONS\b']
    }
    
    def find_section_headers(self, text: str) -> List[Tuple[SectionType, int, str]]:
        """Find all section headers in the text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of tuples containing (section_type, position, header_text)
        """
        headers = []
        
        for section_type, patterns in self.SECTION_PATTERNS.items():
            for pattern in patterns:
                # Look for pattern followed by colon or period
                full_pattern = pattern + r'\s*[:\.]'
                matches = re.finditer(full_pattern, text, re.IGNORECASE)
                
                for match in matches:
                    headers.append((section_type, match.start(), match.group()))
        
        # Sort by position
        headers.sort(key=lambda x: x[1])
        return headers
    
    def analyze_structure(self, text: str) -> Dict:
        """Analyze the overall structure of an abstract.
        
        Args:
            text: Input abstract text
            
        Returns:
            Dictionary containing structural analysis results
        """
        headers = self.find_section_headers(text)
        
        analysis = {
            'total_length': len(text),
            'word_count': len(text.split()),
            'sentence_count': len(re.findall(r'[.!?]+', text)),
            'has_structured_sections': len(headers) > 0,
            'section_headers': headers,
            'sections': self._extract_sections(text, headers),
            'technical_terms': self._find_technical_terms(text),
            'measurements': self._find_measurements(text)
        }
        
        return analysis
    
    def _extract_sections(self, text: str, headers: List[Tuple[SectionType, int, str]]) -> List[AbstractSection]:
        """Extract text sections based on identified headers."""
        sections = []
        
        for i, (section_type, start_pos, header_text) in enumerate(headers):
            # Find the end of this section (start of next section or end of text)
            if i + 1 < len(headers):
                end_pos = headers[i + 1][1]
            else:
                end_pos = len(text)
            
            # Extract content (skip the header itself)
            header_end = start_pos + len(header_text)
            content = text[header_end:end_pos].strip()
            
            sections.append(AbstractSection(
                section_type=section_type,
                content=content,
                start_pos=start_pos,
                end_pos=end_pos
            ))
        
        return sections
    
    def _find_technical_terms(self, text: str) -> List[str]:
        """Find technical terms and abbreviations."""
        # Find terms in parentheses (likely abbreviations)
        abbreviations = re.findall(r'\(([A-Z]{2,})\)', text)
        
        # Find measurement units
        units = re.findall(r'\b\d+(?:\.\d+)?\s*([A-Za-z]+)(?:\b|\d)', text)
        
        return list(set(abbreviations + units))
    
    def _find_measurements(self, text: str) -> List[str]:
        """Find numerical measurements and statistics."""
        # Pattern for numbers with units, percentages, ranges, etc.
        patterns = [
            r'\b\d+(?:\.\d+)?\s*[%±]',  # Percentages and ± values
            r'\b\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?',  # Ranges
            r'\b\d+(?:\.\d+)?\s*[A-Za-z]+(?:/[A-Za-z]+)*',  # Numbers with units
            r'[<>=≤≥]\s*\d+(?:\.\d+)?'  # Comparison operators
        ]
        
        measurements = []
        for pattern in patterns:
            measurements.extend(re.findall(pattern, text))
        
        return measurements