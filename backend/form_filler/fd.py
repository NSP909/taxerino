import json
from pprint import pprint
from PyPDFForm import PdfWrapper

pdf_form_schema = PdfWrapper("w9.pdf").schema

print(json.dumps(pdf_form_schema, indent=4, sort_keys=True))
pprint(PdfWrapper("w9.pdf").sample_data)