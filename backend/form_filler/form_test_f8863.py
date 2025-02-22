from PyPDFForm import PdfWrapper

def fill_form():
    # Use the exact sample data
    form_data = {
        'NameShown[0]': 'NameShown[0]', # Name shown on return
        'StudentName[0]': 'StudentName[0]', # name of student
        'c1_1[0]': True, # Line 7 check box(f1_12[0]) If you were under age 24 at the end of the year and meet the conditions described in the instructions, you can’ t take the refundable American opportunity credit; skip line 8(f1_13[0]), enter the amount from line 7(f1_12[0]) on line 9(f1_14[0]), and check this box
        'c2_1[0]': True, # first educational institution - Did the student receive Form 1098-T from this institution for 2024? - YES
        'c2_1[1]': True, # first educational institution - Did the student receive Form 1098-T from this institution for 2024? - NO
        'c2_2[0]': True, # first educational institution - Did the student receive Form 1098-T from this institution for 2023 with box 7 checked? - YES
        'c2_2[1]': True, # first educational institution - Did the student receive Form 1098-T from this institution for 2023 with box 7 checked? - NO
        'c2_3[0]': True, # second or any educational institution - Did the student receive Form 1098-T from this institution for 2024? - YES
        'c2_3[1]': True, # second or any educational institution - Did the student receive Form 1098-T from this institution for 2024? - NO
        'c2_4[0]': True, # second educational institution - Did the student receive Form 1098-T from this institution for 2023 with box 7 checked? - YES
        'c2_4[1]': True, # second educational institution - Did the student receive Form 1098-T from this institution for 2023 with box 7 checked? - NO
        'c2_5[0]': True, # Has the American opportunity credit been claimed for this student for any 4 prior tax years? - YES - STOP! go to line 31(f2_33[0])
        'c2_5[1]': True, # Has the American opportunity credit been claimed for this student for any 4 prior tax years? - NO go to line 24(c2_6[0] and c2_6[1])
        'c2_6[0]': True, # YES - Was the student enrolled at least half-time for at least one academic period that began or is treated as having begun in 2024 at an eligible educational institution in a program leading towards a postsecondary degree, certificate, or other recognized postsecondary educational credential? and go to line 25(c2_7[0] and c2_7[1])
        'c2_6[1]': True, # NO - STOP! - Was the student enrolled at least half-time for at least one academic period that began or is treated as having begun in 2024 at an eligible educational institution in a program leading towards a postsecondary degree, certificate, or other recognized postsecondary educational credential? and go to line 31(f2_33[0])
        'c2_7[0]': True, # YES - STOP! Did the student complete the first 4 years of postsecondary education before 2024? go to line 31(f2_33[0])
        'c2_7[1]': True, # NO - Did the student complete the first 4 years of postsecondary education before 2024? go to line 26(c2_8[0] and c2_8[1])
        'c2_8[0]': False, # YES - STOP! - Was the student convicted, before the end of 2024, of a felony for possession or distribution of a controlled substance? go to line 31(f2_33[0])
        'c2_8[1]': True, # NO - Was the student convicted, before the end of 2024, of a felony for possession or distribution of a controlled substance? complete lines 27(f2_29[0]) through 30(f2_32[0])
        'f1_10[0]': 'f1_10[0]', # Enter 1000 if line 4 (f1_8[0]) is equal to or more than line 5 (f1_9[0]).
        'f1_11[0]': 'f1_11[0]', # If line 4 (f1_8[0]) is less than line 5 (f1_9[0]), divide line 4 by line 5 and enter the result as a decimal (rounded to at least three places).
        'f1_12[0]': 'f1_12[0]', # Multiply line 1(f1_5[0]) by line 6(f1_10[0] f1_11[0])
        'f1_13[0]': 'f1_13[0]', # Refundable American opportunity credit. Multiply line 7(f1_12[0]) by 40% (0.40). Enter the amount here and on Form 1040 or 1040-SR, line 29(f2_31[0]). Then go to line 9(f1_14[0])
        'f1_14[0]': 'f1_14[0]', # Subtract line 8(f1_13[0]) from line 7(f1_12[0]). Enter here and on line 2 of the Credit Limit Worksheet (Form 8863, line 2)
        'f1_15[0]': 'f1_15[0]', # After completing Part III for each student, enter the total of all amounts from all Parts III, line 31(f2_33[0]). If zero, skip lines 11(f1_16[0]) through 17(f1_22[0] f1_23[0]), enter -0- on line 18(f1_24[0]), and go to line 19(f1_25[0])
        'f1_16[0]': 'f1_16[0]', # Enter the smaller of line 10(f1_15[0]) or $10,000
        'f1_17[0]': 'f1_17[0]', # Multiply line 11(f1_16[0]) by 20% (0.20)
        'f1_18[0]': 'f1_18[0]', # Enter: $180,000 if married filing jointly; $90,000 if single, head of household, or qualifying surviving spouse
        'f1_19[0]': 'f1_19[0]', # Enter the amount from Form 1040 or 1040-SR, line 11. But if you’ re filing Form 2555 or 4563, or you’re excluding income from Puerto Rico, see Pub. 970 forthe amount to enter instead
        'f1_1[0]': 'f1_1[0]', # Name shown on return
        'f1_20[0]': 'f1_20[0]', # Subtract line 14(f1_19[0]) from line 13(f1_18[0]). If zero or less, skip lines 16(f1_21[0]) and 17(f1_22[0] f1_23[0]), enter -0- on line 18(f1_24[0]), and go to line 19(f1_25[0])
        'f1_21[0]': 'f1_21[0]', # Enter: $20,000 if married filing jointly; $10,000 if single, head of household, or qualifying surviving spouse
        'f1_22[0]': 'f1_22[0]', # Enter 1000 if line 15 (f1_20[0]) is equal to or more than line 16 (f1_21[0]) and skip f1_23[0]
        'f1_23[0]': 'f1_23[0]', # If line 15 (f1_20[0]) is less than line 16 (f1_21[0]), divide line 15 by line 16 and enter the result as a decimal.
        'f1_24[0]': 'f1_24[0]', # Multiply line 12 by line 17(f1_17[0] * (f1_22[0] or f1_23[0]))
        'f1_25[0]': 'f1_25[0]', # Nonrefundable education credits.
        'f1_2[0]': 'f1_', # first 3 digits of ssn
        'f1_3[0]': 'f1', # middle 2 digits of ssn
        'f1_4[0]': 'f1_4', # last 4 digits of ssn
        'f1_5[0]': 'f1_5[0]', # After completion of Student and Educational Institution Information, total of all amounts from this part
        'f1_6[0]': 'f1_6[0]', # Refundable American Opportunity Credit; Enter: $180,000 if married filing jointly; $90,000 if single, head of household, or qualifying surviving spouse
        'f1_7[0]': 'f1_7[0]', # Enter the amount from Form 1040 or 1040-SR, line 11. But if you’ re filing Form 2555 or 4563, or you’re excluding income from Puerto Rico, see Pub. 970 for the amount to enter instead
        'f1_8[0]': 'f1_8[0]', # Subtract the amount from Form 1040 or 1040-SR, line 11, from the applicable credit limit ($180,000 or $90,000). If the result is zero or less, stop; no education credit is allowed.
        'f1_9[0]': 'f1_9[0]', # Enter: $20,000 if married filing jointly; $10,000 if single, head of household, or qualifying surviving spouse
        'f2_10[0]': 'f', # first educational institution - 2nd digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_11[0]': 'f', # first educational institution - 3rd digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_12[0]': 'f', # first educational institution - 4th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_13[0]': 'f', # first educational institution - 5th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_14[0]': 'f', # first educational institution - 6th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_15[0]': 'f', # first educational institution - 7th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_16[0]': 'f', # first educational institution - 8th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_17[0]': 'f', # first educational institution - 9th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_18[0]': 'f2_18[0]', # Name of second educational institution (if any)
        'f2_19[0]': 'f2_19[0]', # Address. Number and street (or P.O. box). City, town or post office, state, and ZIP code.
        'f2_1[0]': 'f2_', # First 3 digits of Student social security number
        'f2_20[0]': 'f', # second educational institution - 1st digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_21[0]': 'f', # second educational institution - 2st digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_22[0]': 'f', # second educational institution - 3rd digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_23[0]': 'f', # second educational institution - 4th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_24[0]': 'f', # second educational institution - 5th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_25[0]': 'f', # second educational institution - 6th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_26[0]': 'f', # second educational institution - 7th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_27[0]': 'f', # second educational institution - 8th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_28[0]': 'f', # second educational institution - 9th digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        'f2_29[0]': 'f2_29[0]', # American Opportunity Credit - Adjusted qualified education expenses - Don’t enter more than $4,000
        'f2_2[0]': 'f2', # Middle 2 digits of Student social security number
        'f2_30[0]': 'f2_30[0]', # American Opportunity Credit - Subtract $2,000 from Adjusted qualified education expenses. If zero or less, enter -0-
        'f2_31[0]': 'f2_31[0]', # American Opportunity Credit - Multiply (Subtract $2,000 from Adjusted qualified education expenses) by 25%
        'f2_32[0]': 'f2_32[0]', # American Opportunity Credit - If line (Subtract $2,000 from Adjusted qualified education expenses) is zero, enter the amount from line Adjusted qualified education expenses. Otherwise, add $2,000 to the amount on (Multiply line 28 by 25% (0.25)) and enter the result.
        'f2_33[0]': 'f2_33[0]', # Lifetime Learning Credit - Adjusted qualified education expenses . Include the total of all amounts from all Parts III, line 31  on Part II, line 1
        'f2_3[0]': 'f2_3', # Last 4 digits of Student social security number
        'f2_4[0]': 'f2_', # first 3 digits of Student social security number
        'f2_5[0]': 'f2', # middle 2 digits of Student social security number
        'f2_6[0]': 'f2_6', # last 4 digits of Student social security number
        'f2_7[0]': 'f2_7[0]', # Name of first educational institution
        'f2_8[0]': 'f2_8[0]', # first educational institution - Address. Number and street (or P.O. box). City, town or post office, state, and ZIP code. 
        'f2_9[0]': 'f2_9[0]' # first educational institution - 1st digit - Enter the institution’s employer identification number (EIN) if you’re claiming the American opportunity credit or if you checked “Yes” in (2) or (3). You can get the EIN from Form 1098-T or from the institution.
        }
    # Fill the form
    filled_form = PdfWrapper("f8863.pdf").fill(form_data)
    
    # Save the filled form
    with open("filled_f8863.pdf", "wb+") as output:
        output.write(filled_form.read())

# Run the function
fill_form()