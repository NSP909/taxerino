from PyPDFForm import PdfWrapper

def fill_w4_form(
    # Personal Information
    first_middle_name: str,         # f1_01[0] - First name and middle initial
    last_name: str,                 # f1_02[0] - Last name
    address: str,                   # f1_03[0] - Address
    city_state_zip: str,            # f1_04[0] - City/town, state, zip code
    ssn: str,                       # f1_05[0] - Social Security Number

    # Checkboxes
    single_or_married_filing_separately: bool = False,  # c1_1[0] - Single or married filing separately
    married_filing_jointly: bool = False,               # c1_1[1] - Married filing jointly
    head_of_household: bool = False,                     # c1_1[2] - Head of household
    two_jobs_only: bool = False,               # c1_2[0] - If there are only two jobs total, you may check this box. Do the same on Form W-4 for the other job. This option is generally more accurate than (b) if pay at the lower paying job is more than half of the pay at the higher paying job. Otherwise, (b) is more accurate 
    
    # Tax Credits
    child_tax_credits: float = 0,   # f1_06[0] - Total child tax credits ($2000 per child under 17)
    dependent_credits: float = 0,   # f1_07[0] - Other dependent credits ($500 per dependent)
    total_credits: float = 0,       # f1_09[0] - Sum of child and dependent credits
    
    # Additional Income and Deductions
    other_income: float = 0,        # f1_10[0] - Other income, not from jobs
    deductions: float = 0,          # f1_11[0] - Deductions
    extra_withholding: float = 0,   # f1_12[0] - Extra withholding per pay period
    
    # Employer Information
    employer_info: str = "",        # f1_13[0] - Employer's name and address
    employment_date: str = "",      # f1_14[0] - First date of employment
    employer_ein: str = "",         # f1_15[0] - Employer Identification Number
    
    # Multiple Jobs Worksheet
    two_jobs_value: float = 0,      # f3_01[0] - Intersection value for 2 jobs
    three_jobs_highest: float = 0,  # f3_02[0] - Intersection value for 2 highest paying jobs (3 jobs)
    three_jobs_third: float = 0,    # f3_03[0] - Intersection value with third job
    total_jobs_value: float = 0,    # f3_04[0] - Sum of intersection values
    pay_periods: int = 0,           # f3_05[0] - Number of pay periods
    per_period_value: float = 0,    # f3_06[0] - Per-period withholding calculation
    
    # Deductions Worksheet
    itemized_deductions: float = 0, # f3_07[0] - Estimated itemized deductions for 2025
    standard_deduction: float = 0,  # f3_08[0] - Standard deduction based on filing status
    deduction_difference: float = 0, # f3_09[0] - Deduction comparison result
    other_adjustments: float = 0,   # f3_10[0] - Student loan interest, IRA contributions, etc.
    total_adjustments: float = 0    # f3_11[0] - Total adjustments for Step 4(b)
):
    """
    Fill out IRS Form W-4 with provided information.
    """
    # Initialize form data with default values
    form_data = {
        'c1_1[0]': single_or_married_filing_separately,
        'c1_1[1]': married_filing_jointly,
        'c1_1[2]': head_of_household,
        'c1_2[0]': two_jobs_only,
        'f1_01[0]': first_middle_name,
        'f1_02[0]': last_name,
        'f1_03[0]': address,
        'f1_04[0]': city_state_zip,
        'f1_05[0]': ssn,
        'f1_06[0]': str(child_tax_credits),
        'f1_07[0]': str(dependent_credits),
        'f1_09[0]': str(total_credits),
        'f1_10[0]': str(other_income),
        'f1_11[0]': str(deductions),
        'f1_12[0]': str(extra_withholding),
        'f1_13[0]': employer_info,
        'f1_14[0]': employment_date,
        'f1_15[0]': employer_ein,
        'f3_01[0]': str(two_jobs_value),
        'f3_02[0]': str(three_jobs_highest),
        'f3_03[0]': str(three_jobs_third),
        'f3_04[0]': str(total_jobs_value),
        'f3_05[0]': str(pay_periods),
        'f3_06[0]': str(per_period_value),
        'f3_07[0]': str(itemized_deductions),
        'f3_08[0]': str(standard_deduction),
        'f3_09[0]': str(deduction_difference),
        'f3_10[0]': str(other_adjustments),
        'f3_11[0]': str(total_adjustments)
    }

    # Fill and save the form
    filled_form = PdfWrapper("/Users/priyadarshannarayanasamy/Desktop/hacklytics/taxerino/backend/form_filler/templates/w4.pdf").fill(form_data)
    with open("filled/filled_w4.pdf", "wb+") as output:
        output.write(filled_form.read())

# Example usage
if __name__ == "__main__":
    fill_w4_form(
        first_middle_name="John A",
        last_name="Doe",
        address="123 Main St",
        city_state_zip="San Francisco, CA 94105",
        ssn="123-45-6789",
        child_tax_credits=4000,  # 2 children under 17
        dependent_credits=500,   # 1 other dependent
        total_credits=4500,
        employer_info="ACME Corp\n123 Business Ave\nSan Francisco, CA 94105",
        employment_date="2025-01-15",
        employer_ein="12-3456789",
        pay_periods=26,         # Biweekly pay
        itemized_deductions=28000,
        standard_deduction=30000  # Married filing jointly
    )