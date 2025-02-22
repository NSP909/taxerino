import json
from pprint import pprint
from PyPDFForm import PdfWrapper


pdf_form_schema = PdfWrapper("f8863-2023.pdf").schema
pdf_form_schema = PdfWrapper("w8ben.pdf").schema

print(json.dumps(pdf_form_schema, indent=4, sort_keys=True))
pprint(PdfWrapper("w8ben.pdf").sample_data)
