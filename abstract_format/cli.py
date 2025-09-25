"""
Command-line interface for the abstract formatter.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from . import ScientificDocumentFormatter, SpacyAbstractFormatter, AbstractFormatter


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Format scientific abstracts for better readability",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Format from stdin
  echo "Your abstract here..." | abstract-format
  
  # Format from file
  abstract-format input.txt
  
  # Format to HTML
  abstract-format --format html input.txt
  
  # Use basic formatter (no spaCy)
  abstract-format --no-spacy input.txt
  
  # Save to file
  abstract-format input.txt -o formatted.md
        """
    )
    
    parser.add_argument(
        'input', 
        nargs='?', 
        help='Input file containing abstract text (default: stdin)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )
    
    parser.add_argument(
        '--format',
        choices=['markdown', 'html', 'plain'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--no-spacy',
        action='store_true',
        help='Use basic formatter instead of spaCy-enhanced version'
    )
    
    parser.add_argument(
        '--line-width',
        type=int,
        default=80,
        help='Maximum line width for text wrapping (default: 80)'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Show analysis information instead of formatting'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    try:
        # Read input
        if args.input:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"Error: File '{args.input}' not found", file=sys.stderr)
                sys.exit(1)
            text = input_path.read_text(encoding='utf-8')
        else:
            text = sys.stdin.read()
        
        if not text.strip():
            print("Error: No input text provided", file=sys.stderr)
            sys.exit(1)
        
        # Choose formatter
        if args.analyze:
            from .analyzers import AbstractAnalyzer
            analyzer = AbstractAnalyzer()
            analysis = analyzer.analyze_structure(text)
            
            output = format_analysis(analysis)
        else:
            if args.no_spacy:
                formatter = AbstractFormatter(line_width=args.line_width)
            else:
                formatter = ScientificDocumentFormatter(use_spacy=True)
            
            if hasattr(formatter, 'format_document'):
                output = formatter.format_document(text, output_format=args.format)
            else:
                output = formatter.format_abstract(text, output_format=args.format)
        
        # Write output
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output, encoding='utf-8')
            print(f"Formatted abstract saved to: {args.output}", file=sys.stderr)
        else:
            print(output)
    
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def format_analysis(analysis: dict) -> str:
    """Format analysis results for display."""
    lines = [
        "ABSTRACT ANALYSIS",
        "=" * 50,
        f"Length: {analysis['total_length']} characters",
        f"Words: {analysis['word_count']}",
        f"Sentences: {analysis['sentence_count']}",
        f"Average sentence length: {analysis['word_count']/analysis['sentence_count']:.1f} words",
        f"Structured sections: {'Yes' if analysis['has_structured_sections'] else 'No'}",
    ]
    
    if analysis['section_headers']:
        lines.append("\nSection headers found:")
        for section_type, pos, header in analysis['section_headers']:
            lines.append(f"  - {section_type.value}: '{header.strip()}' at position {pos}")
    
    if analysis['technical_terms']:
        lines.append(f"\nTechnical terms: {len(analysis['technical_terms'])}")
        terms_preview = ', '.join(analysis['technical_terms'][:10])
        if len(analysis['technical_terms']) > 10:
            terms_preview += "..."
        lines.append(f"  {terms_preview}")
    
    if analysis['measurements']:
        lines.append(f"\nMeasurements: {len(analysis['measurements'])}")
        measurements_preview = ', '.join(analysis['measurements'][:10])
        if len(analysis['measurements']) > 10:
            measurements_preview += "..."
        lines.append(f"  {measurements_preview}")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    main()