from PyPDFForm import PdfWrapper

def fill_form():
    # Use the exact sample data
    form_data = {
        'c1_1[0]': True, # Individual/sole proprietor
        'c1_1[1]': True, #C corporation
        'c1_1[2]': True, # S corporation
        'c1_1[3]': True, # Partnership
        'c1_1[4]': True, # Trust/estate
        'c1_1[5]': True, #LLC
        'c1_1[6]': True, #Other
        'c1_2[0]': True, #foreign partners / owners / beneficiaries
        'f1_01[0]': 'f1_01[0]', # Name of entity/individual
        'f1_02[0]': 'f1_02[0]', # Business name/disregarded entity name, if different from above
        'f1_03[0]': 'f1_03[0]', # LLC tax classification(C = C corporation, S = S corporation or P = Partnership)
        'f1_04[0]': 'f1_04[0]', # Other tax classification
        'f1_05[0]': 'f1_05[0]', # Exempt payee code
        'f1_06[0]': 'f1_06[0]', #Exemption from Foreign Account Tax Compliance Act (FATCA) reporting  code
        'f1_07[0]': 'f1_07[0]', #Address (number, street, and apt. or suite no.). S
        'f1_08[0]': 'f1_08[0]', #City, state, and ZIP code
        'f1_09[0]': 'f1_09[0]', # Requester’s name and address (optional)
        'f1_10[0]': 'f1_10[0]', #List account number(s) here (optional)
        'f1_11[0]': 123,#ssn part-1 3 digits max
        'f1_12[0]': 45,#ssn part-2 2 digits max
        'f1_13[0]': 5677,#ssn part-3 4 digits max
        'f1_14[0]': 27,#ein part-1 2 digits max
        'f1_15[0]': 9888897#ein part-2 7 digits max
    }

    # Fill the form
    filled_form = PdfWrapper("w9.pdf").fill(form_data)
    
    # Save the filled form
    with open("filled_w9.pdf", "wb+") as output:
        output.write(filled_form.read())

# Run the function
fill_form()