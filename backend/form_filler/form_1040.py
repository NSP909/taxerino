from PyPDFForm import PdfWrapper
from typing import List, Optional

def fill_1040_form(
    # Part I - Basic Information
    tax_year_begin: str,            # f1_01[0] - Year beginning date
    tax_year_end: str,              # f1_02[0] - Year ending date
    year_20: str,                   # f1_03[0] - 20__ year
    first_name: str,                # f1_04[0] - First name and middle initial
    last_name: str,                 # f1_05[0] - Last name
    ssn: str,                       # f1_06[0] - Your social security number
    spouse_first_name: str = "",    # f1_07[0] - Spouse's first name and middle initial
    spouse_last_name: str = "",     # f1_08[0] - Spouse's last name
    spouse_ssn: str = "",           # f1_09[0] - Spouse's social security number
    home_address: str = "",         # f1_10[0] - Home address
    apt_no: str = "",              # f1_11[0] - Apartment number
    city: str = "",                # f1_12[0] - City or town
    state: str = "",               # f1_13[0] - State
    zip_code: str = "",            # f1_14[0] - ZIP code
    foreign_country: str = "",     # f1_15[0] - Foreign country name
    foreign_province: str = "",    # f1_16[0] - Foreign province/state
    foreign_postal_code: str = "", # f1_17[0] - Foreign postal code
    mfs_spouse_name: str = "",     # f1_18[0] - If MFS, spouse's name or HOH qualifying person
    nonresident_spouse_name: str = "", # f1_19[0] - Nonresident alien spouse's name

    # Filing Status and Election Campaign
    filing_single: bool = False,    # c1_3[0] - Single filing status
    filing_joint: bool = False,     # c1_3[1] - Married filing jointly
    filing_separate: bool = False,  # c1_3[2] - Married filing separately
    nonresident_alien_spouse: bool = False,  # c1_4[0] - Nonresident alien spouse checkbox
    you_election_fund: bool = False,    # c1_1[0] - Your election campaign fund
    spouse_election_fund: bool = False, # c1_2[0] - Spouse election campaign fund

    # Digital Assets
    digital_assets_yes: bool = False,   # c1_5[0] - Digital assets Yes
    digital_assets_no: bool = False,    # c1_5[1] - Digital assets No

    # Standard Deduction
    you_dependent: bool = False,        # c1_6[0] - Someone can claim you as dependent
    spouse_dependent: bool = False,     # c1_7[0] - Someone can claim your spouse as dependent
    spouse_itemizes: bool = False,      # c1_8[0] - Spouse itemizes on separate return
    
    # Age/Blindness
    you_born_before_1960: bool = False, # c1_9[0] - You were born before January 2, 1960
    you_blind: bool = False,            # c1_10[0] - You are blind
    spouse_born_before_1960: bool = False, # c1_11[0] - Spouse born before January 2, 1960
    spouse_blind: bool = False,         # c1_12[0] - Spouse is blind
    
    # Dependents
    more_than_four_dependents: bool = False,  # c1_13[0] - More than 4 dependents
    dependents: List[dict] = None,     # List of dependent information
    
    # Dependent Tax Credit Qualifications
    dependent_1_child_credit: bool = False,   # c1_14[0] - First dependent qualifies for child tax credit
    dependent_1_other_credit: bool = False,   # c1_15[0] - First dependent qualifies for other dependent credit
    dependent_2_child_credit: bool = False,   # c1_16[0] - Second dependent qualifies for child tax credit
    dependent_2_other_credit: bool = False,   # c1_17[0] - Second dependent qualifies for other dependent credit
    dependent_3_child_credit: bool = False,   # c1_18[0] - Third dependent qualifies for child tax credit
    dependent_3_other_credit: bool = False,   # c1_19[0] - Third dependent qualifies for other dependent credit
    dependent_4_child_credit: bool = False,   # c1_20[0] - Fourth dependent qualifies for child tax credit
    dependent_4_other_credit: bool = False,   # c1_21[0] - Fourth dependent qualifies for other dependent credit

    # Additional Elections
    lump_sum_election: bool = False,    # c1_22[0] - Lump-sum election method
    capital_gain_no_schedule: bool = False,  # c1_23[0] - Capital gain without Schedule D

    # Income Information
    w2_income: str = "",               # f1_32[0] - W-2 wages (box 1)
    household_wages: str = "",         # f1_33[0] - Household employee wages
    tip_income: str = "",             # f1_34[0] - Unreported tip income
    medicaid_waiver: str = "",        # f1_35[0] - Medicaid waiver payments
    dependent_care_benefits: str = "", # f1_36[0] - Dependent care benefits
    adoption_benefits: str = "",       # f1_37[0] - Adoption benefits
    wages_8919: str = "",             # f1_38[0] - Wages from Form 8919
    other_earned_income: str = "",    # f1_39[0] - Other earned income
    nontaxable_combat_pay: str = "",  # f1_40[0] - Nontaxable combat pay
    total_income: str = "",           # f1_41[0] - Total income

    # Interest and Dividends
    tax_exempt_interest: str = "",    # f1_42[0] - Tax-exempt interest
    taxable_interest: str = "",       # f1_43[0] - Taxable interest
    qualified_dividends: str = "",    # f1_44[0] - Qualified dividends
    ordinary_dividends: str = "",     # f1_45[0] - Ordinary dividends

    # Retirement Income
    ira_distributions: str = "",      # f1_46[0] - IRA distributions
    ira_taxable_amount: str = "",     # f1_47[0] - Taxable IRA amount
    pensions_annuities: str = "",     # f1_48[0] - Pensions and annuities
    pensions_taxable_amount: str = "", # f1_49[0] - Taxable pension amount
    
    # Social Security Benefits
    social_security_benefits: str = "", # f1_50[0] - Social security benefits
    social_security_taxable: str = "",  # f1_51[0] - Taxable social security
    
    # Additional Income
    capital_gain_loss: str = "",       # f1_52[0] - Capital gain or loss
    schedule_1_income: str = "",       # f1_53[0] - Additional income from Schedule 1
    total_income_all: str = "",        # f1_54[0] - Total income (all sources)
    adjustments_to_income: str = "",   # f1_55[0] - Adjustments to income
    adjusted_gross_income: str = "",   # f1_56[0] - Adjusted gross income
    
    # Deductions
    standard_deduction: str = "",      # f1_57[0] - Standard deduction amount
    qbi_deduction: str = "",          # f1_58[0] - Qualified business income deduction
    total_deductions: str = "",       # f1_59[0] - Total deductions
    taxable_income: str = "",         # f1_60[0] - Taxable income

    # Tax and Credits
    tax_amount: str = "",             # f2_02[0] - Tax amount
    schedule_2_line_3: str = "",      # f2_03[0] - Additional taxes
    total_tax: str = "",             # f2_04[0] - Total tax
    child_tax_credit: str = "",      # f2_05[0] - Child tax credit
    schedule_3_line_8: str = "",     # f2_06[0] - Other credits
    total_credits: str = "",         # f2_07[0] - Total credits
    tax_less_credits: str = "",      # f2_08[0] - Tax less credits
    other_taxes: str = "",           # f2_09[0] - Other taxes
    total_tax_due: str = "",         # f2_10[0] - Total tax due

    # Tax Forms Attachments
    form_8814_attached: bool = False,   # c2_1[0] - Form 8814 attached
    form_4972_attached: bool = False,   # c2_2[0] - Form 4972 attached
    other_form: str = "",              # f2_01[0] - Other tax form
    
    # Payments and Refundable Credits
    w2_withholding: str = "",         # f2_11[0] - W-2 withholding
    form_1099_withholding: str = "",  # f2_12[0] - 1099 withholding
    other_withholding: str = "",      # f2_13[0] - Other withholding
    total_withholding: str = "",      # f2_14[0] - Total withholding
    estimated_tax_payments: str = "",  # f2_15[0] - Estimated tax payments
    earned_income_credit: str = "",    # f2_16[0] - Earned income credit
    additional_child_tax_credit: str = "", # f2_17[0] - Additional child tax credit
    american_opportunity_credit: str = "",  # f2_18[0] - American opportunity credit
    reserved_future: str = "",         # f2_19[0] - Reserved for future use
    schedule_3_line_15: str = "",      # f2_20[0] - Schedule 3, line 15 amount
    total_other_payments: str = "",    # f2_21[0] - Total other payments
    total_payments: str = "",          # f2_22[0] - Total payments

    # Refund Information
    overpaid_amount: str = "",         # f2_23[0] - Amount overpaid
    refund_amount: str = "",           # f2_24[0] - Amount to be refunded
    routing_number: str = "",          # f2_25[0] - Bank routing number
    account_number: str = "",          # f2_26[0] - Bank account number
    account_type_checking: bool = False,  # c2_5[0] - Checking account
    account_type_savings: bool = False,   # c2_5[1] - Savings account
    form_8888_attached: bool = False,     # c2_4[0] - Form 8888 attached
    applied_to_estimated_tax: str = "",   # f2_27[0] - Applied to estimated tax
    amount_you_owe: str = "",            # f2_28[0] - Amount you owe
    estimated_tax_penalty: str = "",      # f2_29[0] - Estimated tax penalty

    # Third Party Designee
    third_party_designee: bool = False,   # c2_6[0] - Allow third party designee
    designee_name: str = "",              # f2_30[0] - Designee name
    designee_phone: str = "",             # f2_31[0] - Designee phone
    designee_pin: str = "",               # f2_32[0] - Designee PIN

    # Signature Information
    your_occupation: str = "",            # f2_33[0] - Your occupation
    your_identity_pin: str = "",          # f2_34[0] - Your identity PIN
    spouse_occupation: str = "",          # f2_35[0] - Spouse occupation
    spouse_identity_pin: str = "",        # f2_36[0] - Spouse identity PIN
    phone_number: str = "",               # f2_37[0] - Phone number
    email_address: str = "",              # f2_38[0] - Email address

    # Paid Preparer Information
    preparer_name: str = "",              # f2_39[0] - Preparer name
    preparer_ptin: str = "",              # f2_40[0] - Preparer PTIN
    preparer_self_employed: bool = False, # c2_7[0] - Preparer self-employed
    firm_name: str = "",                  # f2_41[0] - Firm name
    firm_phone: str = "",                 # f2_42[0] - Firm phone
    firm_address: str = "",               # f2_43[0] - Firm address
    firm_ein: str = ""                    # f2_44[0] - Firm EIN
):
    """
    Fill out IRS Form 1040 with comprehensive field support.
    All monetary values should be provided as strings in the format "0.00"
    """
    
    form_data = {
        # Basic Information
        'f1_01[0]': tax_year_begin,
        'f1_02[0]': tax_year_end,
        'f1_03[0]': year_20,
        'f1_04[0]': first_name,
        'f1_05[0]': last_name,
        'f1_06[0]': ssn,
        'f1_07[0]': spouse_first_name,
        'f1_08[0]': spouse_last_name,
        'f1_09[0]': spouse_ssn,
        'f1_10[0]': home_address,
        'f1_11[0]': apt_no,
        'f1_12[0]': city,
        'f1_13[0]': state,
        'f1_14[0]': zip_code,
        'f1_15[0]': foreign_country,
        'f1_16[0]': foreign_province,
        'f1_17[0]': foreign_postal_code,
        'f1_18[0]': mfs_spouse_name,
        'f1_19[0]': nonresident_spouse_name,

        # Filing Status and Elections
        'c1_3[0]': filing_single,
        'c1_3[1]': filing_joint,
        'c1_3[2]': filing_separate,
        'c1_4[0]': nonresident_alien_spouse,
        'c1_1[0]': you_election_fund,
        'c1_2[0]': spouse_election_fund,

        # Digital Assets
        'c1_5[0]': digital_assets_yes,
        'c1_5[1]': digital_assets_no,

        # Standard Deduction
        'c1_6[0]': you_dependent,
        'c1_7[0]': spouse_dependent,
        'c1_8[0]': spouse_itemizes,

        # Age/Blindness
        'c1_9[0]': you_born_before_1960,
        'c1_10[0]': you_blind,
        'c1_11[0]': spouse_born_before_1960,
        'c1_12[0]': spouse_blind,

          # Dependents
        'c1_13[0]': more_than_four_dependents,
        
        # Dependent Tax Credits
        'c1_14[0]': dependent_1_child_credit,
        'c1_15[0]': dependent_1_other_credit,
        'c1_16[0]': dependent_2_child_credit,
        'c1_17[0]': dependent_2_other_credit,
        'c1_18[0]': dependent_3_child_credit,
        'c1_19[0]': dependent_3_other_credit,
        'c1_20[0]': dependent_4_child_credit,
        'c1_21[0]': dependent_4_other_credit,

        # Additional Elections
        'c1_22[0]': lump_sum_election,
        'c1_23[0]': capital_gain_no_schedule,

        # Income Information
        'f1_32[0]': w2_income,
        'f1_33[0]': household_wages,
        'f1_34[0]': tip_income,
        'f1_35[0]': medicaid_waiver,
        'f1_36[0]': dependent_care_benefits,
        'f1_37[0]': adoption_benefits,
        'f1_38[0]': wages_8919,
        'f1_39[0]': other_earned_income,
        'f1_40[0]': nontaxable_combat_pay,
        'f1_41[0]': total_income,

        # Interest and Dividends
        'f1_42[0]': tax_exempt_interest,
        'f1_43[0]': taxable_interest,
        'f1_44[0]': qualified_dividends,
        'f1_45[0]': ordinary_dividends,

        # Retirement Income
        'f1_46[0]': ira_distributions,
        'f1_47[0]': ira_taxable_amount,
        'f1_48[0]': pensions_annuities,
        'f1_49[0]': pensions_taxable_amount,

        # Social Security Benefits
        'f1_50[0]': social_security_benefits,
        'f1_51[0]': social_security_taxable,

        # Additional Income
        'f1_52[0]': capital_gain_loss,
        'f1_53[0]': schedule_1_income,
        'f1_54[0]': total_income_all,
        'f1_55[0]': adjustments_to_income,
        'f1_56[0]': adjusted_gross_income,

        # Deductions
        'f1_57[0]': standard_deduction,
        'f1_58[0]': qbi_deduction,
        'f1_59[0]': total_deductions,
        'f1_60[0]': taxable_income,

        # Tax and Credits
        'f2_01[0]': other_form,
        'f2_02[0]': tax_amount,
        'f2_03[0]': schedule_2_line_3,
        'f2_04[0]': total_tax,
        'f2_05[0]': child_tax_credit,
        'f2_06[0]': schedule_3_line_8,
        'f2_07[0]': total_credits,
        'f2_08[0]': tax_less_credits,
        'f2_09[0]': other_taxes,
        'f2_10[0]': total_tax_due,

        # Tax Forms
        'c2_1[0]': form_8814_attached,
        'c2_2[0]': form_4972_attached,

        # Payments and Credits
        'f2_11[0]': w2_withholding,
        'f2_12[0]': form_1099_withholding,
        'f2_13[0]': other_withholding,
        'f2_14[0]': total_withholding,
        'f2_15[0]': estimated_tax_payments,
        'f2_16[0]': earned_income_credit,
        'f2_17[0]': additional_child_tax_credit,
        'f2_18[0]': american_opportunity_credit,
        'f2_19[0]': reserved_future,
        'f2_20[0]': schedule_3_line_15,
        'f2_21[0]': total_other_payments,
        'f2_22[0]': total_payments,

        # Refund Information
        'f2_23[0]': overpaid_amount,
        'f2_24[0]': refund_amount,
        'f2_25[0]': routing_number,
        'f2_26[0]': account_number,
        'c2_5[0]': account_type_checking,
        'c2_5[1]': account_type_savings,
        'c2_4[0]': form_8888_attached,
        'f2_27[0]': applied_to_estimated_tax,
        'f2_28[0]': amount_you_owe,
        'f2_29[0]': estimated_tax_penalty,

        # Third Party Designee
        'c2_6[0]': third_party_designee,
        'f2_30[0]': designee_name,
        'f2_31[0]': designee_phone,
        'f2_32[0]': designee_pin,

        # Signature Information
        'f2_33[0]': your_occupation,
        'f2_34[0]': your_identity_pin,
        'f2_35[0]': spouse_occupation,
        'f2_36[0]': spouse_identity_pin,
        'f2_37[0]': phone_number,
        'f2_38[0]': email_address,

        # Paid Preparer Information
        'f2_39[0]': preparer_name,
        'f2_40[0]': preparer_ptin,
        'c2_7[0]': preparer_self_employed,
        'f2_41[0]': firm_name,
        'f2_42[0]': firm_phone,
        'f2_43[0]': firm_address,
        'f2_44[0]': firm_ein
    }

    # Handle dependents if provided
    if dependents:
        dependent_fields = [
            ('f1_20[0]', 'f1_21[0]', 'f1_22[0]'),  # First dependent
            ('f1_23[0]', 'f1_24[0]', 'f1_25[0]'),  # Second dependent
            ('f1_26[0]', 'f1_27[0]', 'f1_28[0]'),  # Third dependent
            ('f1_29[0]', 'f1_30[0]', 'f1_31[0]')   # Fourth dependent
        ]
        
        for i, dependent in enumerate(dependents[:4]):
            form_data[dependent_fields[i][0]] = dependent.get('name', '')
            form_data[dependent_fields[i][1]] = dependent.get('ssn', '')
            form_data[dependent_fields[i][2]] = dependent.get('relationship', '')

    try:
        filled_form = PdfWrapper("/Users/priyadarshannarayanasamy/Desktop/hacklytics/taxerino/backend/form_filler/filled_1040.pdf").fill(form_data)
        with open("filled/filled_1040.pdf", "wb+") as output:
            output.write(filled_form.read())
        print("Form 1040 filled successfully! Check filled_1040.pdf")
        return True
    except Exception as e:
        print(f"Error filling Form 1040: {str(e)}")
        return False
    
if __name__ == "__main__":
    # Test dependent data
    test_dependents = [
        {
            "name": "Jane Smith",
            "ssn": "123-45-6780",
            "relationship": "Daughter"
        },
        {
            "name": "John Smith Jr",
            "ssn": "123-45-6781",
            "relationship": "Son"
        },
        {
            "name": "Mary Smith",
            "ssn": "123-45-6782",
            "relationship": "Daughter"
        },
        {
            "name": "Robert Smith",
            "ssn": "123-45-6783",
            "relationship": "Son"
        }
    ]

    fill_1040_form(
        # Basic Information
        tax_year_begin="01/01/2024",
        tax_year_end="12/31/2024",
        year_20="24",
        first_name="John W",
        last_name="Smith",
        ssn="123-45-6789",
        spouse_first_name="Sarah J",
        spouse_last_name="Smith",
        spouse_ssn="987-65-4321",
        home_address="123 Main Street",
        apt_no="4B",
        city="New York",
        state="NY",
        zip_code="10001",
        foreign_country="",
        foreign_province="",
        foreign_postal_code="",
        mfs_spouse_name="",
        nonresident_spouse_name="",

        # Filing Status and Elections
        filing_single=False,
        filing_joint=True,
        filing_separate=False,
        nonresident_alien_spouse=False,
        you_election_fund=True,
        spouse_election_fund=True,

        # Digital Assets
        digital_assets_yes=False,
        digital_assets_no=True,

        # Standard Deduction
        you_dependent=False,
        spouse_dependent=False,
        spouse_itemizes=False,

        # Age/Blindness
        you_born_before_1960=True,
        you_blind=False,
        spouse_born_before_1960=False,
        spouse_blind=False,

        # Dependents
        more_than_four_dependents=False,
        dependents=test_dependents,

        # Dependent Tax Credits
        dependent_1_child_credit=True,
        dependent_1_other_credit=False,
        dependent_2_child_credit=True,
        dependent_2_other_credit=False,
        dependent_3_child_credit=True,
        dependent_3_other_credit=False,
        dependent_4_child_credit=True,
        dependent_4_other_credit=False,

        # Additional Elections
        lump_sum_election=True,
        capital_gain_no_schedule=True,

        # Income Information
        w2_income="120000.00",
        household_wages="0.00",
        tip_income="1500.00",
        medicaid_waiver="0.00",
        dependent_care_benefits="2000.00",
        adoption_benefits="0.00",
        wages_8919="0.00",
        other_earned_income="500.00",
        nontaxable_combat_pay="0.00",
        total_income="124000.00",

        # Interest and Dividends
        tax_exempt_interest="500.00",
        taxable_interest="1200.00",
        qualified_dividends="3000.00",
        ordinary_dividends="4000.00",

        # Retirement Income
        ira_distributions="10000.00",
        ira_taxable_amount="8000.00",
        pensions_annuities="20000.00",
        pensions_taxable_amount="18000.00",

        # Social Security Benefits
        social_security_benefits="24000.00",
        social_security_taxable="18000.00",

        # Additional Income
        capital_gain_loss="5000.00",
        schedule_1_income="2000.00",
        total_income_all="185200.00",
        adjustments_to_income="12000.00",
        adjusted_gross_income="173200.00",

        # Deductions
        standard_deduction="27700.00",
        qbi_deduction="2000.00",
        total_deductions="29700.00",
        taxable_income="143500.00",

        # Tax and Credits
        tax_amount="22300.00",
        schedule_2_line_3="1500.00",
        total_tax="23800.00",
        child_tax_credit="8000.00",
        schedule_3_line_8="2000.00",
        total_credits="10000.00",
        tax_less_credits="13800.00",
        other_taxes="2200.00",
        total_tax_due="16000.00",

        # Tax Forms
        form_8814_attached=True,
        form_4972_attached=False,
        other_form="8888",

        # Payments and Credits
        w2_withholding="18000.00",
        form_1099_withholding="2000.00",
        other_withholding="500.00",
        total_withholding="20500.00",
        estimated_tax_payments="4000.00",
        earned_income_credit="0.00",
        additional_child_tax_credit="2000.00",
        american_opportunity_credit="2500.00",
        reserved_future="",
        schedule_3_line_15="1000.00",
        total_other_payments="5500.00",
        total_payments="30000.00",

        # Refund Information
        overpaid_amount="14000.00",
        refund_amount="13000.00",
        routing_number="123456789",
        account_number="987654321",
        account_type_checking=True,
        account_type_savings=False,
        form_8888_attached=True,
        applied_to_estimated_tax="1000.00",
        amount_you_owe="0.00",
        estimated_tax_penalty="0.00",

        # Third Party Designee
        third_party_designee=True,
        designee_name="Jane Accountant",
        designee_phone="555-123-4567",
        designee_pin="12345",

        # Signature Information
        your_occupation="Software Engineer",
        your_identity_pin="123456",
        spouse_occupation="Teacher",
        spouse_identity_pin="654321",
        phone_number="555-987-6543",
        email_address="john.smith@email.com",

        # Paid Preparer Information
        preparer_name="Thomas Tax",
        preparer_ptin="P12345678",
        preparer_self_employed=True,
        firm_name="Tax Experts LLC",
        firm_phone="555-555-5555",
        firm_address="456 Tax Street, Suite 789, New York, NY 10002",
        firm_ein="12-3456789"
    )