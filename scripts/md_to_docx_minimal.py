#!/usr/bin/env python3
"""Minimal DOCX writer without external dependencies.
Converts markdown by splitting on blank lines into paragraphs.
Usage: python md_to_docx_minimal.py input.md output.docx
"""
import sys
from pathlib import Path
import zipfile
import xml.sax.saxutils as sax

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''

RELS_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_XML_TEMPLATE_HEAD = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>'''
DOC_XML_TEMPLATE_TAIL = '''    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''


def paragraph_xml(text: str) -> str:
    # escape xml special chars and preserve leading/trailing spaces
    esc = sax.escape(text)
    # Replace multiple spaces with xml:space preservation
    return f"    <w:p><w:r><w:t xml:space=\"preserve\">{esc}</w:t></w:r></w:p>\n"


def convert(inp: Path, out: Path) -> int:
    txt = inp.read_text(encoding='utf-8')
    # Split into blocks by two or more newlines
    blocks = [b.strip() for b in txt.split('\n\n') if b.strip()]
    doc_xml = [DOC_XML_TEMPLATE_HEAD + "\n"]
    for b in blocks:
        # For long blocks, split lines and join with line breaks
        lines = b.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == '':
                doc_xml.append(paragraph_xml(''))
            else:
                doc_xml.append(paragraph_xml(line))
    doc_xml.append(DOC_XML_TEMPLATE_TAIL)
    # Write files into zip
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS_RELS)
        z.writestr('word/document.xml', ''.join(doc_xml))
    return 0


def main():
    if len(sys.argv) < 3:
        print('Usage: md_to_docx_minimal.py input.md output.docx')
        sys.exit(2)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    if not inp.exists():
        print('Input not found:', inp)
        sys.exit(2)
    rc = convert(inp, out)
    if rc == 0:
        print('Wrote', out)
    sys.exit(rc)

if __name__ == '__main__':
    main()
