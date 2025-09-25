"""
Example usage of the abstract-format library.
"""

from abstract_format import (
    AbstractFormatter, 
    SpacyAbstractFormatter, 
    ScientificDocumentFormatter,
    AbstractAnalyzer
)


def main():
    """Demonstrate various usage patterns."""
    
    # Sample abstracts for testing
    structured_abstract = """
    BACKGROUND: FLASH radiotherapy is an emerging treatment modality using ultra-high dose rate beams. Much effort has been made to develop suitable dosimeters for reference dosimetry, yet the spatial beam characteristics must also be characterized to enable computerized treatment planning, as well as quality control and service of a treatment delivery device. PURPOSE: The study presents the development and characterization of a two-dimensional detector array for measuring pulse-resolved spatial fluence distributions in real-time. METHODS: The performance of the SunPoint 1 diode was evaluated by measuring the response of the EDGE Detector in a 20 MeV UHPDR electron beam. RESULTS: The FLASH Profiler exhibited a linear response within ± 3% deviation over the investigated dose per pulse range. CONCLUSION: The FLASH Profiler could be used for characterizing UHPDR electron beams and facilitating quality control.
    """
    
    unstructured_abstract = """
    Magnetic resonance imaging (MRI) has become an essential diagnostic tool in clinical practice, offering superior soft tissue contrast compared to computed tomography (CT) and avoiding ionizing radiation exposure. However, traditional MRI acquisition techniques suffer from long scan times, limiting patient throughput and increasing the likelihood of motion artifacts. Recent advances in compressed sensing and machine learning have enabled significant acceleration of MRI data acquisition while maintaining image quality. We developed a novel deep learning-based reconstruction algorithm that combines convolutional neural networks (CNNs) with iterative reconstruction techniques to achieve up to 8-fold acceleration in MRI scanning. Additionally, our approach utilizes a U-Net architecture with attention mechanisms to learn sparse representations of MRI data. The proposed method achieved a PSNR of 42.3 ± 2.1 dB, SSIM of 0.94 ± 0.03, and NMSE of 0.015 ± 0.008 for 8-fold acceleration. Consequently, clinical deployment of our algorithm has reduced average scan times from 45 minutes to 6 minutes for standard brain MRI protocols.
    """
    
    print("=" * 80)
    print("ABSTRACT FORMAT - EXAMPLE USAGE")
    print("=" * 80)
    
    # Example 1: Basic formatter
    print("\n1. BASIC FORMATTER")
    print("-" * 40)
    basic_formatter = AbstractFormatter(line_width=70)
    result = basic_formatter.format_abstract(structured_abstract)
    print(result)
    
    # Example 2: spaCy formatter
    print("\n\n2. SPACY FORMATTER (STRUCTURED)")
    print("-" * 40)
    spacy_formatter = SpacyAbstractFormatter()
    result = spacy_formatter.format_abstract(structured_abstract)
    print(result)
    
    # Example 3: spaCy formatter on unstructured text
    print("\n\n3. SPACY FORMATTER (UNSTRUCTURED - DISCOURSE MARKERS)")
    print("-" * 40)
    result = spacy_formatter.format_abstract(unstructured_abstract)
    print(result)
    
    # Example 4: Document formatter (auto-detection)
    print("\n\n4. DOCUMENT FORMATTER (AUTO-DETECTION)")
    print("-" * 40)
    doc_formatter = ScientificDocumentFormatter()
    result = doc_formatter.format_document(unstructured_abstract)
    print(result)
    
    # Example 5: Analysis mode
    print("\n\n5. ANALYSIS MODE")
    print("-" * 40)
    analyzer = AbstractAnalyzer()
    analysis = analyzer.analyze_structure(unstructured_abstract)
    
    print(f"Length: {analysis['total_length']} characters")
    print(f"Words: {analysis['word_count']}")
    print(f"Sentences: {analysis['sentence_count']}")
    print(f"Average sentence length: {analysis['word_count']/analysis['sentence_count']:.1f} words")
    print(f"Structured sections: {analysis['has_structured_sections']}")
    print(f"Technical terms: {len(analysis['technical_terms'])}")
    if analysis['technical_terms']:
        print(f"  Examples: {', '.join(analysis['technical_terms'][:5])}...")
    
    # Example 6: Different output formats
    print("\n\n6. DIFFERENT OUTPUT FORMATS")
    print("-" * 40)
    sample_text = "We tested MRI (Magnetic Resonance Imaging) and found 95% accuracy."
    
    print("Markdown:")
    result_md = spacy_formatter.format_abstract(sample_text, output_format='markdown')
    print(result_md)
    
    print("\nHTML:")
    result_html = spacy_formatter.format_abstract(sample_text, output_format='html') 
    print(result_html)
    
    print("\nPlain text:")
    result_plain = spacy_formatter.format_abstract(sample_text, output_format='plain')
    print(result_plain)


if __name__ == "__main__":
    main()