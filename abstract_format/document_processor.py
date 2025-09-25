"""
Extensible document processing framework for different types of scientific documents.
"""

from abc import ABC, abstractmethod
from typing import Union, Dict, Any

from .formatters import AbstractFormatter, SpacyAbstractFormatter


class DocumentProcessor(ABC):
    """Abstract base class for document processors."""
    
    @abstractmethod
    def can_process(self, document: Union[str, dict]) -> bool:
        """Check if this processor can handle the given document.
        
        Args:
            document: Document content as string or dictionary
            
        Returns:
            True if this processor can handle the document
        """
        pass
    
    @abstractmethod
    def process(self, document: Union[str, dict], **kwargs) -> str:
        """Process the document and return formatted output.
        
        Args:
            document: Document content as string or dictionary
            **kwargs: Additional processing options
            
        Returns:
            Formatted document content
        """
        pass


class AbstractProcessor(DocumentProcessor):
    """Processor for scientific abstracts."""
    
    def __init__(self, use_spacy: bool = True):
        """Initialize the abstract processor.
        
        Args:
            use_spacy: Whether to use spaCy-enhanced formatting (default: True)
        """
        if use_spacy:
            self.formatter = SpacyAbstractFormatter()
        else:
            self.formatter = AbstractFormatter()
    
    def can_process(self, document: Union[str, dict]) -> bool:
        """Check if document looks like an abstract.
        
        Args:
            document: Document to check
            
        Returns:
            True if document appears to be an abstract
        """
        if isinstance(document, dict):
            return 'abstract' in document or 'summary' in document
        
        # Simple heuristic: abstracts are typically 50-2000 words
        word_count = len(document.split())
        return 50 <= word_count <= 2000
    
    def process(self, document: Union[str, dict], **kwargs) -> str:
        """Process abstract using the configured formatter.
        
        Args:
            document: Abstract content
            **kwargs: Formatting options (output_format, etc.)
            
        Returns:
            Formatted abstract
        """
        text = document if isinstance(document, str) else document.get('abstract', '')
        output_format = kwargs.get('output_format', 'markdown')
        return self.formatter.format_abstract(text, output_format)


class FullTextProcessor(DocumentProcessor):
    """Processor for full-text scientific articles."""
    
    def can_process(self, document: Union[str, dict]) -> bool:
        """Check if document looks like a full article.
        
        Args:
            document: Document to check
            
        Returns:
            True if document appears to be a full article
        """
        if isinstance(document, dict):
            return 'sections' in document or 'full_text' in document
        
        # Heuristic: full articles are typically much longer than abstracts
        word_count = len(document.split())
        return word_count > 2000
    
    def process(self, document: Union[str, dict], **kwargs) -> str:
        """Process full-text article.
        
        Args:
            document: Article content
            **kwargs: Processing options
            
        Returns:
            Formatted article (placeholder implementation)
        """
        return ("Full-text processing not yet implemented.\n"
                "Would handle sections, figures, tables, citations, etc.\n"
                f"Document length: {len(str(document))} characters")


class ScientificDocumentFormatter:
    """Main formatter that delegates to appropriate processors based on document type."""
    
    def __init__(self, use_spacy: bool = True):
        """Initialize the document formatter.
        
        Args:
            use_spacy: Whether to use spaCy for abstract processing
        """
        self.processors = [
            AbstractProcessor(use_spacy=use_spacy),
            FullTextProcessor()
        ]
    
    def format_document(self, document: Union[str, dict], **kwargs) -> str:
        """Format a scientific document using the appropriate processor.
        
        Args:
            document: Document content
            **kwargs: Formatting options
            
        Returns:
            Formatted document content
        """
        for processor in self.processors:
            if processor.can_process(document):
                return processor.process(document, **kwargs)
        
        return "No suitable processor found for this document type."
    
    def add_processor(self, processor: DocumentProcessor):
        """Add a custom document processor.
        
        Args:
            processor: Custom processor to add
        """
        self.processors.insert(0, processor)  # Add at beginning for priority
    
    def get_processor_info(self) -> Dict[str, Any]:
        """Get information about available processors.
        
        Returns:
            Dictionary with processor information
        """
        return {
            'processors': [type(p).__name__ for p in self.processors],
            'total_processors': len(self.processors)
        }