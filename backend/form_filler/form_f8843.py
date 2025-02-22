from PyPDFForm import PdfWrapper

def fill_form_8843(
    # Personal Information
    first_name: str,              # f1_4[0]
    last_name: str,               # f1_5[0]
    us_tax_id: str = "",          # f1_6[0]
    foreign_address: str = "",     # f1_7[0]
    us_address: str = "",         # f1_8[0]
    
    # Visa and Status
    current_visa: str = "",       # f1_9[0]
    current_status: str = "",     # f1_10[0]
    citizenship_countries: str = "", # f1_11[0]
    passport_countries: str = "",  # f1_12[0]
    passport_numbers: str = "",    # f1_13[0]
    
    # Days Present
    days_2024: str = "",          # f1_14[0]
    days_2023: str = "",          # f1_15[0]
    days_2022: str = "",          # f1_16[0]
    excluded_days: str = "",      # f1_17[0]
    
    # Tax Year Period
    year_start: str = "",         # f1_1[0]
    year_end: str = "",           # f1_2[0]
    alt_year: str = "",           # f1_3[0]
    
    # Academic Information - Teachers
    teacher_institution: str = "", # f1_18[0]
    teacher_address: str = "",     # f1_19[0]
    teacher_phone: str = "",       # f1_20[0]
    
    # Director Information - Teachers
    teacher_director: str = "",    # f1_21[0]
    teacher_dir_address: str = "", # f1_22[0]
    teacher_dir_phone: str = "",   # f1_23[0]
    
    # Academic Information - Students
    student_institution: str = "", # f1_30[0]
    student_address: str = "",     # f1_31[0]
    student_phone: str = "",       # f1_32[0]
    student_director: str = "",    # f1_33[0]
    student_dir_address: str = "", # f1_34[0]
    student_dir_phone: str = "",   # f1_35[0]
    
    # Visa History - Teachers (J or Q)
    teacher_visa_2018: str = "",   # f1_24[0]
    teacher_visa_2019: str = "",   # f1_25[0]
    teacher_visa_2020: str = "",   # f1_26[0]
    teacher_visa_2021: str = "",   # f1_27[0]
    teacher_visa_2022: str = "",   # f1_28[0]
    teacher_visa_2023: str = "",   # f1_29[0]
    
    # Visa History - Students (F, J, M, or Q)
    student_visa_2018: str = "",   # f1_36[0]
    student_visa_2019: str = "",   # f1_37[0]
    student_visa_2020: str = "",   # f1_38[0]
    student_visa_2021: str = "",   # f1_39[0]
    student_visa_2022: str = "",   # f1_40[0]
    student_visa_2023: str = "",   # f1_41[0]
    
    # Yes/No Questions
    exempt_2years: bool = False,   # c1_1[0]/[1]
    exempt_5years: bool = False,   # c1_2[0]/[1]
    permanent_residence: bool = False, # c1_3[0]/[1]
    
    # Permanent Residence Explanation
    residence_explain_1: str = "", # f1_42[0]
    residence_explain_2: str = "", # f1_43[0]
    residence_explain_3: str = "", # f1_44[0]
    
    # Professional Athletes
    sports_event_1: str = "",     # f2_1[0]
    sports_event_2: str = "",     # f2_2[0]
    sports_event_3: str = "",     # f2_3[0]
    charity_org_1: str = "",      # f2_4[0]
    charity_org_2: str = "",      # f2_5[0]
    charity_org_3: str = "",      # f2_6[0]
    
    # Medical Condition
    medical_desc_1: str = "",     # f2_7[0]
    medical_desc_2: str = "",     # f2_8[0]
    medical_desc_3: str = "",     # f2_9[0]
    medical_desc_4: str = "",     # f2_10[0]
    intended_leave_date: str = "", # f2_11[0]
    actual_leave_date: str = ""    # f2_12[0]
):
    """
    Fill out IRS Form 8843 with provided information.
    """
    
    # Initialize form data
    form_data = {
        # Personal Information
        'f1_4[0]': first_name,
        'f1_5[0]': last_name,
        'f1_6[0]': us_tax_id,
        'f1_7[0]': foreign_address,
        'f1_8[0]': us_address,
        
        # Visa and Status
        'f1_9[0]': current_visa,
        'f1_10[0]': current_status,
        'f1_11[0]': citizenship_countries,
        'f1_12[0]': passport_countries,
        'f1_13[0]': passport_numbers,
        
        # Days Present
        'f1_14[0]': days_2024,
        'f1_15[0]': days_2023,
        'f1_16[0]': days_2022,
        'f1_17[0]': excluded_days,
        
        # Tax Year Period
        'f1_1[0]': year_start,
        'f1_2[0]': year_end,
        'f1_3[0]': alt_year,
        
        # Academic Information - Teachers
        'f1_18[0]': teacher_institution,
        'f1_19[0]': teacher_address,
        'f1_20[0]': teacher_phone,
        'f1_21[0]': teacher_director,
        'f1_22[0]': teacher_dir_address,
        'f1_23[0]': teacher_dir_phone,
        
        # Academic Information - Students
        'f1_30[0]': student_institution,
        'f1_31[0]': student_address,
        'f1_32[0]': student_phone,
        'f1_33[0]': student_director,
        'f1_34[0]': student_dir_address,
        'f1_35[0]': student_dir_phone,
        
        # Visa History - Teachers
        'f1_24[0]': teacher_visa_2018,
        'f1_25[0]': teacher_visa_2019,
        'f1_26[0]': teacher_visa_2020,
        'f1_27[0]': teacher_visa_2021,
        'f1_28[0]': teacher_visa_2022,
        'f1_29[0]': teacher_visa_2023,
        
        # Visa History - Students
        'f1_36[0]': student_visa_2018,
        'f1_37[0]': student_visa_2019,
        'f1_38[0]': student_visa_2020,
        'f1_39[0]': student_visa_2021,
        'f1_40[0]': student_visa_2022,
        'f1_41[0]': student_visa_2023,
        
        # Yes/No Questions
        'c1_1[0]': exempt_2years,
        'c1_1[1]': not exempt_2years,
        'c1_2[0]': exempt_5years,
        'c1_2[1]': not exempt_5years,
        'c1_3[0]': permanent_residence,
        'c1_3[1]': not permanent_residence,
        
        # Permanent Residence Explanation
        'f1_42[0]': residence_explain_1,
        'f1_43[0]': residence_explain_2,
        'f1_44[0]': residence_explain_3,
        
        # Professional Athletes
        'f2_1[0]': sports_event_1,
        'f2_2[0]': sports_event_2,
        'f2_3[0]': sports_event_3,
        'f2_4[0]': charity_org_1,
        'f2_5[0]': charity_org_2,
        'f2_6[0]': charity_org_3,
        
        # Medical Condition
        'f2_7[0]': medical_desc_1,
        'f2_8[0]': medical_desc_2,
        'f2_9[0]': medical_desc_3,
        'f2_10[0]': medical_desc_4,
        'f2_11[0]': intended_leave_date,
        'f2_12[0]': actual_leave_date
    }

    # Fill and save the form
    filled_form = PdfWrapper("f8843.pdf").fill(form_data)
    with open("filled_f8843.pdf", "wb+") as output:
        output.write(filled_form.read())

# Example usage with all fields filled
fill_form_8843(
    # Personal Information
    first_name="John Wei",
    last_name="Smith",
    us_tax_id="123-45-6789",
    foreign_address="123 Foreign Street, Foreign City, Foreign Country 12345",
    us_address="456 American Ave, New York, NY 10001",
    
    # Visa and Status
    current_visa="F-1 (Entered 01/01/2024)",
    current_status="F-1 Student, Changed from J-1 on 06/15/2024",
    citizenship_countries="China, Canada",
    passport_countries="China, Canada",
    passport_numbers="G12345678, HK98765432",
    
    # Days Present
    days_2024="300",
    days_2023="365",
    days_2022="300",
    excluded_days="250",
    
    # Tax Year Period
    year_start="01/15",
    year_end="12/15",
    alt_year="2023",
    
    # Academic Information - Teachers
    teacher_institution="Columbia University",
    teacher_address="116th St & Broadway, New York, NY 10027",
    teacher_phone="(212) 555-1234",
    teacher_director="Dr. Jane Wilson",
    teacher_dir_address="Mathematics Dept, Columbia University, NY 10027",
    teacher_dir_phone="(212) 555-5678",
    
    # Academic Information - Students
    student_institution="MIT",
    student_address="77 Massachusetts Ave, Cambridge, MA 02139",
    student_phone="(617) 555-1234",
    student_director="Dr. Robert Brown",
    student_dir_address="Computer Science Dept, MIT, MA 02139",
    student_dir_phone="(617) 555-5678",
    
    # Visa History - Teachers
    teacher_visa_2018="J",
    teacher_visa_2019="J",
    teacher_visa_2020="J",
    teacher_visa_2021="J",
    teacher_visa_2022="J",
    teacher_visa_2023="J",
    
    # Visa History - Students
    student_visa_2018="F",
    student_visa_2019="F",
    student_visa_2020="J",
    student_visa_2021="J",
    student_visa_2022="F",
    student_visa_2023="F",
    
    # Yes/No Questions
    exempt_2years=True,
    exempt_5years=False,
    permanent_residence=True,
    
    # Permanent Residence Explanation
    residence_explain_1="Applied for H1-B visa through employer Google Inc.",
    residence_explain_2="Application submitted on March 15, 2024",
    residence_explain_3="Currently awaiting USCIS processing",
    
    # Professional Athletes
    sports_event_1="US Open Tennis Championship 2024, Aug 26-Sep 8",
    sports_event_2="Miami Open 2024, March 17-31",
    sports_event_3="Indian Wells Tennis Tournament 2024, March 3-17",
    charity_org_1="USTA Foundation, EIN: 13-3782331",
    charity_org_2="Miami Youth Tennis, EIN: 65-1234567",
    charity_org_3="Tennis for America, EIN: 84-7654321",
    
    # Medical Condition
    medical_desc_1="Severe ankle injury sustained during tennis match",
    medical_desc_2="Required immediate surgery and physical therapy",
    medical_desc_3="Doctor recommended no travel for 3 months",
    medical_desc_4="Full recovery achieved after rehabilitation",
    intended_leave_date="03/20/2024",
    actual_leave_date="06/20/2024"
)