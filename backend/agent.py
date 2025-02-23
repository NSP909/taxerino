import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
import uvicorn
import sys
from dotenv import load_dotenv
from form_filler.forms import el_filler
from rag import get_relevant_info
from rcarb import get_formatted_syntax
import pyautogui

load_dotenv()


options  = {"W-9": # Part I - Taxpayer Identification
    """name: str,                      # f1_01[0] - Name of entity/individual (required)
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
    ein_second: str = ""           # f1_15[0] - Last 7 digits of EIN }""",
    "W-8BEN": 
    """"    # Personal Information
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
    field_21: str = ""             # f_21[0] - Additional field""",
    "W-4":
    """# Personal Information
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
    total_adjustments: float = 0    # f3_11[0] - Total adjustments for Step 4(b)""",
    "8863": 
    """  # Part I - Basic Taxpayer Information
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
    felony_drug_conviction: bool = False,   # c2_8[0]/[1] - Was student convicted of a felony drug offense before end of 2024?""",
    "1040":
    """
    
    
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
    dependents: json = None,     # List of dependent information

     THIS IS IMPORTANT FOR DEPENDENTS FOLLOW THIS EXAMPLE TO construct the sample json :
    dependents = [
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
        }]
    
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
    firm_ein: str = ""                    # f2_44[0] - Firm EIN""",
    "8843":
    """  # Note: IMPORTANT - ONLY ONE OF PARTS 2, 3, 4, OR 5 NEEDS TO BE FILLED OUT
    # PART 2 - FOR TEACHERS/RESEARCHERS (F1_18 through F1_29)
    # PART 3 - FOR STUDENTS (F1_30 through F1_41)
    # PART 4 - FOR PROFESSIONAL ATHLETES (F2_1 through F2_6)
    # PART 5 - FOR INDIVIDUALS WITH A MEDICAL CONDITION (F2_7 through F2_12)
    THE REST SHOULD BE of the parts should be "" or 0 or False

    # Part 1 - Personal Information (Required for all filers)
    first_name: str,              # f1_4[0] - Your first name and middle initial(s)
    last_name: str,               # f1_5[0] - Your last name (family name)
    us_tax_id: str = "",          # f1_6[0] - Your U.S. taxpayer identification number (SSN or ITIN)
    foreign_address: str = "",     # f1_7[0] - Address in country of residence (include city, province, postal code)
    us_address: str = "",         # f1_8[0] - Address in the United States (include city, state, ZIP code)
    
    # Part 1 - Visa Status Information
    current_visa: str = "",       # f1_9[0] - Current nonimmigrant visa type and date of entry (e.g., "F-1 entered 08/15/2024")
    current_status: str = "",     # f1_10[0] - Current immigration status if different from visa (e.g., "Changed to F-1 from J-1")
    citizenship_countries: str = "", # f1_11[0] - List all countries where you hold citizenship
    passport_countries: str = "",  # f1_12[0] - Countries that issued your passports
    passport_numbers: str = "",    # f1_13[0] - Passport numbers (list all if multiple)
    
    # Part 1 - Days Present in the United States
    days_2024: str = "",          # f1_14[0] - Number of days present in U.S. during 2024
    days_2023: str = "",          # f1_15[0] - Number of days present in U.S. during 2023
    days_2022: str = "",          # f1_16[0] - Number of days present in U.S. during 2022
    excluded_days: str = "",      # f1_17[0] - Number of days you claim exempt in 2024
    
    # Part 1 - Tax Year Information
    year_start: str = "",         # f1_1[0] - First day of tax year (MM/DD format, e.g., "01/01")
    year_end: str = "",           # f1_2[0] - Last day of tax year (MM/DD format, e.g., "12/31")
    alt_year: str = "",           # f1_3[0] - If applicable, enter alternative tax year

    # Part 2 - Teachers/Researchers Information (Fill only if you're a teacher/researcher)
    teacher_institution: str = "", # f1_18[0] - Name of academic institution where you taught/researched
    teacher_address: str = "",     # f1_19[0] - Complete address of the academic institution
    teacher_phone: str = "",       # f1_20[0] - Phone number of the academic institution
    teacher_director: str = "",    # f1_21[0] - Name of director of academic program
    teacher_dir_address: str = "", # f1_22[0] - Address of the director
    teacher_dir_phone: str = "",   # f1_23[0] - Phone number of the director
    
    # Part 2 - Visa History for Teachers/Researchers
    teacher_visa_2018: str = "",   # f1_24[0] - Type of visa you held during 2018 (J or Q)
    teacher_visa_2019: str = "",   # f1_25[0] - Type of visa you held during 2019 (J or Q)
    teacher_visa_2020: str = "",   # f1_26[0] - Type of visa you held during 2020 (J or Q)
    teacher_visa_2021: str = "",   # f1_27[0] - Type of visa you held during 2021 (J or Q)
    teacher_visa_2022: str = "",   # f1_28[0] - Type of visa you held during 2022 (J or Q)
    teacher_visa_2023: str = "",   # f1_29[0] - Type of visa you held during 2023 (J or Q)
    
    # Part 3 - Student Information (Fill only if you're a student)
    student_institution: str = "", # f1_30[0] - Name of academic institution you attended
    student_address: str = "",     # f1_31[0] - Complete address of the academic institution
    student_phone: str = "",       # f1_32[0] - Phone number of the academic institution
    student_director: str = "",    # f1_33[0] - Name of director of academic program
    student_dir_address: str = "", # f1_34[0] - Address of the director
    student_dir_phone: str = "",   # f1_35[0] - Phone number of the director
    
    # Part 3 - Visa History for Students
    student_visa_2018: str = "",   # f1_36[0] - Type of visa you held during 2018 (F, J, M, or Q)
    student_visa_2019: str = "",   # f1_37[0] - Type of visa you held during 2019 (F, J, M, or Q)
    student_visa_2020: str = "",   # f1_38[0] - Type of visa you held during 2020 (F, J, M, or Q)
    student_visa_2021: str = "",   # f1_39[0] - Type of visa you held during 2021 (F, J, M, or Q)
    student_visa_2022: str = "",   # f1_40[0] - Type of visa you held during 2022 (F, J, M, or Q)
    student_visa_2023: str = "",   # f1_41[0] - Type of visa you held during 2023 (F, J, M, or Q)
    
    # Yes/No Questions for Students/Teachers
    exempt_2years: bool = False,   # c1_1[0]/[1] - Have you claimed exemption for 2 years? Yes/No
    exempt_5years: bool = False,   # c1_2[0]/[1] - Have you claimed exemption for any 5 years? Yes/No
    permanent_residence: bool = False, # c1_3[0]/[1] - Are you taking steps toward permanent residence? Yes/No
    
    # Explanation if Taking Steps Toward Permanent Residence
    residence_explain_1: str = "", # f1_42[0] - Line 1 of explanation for permanent residence steps
    residence_explain_2: str = "", # f1_43[0] - Line 2 of explanation for permanent residence steps
    residence_explain_3: str = "", # f1_44[0] - Line 3 of explanation for permanent residence steps
    
    # Part 4 - Professional Athletes Information (Fill only if you're a professional athlete)
    sports_event_1: str = "",     # f2_1[0] - Name and dates of charitable sports event 1
    sports_event_2: str = "",     # f2_2[0] - Name and dates of charitable sports event 2
    sports_event_3: str = "",     # f2_3[0] - Name and dates of charitable sports event 3
    charity_org_1: str = "",      # f2_4[0] - Name and EIN of charitable organization 1
    charity_org_2: str = "",      # f2_5[0] - Name and EIN of charitable organization 2
    charity_org_3: str = "",      # f2_6[0] - Name and EIN of charitable organization 3
    
    # Part 5 - Medical Condition Information (Fill only if you had a medical condition)
    medical_desc_1: str = "",     # f2_7[0] - Line 1 of medical condition description
    medical_desc_2: str = "",     # f2_8[0] - Line 2 of medical condition description
    medical_desc_3: str = "",     # f2_9[0] - Line 3 of medical condition description
    medical_desc_4: str = "",     # f2_10[0] - Line 4 of medical condition description
    intended_leave_date: str = "", # f2_11[0] - Date you intended to leave U.S. (MM/DD/YYYY)
    actual_leave_date: str = ""    # f2_12[0] - Actual date you left U.S. (MM/DD/YYYY)"""}

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PORT = int(os.getenv('PORT', 5050))

VOICE = 'ash'
LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created',
    'error',
    'response.content.done',
    'rate_limits.updated',
    'response.done',
    'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped',
    'input_audio_buffer.speech_started',
    'session.created',

    # Transcripts
    'response.audio_transcript.done',
    'conversation.item.input_audio_transcription.completed',
]
SHOW_TIMING_MATH = False

conv_history=[]
app = FastAPI()

if not OPENAI_API_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response to connect to Media Stream."""
    response = VoiceResponse()
    response.say("Please wait")
    response.pause(length=1)
    response.say("O.K. you can start talking!")
    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")

@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections between Twilio and OpenAI."""
    print("Client connected")
    await websocket.accept()

    async with websockets.connect(
        'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17',
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as openai_ws:
        await initialize_session(openai_ws)

        # Connection specific state
        stream_sid = None
        latest_media_timestamp = 0
        last_assistant_item = None
        mark_queue = []
        response_start_timestamp_twilio = None
        
        async def receive_from_twilio():
            """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
            nonlocal stream_sid, latest_media_timestamp
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)
                    if data['event'] == 'media' and openai_ws.open:
                        latest_media_timestamp = int(data['media']['timestamp'])
                        audio_append = {
                            "type": "input_audio_buffer.append",
                            "audio": data['media']['payload']
                        }
                        await openai_ws.send(json.dumps(audio_append))
                    elif data['event'] == 'start':
                        stream_sid = data['start']['streamSid']
                        print(f"Incoming stream has started {stream_sid}")
                        response_start_timestamp_twilio = None
                        latest_media_timestamp = 0
                        last_assistant_item = None
                    elif data['event'] == 'mark':
                        if mark_queue:
                            mark_queue.pop(0)
                    elif data['event'] == 'stop':
                        print("Stream ended.")
                        with open('output.txt', 'w') as file:
                            file.write(str(conv_history))
                        # extract_and_update()
                        sys.exit(0)
                        break
            except WebSocketDisconnect:
                print("Client disconnected.")
                
                if openai_ws.open:
                    await openai_ws.close()

        async def send_to_twilio():
            """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
            nonlocal stream_sid, last_assistant_item, response_start_timestamp_twilio
            try:
                async for openai_message in openai_ws:
                    response = json.loads(openai_message)
                    if response['type'] in LOG_EVENT_TYPES:
                        print(f"Received event: {response['type']}", response)
                        if (response.get('type') == 'response.done' and 
                            response.get("response", {}).get("output") and  # Check if output exists and is not empty
                            len(response["response"]["output"]) > 0 and     # Check if output has at least one element
                            response["response"]["output"][0].get("type") == "function_call"):
                            # if  response["response"]["output"][0]["name"]=="plan_meeting"\
                            #     and "arguments" in response["response"]["output"][0]:
                            #     arguments = json.loads(response["response"]["output"][0]["arguments"])
                            #     print(arguments)
                            #     email="nspd@umd.edu"
                            #     date=arguments["date"]
                            #     time=arguments["time"]
                            #     duration=arguments["duration"]
                            #     subject=arguments["subject"]
                            #     plan_meeting(email, date, time, duration, subject)
                            #     print("added meeting SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                            if response["response"]["output"][0]["name"]=="get_relevant_information"\
                                and "arguments" in response["response"]["output"][0]:
                                arguments = json.loads(response["response"]["output"][0]["arguments"])
                                print(arguments)
                                topic=arguments["topic"]
                                context = get_relevant_info(topic)
                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"Use this information to answer the user's query: {context} "
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item))
                                print("added info SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                            if response["response"]["output"][0]["name"]=="get_form_syntax" \
                                and "arguments" in response["response"]["output"][0]:
                                arguments = json.loads(response["response"]["output"][0]["arguments"])
                                print(arguments)
                                form=arguments["form"]
                                with open("info.json", "r") as f:
                                    info = json.load(f)
                                info=str(info)
                                if form in options:
                                    syntax = options[form]
                                final_syntax= get_formatted_syntax(syntax, info)
                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"""Here is the updated syntax with info filled in:
                                                        {final_syntax}
                                                        """
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item)) 
                                await openai_ws.send(json.dumps({"type": "response.create"}))
                                print("added syntax SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS") 
                            if response["response"]["output"][0]["name"]=="fill_form" \
                                and "arguments" in response["response"]["output"][0]:
                                arguments = json.loads(response["response"]["output"][0]["arguments"])
                                print(arguments)
                                form=arguments["form"]
                                data=arguments["data"]
                                dikt= json.loads(data)
                                output = el_filler(form, dikt)

                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"""Status of form : {output}"""
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item)) 
                                await openai_ws.send(json.dumps({"type": "response.create"}))
                                print("filled form SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")  
                        if (response.get('type') == 'response.done' and 
                            response.get("response", {}).get("output") and  # Check if output exists and is not empty
                            len(response["response"]["output"]) > 1 and     # Check if output has at least one element
                            response["response"]["output"][1].get("type") == "function_call"):
                            if response["response"]["output"][1]["name"]=="get_relevant_information" \
                                and "arguments" in response["response"]["output"][1]:
                                arguments = json.loads(response["response"]["output"][1]["arguments"])
                                print(arguments)
                                topic=arguments["topic"]
                                context = get_relevant_info(topic)
                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"Use this information to answer the user's query: {context} "
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item)) 
                                await openai_ws.send(json.dumps({"type": "response.create"}))
                                print("added info SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS") 
                        if (response.get('type') == 'response.done' and 
                            response.get("response", {}).get("output") and  # Check if output exists and is not empty
                            len(response["response"]["output"]) > 1 and     # Check if output has at least one element
                            response["response"]["output"][1].get("type") == "function_call"):
                            if response["response"]["output"][1]["name"]=="get_form_syntax" \
                                and "arguments" in response["response"]["output"][1]:
                                arguments = json.loads(response["response"]["output"][1]["arguments"])
                                print(arguments)
                                form=arguments["form"]
                                with open("info.json", "r") as f:
                                    info = json.load(f)
                                info=str(info)
                                if form in options:
                                    syntax = options[form]
                                final_syntax= get_formatted_syntax(syntax, info)
                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"""Here is the updated syntax with info filled in:
                                                        {final_syntax}
                                                        """
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item)) 
                                await openai_ws.send(json.dumps({"type": "response.create"}))
                                print("added syntax SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS") 
                        if (response.get('type') == 'response.done' and 
                            response.get("response", {}).get("output") and  # Check if output exists and is not empty
                            len(response["response"]["output"]) > 1 and     # Check if output has at least one element
                            response["response"]["output"][1].get("type") == "function_call"):
                            if response["response"]["output"][1]["name"]=="fill_form" \
                                and "arguments" in response["response"]["output"][1]:
                                arguments = json.loads(response["response"]["output"][1]["arguments"])
                                print(arguments)
                                form=arguments["form"]
                                data=arguments["data"]
                                dikt= json.loads(data)
                                output = el_filler(form, dikt)
                                conversation_item = {
                                        "type": "conversation.item.create",
                                        "item": {
                                        "type": "message",
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "input_text",
                                                "text": f"""Status of form : {output}"""
                                            }
                                        ]
                                    }
                                }
                                await openai_ws.send(json.dumps(conversation_item)) 
                                await openai_ws.send(json.dumps({"type": "response.create"}))
                                print("filled form SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")  
                        elif response['type']=='conversation.item.input_audio_transcription.completed':
                            conv_history.append(response)   
                        elif response["type"]=='response.audio_transcript.done ':
                            conv_history.append(response)

                    if response.get('type') == 'response.audio.delta' and 'delta' in response:
                        audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                        audio_delta = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {
                                "payload": audio_payload
                            }
                        }
                        await websocket.send_json(audio_delta)

                        if response_start_timestamp_twilio is None:
                            response_start_timestamp_twilio = latest_media_timestamp
                            if SHOW_TIMING_MATH:
                                print(f"Setting start timestamp for new response: {response_start_timestamp_twilio}ms")

                        # Update last_assistant_item safely
                        if response.get('item_id'):
                            last_assistant_item = response['item_id']

                        await send_mark(websocket, stream_sid)
                   
                    # Trigger an interruption. Your use case might work better using `input_audio_buffer.speech_stopped`, or combining the two.
                    if response.get('type') == 'input_audio_buffer.speech_started':
                        print("Speech started detected.")
                        if last_assistant_item:
                            print(f"Interrupting response with id: {last_assistant_item}")
                            await handle_speech_started_event()
            except Exception as e:
                print(f"Error in send_to_twilio: {e}")

        async def handle_speech_started_event():
            """Handle interruption when the caller's speech starts."""
            nonlocal response_start_timestamp_twilio, last_assistant_item
            print("Handling speech started event.")
            if mark_queue and response_start_timestamp_twilio is not None:
                elapsed_time = latest_media_timestamp - response_start_timestamp_twilio
                if SHOW_TIMING_MATH:
                    print(f"Calculating elapsed time for truncation: {latest_media_timestamp} - {response_start_timestamp_twilio} = {elapsed_time}ms")

                if last_assistant_item:
                    if SHOW_TIMING_MATH:
                        print(f"Truncating item with ID: {last_assistant_item}, Truncated at: {elapsed_time}ms")

                    truncate_event = {
                        "type": "conversation.item.truncate",
                        "item_id": last_assistant_item,
                        "content_index": 0,
                        "audio_end_ms": elapsed_time
                    }
                    await openai_ws.send(json.dumps(truncate_event))

                await websocket.send_json({
                    "event": "clear",
                    "streamSid": stream_sid
                })

                mark_queue.clear()
                last_assistant_item = None
                response_start_timestamp_twilio = None

        async def send_mark(connection, stream_sid):
            if stream_sid:
                mark_event = {
                    "event": "mark",
                    "streamSid": stream_sid,
                    "mark": {"name": "responsePart"}
                }
                await connection.send_json(mark_event)
                mark_queue.append('responsePart')

        await asyncio.gather(receive_from_twilio(), send_to_twilio())

async def send_initial_conversation_item(openai_ws):
    """Send initial conversation item if AI talks first."""
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Greet the user in an energetic tone nd ask how you can help them today."
                }
            ]
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))


async def initialize_session(openai_ws):
    """Control initial session with OpenAI."""
    with open("info.json", "r") as f:
        info = json.load(f)
    info=str(info)
    
    SYSTEM_MESSAGE = (
       f"""You are TaxDaddy - the tax expert.
           Your job is to help users fill out their tax forms and assist with their tax-related queries.
           This is the data that we have on file about the user.
           {info} 
           MAKE SURE YOU UNDERSTAND THAT YOU HAVE THIS INFORMATION AND USE IT ACCORDINGLY

           If the user has any kind of specific question then use the function get_relevant_information to get the information from the database before answering the question.

           You also help out in filling forms. We have 5 forms available right now
              1. W-9 -  This form is used by independent contractors, freelancers, and self-employed individuals who are U.S. citizens or resident aliens.
              2. W-8BEN - This form is used by non-resident aliens who earn income in the U.S. This form is specifically for foreign individuals who: Are not U.S. citizens or resident aliens, Receive income from U.S. sources (like investments or contract work), Need to claim tax treaty benefits, Are working with U.S. companies or receiving payments from U.S. sources
              3. W-4 - This form is filled out by employees who are U.S. citizens or resident aliens when starting a new job. It tells your employer how much tax to withhold from your paycheck 
              4. 1040 - Form 1040 is the main tax return that you must file annually if you're a U.S. citizen, permanent resident, or resident alien reporting your income, claiming deductions and credits, and calculating your tax liability or refund. You need to submit this by April 15th each year.
              5. 8863 - Form 8863 should be filed along with your Form 1040 if you, your spouse, or your dependents paid qualified educational expenses at an eligible institution and want to claim education credits like the American Opportunity Credit or the Lifetime Learning Credit.
              6. 8843 - Form 8843 needs to be filed if you're an international student, teacher, researcher on F, J, M, or Q visas, or someone with a medical condition that prevented you from leaving the U.S. Submit this by April 15th if you're also filing a tax return, or by June 15th if you don't need to file a return. You can file Form 8843 by itself if you had no U.S. income to report.

           Once the user gives you enough information call the get_form_syntax function and you shall recieve the exact fields that you will need to fill out the application.
           THe get_form_syntax function will return the syntax of the form with some data already filled in based on the user's info on file. 
           You need to figure out the rest of the fields that requires info by talking to the user
           Once you have the syntax maintain normal converstion and gather all the data required. Ask information one by one like a normal human
           Once you have all the data required call the fill_form function with the correct forn and the data you have gathered.
           If the user instructs you to fill out the form with the existing information then mark all other fields as zero or empty  and fill out the form with the existing information.
           
           I will also provide you infomation about the user, fill out as much as info as you can by using this information

           MAKE SURE TO USE THE FUNCTIONS WHENEVER REQUIRED
           
           Be Pleasant and witty!!

            """
            )
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
            "input_audio_transcription": {
            "model": "whisper-1",
            },
            "tools":[
                {"type": "function",
                    "name": "get_relevant_information",
                    "description": """Get any kind of tax information from the database.
                    Use this whenever the user asks any specific/non-generic question.
                    Always let the user know that you are getting information so they can wait

                     """,
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The topic you want to know more about"
                        }
                    },
                    "required": [ "topic"]            
                    }
                },{"type": "function",
                    "name": "get_form_syntax",
                    "description": """Get the fields required to fill out a particular form.
                    Use this when you have decided which form you need to fil out and need a list of fields to fill out
                    The form will already be filled out with the data you have so far
                    You need to look out for the fields that require more info and ask the user questions based on that
                    Currently we can fill out these forms W-9, W-8BEN, W-4, 1040, 8863, 8843
                     """,
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "form": {
                            "type": "string",
                            "description": "The name of the form to be filled out (W-9, W-8BEN, W-4). Make sure it is all caps and exactly in the format given"
                        }
                    },
                    "required": [ "form"]            
                    }
                }, {"type": "function",
                    "name": "fill_form",
                    "description": """Fill out the form with the data provided.
                    Use this when you have all the data required to fill out the form
                    Currently we can fill out these forms W-9, W-8BEN, W-4
                     """,
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "form": {
                            "type": "string",
                            "description": "The name of the form to be filled out (W-9, W-8BEN, W-4). Make sure it is all caps and exactly in the format given"
                        },
                        "data": {
                            "type": "string",
                            "description": """The data required to fill out the form. Make sure it is in json according to the fields format as it immediately goes to the form filler.
                             Empty String fields should be ""  and empty booleans should be false and empty numbers should be 0
                             Make sure it is a json in string format"""
                        }
                    },
                    "required": [ "form", "data"]            
                    }
                },
             
                
            ]
            
        }
    }
    conv_history=[]
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))
    # Uncomment the next line to have the AI speak first
    await send_initial_conversation_item(openai_ws)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)