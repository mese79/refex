
import time
import json
import re
from pprint import pprint
from typing import Optional, Tuple, List

import jinja2
import textract
from PyPDF2 import PdfFileReader, DocumentInformation
from scholarly import scholarly, ProxyGenerator

from citations import REF_TITLE, CITATIONS


HTML_TEMPLATE_FILE = 'template.html'


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

    print(f'\n{txt}\n')
    return information


def extract_refs(pdf_path: str):
    # get given pdf info
    pdf_info = extract_information(pdf_path)
    # extract the references
    text = textract.process(pdf_path, encoding='utf-8').decode()
    ref_index = text.find(REF_TITLE)
    if ref_index > -1:
        text = clean_refs(text[ref_index:])
        print(f'\n\n{text[:500]}')
        cit_name, pattern = find_pattern(text[:500])
        print(f'\n{cit_name}\n{pattern}')

        if pattern is None:
            pass
        else:
            titles = get_ref_titles(text, pattern)
            pprint(titles)
            print()

            # pg = ProxyGenerator()
            # print(pg.FreeProxies())
            # scholarly.use_proxy(pg)
            pubs = query_scholars(titles)
            data = {
                'title': pdf_info.title,
                'author': pdf_info.author,
                'refs': pubs
            }
            print(data)
            save_html(data, HTML_TEMPLATE_FILE, 'output.html')


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


def get_ref_titles(text: str, pattern: str) -> List:
    titles = []
    for match in re.finditer(pattern, text):
        titles.append(match.group('title'))

    return titles


def query_scholars(titles: List[str]):
    pubs = []
    for title in titles[:3]:
        time.sleep(10)
        print(f'querying "{title}" ...')
        query = scholarly.search_pubs(title)
        pub = next(query)  # get the first result
        # pub = scholarly.fill(pub)
        # pprint(scholarly.bibtex(pub))
        #     with open('scholar_result.json', 'w') as f:
        #         json.dump(pub, f)
        pubs.append(pub)

    return pubs


def save_html(data: dict, template_file: str, out_file: str):
    # get the html template
    with open(template_file, mode='r', encoding='utf-8') as f:
        source_html = f.read()

    template = jinja2.Template(source_html)
    rendered_html = template.render(data=data)
    with open(out_file, mode='w', encoding='utf-8') as out:
        out.write(rendered_html)
    return True



if __name__ == '__main__':
    # extract_information('./pdf/molgan.pdf')
    extract_refs('./pdf/molgan.pdf')
