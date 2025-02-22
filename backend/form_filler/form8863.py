from PyPDFForm import PdfWrapper

def test_form_8863():
    """Test all fields in Form 8863 with sample data"""
    
    # Create test data for every possible field
    form_data = {
        # Part I - Basic Information
        'NameShown[0]': 'Test Taxpayer',
        'f1_1[0]': 'Test Taxpayer',
        'f1_2[0]': '123',  # First 3 of SSN
        'f1_3[0]': '45',   # Middle 2 of SSN
        'f1_4[0]': '6789', # Last 4 of SSN
        
        # Refundable Credit Section
        'f1_5[0]': '4000',    # Line 1: Tentative credit
        'f1_6[0]': '180000',  # Line 2: Income limit (MFJ)
        'f1_7[0]': '160000',  # Line 3: Modified AGI
        'f1_8[0]': '20000',   # Line 4: Subtract line 3 from line 2
        'f1_9[0]': '20000',   # Line 5: Income phase-out amount
        'f1_10[0]': '1.000',  # Line 6: Decimal amount (if line 4 >= line 5)
        'f1_11[0]': '0.750',  # Line 6: Alternative decimal calculation
        'f1_12[0]': '3000',   # Line 7: Multiply line 1 by line 6
        'f1_13[0]': '1200',   # Line 8: Multiply line 7 by 40%
        'f1_14[0]': '1800',   # Line 9: Subtract line 8 from line 7
        
        # Part II - Nonrefundable Education Credits
        'f1_15[0]': '2500',   # Line 10: Qualified expenses for LLC
        'f1_16[0]': '2500',   # Line 11: Smaller of line 10 or $10,000
        'f1_17[0]': '500',    # Line 12: Multiply line 11 by 20%
        'f1_18[0]': '180000', # Line 13: Income limit
        'f1_19[0]': '160000', # Line 14: Modified AGI
        'f1_20[0]': '20000',  # Line 15: Subtract line 14 from line 13
        'f1_21[0]': '20000',  # Line 16: Income phase-out amount
        'f1_22[0]': '1.000',  # Line 17: Phase-out decimal (if line 15 >= line 16)
        'f1_23[0]': '0.750',  # Line 17: Alternative phase-out calculation
        'f1_24[0]': '500',    # Line 18: Multiply line 12 by line 17
        'f1_25[0]': '2300',   # Line 19: Nonrefundable education credits
        
        # Part III - Student Information
        'StudentName[0]': 'Test Student',
        'f2_1[0]': '987',     # First 3 of student SSN
        'f2_2[0]': '65',      # Middle 2 of student SSN
        'f2_3[0]': '4321',    # Last 4 of student SSN
        'f2_4[0]': '987', # First 3 of student SSN
        'f2_5[0]': '65', # Middle 2 of student SSN
        'f2_6[0]': '4321', # Last 4 of student SSN
        
        # First Educational Institution
        'f2_7[0]': 'Test University',
        'f2_8[0]': '123 Education St, Test City, TS 12345',
        'f2_9[0]': '1',       # EIN digit 1
        'f2_10[0]': '2',      # EIN digit 2
        'f2_11[0]': '3',      # EIN digit 3
        'f2_12[0]': '4',      # EIN digit 4
        'f2_13[0]': '5',      # EIN digit 5
        'f2_14[0]': '6',      # EIN digit 6
        'f2_15[0]': '7',      # EIN digit 7
        'f2_16[0]': '8',      # EIN digit 8
        'f2_17[0]': '9',      # EIN digit 9
        
        # Second Educational Institution
        'f2_18[0]': 'Second Test College',
        'f2_19[0]': '456 Learning Ave, Study City, SC 67890',
        'f2_20[0]': '9',      # EIN digit 1
        'f2_21[0]': '8',      # EIN digit 2
        'f2_22[0]': '7',      # EIN digit 3
        'f2_23[0]': '6',      # EIN digit 4
        'f2_24[0]': '5',      # EIN digit 5
        'f2_25[0]': '4',      # EIN digit 6
        'f2_26[0]': '3',      # EIN digit 7
        'f2_27[0]': '2',      # EIN digit 8
        'f2_28[0]': '1',      # EIN digit 9
        
        # Education Credit Amounts
        'f2_29[0]': '4000',   # Adjusted qualified education expenses
        'f2_30[0]': '2000',   # Subtract $2,000 from expenses
        'f2_31[0]': '500',    # Multiply line 28 by 25%
        'f2_32[0]': '2500',   # Add $2,000 to line 29
        'f2_33[0]': '4000',   # Total education credits
        
        # Checkboxes
        'c1_1[0]': True,      # Under age 24
        'c2_1[0]': True,      # Received 2024 1098-T (first institution)
        'c2_1[1]': False,     # Did NOT receive 2024 1098-T
        'c2_2[0]': True,      # 2023 1098-T box 7 checked (first institution)
        'c2_2[1]': False,     # 2023 1098-T box 7 NOT checked
        'c2_3[0]': True,      # Received 2024 1098-T (second institution)
        'c2_3[1]': False,     # Did NOT receive 2024 1098-T
        'c2_4[0]': True,      # 2023 1098-T box 7 checked (second institution)
        'c2_4[1]': False,     # 2023 1098-T box 7 NOT checked
        'c2_5[0]': False,     # AOC NOT claimed in 4 prior years
        'c2_5[1]': True,      # AOC claimed in 4 prior years
        'c2_6[0]': True,      # Enrolled at least half-time
        'c2_6[1]': False,     # NOT enrolled at least half-time
        'c2_7[0]': False,     # Did NOT complete first 4 years
        'c2_7[1]': True,      # Completed first 4 years
        'c2_8[0]': False,     # No felony drug conviction
        'c2_8[1]': True       # Has felony drug conviction
    }
    
    try:
        # Fill the form with test data
        filled_form = PdfWrapper("f8863.pdf").fill(form_data)
        
        # Save the filled form
        with open("test_filled_f8863.pdf", "wb+") as output:
            output.write(filled_form.read())
            
        print("Test form filled successfully! Please check test_filled_f8863.pdf")
        print("\nTest data summary:")
        print("- Taxpayer Name:", form_data['NameShown[0]'])
        print("- Student Name:", form_data['StudentName[0]'])
        print("- First Institution:", form_data['f2_7[0]'])
        print("- Second Institution:", form_data['f2_18[0]'])
        print("- Qualified Expenses:", form_data['f2_29[0]'])
        print("- Total Education Credit:", form_data['f2_33[0]'])
        return True
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    test_form_8863()