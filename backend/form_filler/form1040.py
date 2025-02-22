from PyPDFForm import PdfWrapper
from typing import List, Optional

def fill_1040_form(
    # Personal Information
    tax_year_begin: str,
    tax_year_end: str,
    first_name: str,
    last_name: str,
    ssn: str,
    spouse_first_name: str = "",
    spouse_last_name: str = "",
    spouse_ssn: str = "",
    address: str = "",
    apt_no: str = "",
    city: str = "",
    state: str = "",
    zip_code: str = "",
    foreign_country: str = "",
    foreign_province: str = "",
    foreign_postal_code: str = "",
    
    # Filing Status
    filing_status: str = "single",  # single, joint, separate
    
    # Presidential Election Campaign
    you_election_fund: bool = False,
    spouse_election_fund: bool = False,
    
    # Digital Assets
    digital_assets: str = "no",  # yes, no
    
    # Standard Deduction
    you_dependent: bool = False,
    spouse_dependent: bool = False,
    spouse_itemizes: bool = False,
    
    # Age/Blindness
    you_born_before_1960: bool = False,
    you_blind: bool = False,
    spouse_born_before_1960: bool = False,
    spouse_blind: bool = False,
    
    # Dependents
    dependents: List[dict] = None,  # List of dicts with name, ssn, relationship
    more_than_four_dependents: bool = False,
    
    # Tax and Credits
    tax_amount: str = "",
    form_8814: bool = False,
    form_4972: bool = False,
    other_tax_form: str = "",
    schedule_2_line_3: str = "",
    child_tax_credit: str = "",
    schedule_3_line_8: str = "",
    schedule_2_line_21: str = "",
    
    # Payments
    w2_withholding: str = "",
    form_1099_withholding: str = "",
    other_withholding: str = "",
    estimated_tax_payments: str = "",
    earned_income_credit: str = "",
    additional_child_tax_credit: str = "",
    american_opportunity_credit: str = "",
    schedule_3_line_15: str = "",
    estimated_tax_penalty: str = "",
    
    # Income
    w2_income: str = "",
    household_employee_wages: str = "",
    tip_income: str = "",
    medicaid_waiver: str = "",
    dependent_care_benefits: str = "",
    adoption_benefits: str = "",
    wages_8919: str = "",
    other_earned_income: str = "",
    nontaxable_combat_pay: str = "",
    
    # Interest and Dividends
    tax_exempt_interest: str = "",
    taxable_interest: str = "",
    qualified_dividends: str = "",
    ordinary_dividends: str = "",
    
    # IRA and Pension
    ira_distributions: str = "",
    ira_taxable_amount: str = "",
    pensions_annuities: str = "",
    pensions_taxable_amount: str = "",
    
    # Social Security
    social_security_benefits: str = "",
    social_security_taxable: str = "",
    
    # Additional Income
    capital_gain_loss: str = "",
    schedule_1_income: str = "",
    
    # Direct Deposit
    routing_number: str = "",
    account_number: str = "",
    account_type: str = "checking",  # checking, savings
    
    # Third Party Designee
    allow_discussant: bool = False,
    designee_name: str = "",
    designee_phone: str = "",
    designee_pin: str = "",
    
    # Occupation Info
    your_occupation: str = "",
    spouse_occupation: str = "",
    your_pin: str = "",
    spouse_pin: str = "",
    phone: str = "",
    email: str = "",
    
    # Preparer Info
    preparer_name: str = "",
    preparer_ptin: str = "",
    preparer_self_employed: bool = False,
    firm_name: str = "",
    firm_phone: str = "",
    firm_address: str = "",
    firm_ein: str = ""
):
    """Fill out IRS Form 1040 with provided information including tax and payment sections."""
    
    form_data = {
        # Basic Information
        'f1_01[0]': tax_year_begin,
        'f1_02[0]': tax_year_end,
        'f1_04[0]': first_name,
        'f1_05[0]': last_name,
        'f1_06[0]': ssn,
        'f1_07[0]': spouse_first_name,
        'f1_08[0]': spouse_last_name,
        'f1_09[0]': spouse_ssn,
        'f1_10[0]': address,
        'f1_11[0]': apt_no,
        'f1_12[0]': city,
        'f1_13[0]': state,
        'f1_14[0]': zip_code,
        'f1_15[0]': foreign_country,
        'f1_16[0]': foreign_province,
        'f1_17[0]': foreign_postal_code,
        
        # Filing Status
        'c1_3[0]': filing_status == "single",
        'c1_3[1]': filing_status == "joint",
        'c1_3[2]': filing_status == "separate",
        
        # Presidential Election Campaign
        'c1_1[0]': you_election_fund,
        'c1_2[0]': spouse_election_fund,
        
        # Digital Assets
        'c1_5[0]': digital_assets == "yes",
        'c1_5[1]': digital_assets == "no",
        
        # Standard Deduction
        'c1_6[0]': you_dependent,
        'c1_7[0]': spouse_dependent,
        'c1_8[0]': spouse_itemizes,
        
        # Age/Blindness
        'c1_9[0]': you_born_before_1960,
        'c1_10[0]': you_blind,
        'c1_11[0]': spouse_born_before_1960,
        'c1_12[0]': spouse_blind,
        
        # Dependents Section
        'c1_13[0]': more_than_four_dependents,
        
        # Income Fields
        'f1_32[0]': w2_income,
        'f1_33[0]': household_employee_wages,
        'f1_34[0]': tip_income,
        'f1_35[0]': medicaid_waiver,
        'f1_36[0]': dependent_care_benefits,
        'f1_37[0]': adoption_benefits,
        'f1_38[0]': wages_8919,
        'f1_39[0]': other_earned_income,
        'f1_40[0]': nontaxable_combat_pay,
        
        # Interest and Dividends
        'f1_42[0]': tax_exempt_interest,
        'f1_43[0]': taxable_interest,
        'f1_44[0]': qualified_dividends,
        'f1_45[0]': ordinary_dividends,
        
        # IRA and Pension
        'f1_46[0]': ira_distributions,
        'f1_47[0]': ira_taxable_amount,
        'f1_48[0]': pensions_annuities,
        'f1_49[0]': pensions_taxable_amount,
        
        # Social Security
        'f1_50[0]': social_security_benefits,
        'f1_51[0]': social_security_taxable,
        
        # Additional Income
        'f1_52[0]': capital_gain_loss,
        'f1_53[0]': schedule_1_income,
        
        # Tax and Credits
        'f2_02[0]': tax_amount,
        'c2_1[0]': form_8814,
        'c2_2[0]': form_4972,
        'f2_01[0]': other_tax_form,
        'f2_03[0]': schedule_2_line_3,
        'f2_04[0]': str(float(tax_amount or 0) + float(schedule_2_line_3 or 0)),  # Add lines 16 and 17
        'f2_05[0]': child_tax_credit,
        'f2_06[0]': schedule_3_line_8,
        'f2_07[0]': str(float(child_tax_credit or 0) + float(schedule_3_line_8 or 0)),  # Add lines 19 and 20
        'f2_08[0]': str(max(0, float(tax_amount or 0) + float(schedule_2_line_3 or 0) - float(child_tax_credit or 0) - float(schedule_3_line_8 or 0))),  # Line 22
        'f2_09[0]': schedule_2_line_21,
        'f2_10[0]': str(float(schedule_2_line_21 or 0) + float(str(max(0, float(tax_amount or 0) + float(schedule_2_line_3 or 0) - float(child_tax_credit or 0) - float(schedule_3_line_8 or 0))) or 0)),  # Add lines 22 and 23
        
        # Payments
        'f2_11[0]': w2_withholding,
        'f2_12[0]': form_1099_withholding,
        'f2_13[0]': other_withholding,
        'f2_14[0]': str(sum(float(x or 0) for x in [w2_withholding, form_1099_withholding, other_withholding])),  # Add lines 25a through 25c
        'f2_15[0]': estimated_tax_payments,
        'f2_16[0]': earned_income_credit,
        'f2_17[0]': additional_child_tax_credit,
        'f2_18[0]': american_opportunity_credit,
        'f2_20[0]': schedule_3_line_15,
        'f2_21[0]': str(sum(float(x or 0) for x in [earned_income_credit, additional_child_tax_credit, american_opportunity_credit, schedule_3_line_15])),  # Add lines 27, 28, 29, and 31
        'f2_22[0]': str(sum(float(x or 0) for x in [str(sum(float(x or 0) for x in [w2_withholding, form_1099_withholding, other_withholding])), estimated_tax_payments, str(sum(float(x or 0) for x in [earned_income_credit, additional_child_tax_credit, american_opportunity_credit, schedule_3_line_15]))])),  # Add lines 25d, 26, and 32
        'f2_29[0]': estimated_tax_penalty,
        
        # Direct Deposit
        'f2_25[0]': routing_number,
        'f2_26[0]': account_number,
        'c2_5[0]': account_type == "checking",
        'c2_5[1]': account_type == "savings",
        
        # Third Party Designee
        'c2_6[0]': allow_discussant,
        'f2_30[0]': designee_name,
        'f2_31[0]': designee_phone,
        'f2_32[0]': designee_pin,
        
        # Occupation and Contact
        'f2_33[0]': your_occupation,
        'f2_34[0]': your_pin,
        'f2_35[0]': spouse_occupation,
        'f2_36[0]': spouse_pin,
        'f2_37[0]': phone,
        'f2_38[0]': email,
        
        # Preparer Information
        'c2_7[0]': preparer_self_employed,
        'f2_39[0]': preparer_name,
        'f2_40[0]': preparer_ptin,
        'f2_41[0]': firm_name,
        'f2_42[0]': firm_phone,
        'f2_43[0]': firm_address,
        'f2_44[0]': firm_ein
    }
    
    # Handle dependents if provided
    if dependents:
        dependent_fields = [
            ('f1_20[0]', 'f1_21[0]', 'f1_22[0]'),
            ('f1_23[0]', 'f1_24[0]', 'f1_25[0]'),
            ('f1_26[0]', 'f1_27[0]', 'f1_28[0]'),
            ('f1_29[0]', 'f1_30[0]', 'f1_31[0]')
        ]
        
        for i, dependent in enumerate(dependents[:4]):  # Limit to 4 dependents
            form_data[dependent_fields[i][0]] = dependent.get('name', '')
            form_data[dependent_fields[i][1]] = dependent.get('ssn', '')
            form_data[dependent_fields[i][2]] = dependent.get('relationship', '')
    
    # Fill and save the form
    filled_form = PdfWrapper("1040.pdf").fill(form_data)
    with open("filled_1040.pdf", "wb+") as output:
        output.write(filled_form.read())

# Example usage with test data
if __name__ == "__main__":
    test_dependents = [
        {"name": "John Jr", "ssn": "123-45-6789", "relationship": "Son"},
        {"name": "Mary Smith", "ssn": "987-65-4321", "relationship": "Daughter"}
    ]
    
    fill_1040_form(
        # Personal Information
        tax_year_begin="01/01/2024",
        tax_year_end="12/31/2024",
        first_name="John",
        last_name="Smith",
        ssn="123-45-6789",
        spouse_first_name="Jane",
        spouse_last_name="Smith",
        spouse_ssn="987-65-4321",
        address="123 Main Street",
        apt_no="4B",
        city="New York",
        state="NY",
        zip_code="10001",
        
        # Filing Status
        filing_status="joint",
        
        # Elections and Status
        you_election_fund=True,
        spouse_election_fund=True,
        digital_assets="no",
        
        # Standard Deduction
        you_dependent=True,
        spouse_dependent=False,
        spouse_itemizes=False,
        
        # Age/Blindness
        you_born_before_1960=True,
        you_blind=False,
        spouse_born_before_1960=False,
        spouse_blind=False,
        
        # Dependents
        dependents=test_dependents,
        more_than_four_dependents=False,
        
        # Income
        w2_income="75000",
        household_employee_wages="0",
        tip_income="1000",
        medicaid_waiver="0",
        dependent_care_benefits="2000",
        adoption_benefits="0",
        wages_8919="0",
        other_earned_income="500",
        nontaxable_combat_pay="0",
        
        # Interest and Dividends
        tax_exempt_interest="100",
        taxable_interest="1500",
        qualified_dividends="2000",
        ordinary_dividends="2500",
        
        # IRA and Pension
        ira_distributions="10000",
        ira_taxable_amount="8000",
        pensions_annuities="20000",
        pensions_taxable_amount="18000",
        
        # Social Security
        social_security_benefits="15000",
        social_security_taxable="12000",
        
        # Additional Income
        capital_gain_loss="5000",
        schedule_1_income="3000",
        
        # Tax and Credits
        tax_amount="15000",
        form_8814=True,
        form_4972=False,
        other_tax_form="1234",
        schedule_2_line_3="2000",
        child_tax_credit="3000",
        schedule_3_line_8="1500",
        schedule_2_line_21="500",
        
        # Payments
        w2_withholding="12000",
        form_1099_withholding="3000",
        other_withholding="1000",
        estimated_tax_payments="4000",
        earned_income_credit="2000",
        additional_child_tax_credit="1500",
        american_opportunity_credit="2500",
        schedule_3_line_15="1000",
        estimated_tax_penalty="250",
        
        # Direct Deposit
        routing_number="123456789",
        account_number="987654321",
        account_type="checking",
        
        # Third Party Designee
        allow_discussant=True,
        designee_name="Mike Jones",
        designee_phone="555-123-4567",
        designee_pin="12345",
        
        # Occupation Info
        your_occupation="Software Engineer",
        spouse_occupation="Teacher",
        your_pin="54321",
        spouse_pin="98765",
        phone="555-987-6543",
        email="john.smith@email.com",
        
        # Preparer Info
        preparer_name="Tom Tax",
        preparer_ptin="P12345678",
        preparer_self_employed=True,
        firm_name="Tax Prep Inc",
        firm_phone="555-555-5555",
        firm_address="456 Tax Street, Tax City, TC 12345",
        firm_ein="12-3456789"
    )