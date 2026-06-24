#!/usr/bin/env python3
"""Convert Markdown to DOCX with fallbacks.

Usage:
  python convert_md_to_docx.py input.md output.docx

The script tries, in order:
 - html2docx (best fidelity)
 - pypandoc (if pandoc is installed)
 - fallback: plain-text paragraph export using python-docx

Install recommended packages:
  pip install markdown html2docx python-docx pypandoc

"""
import sys
from pathlib import Path


def md_to_html(md_text: str) -> str:
    try:
        import markdown
        return markdown.markdown(md_text, extensions=["extra", "smarty", "tables", "toc"])
    except Exception:
        return "<pre>" + md_text + "</pre>"


def html_to_docx_via_html2docx(html: str, out_path: str) -> bool:
    try:
        from html2docx import html2docx
        doc = html2docx(html)
        doc.save(out_path)
        return True
    except Exception:
        return False


def html_to_docx_via_pypandoc(html: str, out_path: str) -> bool:
    try:
        import pypandoc
        pypandoc.convert_text(html, 'docx', format='html', outputfile=out_path)
        return True
    except Exception:
        return False


def html_to_docx_fallback(html: str, out_path: str) -> bool:
    try:
        from docx import Document
        import re
        # Strip simple HTML tags and convert to paragraphs
        text = re.sub(r'<[^>]+>', '', html)
        # Normalize Windows newlines
        text = text.replace('\r\n', '\n')
        doc = Document()
        for para in [p.strip() for p in text.split('\n\n') if p.strip()]:
            doc.add_paragraph(para)
        doc.save(out_path)
        return True
    except Exception:
        return False


def convert(input_md: Path, output_docx: Path) -> int:
    md_text = input_md.read_text(encoding='utf-8')
    html = md_to_html(md_text)

    # Try html2docx
    if html_to_docx_via_html2docx(html, str(output_docx)):
        print('Converted with html2docx')
        return 0

    # Try pypandoc
    if html_to_docx_via_pypandoc(html, str(output_docx)):
        print('Converted with pypandoc')
        return 0

    # Fallback
    if html_to_docx_fallback(html, str(output_docx)):
        print('Converted with fallback plain-text method')
        return 0

    print('Conversion failed: required packages missing')
    return 2


def main():
    if len(sys.argv) < 3:
        print('Usage: convert_md_to_docx.py input.md output.docx')
        sys.exit(2)
    input_md = Path(sys.argv[1])
    output_docx = Path(sys.argv[2])
    if not input_md.exists():
        print('Input file not found:', input_md)
        sys.exit(2)
    rc = convert(input_md, output_docx)
    sys.exit(rc)


if __name__ == '__main__':
    main()
