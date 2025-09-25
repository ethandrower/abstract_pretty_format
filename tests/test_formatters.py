"""
Tests for abstract formatters.
"""

import pytest
from abstract_format import AbstractFormatter, SpacyAbstractFormatter
from abstract_format.analyzers import SectionType


class TestAbstractFormatter:
    """Test cases for the basic AbstractFormatter."""
    
    def test_structured_abstract(self):
        """Test formatting of structured abstract with section headers."""
        text = ("BACKGROUND: This is background text. "
                "METHODS: This is methods text. "
                "RESULTS: This shows results.")
        
        formatter = AbstractFormatter()
        result = formatter.format_abstract(text)
        
        assert "### BACKGROUND" in result
        assert "### METHODS" in result 
        assert "### RESULTS" in result
        assert "background text" in result.lower()
    
    def test_unstructured_abstract(self):
        """Test formatting of unstructured abstract."""
        text = ("We tested a new approach. "
                "The results were promising. "
                "Our method showed improvement.")
        
        formatter = AbstractFormatter()
        result = formatter.format_abstract(text)
        
        # Should create at least one paragraph
        assert len(result.strip()) > 0
        assert "We tested" in result
    
    def test_technical_term_highlighting_markdown(self):
        """Test highlighting of technical terms in markdown format."""
        text = "The method used MRI (Magnetic Resonance Imaging) with 95% accuracy."
        
        formatter = AbstractFormatter()
        result = formatter.format_abstract(text, output_format='markdown')
        
        # Should highlight abbreviation and percentage
        assert "(**MRI**)" in result or "**MRI**" in result
        assert "**95%**" in result
    
    def test_technical_term_highlighting_html(self):
        """Test highlighting of technical terms in HTML format."""
        text = "The MRI (Medical Imaging) showed 85% improvement."
        
        formatter = AbstractFormatter()
        result = formatter.format_abstract(text, output_format='html')
        
        # Should highlight abbreviation and percentage
        assert "<strong>" in result
    
    def test_line_width_wrapping(self):
        """Test text wrapping at specified line width."""
        long_text = "This is a very long sentence that should be wrapped " * 5
        
        formatter = AbstractFormatter(line_width=50)
        result = formatter.format_abstract(long_text)
        
        lines = result.split('\n')
        # Most lines should be <= 50 characters (allowing some flexibility for word boundaries)
        long_lines = [line for line in lines if len(line) > 60]
        assert len(long_lines) == 0, f"Lines too long: {long_lines}"


class TestSpacyAbstractFormatter:
    """Test cases for the spaCy-enhanced formatter."""
    
    def test_discourse_marker_detection(self):
        """Test detection of discourse markers."""
        formatter = SpacyAbstractFormatter()
        
        # Test various discourse markers
        test_cases = [
            "However, this approach failed.",
            "Additionally, we found issues.",
            "Consequently, we changed methods.",
            "Furthermore, the results improved."
        ]
        
        for sentence in test_cases:
            has_marker = formatter._starts_with_discourse_marker(sentence)
            assert has_marker, f"Should detect discourse marker in: {sentence}"
    
    def test_discourse_marker_paragraph_breaks(self):
        """Test that discourse markers create paragraph breaks."""
        text = ("We started with method A. "
                "However, this approach had limitations. "
                "Additionally, we tried method B. "
                "Consequently, we achieved better results.")
        
        formatter = SpacyAbstractFormatter()
        # Skip test if spaCy not available
        if not formatter.nlp:
            pytest.skip("spaCy not available")
            
        result = formatter.format_abstract(text)
        
        # Should create multiple paragraphs due to discourse markers
        paragraphs = [p.strip() for p in result.split('\n\n') if p.strip()]
        assert len(paragraphs) > 1, f"Expected multiple paragraphs, got: {paragraphs}"
    
    def test_fallback_to_basic_formatter(self):
        """Test fallback when spaCy is not available."""
        # Create formatter without spaCy
        formatter = SpacyAbstractFormatter()
        original_nlp = formatter.nlp
        formatter.nlp = None  # Simulate spaCy not available
        
        text = "This is a test abstract. It should still be formatted."
        result = formatter.format_abstract(text)
        
        # Should still produce output
        assert len(result.strip()) > 0
        assert "test abstract" in result
        
        # Restore original state
        formatter.nlp = original_nlp
    
    def test_structured_vs_unstructured_detection(self):
        """Test detection of structured vs unstructured abstracts."""
        formatter = SpacyAbstractFormatter()
        
        structured_text = "BACKGROUND: Some text. METHODS: More text."
        unstructured_text = "We conducted a study. The results were interesting."
        
        assert formatter._has_section_headers(structured_text)
        assert not formatter._has_section_headers(unstructured_text)


class TestFormatterComparison:
    """Compare basic vs spaCy formatters."""
    
    def test_content_preservation(self):
        """Test that both formatters preserve content."""
        test_text = ("This is a test abstract with technical terms like "
                    "MRI (Magnetic Resonance Imaging) and statistics like 95% accuracy. "
                    "However, we found some limitations. "
                    "Additionally, further research is needed.")
        
        basic_formatter = AbstractFormatter()
        spacy_formatter = SpacyAbstractFormatter()
        
        basic_result = basic_formatter.format_abstract(test_text, output_format='plain')
        
        if spacy_formatter.nlp:
            spacy_result = spacy_formatter.format_abstract(test_text, output_format='plain')
        else:
            pytest.skip("spaCy not available")
            return
        
        # Remove formatting and compare word content
        basic_words = set(basic_result.lower().split())
        spacy_words = set(spacy_result.lower().split())
        original_words = set(test_text.lower().split())
        
        # Both should preserve most original words
        basic_preservation = len(basic_words.intersection(original_words)) / len(original_words)
        spacy_preservation = len(spacy_words.intersection(original_words)) / len(original_words)
        
        assert basic_preservation > 0.95, f"Basic formatter preserved {basic_preservation:.2%} of words"
        assert spacy_preservation > 0.95, f"spaCy formatter preserved {spacy_preservation:.2%} of words"