from PyPDFForm import PdfWrapper

def fill_8863_form(
    # Part I - Basic Taxpayer Information
    taxpayer_name: str,                # NameShown[0] and f1_1[0] - Full legal name as shown on your tax return
    taxpayer_ssn: str,                 # f1_2[0], f1_3[0], f1_4[0] - Your Social Security Number in format XXX-XX-XXXX
    
    # Part I - Credit Calculation and Income Limits
    tentative_credit: str = "",        # f1_5[0] - Total education credits from Part III for all students. Sum all amounts from Part III, line 31
    income_limit: str = "",            # f1_6[0] - Enter $180,000 if married filing jointly, or $90,000 if single/head of household/qualifying surviving spouse
    modified_agi: str = "",            # f1_7[0] - Your modified adjusted gross income from Form 1040/1040-SR line 11 (see instructions for Form 2555/4563)
    income_difference: str = "",        # f1_8[0] - Subtract line 3 (modified AGI) from line 2 (income limit). If zero or less, stop; no credit allowed
    phase_out_amount: str = "",        # f1_9[0] - Phase-out threshold: Enter $20,000 if married filing jointly, $10,000 if single/head of household
    decimal_amount_1000: str = "",     # f1_10[0] - If line 4 is equal to or greater than line 5, enter 1.000
    decimal_amount_other: str = "",    # f1_11[0] - If line 4 is less than line 5, divide line 4 by line 5 and enter as decimal (e.g., 0.750)
    multiply_result: str = "",         # f1_12[0] - Multiply line 1 (tentative credit) by decimal from line 6 (either 1.000 or calculated)
    refundable_credit: str = "",       # f1_13[0] - Refundable portion: Multiply line 7 by 40% (0.40). Enter on Form 1040/1040-SR, line 29
    credit_limit: str = "",            # f1_14[0] - Subtract line 8 (refundable credit) from line 7. Enter on Credit Limit Worksheet, line 2
    
    # Part II - Nonrefundable Education Credits Calculation
    total_expenses: str = "",          # f1_15[0] - After completing Part III for each student, enter total from all Parts III, line 31
    smaller_amount: str = "",          # f1_16[0] - Enter the smaller of line 10 or $10,000
    multiply_20_percent: str = "",     # f1_17[0] - Multiply line 11 by 20% (0.20)
    married_limit: str = "",           # f1_18[0] - Income limit: $180,000 if married filing jointly, $90,000 if single/head of household
    form_1040_amount: str = "",        # f1_19[0] - Amount from Form 1040/1040-SR, line 11 (see instructions for special cases)
    subtract_result: str = "",         # f1_20[0] - Subtract line 14 from line 13. If zero or less, skip lines 16-17, enter -0- on line 18
    filing_status_amount: str = "",    # f1_21[0] - Enter $20,000 if married filing jointly, $10,000 if single/head of household
    decimal_amount_2_1000: str = "",   # f1_22[0] - If line 15 is equal to or greater than line 16, enter 1.000
    decimal_amount_2_other: str = "",  # f1_23[0] - If line 15 is less than line 16, divide line 15 by line 16, enter as decimal
    multiply_final: str = "",          # f1_24[0] - Multiply line 12 by decimal from line 17 (either 1.000 or calculated)
    nonrefundable_credits: str = "",   # f1_25[0] - Your nonrefundable education credits. Enter this amount on Schedule 3, line 3
    
    # Part III - Student and Educational Institution Information
    student_name: str = "",            # StudentName[0] - Full legal name of student (can be you, your spouse, or your dependent)
    student_ssn: str = "",             # f2_1[0], f2_2[0], f2_3[0] - Student's Social Security Number in format XXX-XX-XXXX
    student_ssn_2: str = "",           # f2_4[0], f2_5[0], f2_6[0] - Repeat student's SSN (verification field)
    
    # First Educational Institution Details
    institution_1_name: str = "",      # f2_7[0] - Full name of first eligible educational institution
    institution_1_address: str = "",    # f2_8[0] - Complete address including street, city, state, and ZIP code
    institution_1_ein: str = "",       # f2_9[0] through f2_17[0] - Institution's 9-digit Employer Identification Number from 1098-T
    
    # Second Educational Institution Details (if attended multiple schools)
    institution_2_name: str = "",      # f2_18[0] - Full name of second eligible educational institution
    institution_2_address: str = "",    # f2_19[0] - Complete address including street, city, state, and ZIP code
    institution_2_ein: str = "",       # f2_20[0] through f2_28[0] - Institution's 9-digit Employer Identification Number from 1098-T
    
    # Part III continued - American Opportunity Credit Amounts
    qualified_expenses: str = "",      # f2_29[0] - Adjusted qualified education expenses (maximum $4,000)
    expenses_minus_2000: str = "",     # f2_30[0] - Subtract $2,000 from qualified expenses. If zero or less, enter -0-
    multiply_25_percent: str = "",     # f2_31[0] - Multiply amount on line 28 by 25% (0.25)
    final_amount: str = "",            # f2_32[0] - If line 28 is zero, enter amount from line 27; otherwise add $2,000 to line 29
    lifetime_learning_credit: str = "", # f2_33[0] - Enter total Lifetime Learning Credit amount. Include on Part II, line 1
    
    # Student Age and Credit Eligibility
    under_24: bool = False,            # c1_1[0] - Check if student was under 24 at end of year (affects refundable credit eligibility)
    
    # First Institution Form 1098-T Information
    received_1098t_inst1: bool = False,     # c2_1[0]/[1] - Did student receive Form 1098-T from first institution for 2024?
    box_7_checked_inst1: bool = False,      # c2_2[0]/[1] - Was box 7 checked on first institution's Form 1098-T for 2023?
    
    # Second Institution Form 1098-T Information
    received_1098t_inst2: bool = False,     # c2_3[0]/[1] - Did student receive Form 1098-T from second institution for 2024?
    box_7_checked_inst2: bool = False,      # c2_4[0]/[1] - Was box 7 checked on second institution's Form 1098-T for 2023?
    
    # Additional Credit Eligibility Conditions
    aoc_claimed_prior: bool = False,        # c2_5[0]/[1] - Has AOC been claimed for this student for any 4 prior tax years?
    half_time_enrollment: bool = False,     # c2_6[0]/[1] - Was student enrolled at least half-time for at least one academic period?
    completed_first_4_years: bool = False,  # c2_7[0]/[1] - Did student complete first 4 years of postsecondary education before 2024?
    felony_drug_conviction: bool = False,   # c2_8[0]/[1] - Was student convicted of a felony drug offense before end of 2024?
):
    """
    Fill out IRS Form 8863 (Education Credits) with all possible fields.
    String values should be provided as is, no formatting will be applied.
    Boolean values will be converted to appropriate checkbox selections.
    """
    # Split SSNs into components
    tax_ssn_parts = taxpayer_ssn.split("-")
    stu_ssn_parts = student_ssn.split("-")
    stu_ssn_2_parts = student_ssn_2.split("-") if student_ssn_2 else stu_ssn_parts
    
    # Split EINs into individual digits
    ein1_digits = list(institution_1_ein.replace("-", "")) if institution_1_ein else [""] * 9
    ein2_digits = list(institution_2_ein.replace("-", "")) if institution_2_ein else [""] * 9

    form_data = {
        # Part I
        'NameShown[0]': taxpayer_name,
        'f1_1[0]': taxpayer_name,
        'f1_2[0]': tax_ssn_parts[0],
        'f1_3[0]': tax_ssn_parts[1],
        'f1_4[0]': tax_ssn_parts[2],
        'f1_5[0]': tentative_credit,
        'f1_6[0]': income_limit,
        'f1_7[0]': modified_agi,
        'f1_8[0]': income_difference,
        'f1_9[0]': phase_out_amount,
        'f1_10[0]': decimal_amount_1000,
        'f1_11[0]': decimal_amount_other,
        'f1_12[0]': multiply_result,
        'f1_13[0]': refundable_credit,
        'f1_14[0]': credit_limit,
        'f1_15[0]': total_expenses,
        'f1_16[0]': smaller_amount,
        'f1_17[0]': multiply_20_percent,
        'f1_18[0]': married_limit,
        'f1_19[0]': form_1040_amount,
        'f1_20[0]': subtract_result,
        'f1_21[0]': filing_status_amount,
        'f1_22[0]': decimal_amount_2_1000,
        'f1_23[0]': decimal_amount_2_other,
        'f1_24[0]': multiply_final,
        'f1_25[0]': nonrefundable_credits,
        
        # Part III - Student
        'StudentName[0]': student_name,
        'f2_1[0]': stu_ssn_parts[0],
        'f2_2[0]': stu_ssn_parts[1],
        'f2_3[0]': stu_ssn_parts[2],
        'f2_4[0]': stu_ssn_2_parts[0],
        'f2_5[0]': stu_ssn_2_parts[1],
        'f2_6[0]': stu_ssn_2_parts[2],
        
        # First Institution
        'f2_7[0]': institution_1_name,
        'f2_8[0]': institution_1_address,
        
        # First Institution EIN
        **{f'f2_{i+9}[0]': d for i, d in enumerate(ein1_digits)},
        
        # Second Institution
        'f2_18[0]': institution_2_name,
        'f2_19[0]': institution_2_address,
        
        # Second Institution EIN
        **{f'f2_{i+20}[0]': d for i, d in enumerate(ein2_digits)},
        
        # Credit Calculations
        'f2_29[0]': qualified_expenses,
        'f2_30[0]': expenses_minus_2000,
        'f2_31[0]': multiply_25_percent,
        'f2_32[0]': final_amount,
        'f2_33[0]': lifetime_learning_credit,
        
        # Checkboxes
        'c1_1[0]': under_24,
        'c2_1[0]': received_1098t_inst1,
        'c2_1[1]': not received_1098t_inst1,
        'c2_2[0]': box_7_checked_inst1,
        'c2_2[1]': not box_7_checked_inst1,
        'c2_3[0]': received_1098t_inst2,
        'c2_3[1]': not received_1098t_inst2,
        'c2_4[0]': box_7_checked_inst2,
        'c2_4[1]': not box_7_checked_inst2,
        'c2_5[0]': not aoc_claimed_prior,
        'c2_5[1]': aoc_claimed_prior,
        'c2_6[0]': half_time_enrollment,
        'c2_6[1]': not half_time_enrollment,
        'c2_7[0]': not completed_first_4_years,
        'c2_7[1]': completed_first_4_years,
        'c2_8[0]': not felony_drug_conviction,
        'c2_8[1]': felony_drug_conviction
    }

    try:
        filled_form = PdfWrapper("/Users/priyadarshannarayanasamy/Desktop/hacklytics/taxerino/backend/form_filler/templates/8863.pdf").fill(form_data)
        with open("filled/filled_form_8863.pdf", "wb+") as output:
            output.write(filled_form.read())
        print("Form 8863 filled successfully! Check filled_form_8863.pdf")
        return True
    except Exception as e:
        print(f"Error filling Form 8863: {str(e)}")
        return False
    
if __name__ == "__main__":
    fill_8863_form(
        # Basic Information
        taxpayer_name="John A Smith",
        taxpayer_ssn="123-45-6789",
        
        # Student Information
        student_name="Jane B Smith",
        student_ssn="987-65-4321",
        student_ssn_2="987-65-4321",
        
        # Part I - Financial Information
        tentative_credit="4000",
        income_limit="180000",
        modified_agi="160000",
        income_difference="20000",
        phase_out_amount="20000",
        decimal_amount_1000="1.000",
        decimal_amount_other="0.750",
        multiply_result="3000",
        refundable_credit="1200",
        credit_limit="1800",
        
        # Part II - Nonrefundable Education Credits
        total_expenses="2500",
        smaller_amount="2500",
        multiply_20_percent="500",
        married_limit="180000",
        form_1040_amount="160000",
        subtract_result="20000",
        filing_status_amount="20000",
        decimal_amount_2_1000="1.000",
        decimal_amount_2_other="0.750",
        multiply_final="500",
        nonrefundable_credits="2300",
        
        # Educational Institutions
        institution_1_name="Test University",
        institution_1_address="123 Education St, Test City, TS 12345",
        institution_1_ein="123456789",
        
        institution_2_name="Second Test College",
        institution_2_address="456 Learning Ave, Study City, SC 67890",
        institution_2_ein="987654321",
        
        # Credit Calculations
        qualified_expenses="4000",
        expenses_minus_2000="2000",
        multiply_25_percent="500",
        final_amount="2500",
        lifetime_learning_credit="4000",
        
        # Status Checkboxes
        under_24=True,
        received_1098t_inst1=True,
        box_7_checked_inst1=False,
        received_1098t_inst2=True,
        box_7_checked_inst2=False,
        aoc_claimed_prior=False,
        half_time_enrollment=True,
        completed_first_4_years=False,
        felony_drug_conviction=False
    )