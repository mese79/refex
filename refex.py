import time
import random
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
        text = text[ref_index + len(REF_TITLE):]  # omit the 'Reference' word
        text = clean_text(text)
        print(f'\n\n{text[:500]}')
        cit_name, pattern = find_pattern(text[:500])
        print(f'\n{cit_name}\n{pattern}\n')

        if pattern is None:
            pass
        else:
            refs = get_refs_from_text(text, pattern)
            pprint(refs)
            print()

            pg = ProxyGenerator()
            # print(pg.FreeProxies())
            scholarly.use_proxy(pg, pg)
            pubs = query_scholars(refs)
            data = {
                'title': pdf_info.title,
                'author': pdf_info.author,
                'refs': refs[:3],
                'pubs': pubs[:3]
            }
            print(data)
            save_html(data, HTML_TEMPLATE_FILE, 'output.html')


def clean_text(text: str) -> str:
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('\n', ' ').strip()
    return text


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


def get_refs_from_text(text: str, pattern: str) -> List[dict]:
    refs = []
    for match in re.finditer(pattern, text):
        d = match.groupdict()
        # add the matched text too
        d.update({
            'text': clean_text(text[match.start(): match.end()])
        })
        refs.append(d)

    return refs


def query_scholars(refs: List[dict]):
    pubs = []
    for ref in refs[:3]:
        time.sleep(5 + random.randint(0, 7))
        title = ref['title']
        print(f'querying "{title}" ...')
        query = scholarly.search_pubs(title)
        pub = next(query)  # get the first result
        # pub = scholarly.fill(pub)
        # pprint(scholarly.bibtex(pub))
        with open('scholar_result.json', 'w') as f:
            json.dump(pub, f)
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
