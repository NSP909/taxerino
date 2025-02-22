from PyPDFForm import PdfWrapper

def fill_w8ben_form(
    # Personal Information
    name: str,                      # f_1[0] - Name of individual
    country_citizenship: str,       # f_2[0] - Country of citizenship
    
    # Permanent Residence Address
    perm_address: str,              # f_3[0] - Permanent residence address
    perm_city_state_zip: str,       # f_4[0] - City/town, state/province, postal code
    perm_country: str,              # f_5[0] - Country
    
    # Mailing Address (if different)
    mailing_address: str = "",      # f_6[0] - Mailing address
    mailing_city_state_zip: str = "",# f_7[0] - City/town, state/province, postal code
    mailing_country: str = "",      # f_8[0] - Country
    
    # Tax Identification Information
    ssn_itin: str = "",            # f_9[0] - U.S. SSN or ITIN
    foreign_tax_id: str = "",      # f_10[0] - Foreign tax identifying number
    ftin_not_required: bool = False,# c1_01[0] - Check if FTIN not required
    reference_number: str = "",     # f_11[0] - Reference number(s)
    
    # Additional Information
    date_of_birth: str = "",        # f_12[0] - Date of birth (MM-DD-YYYY)
    country_residence: str = "",     # f_13[0] - Country of residence
    
    # Treaty Information
    treaty_article: str = "",       # f_14[0] - Article number
    withholding_rate: str = "",     # f_15[0] - Withholding rate percentage
    income_type: str = "",          # f_16[0] - Type of income
    treaty_article_cite: str = "",  # f_17[0] - Tax treaty article citation
    treaty_paragraph: str = "",     # f_18[0] - Tax treaty paragraph citation
    
    # Additional Fields
    field_21: str = ""             # f_21[0] - Additional field
):
    """
    Fill out IRS Form W-8BEN (Certificate of Foreign Status of Beneficial Owner for United States Tax Withholding and Reporting - Individuals).
    """
    
    # Initialize form data
    form_data = {
        'f_1[0]': name,
        'f_2[0]': country_citizenship,
        'f_3[0]': perm_address,
        'f_4[0]': perm_city_state_zip,
        'f_5[0]': perm_country,
        'f_6[0]': mailing_address,
        'f_7[0]': mailing_city_state_zip,
        'f_8[0]': mailing_country,
        'f_9[0]': ssn_itin,
        'f_10[0]': foreign_tax_id,
        'c1_01[0]': ftin_not_required,
        'f_11[0]': reference_number,
        'f_12[0]': date_of_birth,
        'f_13[0]': country_residence,
        'f_14[0]': treaty_article,
        'f_15[0]': withholding_rate,
        'f_16[0]': income_type,
        'f_17[0]': treaty_article_cite,
        'f_18[0]': treaty_paragraph,
        'f_21[0]': field_21
    }

    # Fill and save the form
    filled_form = PdfWrapper("w8ben.pdf").fill(form_data)
    with open("filled_w8ben.pdf", "wb+") as output:
        output.write(filled_form.read())

# Example usage
fill_w8ben_form(
    name="John Smith",
    country_citizenship="United Kingdom",
    perm_address="123 Oxford Street",
    perm_city_state_zip="London, W1D 1DF",
    perm_country="United Kingdom",
    mailing_country="United Kingdom",
    mailing_address="abc street",
    mailing_city_state_zip="Reading, RG5HF",
    ssn_itin="123-45-6789",
    foreign_tax_id="GB123456789",
    date_of_birth="1980-01-01",
    country_residence="United Kingdom",
    treaty_article="Article 15",
    withholding_rate="15",
    income_type="Royalties",
    treaty_article_cite="Income from Employment",
    treaty_paragraph="Paragraph 2"
)