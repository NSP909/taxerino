from PyPDFForm import PdfWrapper

def fill_form():
    # Use the exact sample data
    form_data = {#'Date[0]': 'Date[0]', 
    'c1_01[0]': True, #FTIN reqired or not 
    #'c1_02[0]': True, 
    'f_10[0]': 'f_10[0]', #Foreign Tax Identifying Number
    'f_11[0]': 'f_11[0]', #Reference Number 
    'f_12[0]': 'f_12[0]', #DOB 
    'f_13[0]': 'f_13[0]', #Country of residence
    'f_14[0]': 'f_14[0]', #The beneficial owner is claiming the provisions of Article and paragraph ____ of the treaty
    'f_15[0]': 'f_15[0]', #identified on line 9 above to claim a _____% rate of withholding on
    'f_16[0]': 'f_16[0]', #type of income 
    'f_17[0]': 'f_17[0]', #Tax treaty article used to claim rate of withholding
    'f_18[0]': 'f_18[0]', #Tax treaty paragraph used to claim rate of withholding
    'f_1[0]': 'f_1[0]', #Name
    #'f_20[0]': 'kk',
    'f_21[0]': 'f_21[0]',
    'f_2[0]': 'f_2[0]', #Country of Citizenship
    'f_3[0]': 'f_3[0]', #Permanent Residence Address (PRA)
    'f_4[0]': 'f_4[0]', #City/Town, State/Province, Postal Code of PRA
    'f_5[0]': 'f_5[0]', #Country of PRA
    'f_6[0]': 'f_6[0]', #Mailing Address
    'f_7[0]': 'f_7[0]', #City/Town, State/Province, Postal Code of Mailing Address
    'f_8[0]': 'f_8[0]', #County of Mailing Address
    'f_9[0]': 'f_9[0]' #SSN/ITIN
    }

    # Fill the form
    filled_form = PdfWrapper("w8ben.pdf").fill(form_data)
    
    # Save the filled form
    with open("filled_w8ben.pdf", "wb+") as output:
        output.write(filled_form.read())

# Run the function
fill_form()