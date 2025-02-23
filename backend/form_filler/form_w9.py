from PyPDFForm import PdfWrapper

def fill_w9_form(
    # Part I - Taxpayer Identification
    name: str,                      # f1_01[0] - Name of entity/individual (required)
    business_name: str = "",        # f1_02[0] - Business name/disregarded entity name
    
    # Tax Classification - Select only ONE
    tax_classification: str ="",        # One of: "individual", "ccorp", "scorp", "partnership", "trust", "llc", "other"
    llc_classification: str = "",   # f1_03[0] - LLC tax classification (C, S, or P) - only if LLC selected
    other_classification: str = "", # f1_04[0] - Other tax classification description
    
    # Foreign Status
    has_foreign_partners: bool = False,  # c1_2[0] - Foreign partners/owners/beneficiaries
    
    # Exemption Codes
    exempt_payee_code: str = "",    # f1_05[0] - Exempt payee code
    fatca_code: str = "",           # f1_06[0] - FATCA exemption code
    
    # Address Information
    address: str = "",              # f1_07[0] - Street address
    city_state_zip: str = "",       # f1_08[0] - City, state, and ZIP code
    requester_info: str = "",       # f1_09[0] - Requester's name and address
    account_numbers: str = "",      # f1_10[0] - Account number(s)
    
    # Tax ID Numbers (Fill either SSN OR EIN)
    ssn_first: str = "",           # f1_11[0] - First 3 digits of SSN
    ssn_second: str = "",          # f1_12[0] - Middle 2 digits of SSN
    ssn_third: str = "",           # f1_13[0] - Last 4 digits of SSN
    ein_first: str = "",           # f1_14[0] - First 2 digits of EIN
    ein_second: str = ""           # f1_15[0] - Last 7 digits of EIN
):
    """
    Fill out IRS Form W-9 with provided information.
    """
    # Map tax classification to checkboxes
    tax_classes = {
        "individual": "c1_1[0]",
        "ccorp": "c1_1[1]",
        "scorp": "c1_1[2]",
        "partnership": "c1_1[3]",
        "trust": "c1_1[4]",
        "llc": "c1_1[5]",
        "other": "c1_1[6]"
    }
    
    # Initialize all tax classification checkboxes as False
    form_data = {key: False for key in tax_classes.values()}
    
    # Set the selected classification to True
    if tax_classification in tax_classes:
        form_data[tax_classes[tax_classification]] = True
    
    # Add all other form fields
    form_data.update({
        'f1_01[0]': name,
        'f1_02[0]': business_name,
        'f1_03[0]': llc_classification,
        'f1_04[0]': other_classification,
        'c1_2[0]': has_foreign_partners,
        'f1_05[0]': exempt_payee_code,
        'f1_06[0]': fatca_code,
        'f1_07[0]': address,
        'f1_08[0]': city_state_zip,
        'f1_09[0]': requester_info,
        'f1_10[0]': account_numbers,
        'f1_11[0]': ssn_first,
        'f1_12[0]': ssn_second,
        'f1_13[0]': ssn_third,
        'f1_14[0]': ein_first,
        'f1_15[0]': ein_second
    })

    # Fill and save the form
    filled_form = PdfWrapper("/Users/priyadarshannarayanasamy/Desktop/hacklytics/taxerino/backend/form_filler/templates/w9.pdf").fill(form_data)
    with open("filled/filled_w9.pdf", "wb+") as output:
        output.write(filled_form.read())

# Example usage
if __name__=="__main__":

    fill_w9_form(
        name="John Doe",
        business_name="Doe Enterprises LLC",
        tax_classification="llc",
        llc_classification="C",
        address="123 Business St",
        city_state_zip="San Francisco, CA 94105",
        exempt_payee_code="123",
        fatca_code="456",
        requester_info="IRS",
        account_numbers="12345",
        ssn_first="123",
        ssn_second="45",
        ssn_third="6789",
        ein_first="12",
        ein_second="3456789"
    )