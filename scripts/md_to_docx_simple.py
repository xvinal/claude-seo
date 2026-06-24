#!/usr/bin/env python3
"""Simple Markdown -> DOCX fallback: writes raw Markdown paragraphs into a .docx file.

Usage: python md_to_docx_simple.py input.md output.docx
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print('Usage: md_to_docx_simple.py input.md output.docx')
        sys.exit(2)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    if not inp.exists():
        print('Input not found:', inp)
        sys.exit(2)
    text = inp.read_text(encoding='utf-8')
    try:
        from docx import Document
    except Exception as e:
        print('python-docx not available:', e)
        sys.exit(3)
    doc = Document()
    # Split on two or more newlines to preserve blocks
    blocks = [b.strip() for b in text.split('\n\n') if b.strip()]
    for b in blocks:
        doc.add_paragraph(b)
    doc.save(out)
    print('Wrote', out)

if __name__ == '__main__':
    main()
