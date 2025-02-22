from PyPDFForm import PdfWrapper

def fill_form():
    # Use the exact sample data
    form_data = {
    'c1_1[0]': True,
    'c1_1[1]': True,
    'c1_1[2]': True,
    'c1_2[0]': True,
    'f1_01[0]': 'f1_01[0]', #First name and middle initial
    'f1_02[0]': 'f1_02[0]', #Last name
    'f1_03[0]': 'f1_03[0]', #Address
    'f1_04[0]': 'f1_04[0]', #City/town, state, zip code
    'f1_05[0]': 'f1_05[0]', #SSN
    'f1_06[0]': 'f1_06[0]', #Total child tax credits (number of kids under 17 * $2000) (if income 200k or less, or 400k or less if married filing jointly)
    'f1_07[0]': 'f1_07[0]', #Other dependant tax credits (number of other dependants * $500) (if income 200k or less, or 400k or less if married filing jointly)
    'f1_09[0]': 'f1_09[0]', #sum of total child tax credits and other dependant tax credits (if income 200k or less, or 400k or less if married filing jointly)
    'f1_10[0]': 'f1_10[0]', #other income, not from jobs 
    'f1_11[0]': 'f1_11[0]', #deductions
    'f1_12[0]': 'f1_12[0]', #extra withholding per pay period
    'f1_13[0]': 'f1_13[0]', #employer's name and address
    'f1_14[0]': 'f1_14[0]', #first date of employment 
    'f1_15[0]': 'f1_15[0]', #ein
    'f3_01[0]': 'f3_01[0]', #intersection value of lower and higher paying job if family has combined 2 jobs 
    'f3_02[0]': 'f3_02[0]', #intersection value of 2 highest paying jobs if family has 3 jobs combined
    'f3_03[0]': 'f3_03[0]', #intersection value of sum of 2 highest paying jobs and 3rd job
    'f3_04[0]': 'f3_04[0]', #sum of (intersection value of lower and higher paying job if family has combined 2 jobs) and (intersection value of sum of 2 highest paying jobs and 3rd job)
    'f3_05[0]': 'f3_05[0]', #number of pay periods of highest paying job
    'f3_06[0]': 'f3_06[0]', #intersection value of lower and higher paying job if family has combined 2 jobs divided by pay periods if family has combined 2 jobs, else sum of (intersection value of lower and higher paying job if family has combined 2 jobs) and (intersection value of sum of 2 highest paying jobs and 3rd job) divided by pay periods if 3 jobs combined in household
    'f3_07[0]': 'f3_07[0]', #estimated itemized deductions for 2025
    'f3_08[0]': 'f3_08[0]', #$30k usd if married filing jointly or a qualifying surviving spouse, $22500 if head of household, or $15000 if single or married filing separately
    'f3_09[0]': 'f3_09[0]', #If line 1 is greater than line 2, subtract line 2 from line 1 and enter the result here. If line 2 is greater than line 1, enter “-0-”
    'f3_10[0]': 'f3_10[0]', #Enter an estimate of your student loan interest, deductible IRA contributions, and certain other adjustments
    'f3_11[0]': 'f3_11[0]' #Add lines 3 and 4. Enter the result here and in Step 4(b) of Form W-4 
 }

    # Fill the form
    filled_form = PdfWrapper("w4.pdf").fill(form_data)
    
    # Save the filled form
    with open("filled_w4.pdf", "wb+") as output:
        output.write(filled_form.read())

# Run the function
fill_form()