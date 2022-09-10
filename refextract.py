from PyPDF2 import PdfFileReader
import textract

from citations import REF_TITLE, CITATIONS


def extract_information(pdf_path):
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


def extract_refs(pdf_path):
    text = textract.process(pdf_path, encoding='utf-8').decode()
    ref_index = text.find(REF_TITLE)
    if ref_index > -1:
        refs = clean_refs(text[ref_index:])
        print(f'\n\n{refs}')
        # with open(f'{pdf_path}.txt', mode='w') as f:
        #     f.write(refs)


def clean_refs(refs):
    refs = refs[len(REF_TITLE):]
    refs = refs.replace('“', '"').replace('”', '"')
    # refs = refs.replace('\n', ' ')
    return refs



if __name__ == '__main__':
    print(extract_information('./pdf/molgan.pdf'))
    # extract_refs('./molgan.pdf')
