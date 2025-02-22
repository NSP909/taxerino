from PyPDFForm import PdfWrapper
from typing import List, Optional, Dict, Union
from datetime import date
from dataclasses import dataclass

@dataclass
class Dependent:
    name: str
    identifying_number: str
    relationship: str
    child_tax_credit: bool = False
    other_dependent_credit: bool = False

def fill_1040nr_form(
    # Personal Information
    first_name: str,                    # f1_4[0]
    last_name: str,                     # f1_5[0]
    identifying_number: str,            # f1_6[0]
    address: str,                       # f1_7[0]
    apt_no: Optional[str] = None,       # f1_8[0]
    city: str = None,                   # f1_9[0]
    state: str = None,                  # f1_10[0]
    zip_code: str = None,               # f1_11[0]
    foreign_country: Optional[str] = None,     # f1_12[0]
    foreign_province: Optional[str] = None,    # f1_13[0]
    foreign_postal: Optional[str] = None,      # f1_14[0]

    # Tax Year Information
    tax_year_start: Optional[str] = None,      # f1_1[0]
    tax_year_end: Optional[str] = None,        # f1_2[0]
    tax_year: str = "2024",                    # f1_3[0]

    # Filing Status (choose one)
    is_single: bool = False,                   # c1_1[0]
    is_married_filing_separately: bool = False, # c1_1[1]
    is_qualifying_surviving_spouse: bool = False, # c1_1[2]
    is_estate: bool = False,                   # c1_1[3]
    is_trust: bool = False,                    # c1_1[4]

    # QSS Information
    qss_child_name: Optional[str] = None,      # f1_15[0]

    # Income Information
    w2_income: float = 0,                      # f1_28[0]
    household_employee_wages: float = 0,        # f1_29[0]
    tip_income: float = 0,                     # f1_30[0]
    medicaid_waiver: float = 0,                # f1_31[0]
    dependent_care_benefits: float = 0,         # f1_32[0]
    adoption_benefits: float = 0,               # f1_33[0]
    form_8919_wages: float = 0,                # f1_34[0]
    other_earned_income: float = 0,            # f1_35[0]
    treaty_exempt_income: float = 0,           # f1_38[0]
    total_income: float = 0,                   # f1_39[0]

    # Investment Income
    tax_exempt_interest: float = 0,            # f1_40[0]
    taxable_interest: float = 0,               # f1_41[0]
    qualified_dividends: float = 0,            # f1_42[0]
    ordinary_dividends: float = 0,             # f1_43[0]

    # Retirement Income
    ira_distributions: float = 0,              # f1_44[0]
    taxable_ira: float = 0,                    # f1_45[0]
    pensions_annuities: float = 0,             # f1_46[0]
    taxable_pensions: float = 0,               # f1_47[0]

    # Additional Income
    capital_gain_loss: float = 0,              # f1_49[0]
    additional_schedule1_income: float = 0,     # f1_50[0]
    total_effective_income: float = 0,          # f1_51[0]
    income_adjustments: float = 0,              # f1_52[0]
    adjusted_gross_income: float = 0,           # f1_53[0]
    itemized_deductions: float = 0,             # f1_54[0]
    qbi_deduction: float = 0,                   # f1_55[0]
    estate_trust_exemption: float = 0,          # f1_56[0]
    total_deductions_exemptions: float = 0,     # f1_57[0]
    total_deductions: float = 0,                # f1_58[0]
    taxable_income: float = 0,                  # f1_59[0]

    # Tax Forms and Amounts
    form_8814_tax: float = 0,                  # f2_1[0]
    form_8814_amount: float = 0,               # f2_2[0]
    form_4972_tax: float = 0,                  # other tax forms amount combined
    line_23d_total: float = 0,                 # f2_12[0] - Sum of lines 23a through 23c
    schedule2_amount: float = 0,                # f2_3[0]
    combined_tax: float = 0,                    # f2_4[0]
    child_tax_credit: float = 0,                # f2_5[0]
    schedule3_amount: float = 0,                # f2_6[0]
    total_credits: float = 0,                   # f2_7[0]
    tax_minus_credits: float = 0,               # f2_8[0]
    other_taxes: float = 0,                     # f2_10[0]
    transportation_tax: float = 0,              # f2_11[0]
    total_tax: float = 0,                       # f2_13[0]

    # Payments and Refund
    w2_withholding: float = 0,                  # f2_14[0]
    form1099_withholding: float = 0,            # f2_15[0]
    other_withholding: float = 0,               # f2_16[0]
    form8805_withholding: float = 0,            # f2_18[0]
    form8288a_withholding: float = 0,           # f2_19[0]
    form1042s_withholding: float = 0,           # f2_20[0]
    estimated_tax_payments: float = 0,           # f2_21[0]
    additional_child_tax_credit: float = 0,      # f2_23[0]
    form1040c_credit: float = 0,                # f2_24[0]
    schedule3_credits: float = 0,               # f2_26[0]
    total_payments: float = 0,                  # f2_28[0]
    overpaid_amount: float = 0,                 # f2_29[0]
    refund_amount: float = 0,                   # f2_30[0]
    applied_to_2025: float = 0,                 # f2_34[0]
    amount_owed: float = 0,                     # f2_35[0]
    estimated_tax_penalty: float = 0,           # f2_36[0]

    # Schedule D and Other Forms
    schedule_d_not_required: bool = False,      # c1_13[0]
    form_8814_attached: bool = False,           # c2_1[0]
    form_4972_attached: bool = False,           # c2_2[0]
    other_form_attached: bool = False,          # c2_3[0]
    form_8888_attached: bool = False,           # c2_4[0]

    # Digital Assets
    had_digital_assets: Optional[bool] = None,  # c1_3[0] for Yes, c1_3[1] for No

    # Dependent Information
    dependents: List[Dependent] = None,
    more_than_4_dependents: bool = False,       # c1_4[0]

    # Banking Information
    routing_number: Optional[str] = None,       # f2_31[0]
    account_number: Optional[str] = None,       # f2_32[0]
    is_checking: bool = True,                   # c2_5[0]
    foreign_address_refund: Optional[str] = None, # f2_33[0]

    # Third Party Designee
    allow_designee: bool = False,               # c2_6[0]
    designee_name: Optional[str] = None,        # f2_37[0]
    designee_phone: Optional[str] = None,       # f2_38[0]
    designee_pin: Optional[str] = None,         # f2_39[0]

    # Signer Information
    occupation: Optional[str] = None,           # f2_40[0]
    identity_pin: Optional[str] = None,         # f2_41[0]
    phone_number: Optional[str] = None,         # f2_42[0]
    email: Optional[str] = None,                # f2_43[0]

    # Preparer Information
    self_employed_preparer: bool = False,       # c2_7[0]
    preparer_name: Optional[str] = None,        # f2_44[0]
    preparer_ptin: Optional[str] = None,        # f2_45[0]
    preparer_firm_name: Optional[str] = None,   # f2_46[0]
    preparer_firm_address: Optional[str] = None, # f2_47[0]
    preparer_phone: Optional[str] = None,       # f2_48[0]
    preparer_firm_ein: Optional[str] = None     # f2_49[0]
) -> None:
    """Fill out IRS Form 1040NR with provided information."""
    
    form_data = {
        # Personal Information
        'f1_4[0]': first_name,
        'f1_5[0]': last_name,
        'f1_6[0]': identifying_number,
        'f1_7[0]': address,
        'f1_8[0]': apt_no or '',
        'f1_9[0]': city or '',
        'f1_10[0]': state or '',
        'f1_11[0]': zip_code or '',
        'f1_12[0]': foreign_country or '',
        'f1_13[0]': foreign_province or '',
        'f1_14[0]': foreign_postal or '',

        # Tax Year Information
        'f1_1[0]': tax_year_start or '',
        'f1_2[0]': tax_year_end or '',
        'f1_3[0]': tax_year,

        # Filing Status
        'c1_1[0]': is_single,
        'c1_1[1]': is_married_filing_separately,
        'c1_1[2]': is_qualifying_surviving_spouse,
        'c1_1[3]': is_estate,
        'c1_1[4]': is_trust,
        'f1_15[0]': qss_child_name or '',

        # Digital Assets
        'c1_3[0]': had_digital_assets if had_digital_assets is not None else False,
        'c1_3[1]': not had_digital_assets if had_digital_assets is not None else False,

        # Income Fields
        'f1_28[0]': str(w2_income),
        'f1_29[0]': str(household_employee_wages),
        'f1_30[0]': str(tip_income),
        'f1_31[0]': str(medicaid_waiver),
        'f1_32[0]': str(dependent_care_benefits),
        'f1_33[0]': str(adoption_benefits),
        'f1_34[0]': str(form_8919_wages),
        'f1_35[0]': str(other_earned_income),
        'f1_38[0]': str(treaty_exempt_income),
        'f1_39[0]': str(total_income),

        # Investment Income
        'f1_40[0]': str(tax_exempt_interest),
        'f1_41[0]': str(taxable_interest),
        'f1_42[0]': str(qualified_dividends),
        'f1_43[0]': str(ordinary_dividends),

        # Retirement Income
        'f1_44[0]': str(ira_distributions),
        'f1_45[0]': str(taxable_ira),
        'f1_46[0]': str(pensions_annuities),
        'f1_47[0]': str(taxable_pensions),

        # Additional Income and Deductions
        'f1_49[0]': str(capital_gain_loss),
        'f1_50[0]': str(additional_schedule1_income),
        'f1_51[0]': str(total_effective_income),
        'f1_52[0]': str(income_adjustments),
        'f1_53[0]': str(adjusted_gross_income),
        'f1_54[0]': str(itemized_deductions),
        'f1_55[0]': str(qbi_deduction),
        'f1_56[0]': str(estate_trust_exemption),
        'f1_57[0]': str(total_deductions_exemptions),
        'f1_58[0]': str(total_deductions),
        'f1_59[0]': str(taxable_income),

        # Tax Forms and Amounts
        'f2_1[0]': str(form_8814_tax),         # Form 8814 tax
        'f2_2[0]': str(form_8814_amount),      # Form 8814 amount
        'f2_12[0]': str(line_23d_total),       # Total of lines 23a through 23c
        'f2_3[0]': str(schedule2_amount),
        'f2_4[0]': str(combined_tax),
        'f2_5[0]': str(child_tax_credit),
        'f2_6[0]': str(schedule3_amount),
        'f2_7[0]': str(total_credits),
        'f2_8[0]': str(tax_minus_credits),
        'f2_10[0]': str(other_taxes),
        'f2_11[0]': str(transportation_tax),
        'f2_13[0]': str(total_tax),

        # Payments and Withholding
        'f2_14[0]': str(w2_withholding),
        'f2_15[0]': str(form1099_withholding),
        'f2_16[0]': str(other_withholding),
        'f2_18[0]': str(form8805_withholding),
        'f2_19[0]': str(form8288a_withholding),
        'f2_20[0]': str(form1042s_withholding),
        'f2_21[0]': str(estimated_tax_payments),
        'f2_23[0]': str(additional_child_tax_credit),
        'f2_24[0]': str(form1040c_credit),
        'f2_26[0]': str(schedule3_credits),
        'f2_28[0]': str(total_payments),
        'f2_29[0]': str(overpaid_amount),
        'f2_30[0]': str(refund_amount),
        'f2_34[0]': str(applied_to_2025),
        'f2_35[0]': str(amount_owed),
        'f2_36[0]': str(estimated_tax_penalty),

        # Forms and Schedules
        'c1_13[0]': schedule_d_not_required,
        'c2_1[0]': form_8814_attached,
        'c2_2[0]': form_4972_attached,
        'c2_3[0]': other_form_attached,
        'c2_4[0]': form_8888_attached,

        # Banking Information
        'f2_31[0]': routing_number or '',
        'f2_32[0]': account_number or '',
        'c2_5[0]': is_checking,
        'c2_5[1]': not is_checking,
        'f2_33[0]': foreign_address_refund or '',

        # Third Party Designee
        'c2_6[0]': allow_designee,
        'c2_6[1]': not allow_designee,
        'f2_37[0]': designee_name or '',
        'f2_38[0]': designee_phone or '',
        'f2_39[0]': designee_pin or '',

        # Signer Information
        'f2_40[0]': occupation or '',
        'f2_41[0]': identity_pin or '',
        'f2_42[0]': phone_number or '',
        'f2_43[0]': email or '',

        # Preparer Information
        'c2_7[0]': self_employed_preparer,
        'f2_44[0]': preparer_name or '',
        'f2_45[0]': preparer_ptin or '',
        'f2_46[0]': preparer_firm_name or '',
        'f2_47[0]': preparer_firm_address or '',
        'f2_48[0]': preparer_phone or '',
        'f2_49[0]': preparer_firm_ein or '',
        
        # More than 4 dependents checkbox
        'c1_4[0]': more_than_4_dependents,
    }

    # Handle dependents (up to 4) with tax credits
    if dependents:
        for i, dep in enumerate(dependents[:4], 1):
            base_idx = 16 + (i-1)*3
            credit_idx = 5 + (i-1)*2
            
            # Dependent basic information
            form_data[f'f1_{base_idx}[0]'] = dep.name
            form_data[f'f1_{base_idx + 1}[0]'] = dep.identifying_number
            form_data[f'f1_{base_idx + 2}[0]'] = dep.relationship
            
            # Dependent tax credits
            form_data[f'c1_{credit_idx}[0]'] = dep.child_tax_credit
            form_data[f'c1_{credit_idx + 1}[0]'] = dep.other_dependent_credit

    # Fill and save the form
    filled_form = PdfWrapper("f1040nr.pdf").fill(form_data)
    
    output_filename = f"filled_1040nr.pdf"
    
    with open(output_filename, "wb+") as output:
        output.write(filled_form.read())
    
    print(f"Form saved as: {output_filename}")

# Comprehensive test case
if __name__ == "__main__":
    # Create test dependents
    test_dependents = [
        Dependent(
            name="Sarah Smith",
            identifying_number="987-65-4321",
            relationship="Daughter",
            child_tax_credit=True,
            other_dependent_credit=False
        ),
        Dependent(
            name="Michael Smith",
            identifying_number="987-65-4322",
            relationship="Son",
            child_tax_credit=True,
            other_dependent_credit=False
        ),
        Dependent(
            name="Emma Smith",
            identifying_number="987-65-4323",
            relationship="Daughter",
            child_tax_credit=False,
            other_dependent_credit=True
        ),
        Dependent(
            name="James Smith",
            identifying_number="987-65-4324",
            relationship="Son",
            child_tax_credit=False,
            other_dependent_credit=True
        ),
        Dependent(
            name="Additional Dependent",
            identifying_number="987-65-4325",
            relationship="Child",
            child_tax_credit=True,
            other_dependent_credit=False
        )
    ]

    # Test with all fields populated
    fill_1040nr_form(
        # Personal Information
        first_name="John Michael",
        last_name="Smith",
        identifying_number="123-45-6789",
        address="123 Main Street",
        apt_no="4B",
        city="New York",
        state="NY",
        zip_code="10001",
        foreign_country="Canada",
        foreign_province="Ontario",
        foreign_postal="M5V 2L7",

        # Tax Year Information
        tax_year_start="02-01",
        tax_year_end="12-31",
        tax_year="2024",

        # Filing Status
        is_single=True,
        
        # Income Information
        w2_income=85000.00,
        household_employee_wages=1200.00,
        tip_income=2500.00,
        medicaid_waiver=0.00,
        dependent_care_benefits=1200.00,
        adoption_benefits=0.00,
        form_8919_wages=0.00,
        other_earned_income=1500.00,
        treaty_exempt_income=0.00,
        total_income=91400.00,

        # Investment Income
        tax_exempt_interest=500.00,
        taxable_interest=2000.00,
        qualified_dividends=3000.00,
        ordinary_dividends=4000.00,

        # Retirement Income
        ira_distributions=10000.00,
        taxable_ira=8000.00,
        pensions_annuities=15000.00,
        taxable_pensions=12000.00,

        # Additional Income and Deductions
        capital_gain_loss=5000.00,
        additional_schedule1_income=1000.00,
        total_effective_income=136900.00,
        income_adjustments=5000.00,
        adjusted_gross_income=131900.00,
        itemized_deductions=24000.00,
        qbi_deduction=5000.00,

        # Digital Assets
        had_digital_assets=True,

        # Dependent Information
        dependents=test_dependents,
        more_than_4_dependents=True,

        # Banking Information
        routing_number="123456789",
        account_number="987654321",
        is_checking=True,
        foreign_address_refund="456 Queen Street West, Toronto, ON M5V 2B4",

        # Forms and Schedules
        schedule_d_not_required=True,
        form_8888_attached=True,

        # Third Party Designee
        allow_designee=True,
        designee_name="Jane Wilson",
        designee_phone="(555) 555-1234",
        designee_pin="12345",

        # Signer Information
        occupation="Software Engineer",
        identity_pin="876543",
        phone_number="(555) 555-5678",
        email="john.smith@email.com",

        # Tax Forms and Special Calculations
        form_8814_tax=1500.00,
        form_8814_amount=2000.00,
        form_4972_tax=500.00,
        line_23d_total=4000.00,  # Sum of tax form amounts
        
        # Tax and Credits
        w2_withholding=17000.00,
        form1099_withholding=500.00,
        other_withholding=200.00,
        estimated_tax_payments=4000.00,
        additional_child_tax_credit=2000.00,
        total_payments=23700.00,
        overpaid_amount=1200.00,
        refund_amount=1000.00,
        applied_to_2025=200.00,

        # Preparer Information
        self_employed_preparer=True,
        preparer_name="Jane Wilson",
        preparer_ptin="P12345678",
        preparer_firm_name="Wilson Tax Services",
        preparer_firm_address="789 Professional Plaza, Suite 300, New York, NY 10002",
        preparer_phone="(212) 555-0123",
        preparer_firm_ein="12-3456789"
    )