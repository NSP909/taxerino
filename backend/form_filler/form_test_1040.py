from PyPDFForm import PdfWrapper

def fill_form():
    # Use the exact sample data
    form_data = {
        'c1_10[0]': True, # You - Age/Blindness - Are blind
        'c1_11[0]': True, # Spouse - Was born before January 2, 1960
        'c1_12[0]': True, # Spouse - Is blind
        'c1_13[0]': True, # If more than four dependents, see instructions and check here
        'c1_14[0]': True, # Check the box if qualifies Child tax credit (member 1)
        'c1_15[0]': True, # Check the box if qualifies Credit for other dependents (member 1)
        'c1_16[0]': True, # Check the box if qualifies Child tax credit (member 2)
        'c1_17[0]': True, # Check the box if qualifies Credit for other dependents (member 2)
        'c1_18[0]': True, # Check the box if qualifies Child tax credit (member 3)
        'c1_19[0]': True, # Check the box if qualifies Credit for other dependents (member 3)
        'c1_1[0]': True, # Presidential Election Campaign Check here if you, or your spouse if filing jointly, want $3 to go to this fund. Checking a box below will not change your tax or refund. (YOU)
        'c1_20[0]': True, # Check the box if qualifies Child tax credit (member 4)
        'c1_21[0]': True, # Check the box if qualifies Credit for other dependents (member 4)
        'c1_22[0]': True, # If you elect to use the lump-sum election method, check here 
        'c1_23[0]': True, # Capital gain or (loss). Attach Schedule D if required. If not required, check here
        'c1_2[0]': True, # Presidential Election Campaign Check here if you, or your spouse if filing jointly, want $3 to go to this fund. Checking a box below will not change your tax or refund. (SPOUSE)
        'c1_3[0]': True, # Filing Status - Single or Head of Household - Check here if you are filing as a single or head of household
        'c1_3[1]': True, # Filing - Married filing jointly (even if only one had income)
        'c1_3[2]': True, # Filing - Married filing separately
        'c1_4[0]': True, # Filing - If treating a nonresident alien or dual-status alien spouse as a U.S. resident for the entire tax year, check the box
        'c1_5[0]': True, # At any time during 2024, did you: (a) receive (as a reward, award, or payment for property or services); or (b) sell, exchange, or otherwise dispose of a digital asset (or a financial interest in a digital asset)? (YES)
        'c1_5[1]': True, # At any time during 2024, did you: (a) receive (as a reward, award, or payment for property or services); or (b) sell, exchange, or otherwise dispose of a digital asset (or a financial interest in a digital asset)? (NO)
        'c1_6[0]': True, # Standard Deduction - You as a dependent
        'c1_7[0]': True, # Standard Deduction - Your spouse as a dependent
        'c1_8[0]': True, # Standard Deduction - Spouse itemizes on a separate return or you were a dual-status alien
        'c1_9[0]': True, # Age/Blindness - You: Were born before January 2, 1960
        'c2_1[0]': True, # Tax and Credits - Check if any from Form(s) - 8814
        'c2_2[0]': True, # Tax and Credits - Check if any from Form(s) - 4972
        'c2_3[0]': True, # Tax and Credits - Check if any from Form(s) - f2_01[0]
        'c2_4[0]': True, # If Form 8888 is attached, check here
        'c2_5[0]': True, # Direct Deposit - Type - Checkings
        'c2_5[1]': True, # Direct Deposit - Type - Savings
        'c2_6[0]': True, # Do you want to allow another person to discuss this return with the IRS? - YES
        'c2_6[1]': True, # Do you want to allow another person to discuss this return with the IRS? - NO
        'c2_7[0]': False, # Paid Preparer Use Only Check if self employed
        'f1_01[0]': 'f1_01[0]', # year beginning
        'f1_02[0]': 'f1_02[0]', # ending
        'f1_03[0]': 'f1', # 20 year
        'f1_04[0]': 'f1_04[0]', # first name and middle initial
        'f1_05[0]': 'f1_05[0]', # Last name
        'f1_06[0]': 'f1_06[0]', # social security number
        'f1_07[0]': 'f1_07[0]', # If joint return, spouse’s first name and middle initial 
        'f1_08[0]': 'f1_08[0]', # If joint return, spouse’s Last name
        'f1_09[0]': 'f1_09[0]', # Spouse’s social security number
        'f1_10[0]': 'f1_10[0]', # Home address
        'f1_11[0]': 'f1_11[0]', # Apt. no.
        'f1_12[0]': 'f1_12[0]', # City, town
        'f1_13[0]': 'f1_13[0]', # State
        'f1_14[0]': 'f1_14[0]', # ZIP code
        'f1_15[0]': 'f1_15[0]', # Foreign country name
        'f1_16[0]': 'f1_16[0]', # Foreign province/state/county
        'f1_17[0]': 'f1_17[0]', # Foreign postal code
        'f1_18[0]': 'f1_18[0]', # If you checked the MFS box, enter the name of your spouse. If you checked the HOH or QSS box, enter the child’s name if the qualifying person is a child but not your dependent
        'f1_19[0]': 'f1_19[0]', # If treating a nonresident alien or dual-status alien spouse as a U.S. resident for the entire tax year, check the box and enter their name
        'f1_20[0]': 'f1_20[0]', # Dependents(First Name and Last Name)
        'f1_21[0]': 'f1_21[0]', # Dependents(Social Security Number)
        'f1_22[0]': 'f1_22[0]', # Dependents(Relationship to you)
        'f1_23[0]': 'f1_23[0]', # Dependents(First Name and Last Name)
        'f1_24[0]': 'f1_24[0]', # Dependents(Social Security Number)
        'f1_25[0]': 'f1_25[0]', # Dependents(Relationship to you)
        'f1_26[0]': 'f1_26[0]', # Dependents(First Name and Last Name)
        'f1_27[0]': 'f1_27[0]', # Dependents(Social Security Number)
        'f1_28[0]': 'f1_28[0]', # Dependents(Relationship to you)
        'f1_29[0]': 'f1_29[0]', # Dependents(First Name and Last Name)
        'f1_30[0]': 'f1_30[0]', # Dependents(Social Security Number)
        'f1_31[0]': 'f1_31[0]', # Dependents(Relationship to you)
        'f1_32[0]': 'f1_32[0]', # Income - Total amount from Form(s) W-2, box 1
        'f1_33[0]': 'f1_33[0]', # Income - Household employee wages not reported on Form(s) W-2
        'f1_34[0]': 'f1_34[0]', # Income - Tip income not reported on line 1a(f1_32[0])
        'f1_35[0]': 'f1_35[0]', # Income - Medicaid waiver payments not reported on Form(s) W-2
        'f1_36[0]': 'f1_36[0]', # Income - Taxable dependent care benefits from Form 2441
        'f1_37[0]': 'f1_37[0]', # Income - Employer-provided adoption benefits from Form 8839
        'f1_38[0]': 'f1_38[0]', # Income - Wages from Form 8919
        'f1_39[0]': 'f1_39[0]', # Income - Other earned income
        'f1_40[0]': 'f1_40[0]', # Income - Nontaxable combat pay election
        'f1_41[0]': 'f1_41[0]', # Income - Add lines 1a through 1h
        'f1_42[0]': 'f1_42[0]', # Income - Tax-exempt interest
        'f1_43[0]': 'f1_43[0]', # Income - Taxable interest
        'f1_44[0]': 'f1_44[0]', # Income - Qualified dividends
        'f1_45[0]': 'f1_45[0]', # Income - Ordinary dividends
        'f1_46[0]': 'f1_46[0]', # Income - IRA distributions
        'f1_47[0]': 'f1_47[0]', # Income - Taxable amount
        'f1_48[0]': 'f1_48[0]', # Income - Pensions and annuities
        'f1_49[0]': 'f1_49[0]', # Income - Taxable amount
        'f1_50[0]': 'f1_50[0]', # Income - Social security benefits
        'f1_51[0]': 'f1_51[0]', # Income - Taxable amount
        'f1_52[0]': 'f1_52[0]', # Capital gain or (loss). Attach Schedule D if required. If not required, check here
        'f1_53[0]': 'f1_53[0]', # Additional income from Schedule 1
        'f1_54[0]': 'f1_54[0]', # Add lines 1z, 2b, 3b, 4b, 5b, 6b, 7, and 8. This is your total income
        'f1_55[0]': 'f1_55[0]', # Adjustments to income from Schedule 1
        'f1_56[0]': 'f1_56[0]', # Subtract line 10 from line 9. This is your adjusted gross income
        'f1_57[0]': 'f1_57[0]', # Standard deduction or itemized deductions
        'f1_58[0]': 'f1_58[0]', # Qualified business income deduction from Form 8995 or Form 8995-A
        'f1_59[0]': 'f1_59[0]', # Add lines 12 and 13(f1_57[0] + f1_58[0])
        'f1_60[0]': 'f1_60[0]', # Subtract line 14 from line 11. If zero or less, enter -0-. This is your taxable income
        'f2_01[0]': 'f2_01[0]', # Tax and Credit(option 3)
        'f2_02[0]': 'f2_02[0]', # Tax (see instructions). Check if any from Form(s):
        'f2_03[0]': 'f2_03[0]', # Amount from Schedule 2, line 3
        'f2_04[0]': 'f2_04[0]', # Add lines 16 and 17(f2_02[0] + f2_03[0])
        'f2_05[0]': 'f2_05[0]', # Child tax credit or credit for other dependents from Schedule 8812
        'f2_06[0]': 'f2_06[0]', # Amount from Schedule 3
        'f2_07[0]': 'f2_07[0]', # Add lines 19 and 20(f2_05[0] + f2_06[0])
        'f2_08[0]': 'f2_08[0]', # Subtract line 21 from line 18(f2_04[0] - f2_07[0]). If zero or less, enter -0-
        'f2_09[0]': 'f2_09[0]', # Other taxes, including self-employment tax, from Schedule 2, line 21
        'f2_10[0]': 'f2_10[0]', # Add lines 22 and 23. This is your total tax 
        'f2_11[0]': 'f2_11[0]', # Federal income tax withheld from: Form(s) W-2
        'f2_12[0]': 'f2_12[0]', # Federal income tax withheld from: Form(s) 1099
        'f2_13[0]': 'f2_13[0]', # Federal income tax withheld from: Other forms
        'f2_14[0]': 'f2_14[0]', # Federal income tax withheld from: Add lines 25a through 25c(f2_11[0] + f2_12[0] + f2_13[0])
        'f2_15[0]': 'f2_15[0]', # 2024 estimated tax payments and amount applied from 2023 return
        'f2_16[0]': 'f2_16[0]', # Earned income credit (EIC)
        'f2_17[0]': 'f2_17[0]', # Additional child tax credit from Schedule 8812
        'f2_18[0]': 'f2_18[0]', # American opportunity credit from Form 8863
        'f2_19[0]': 'f2_19[0]', # Reserved for future use
        'f2_20[0]': 'f2_20[0]', # Amount from Schedule 3, line 15
        'f2_21[0]': 'f2_21[0]', # Add lines 27, 28, 29, and 31. These are your total other payments and refundable credits(f2_16[0] + f2_17[0] + f2_18[0] + f2_20[0])
        'f2_22[0]': 'f2_22[0]', # Add lines 25d, 26, and 32. These are your total payments(f2_13[0] + f2_15[0] + f2_21[0])
        'f2_23[0]': 'f2_23[0]', # If line 33 is more than line 24, subtract line 24 from line 33. This is the amount you overpaid
        'f2_24[0]': 'f2_24[0]', # Amount of line 34 you want refunded to you. If Form 8888 is attached
        'f2_25[0]': 'f2_25[0]', # f2_24[0] - Routing number
        'f2_26[0]': 'f2_26[0]', # f2_24[0] - Account Number
        'f2_27[0]': 'f2_27[0]', # Amount of line 34 you want applied to your 2025 estimated tax
        'f2_28[0]': 'f2_28[0]', # Amount you owe - Subtract line 33 from line 24. This is the amount you owe(f2_10[0] - f2_22[0])
        'f2_29[0]': 'f2_29[0]', # Amount you owe - Estimated tax penalty 
        'f2_30[0]': 'f2_30[0]', # Third Party Designee - Designee’s name
        'f2_31[0]': 'f2_31[0]', # Third Party Designee - Phone no.
        'f2_32[0]': 'f2_32', # Third Party Designee - Personal identification number (PIN
        'f2_33[0]': 'f2_33[0]', # Sign here - your occupation
        'f2_34[0]': 'f2_34[', # Sign here - If the IRS sent you an Identity Protection PIN, enter it here
        'f2_35[0]': 'f2_35[0]', # Sign here - Spouse's occupation
        'f2_36[0]': 'f2_36[', # Sign here - If the IRS sent your spouse an Identity Protection PIN, enter it here
        'f2_37[0]': 'f2_37[0]', # Sign here - Phone no.
        'f2_38[0]': 'f2_38[0]', # Sign here - Email address
        'f2_39[0]': 'f2_39[0]', # Paid Preparer Use Only - Preparer's name
        'f2_40[0]': 'f2_40[0]', # Paid Preparer Use Only - PTIN
        'f2_41[0]': 'f2_41[0]', # Paid Preparer Use Only - Firm’s name
        'f2_42[0]': 'f2_42[0]', # Paid Preparer Use Only - Phone no.
        'f2_43[0]': 'f2_43[0]', # Paid Preparer Use Only - Firm’s address
        'f2_44[0]': 'f2_44[0]' # Paid Preparer Use Only - Firm’s EIN
    }

    # Fill the form
    filled_form = PdfWrapper("1040.pdf").fill(form_data)
    
    # Save the filled form
    with open("filled_1040.pdf", "wb+") as output:
        output.write(filled_form.read())

# Run the function
fill_form()