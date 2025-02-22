from PyPDFForm import PdfWrapper

def fill_form():
    # Use the exact sample data
    form_data = {'c1_1[0]': False, #yes if you were exempt as a teacher, trainee, or student for any part of 2 of the preceding 6 calendar years (2018 through 2023)
    'c1_1[1]': False, #no if you were exempt as a teacher, trainee, or student for any part of 2 of the preceding 6 calendar years (2018 through 2023)
    'c1_2[0]': False, #yes if you Were you exempt as a teacher, trainee, or student for any part of more than 5 calendar years
    'c1_2[1]': False, #no if you Were you exempt as a teacher, trainee, or student for any part of more than 5 calendar years 
    'c1_3[0]': False, #yes if During 2024, did you apply for, or take other affirmative steps to apply for, lawful permanent resident status in  the  United  States  or  have  an  application  pending  to  change  your  status  to  that  of  a  lawful  permanent resident of the United States
    'c1_3[1]': False,#no if During 2024, did you apply for, or take other affirmative steps to apply for, lawful permanent resident status in  the  United  States  or  have  an  application  pending  to  change  your  status  to  that  of  a  lawful  permanent resident of the United States
    'f1_10[0]': 'f1_10[0]', #Current nonimmigrant status. If your status has changed, also enter date of change and previous status. See instructions.
    'f1_11[0]': 'f1_11[0]', #Of what country or countries were you a citizen during the tax year?
    'f1_12[0]': 'f1_12[0]', #What country or countries issued you a passport?
    'f1_13[0]': 'f1_13[0]', #Enter your passport number(s)
    'f1_14[0]': 'f1_14[0]', #Enter the actual number of days you were present in the United States during 2024
    'f1_15[0]': 'f1_15[0]', #Enter the actual number of days you were present in the United States during 2023
    'f1_16[0]': 'f1_16[0]', #Enter the actual number of days you were present in the United States during 2022
    'f1_17[0]': 'f1_17[0]', #Enter the number of days in 2024 you claim you can exclude for purposes of the substantial presence test:
    'f1_18[0]': 'f1_18[0]', #For teachers, enter the name of the academic institution where you taught in 2024:
    'f1_19[0]': 'f1_19[0]', #For teachers, enter the address of the academic institution where you taught in 2024:
    'f1_1[0]': 'f1_1[0]', #beginning date and month of 2024 if beginning not jan 1 
    'f1_20[0]': 'f1_20[0]', #For teachers, enter the telephone number of the academic institution where you taught in 2024:
    'f1_21[0]': 'f1_21[0]', #For trainees, enter the name of the director of the academic or other specialized program you participated in during 2024:
    'f1_22[0]': 'f1_22[0]', #For trainees, enter the address of the director of the academic or other specialized program you participated in during 2024:
    'f1_23[0]': 'f1_23[0]', # For trainees, enter the telephone number of the director of the academic or other specialized program you participated in during 2024:
    'f1_24[0]': 'f', #visa type (J or Q) held in 2018 - teachers and trainees
    'f1_25[0]': 'f', #visa type (J or Q) held in 2019 - teachers and trainees
    'f1_26[0]': 'f', #visa type (J or Q) held in 2020 - teachers and trainees
    'f1_27[0]': 'f', #visa type (J or Q) held in 2021 - teachers and trainees
    'f1_28[0]': 'f', #visa type (J or Q) held in 2022 - teachers and trainees
    'f1_29[0]': 'f', #visa type (J or Q) held in 2023 - teachers and trainees
    'f1_2[0]': 'f1_2[0]', #ending date and month of 2024 if ending not dec 31
    'f1_30[0]': 'f1_30[0]', #name of academic institution attended during 2024
    'f1_31[0]': 'f1_31[0]', #address of academic institution attended during 2024
    'f1_32[0]': 'f1_32[0]', #telephone number of academic institution attended during 2024
    'f1_33[0]': 'f1_33[0]', #Enter the name  of the director of the academic or other specialized program you participated in during 2024
    'f1_34[0]': 'f1_34[0]', #Enter the address of the director of the academic or other specialized program you participated in during 2024
    'f1_35[0]': 'f1_35[0]', #Enter the telephone number of the director of the academic or other specialized program you participated in during 2024
    'f1_36[0]': 'f', #visa type (F, J, M, Q) held in 2018 - students
    'f1_37[0]': 'f', #visa type (F, J, M, Q) held in 2019 - students
    'f1_38[0]': 'f', #visa type (F, J, M, Q) held in 2020 - students
    'f1_39[0]': 'f', #visa type (F, J, M, Q) held in 2021 - students
    'f1_3[0]': 'f1', #ending year if ending year not 2024 
    'f1_40[0]': 'f', #visa type (F, J, M, Q) held in 2022 - students
    'f1_41[0]': 'f', #visa type (F, J, M, Q) held in 2023 - students
    'f1_42[0]': 'f1_42[0]', #explain why if During 2024, did you apply for, or take other affirmative steps to apply for, lawful permanent resident status in  the  United  States  or  have  an  application  pending  to  change  your  status  to  that  of  a  lawful  permanent  resident of the United States? (part 1 of 5)
    'f1_43[0]': 'f1_43[0]', #explain why if During 2024, did you apply for, or take other affirmative steps to apply for, lawful permanent resident status in  the  United  States  or  have  an  application  pending  to  change  your  status  to  that  of  a  lawful  permanent  resident of the United States? (part 2 & 3  of 5)
    'f1_44[0]': 'f1_44[0]', #explain why if During 2024, did you apply for, or take other affirmative steps to apply for, lawful permanent resident status in  the  United  States  or  have  an  application  pending  to  change  your  status  to  that  of  a  lawful  permanent  resident of the United States? (part 4 & 5 of 5)
    'f1_4[0]': 'f1_4[0]', #first name and initial of filer
    'f1_5[0]': 'f1_5[0]', #last name of filer
    'f1_6[0]': 'f1_6[0]', #US Taxpayer TIN if any
    'f1_7[0]': 'f1_7[0]', #address in country of residence
    'f1_8[0]': 'f1_8[0]', #address in the united states 
    'f1_9[0]': 'f1_9[0]', #Type of U.S. visa (for example, F, J, M, Q, etc.) and date you entered the United States:
    'f2_10[0]': 'f2_10[0]', #individuals w a medical condition or problem - (4) Describe the medical condition or medical problem that prevented you from leaving the United States. (if any) 
    'f2_11[0]': 'f2_11[0]', #Enter the date you intended to leave the United States prior to the onset of the medical condition or medical problem described on line 17a
    'f2_12[0]': 'f2_12[0]', #Enter the date you actually left the United States:
    #'f2_13[0]': 'f2_13[0]', must be left out 
    #'f2_14[0]': 'f2_14[0]', must be left out 
    #'f2_15[0]': 'f2_15[0]', must be left out 
    'f2_1[0]': 'f2_1[0]', #professional athletes -  (1) Enter  the  name  of  the  charitable  sports  event(s)  in  the  United  States  in  which  you  competed  during  2024  and  the  dates  of competition
    'f2_2[0]': 'f2_2[0]', #professional athletes -  (2) Enter  the  name  of  the  charitable  sports  event(s)  in  the  United  States  in  which  you  competed  during  2024  and  the  dates  of competition
    'f2_3[0]': 'f2_3[0]', #professional athletes -  (3) Enter  the  name  of  the  charitable  sports  event(s)  in  the  United  States  in  which  you  competed  during  2024  and  the  dates  of competition
    'f2_4[0]': 'f2_4[0]', #professional athletes - (1) Enter  the  name(s)  and  employer  identification  number(s)  of  the  charitable  organization(s)  that  benefited  from  the  sports event(s)
    'f2_5[0]': 'f2_5[0]', #professional athletes - (2) Enter  the  name(s)  and  employer  identification  number(s)  of  the  charitable  organization(s)  that  benefited  from  the  sports event(s)
    'f2_6[0]': 'f2_6[0]', #professional athletes - (3) Enter  the  name(s)  and  employer  identification  number(s)  of  the  charitable  organization(s)  that  benefited  from  the  sports event(s)
    'f2_7[0]': 'f2_7[0]', #individuals w a medical condition or problem - (1) Describe the medical condition or medical problem that prevented you from leaving the United States. (if any) 
    'f2_8[0]': 'f2_8[0]', #individuals w a medical condition or problem - (2) Describe the medical condition or medical problem that prevented you from leaving the United States. (if any) 
    'f2_9[0]': 'f2_9[0]' #individuals w a medical condition or problem - (3) Describe the medical condition or medical problem that prevented you from leaving the United States. (if any) 
    }

    # Fill the form
    filled_form = PdfWrapper("f8843.pdf").fill(form_data)
    
    # Save the filled form
    with open("filled_f8843.pdf", "wb+") as output:
        output.write(filled_form.read())

# Run the function
fill_form()