from typing import Optional, Tuple
import re

from PyPDF2 import PdfFileReader, DocumentInformation
import textract

from citations import REF_TITLE, CITATIONS


def extract_information(pdf_path: str) -> DocumentInformation:
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}:

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information


def extract_refs(pdf_path: str):
    text = textract.process(pdf_path, encoding='utf-8').decode()
    ref_index = text.find(REF_TITLE)
    if ref_index > -1:
        refs = clean_refs(text[ref_index:])
        print(f'\n\n{refs[:500]}')
        cit_name, pattern = find_pattern(refs[:500])
        print(f'\n{cit_name}\n{pattern}')


def clean_refs(refs: str) -> str:
    refs = refs[len(REF_TITLE):]  # omit the 'Reference' word
    refs = refs.replace('“', '"').replace('”', '"')
    refs = refs.replace('\n', ' ')
    return refs


def find_pattern(sample: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Try to find reference citation pattern.
    """
    for key, citation in CITATIONS.items():
        for pattern in citation['patterns']:
            match = re.match(pattern, sample)
            if match is not None:
                return key, pattern

    return None, None




if __name__ == '__main__':
    extract_information('./pdf/molgan.pdf')
    extract_refs('./pdf/molgan.pdf')
