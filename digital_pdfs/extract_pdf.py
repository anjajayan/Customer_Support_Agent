'''
Extract a digital PDF with Docling and print the results for manual verification.

'''
import sys

from docling.document_converter import DocumentConverter


def extract_pdf(pdf_path):
    """Convert a PDF with Docling, print what was extracted, and return the Docling document."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    doc = result.document

    # 1. Overview
    print("=" * 80)
    print(f"FILE: {pdf_path}")
    print(f"Pages: {len(doc.pages)} | Text items: {len(doc.texts)} | "
          f"Tables: {len(doc.tables)} | Pictures: {len(doc.pictures)}")

    # Extracting each table as a DataFrame
    for i, table in enumerate(doc.tables, start=1):
        print("=" * 80)
        page = table.prov[0].page_no if table.prov else "?"
        print(f"TABLE {i} (page {page})")
        print("-" * 80)
        print(table.export_to_dataframe(doc).to_string())

    # 4. Structure: label + page for each text element
    print("=" * 80)
    print("DOCUMENT STRUCTURE (label | page | text preview)")
    print("-" * 80)
    for item in doc.texts:
        page = item.prov[0].page_no if item.prov else "?"
        print(f"{item.label:<16} | p{page} | {item.text[:80]!r}")

    return doc



    
