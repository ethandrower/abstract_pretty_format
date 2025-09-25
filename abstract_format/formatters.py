"""
Abstract formatting implementations using different strategies.
"""

import re
import textwrap
from typing import Dict, List, Optional

from .analyzers import AbstractAnalyzer, SectionType


class AbstractFormatter:
    """Basic abstract formatter using regex patterns and heuristics."""
    
    def __init__(self, line_width: int = 80, indent_size: int = 2):
        """Initialize the formatter.
        
        Args:
            line_width: Maximum line width for text wrapping
            indent_size: Number of spaces for indentation
        """
        self.analyzer = AbstractAnalyzer()
        self.line_width = line_width
        self.indent_size = indent_size
    
    def format_abstract(self, text: str, output_format: str = 'markdown') -> str:
        """Format an abstract for improved readability.
        
        Args:
            text: Input abstract text
            output_format: Output format ('markdown', 'html', 'plain')
            
        Returns:
            Formatted abstract text
        """
        # Analyze the structure first
        analysis = self.analyzer.analyze_structure(text)
        
        if analysis['has_structured_sections']:
            return self._format_structured_abstract(text, analysis, output_format)
        else:
            return self._format_unstructured_abstract(text, analysis, output_format)
    
    def _format_structured_abstract(self, text: str, analysis: Dict, output_format: str) -> str:
        """Format an abstract that has clear section headers."""
        formatted_sections = []
        
        # Handle text before first section
        first_section_start = analysis['sections'][0].start_pos if analysis['sections'] else len(text)
        if first_section_start > 0:
            intro_text = text[:first_section_start].strip()
            if intro_text:
                formatted_sections.append(self._format_section_content(intro_text, output_format))
        
        # Format each identified section
        for section in analysis['sections']:
            section_header = self._format_section_header(section.section_type, output_format)
            section_content = self._format_section_content(section.content, output_format)
            
            formatted_sections.append(section_header)
            formatted_sections.append(section_content)
        
        return '\n\n'.join(formatted_sections)
    
    def _format_unstructured_abstract(self, text: str, analysis: Dict, output_format: str) -> str:
        """Format an abstract without clear section headers using heuristics."""
        # Split into sentences
        sentences = self._split_sentences(text)
        
        # Try to identify implicit sections based on content patterns
        grouped_sentences = self._group_sentences_by_topic(sentences)
        
        # Format as paragraphs
        formatted_paragraphs = []
        for group in grouped_sentences:
            paragraph_text = ' '.join(group)
            formatted_paragraph = self._format_section_content(paragraph_text, output_format)
            formatted_paragraphs.append(formatted_paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _format_section_header(self, section_type: SectionType, output_format: str) -> str:
        """Format a section header."""
        header_text = section_type.value.upper()
        
        if output_format == 'markdown':
            return f"### {header_text}"
        elif output_format == 'html':
            return f"<h3>{header_text}</h3>"
        else:  # plain text
            return f"\n{header_text}\n{'=' * len(header_text)}"
    
    def _format_section_content(self, content: str, output_format: str) -> str:
        """Format section content with proper wrapping and emphasis."""
        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Highlight technical terms and measurements
        content = self._highlight_technical_terms(content, output_format)
        
        # Wrap text to appropriate line width
        wrapped = textwrap.fill(content, width=self.line_width)
        
        return wrapped
    
    def _highlight_technical_terms(self, text: str, output_format: str) -> str:
        """Highlight important technical terms and measurements."""
        if output_format not in ['markdown', 'html']:
            return text
        
        # Highlight abbreviations in parentheses
        if output_format == 'markdown':
            text = re.sub(r'\(([A-Z]{2,})\)', r'(**\1**)', text)
            # Highlight numerical results
            text = re.sub(r'(\b\d+(?:\.\d+)?\s*[%±]\s*\d*(?:\.\d+)?)', r'**\1**', text)
        elif output_format == 'html':
            text = re.sub(r'\(([A-Z]{2,})\)', r'(<strong>\1</strong>)', text)
            text = re.sub(r'(\b\d+(?:\.\d+)?\s*[%±]\s*\d*(?:\.\d+)?)', r'<strong>\1</strong>', text)
        
        return text
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling abbreviations carefully."""
        # Simple sentence splitting (could be improved with NLTK/spaCy)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _group_sentences_by_topic(self, sentences: List[str]) -> List[List[str]]:
        """Group sentences into topical paragraphs using simple heuristics."""
        if len(sentences) <= 3:
            return [sentences]
        
        # Simple grouping: break at sentences that seem to introduce new topics
        groups = []
        current_group = []
        
        topic_starters = [r'^We ', r'^Our ', r'^The study', r'^This study', r'^Results', r'^In conclusion']
        
        for sentence in sentences:
            is_topic_starter = any(re.match(pattern, sentence, re.IGNORECASE) for pattern in topic_starters)
            
            if is_topic_starter and current_group:
                groups.append(current_group)
                current_group = [sentence]
            else:
                current_group.append(sentence)
        
        if current_group:
            groups.append(current_group)
        
        return groups


class SpacyAbstractFormatter:
    """Enhanced abstract formatter using spaCy for better NLP processing."""
    
    def __init__(self, line_width: int = 80):
        """Initialize the spaCy formatter.
        
        Args:
            line_width: Maximum line width for text wrapping
        """
        self.line_width = line_width
        
        # Load English model
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except (ImportError, OSError) as e:
            print(f"⚠️  spaCy not available: {e}")
            print("   Install with: pip install spacy && python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Discourse markers that signal topic shifts/transitions
        self.discourse_markers = {
            'contrast': ['however', 'nevertheless', 'nonetheless', 'conversely', 'in contrast', 'on the other hand'],
            'addition': ['additionally', 'furthermore', 'moreover', 'also', 'in addition', 'besides'],
            'result': ['consequently', 'therefore', 'thus', 'as a result', 'hence', 'accordingly'],
            'sequence': ['first', 'second', 'third', 'next', 'then', 'finally', 'subsequently'],
            'emphasis': ['importantly', 'notably', 'significantly', 'remarkably'],
            'conclusion': ['in conclusion', 'in summary', 'to conclude', 'overall', 'in brief']
        }
        
        # Flatten into a single list for easy checking
        self.all_markers = [marker for markers in self.discourse_markers.values() for marker in markers]
    
    def format_abstract(self, text: str, output_format: str = 'markdown') -> str:
        """Format abstract using spaCy for better text analysis.
        
        Args:
            text: Input abstract text
            output_format: Output format ('markdown', 'html', 'plain')
            
        Returns:
            Formatted abstract text
        """
        if not self.nlp:
            # Fallback to basic formatter
            basic_formatter = AbstractFormatter(line_width=self.line_width)
            return basic_formatter.format_abstract(text, output_format)
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # Check for explicit section headers first
        if self._has_section_headers(text):
            return self._format_structured_abstract(text, output_format)
        else:
            return self._format_unstructured_abstract_spacy(doc, output_format)
    
    def _has_section_headers(self, text: str) -> bool:
        """Check if text has explicit section headers."""
        section_patterns = [
            r'\bBACKGROUND\s*:', r'\bPURPOSE\s*:', r'\bMETHODS\s*:', 
            r'\bRESULTS\s*:', r'\bCONCLUSION\s*:', r'\bOBJECTIVE\s*:'
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in section_patterns)
    
    def _format_structured_abstract(self, text: str, output_format: str) -> str:
        """Handle abstracts with explicit section headers."""
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Find section boundaries
        sections = []
        current_section = []
        current_header = None
        
        for sentence in sentences:
            header_match = re.match(r'^(BACKGROUND|PURPOSE|METHODS|RESULTS|CONCLUSION|OBJECTIVE)\s*:\s*(.*)', 
                                  sentence, re.IGNORECASE)
            if header_match:
                if current_section and current_header:
                    sections.append((current_header, current_section))
                current_header = header_match.group(1).upper()
                remaining_text = header_match.group(2).strip()
                current_section = [remaining_text] if remaining_text else []
            else:
                current_section.append(sentence)
        
        if current_section and current_header:
            sections.append((current_header, current_section))
        
        # Format sections
        formatted_sections = []
        for header, content in sections:
            if output_format == 'markdown':
                formatted_sections.append(f"### {header}")
            
            paragraph_text = ' '.join(content)
            formatted_content = self._format_content(paragraph_text, output_format)
            formatted_sections.append(formatted_content)
        
        return '\n\n'.join(formatted_sections)
    
    def _format_unstructured_abstract_spacy(self, doc, output_format: str) -> str:
        """Format unstructured abstract using spaCy's advanced features."""
        sentences = [sent for sent in doc.sents]
        
        if len(sentences) <= 3:
            text = ' '.join([sent.text.strip() for sent in sentences])
            return self._format_content(text, output_format)
        
        # Group sentences using discourse markers and other strategies
        groups = self._smart_sentence_grouping(sentences)
        
        # Format each group as a paragraph
        formatted_paragraphs = []
        for group in groups:
            paragraph_text = ' '.join([sent.text.strip() for sent in group])
            formatted_paragraph = self._format_content(paragraph_text, output_format)
            formatted_paragraphs.append(formatted_paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _smart_sentence_grouping(self, sentences) -> List[List]:
        """Group sentences using discourse markers and NLP strategies."""
        if len(sentences) <= 4:
            return [sentences]
        
        groups = []
        current_group = []
        
        for i, sent in enumerate(sentences):
            sent_text = sent.text.strip()
            
            # Primary strategy: Discourse markers
            has_discourse_marker = self._starts_with_discourse_marker(sent_text)
            
            # Secondary strategies
            is_topic_transition = self._is_topic_transition(sent_text)
            has_entity_shift = False
            if i > 0 and current_group:
                has_entity_shift = self._has_significant_entity_shift(current_group[-1], sent)
            
            is_results_section = self._is_results_indicator(sent_text)
            group_too_long = len(current_group) >= 4
            
            # Decision logic: prioritize discourse markers
            should_break = (has_discourse_marker and current_group) or \
                          (is_topic_transition and current_group and len(current_group) >= 2) or \
                          (has_entity_shift and len(current_group) >= 3) or \
                          (is_results_section and current_group and 
                           not self._is_results_indicator(' '.join([s.text for s in current_group]))) or \
                          group_too_long
            
            if should_break:
                groups.append(current_group)
                current_group = [sent]
            else:
                current_group.append(sent)
        
        if current_group:
            groups.append(current_group)
        
        return self._merge_short_groups(groups)
    
    def _starts_with_discourse_marker(self, sentence: str) -> bool:
        """Check if sentence starts with a discourse marker followed by comma."""
        sentence_lower = sentence.lower()
        
        # Check for discourse markers at the beginning, possibly followed by comma
        for marker in self.all_markers:
            # Pattern: marker at start, followed by comma or space
            if sentence_lower.startswith(marker.lower()):
                after_marker_pos = len(marker)
                if after_marker_pos < len(sentence):
                    next_char = sentence[after_marker_pos]
                    # Must be followed by comma, space, or punctuation
                    if next_char in [',', ' ', '.', ';']:
                        return True
        
        return False
    
    def _is_topic_transition(self, sentence: str) -> bool:
        """Detect sentences that likely start new topics."""
        transition_patterns = [
            r'^(We|Our|The study|This study|The present study)',
            r'^(The \w+ (was|were|showed|demonstrated|indicated))',
            r'^(To |In order to)',
            r'^(Analysis|Investigation|Evaluation) (showed|revealed|demonstrated)'
        ]
        return any(re.match(pattern, sentence, re.IGNORECASE) for pattern in transition_patterns)
    
    def _has_significant_entity_shift(self, prev_sent, curr_sent) -> bool:
        """Check if there's a significant shift in named entities."""
        prev_entities = set([ent.text.lower() for ent in prev_sent.ents 
                           if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'PERSON']])
        curr_entities = set([ent.text.lower() for ent in curr_sent.ents 
                           if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'PERSON']])
        
        if not prev_entities or not curr_entities:
            return False
        
        overlap = len(prev_entities.intersection(curr_entities))
        total_unique = len(prev_entities.union(curr_entities))
        return (overlap / total_unique) < 0.3 if total_unique > 0 else False
    
    def _is_results_indicator(self, text: str) -> bool:
        """Check if sentence indicates results/findings section."""
        result_patterns = [
            r'\b(showed|demonstrated|revealed|found|indicated|observed)\b',
            r'\b(\d+(?:\.\d+)?%|\d+±\d+|\d+ out of \d+)\b',
            r'\b(significant|significantly|correlation|p\s*[<>=])\b',
            r'\b(average|mean|median|range|between.*and)\b'
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in result_patterns)
    
    def _merge_short_groups(self, groups) -> List[List]:
        """Merge groups that are too short with their neighbors."""
        if len(groups) <= 1:
            return groups
        
        merged = []
        i = 0
        
        while i < len(groups):
            current_group = groups[i]
            
            # If current group is very short (1 sentence) and not the last group
            if len(current_group) == 1 and i < len(groups) - 1:
                current_group.extend(groups[i + 1])
                i += 2
            else:
                i += 1
            
            merged.append(current_group)
        
        return merged
    
    def _format_content(self, text: str, output_format: str) -> str:
        """Format content with technical term highlighting."""
        text = re.sub(r'\s+', ' ', text.strip())
        
        if output_format in ['markdown', 'html']:
            text = self._highlight_technical_terms_spacy(text, output_format)
        
        wrapped = textwrap.fill(text, width=self.line_width)
        return wrapped
    
    def _highlight_technical_terms_spacy(self, text: str, output_format: str) -> str:
        """Enhanced technical term highlighting."""
        if output_format == 'markdown':
            # Highlight abbreviations in parentheses
            text = re.sub(r'\(([A-Z]{2,})\)', r'(**\1**)', text)
            
            # Highlight numerical results and measurements
            text = re.sub(r'(\b\d+(?:\.\d+)?(?:\s*[%±]\s*\d*(?:\.\d+)?|\s*-\s*\d+(?:\.\d+)?|×))', r'**\1**', text)
            
            # Highlight statistical significance
            text = re.sub(r'([<>=]?\s*p\s*[<>=]\s*0\.\d+)', r'**\1**', text)
            
        elif output_format == 'html':
            text = re.sub(r'\(([A-Z]{2,})\)', r'(<strong>\1</strong>)', text)
            text = re.sub(r'(\b\d+(?:\.\d+)?(?:\s*[%±]\s*\d*(?:\.\d+)?|\s*-\s*\d+(?:\.\d+)?|×))', r'<strong>\1</strong>', text)
            text = re.sub(r'([<>=]?\s*p\s*[<>=]\s*0\.\d+)', r'<strong>\1</strong>', text)
        
        return text