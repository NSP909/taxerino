from .form_w9 import fill_w9_form
from .form_w4 import fill_w4_form
from .form_w8ben import fill_w8ben_form
from .form_1040 import fill_1040_form
from .form_8863 import fill_8863_form
from .form_8843 import fill_8843_form
from .gmail import send_pdf_via_gmail
import json 
def el_filler(form, data):
    try:
        print("filling form: " + form)
        print(form)
        print(data)
        if form == "W-9":
            fill_w9_form(
                name=data.get("name", ""),
                business_name=data.get("business_name", ""),
                tax_classification=data.get("tax_classification", ""),
                llc_classification=data.get("llc_classification", ""),
                address=data.get("address", ""),
                city_state_zip=data.get("city_state_zip", ""),
                exempt_payee_code=data.get("exempt_payee_code", ""),
                fatca_code=data.get("fatca_code", ""),
                requester_info=data.get("requester_info", ""),
                account_numbers=data.get("account_numbers", ""),
                ssn_first=data.get("ssn_first", ""),
                ssn_second=data.get("ssn_second", ""),
                ssn_third=data.get("ssn_third", ""),
                ein_first=data.get("ein_first", ""),
                ein_second=data.get("ein_second", "")
            )
            send_pdf_via_gmail("filled/filled_w9.pdf")
        elif form == "W-4":
            print("enetring w4")
            fill_w4_form(
                first_middle_name=data.get("first_middle_name", ""),
                last_name=data.get("last_name", ""),
                address=data.get("address", ""),
                city_state_zip=data.get("city_state_zip", ""),
                single_or_married_filing_separately=data.get("single_or_married_filing_separately", False),
                married_filing_jointly=data.get("married_filing_jointly", False),
                head_of_household=data.get("head_of_household", False),
                two_jobs_only=data.get("two_jobs_only", False),
                ssn=data.get("ssn", ""),
                child_tax_credits=data.get("child_tax_credits", 0),
                dependent_credits=data.get("dependent_credits", 0),
                total_credits=data.get("total_credits", 0),
                other_income=data.get("other_income", 0),
                deductions=data.get("deductions", 0),
                extra_withholding=data.get("extra_withholding", 0),
                employer_info=data.get("employer_info", ""),
                employment_date=data.get("employment_date", ""),
                employer_ein=data.get("employer_ein", ""),
                pay_periods=data.get("pay_periods", 0),
                itemized_deductions=data.get("itemized_deductions", 0),
                standard_deduction=data.get("standard_deduction", 0),
                deduction_difference=data.get("deduction_difference", 0),
                other_adjustments=data.get("other_adjustments", 0),
                total_adjustments=data.get("total_adjustments", 0),
                two_jobs_value=data.get("two_jobs_value", 0),
                three_jobs_highest=data.get("three_jobs_highest", 0),
                three_jobs_third=data.get("three_jobs_third", 0),
                total_jobs_value=data.get("total_jobs_value", 0),
                per_period_value=data.get("per_period_value", 0)

            )
            send_pdf_via_gmail("filled/filled_w4.pdf")
        elif form == "W-8BEN":
            fill_w8ben_form(
                name=data.get("name", ""),
                country_citizenship=data.get("country_citizenship", ""),
                perm_address=data.get("perm_address", ""),
                perm_city_state_zip=data.get("perm_city_state_zip", ""),
                perm_country=data.get("perm_country", ""),
                mailing_address=data.get("mailing_address", ""),
                mailing_city_state_zip=data.get("mailing_city_state_zip", ""),
                mailing_country=data.get("mailing_country", ""),
                ssn_itin=data.get("ssn_itin", ""),
                foreign_tax_id=data.get("foreign_tax_id", ""),
                date_of_birth=data.get("date_of_birth", ""),
                country_residence=data.get("country_residence", ""),
                treaty_article=data.get("treaty_article", ""),
                withholding_rate=data.get("withholding_rate", 0),
                income_type=data.get("income_type", ""),
                treaty_article_cite=data.get("treaty_article_cite", ""),
                treaty_paragraph=data.get("treaty_paragraph", "")
            )
            send_pdf_via_gmail("filled/filled_w8ben.pdf")
        elif form == "1040":
            if data.get("dependents"):
                data["dependents"] = json.loads(data["dependents"])
            fill_1040_form(
                # Personal Information
                tax_year_begin=data.get("tax_year_begin", ""),
                tax_year_end=data.get("tax_year_end", ""),
                year_20=data.get("year_20", ""),
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                ssn=data.get("ssn", ""),
                spouse_first_name=data.get("spouse_first_name", ""),
                spouse_last_name=data.get("spouse_last_name", ""),
                spouse_ssn=data.get("spouse_ssn", ""),
                home_address=data.get("home_address", ""),
                apt_no=data.get("apt_no", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                zip_code=data.get("zip_code", ""),
                foreign_country=data.get("foreign_country", ""),
                foreign_province=data.get("foreign_province", ""),
                foreign_postal_code=data.get("foreign_postal_code", ""),
                mfs_spouse_name=data.get("mfs_spouse_name", ""),
                nonresident_spouse_name=data.get("nonresident_spouse_name", ""),

                # Filing Status and Elections
                filing_single=data.get("filing_single", False),
                filing_joint=data.get("filing_joint", False),
                filing_separate=data.get("filing_separate", False),
                nonresident_alien_spouse=data.get("nonresident_alien_spouse", False),
                you_election_fund=data.get("you_election_fund", False),
                spouse_election_fund=data.get("spouse_election_fund", False),

                # Digital Assets
                digital_assets_yes=data.get("digital_assets_yes", False),
                digital_assets_no=data.get("digital_assets_no", False),

                # Standard Deduction
                you_dependent=data.get("you_dependent", False),
                spouse_dependent=data.get("spouse_dependent", False),
                spouse_itemizes=data.get("spouse_itemizes", False),

                # Age/Blindness
                you_born_before_1960=data.get("you_born_before_1960", False),
                you_blind=data.get("you_blind", False),
                spouse_born_before_1960=data.get("spouse_born_before_1960", False),
                spouse_blind=data.get("spouse_blind", False),

                # Dependents
                more_than_four_dependents=data.get("more_than_four_dependents", False),
                dependents=data.get("dependents", []),

                # Dependent Tax Credits
                dependent_1_child_credit=data.get("dependent_1_child_credit", 0),
                dependent_1_other_credit=data.get("dependent_1_other_credit", 0),
                dependent_2_child_credit=data.get("dependent_2_child_credit", 0),
                dependent_2_other_credit=data.get("dependent_2_other_credit", 0),
                dependent_3_child_credit=data.get("dependent_3_child_credit", 0),
                dependent_3_other_credit=data.get("dependent_3_other_credit", 0),
                dependent_4_child_credit=data.get("dependent_4_child_credit", 0),
                dependent_4_other_credit=data.get("dependent_4_other_credit", 0),

                # Additional Elections
                lump_sum_election=data.get("lump_sum_election", False),
                capital_gain_no_schedule=data.get("capital_gain_no_schedule", False),

                # Income Information
                w2_income=data.get("w2_income", 0),
                household_wages=data.get("household_wages", 0),
                tip_income=data.get("tip_income", 0),
                medicaid_waiver=data.get("medicaid_waiver", 0),
                dependent_care_benefits=data.get("dependent_care_benefits", 0),
                adoption_benefits=data.get("adoption_benefits", 0),
                wages_8919=data.get("wages_8919", 0),
                other_earned_income=data.get("other_earned_income", 0),
                nontaxable_combat_pay=data.get("nontaxable_combat_pay", 0),
                total_income=data.get("total_income", 0),

                # Interest and Dividends
                tax_exempt_interest=data.get("tax_exempt_interest", 0),
                taxable_interest=data.get("taxable_interest", 0),
                qualified_dividends=data.get("qualified_dividends", 0),
                ordinary_dividends=data.get("ordinary_dividends", 0),

                # Retirement Income
                ira_distributions=data.get("ira_distributions", 0),
                ira_taxable_amount=data.get("ira_taxable_amount", 0),
                pensions_annuities=data.get("pensions_annuities", 0),
                pensions_taxable_amount=data.get("pensions_taxable_amount", 0),

                # Social Security Benefits
                social_security_benefits=data.get("social_security_benefits", 0),
                social_security_taxable=data.get("social_security_taxable", 0),

                # Additional Income
                capital_gain_loss=data.get("capital_gain_loss", 0),
                schedule_1_income=data.get("schedule_1_income", 0),
                total_income_all=data.get("total_income_all", 0),
                adjustments_to_income=data.get("adjustments_to_income", 0),
                adjusted_gross_income=data.get("adjusted_gross_income", 0),

                # Deductions
                standard_deduction=data.get("standard_deduction", 0),
                qbi_deduction=data.get("qbi_deduction", 0),
                total_deductions=data.get("total_deductions", 0),
                taxable_income=data.get("taxable_income", 0),

                # Tax and Credits
                tax_amount=data.get("tax_amount", 0),
                schedule_2_line_3=data.get("schedule_2_line_3", 0),
                total_tax=data.get("total_tax", 0),
                child_tax_credit=data.get("child_tax_credit", 0),
                schedule_3_line_8=data.get("schedule_3_line_8", 0),
                total_credits=data.get("total_credits", 0),
                tax_less_credits=data.get("tax_less_credits", 0),
                other_taxes=data.get("other_taxes", 0),
                total_tax_due=data.get("total_tax_due", 0),

                # Tax Forms Attachments
                form_8814_attached=data.get("form_8814_attached", False),
                form_4972_attached=data.get("form_4972_attached", False),
                other_form=data.get("other_form", ""),

                # Payments and Credits
                w2_withholding=data.get("w2_withholding", 0),
                form_1099_withholding=data.get("form_1099_withholding", 0),
                other_withholding=data.get("other_withholding", 0),
                total_withholding=data.get("total_withholding", 0),
                estimated_tax_payments=data.get("estimated_tax_payments", 0),
                earned_income_credit=data.get("earned_income_credit", 0),
                additional_child_tax_credit=data.get("additional_child_tax_credit", 0),
                american_opportunity_credit=data.get("american_opportunity_credit", 0),
                reserved_future=data.get("reserved_future", 0),
                schedule_3_line_15=data.get("schedule_3_line_15", 0),
                total_other_payments=data.get("total_other_payments", 0),
                total_payments=data.get("total_payments", 0),

                # Refund Information
                overpaid_amount=data.get("overpaid_amount", 0),
                refund_amount=data.get("refund_amount", 0),
                routing_number=data.get("routing_number", ""),
                account_number=data.get("account_number", ""),
                account_type_checking=data.get("account_type_checking", False),
                account_type_savings=data.get("account_type_savings", False),
                form_8888_attached=data.get("form_8888_attached", False),
                applied_to_estimated_tax=data.get("applied_to_estimated_tax", 0),
                amount_you_owe=data.get("amount_you_owe", 0),
                estimated_tax_penalty=data.get("estimated_tax_penalty", 0),

                # Third Party Designee
                third_party_designee=data.get("third_party_designee", False),
                designee_name=data.get("designee_name", ""),
                designee_phone=data.get("designee_phone", ""),
                designee_pin=data.get("designee_pin", ""),

                # Signature Information
                your_occupation=data.get("your_occupation", ""),
                your_identity_pin=data.get("your_identity_pin", ""),
                spouse_occupation=data.get("spouse_occupation", ""),
                spouse_identity_pin=data.get("spouse_identity_pin", ""),
                phone_number=data.get("phone_number", ""),
                email_address=data.get("email_address", ""),

                # Paid Preparer Information
                preparer_name=data.get("preparer_name", ""),
                preparer_ptin=data.get("preparer_ptin", ""),
                preparer_self_employed=data.get("preparer_self_employed", False),
                firm_name=data.get("firm_name", ""),
                firm_phone=data.get("firm_phone", ""),
                firm_address=data.get("firm_address", ""),
                firm_ein=data.get("firm_ein", "")
            )
            send_pdf_via_gmail("filled/filled_1040.pdf")
        elif form == "8863":
            fill_8863_form(
            # Basic Taxpayer Information
            taxpayer_name=data.get("taxpayer_name", ""),
            taxpayer_ssn=data.get("taxpayer_ssn", ""),
            
            # Part I - Credit Calculation
            tentative_credit=data.get("tentative_credit", 0),
            income_limit=data.get("income_limit", 0),
            modified_agi=data.get("modified_agi", 0),
            income_difference=data.get("income_difference", 0),
            phase_out_amount=data.get("phase_out_amount", 0),
            decimal_amount_1000=data.get("decimal_amount_1000", 0),
            decimal_amount_other=data.get("decimal_amount_other", 0),
            multiply_result=data.get("multiply_result", 0),
            refundable_credit=data.get("refundable_credit", 0),
            credit_limit=data.get("credit_limit", 0),
            
            # Part II - Nonrefundable Education Credits
            total_expenses=data.get("total_expenses", 0),
            smaller_amount=data.get("smaller_amount", 0),
            multiply_20_percent=data.get("multiply_20_percent", 0),
            married_limit=data.get("married_limit", 0),
            form_1040_amount=data.get("form_1040_amount", 0),
            subtract_result=data.get("subtract_result", 0),
            filing_status_amount=data.get("filing_status_amount", 0),
            decimal_amount_2_1000=data.get("decimal_amount_2_1000", 0),
            decimal_amount_2_other=data.get("decimal_amount_2_other", 0),
            multiply_final=data.get("multiply_final", 0),
            nonrefundable_credits=data.get("nonrefundable_credits", 0),
            
            # Part III - Student Information
            student_name=data.get("student_name", ""),
            student_ssn=data.get("student_ssn", ""),
            student_ssn_2=data.get("student_ssn_2", ""),
            
            # First Educational Institution
            institution_1_name=data.get("institution_1_name", ""),
            institution_1_address=data.get("institution_1_address", ""),
            institution_1_ein=data.get("institution_1_ein", ""),
            
            # Second Educational Institution
            institution_2_name=data.get("institution_2_name", ""),
            institution_2_address=data.get("institution_2_address", ""),
            institution_2_ein=data.get("institution_2_ein", ""),
            
            # Part III - American Opportunity Credit
            qualified_expenses=data.get("qualified_expenses", 0),
            expenses_minus_2000=data.get("expenses_minus_2000", 0),
            multiply_25_percent=data.get("multiply_25_percent", 0),
            final_amount=data.get("final_amount", 0),
            lifetime_learning_credit=data.get("lifetime_learning_credit", 0),
            
            # Checkboxes for Student Status
            under_24=data.get("under_24", False),
            
            # Institution 1 Form 1098-T
            received_1098t_inst1=data.get("received_1098t_inst1", False),
            box_7_checked_inst1=data.get("box_7_checked_inst1", False),
            
            # Institution 2 Form 1098-T
            received_1098t_inst2=data.get("received_1098t_inst2", False),
            box_7_checked_inst2=data.get("box_7_checked_inst2", False),
            
            # Additional Eligibility Conditions
            aoc_claimed_prior=data.get("aoc_claimed_prior", False),
            half_time_enrollment=data.get("half_time_enrollment", False),
            completed_first_4_years=data.get("completed_first_4_years", False),
            felony_drug_conviction=data.get("felony_drug_conviction", False)
        )
            send_pdf_via_gmail("filled/filled_form_8863.pdf")
        elif form == "8843":
            fill_8843_form(
            # Part 1 - Personal Information
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            us_tax_id=data.get("us_tax_id", ""),
            foreign_address=data.get("foreign_address", ""),
            us_address=data.get("us_address", ""),
            
            # Part 1 - Visa Status
            current_visa=data.get("current_visa", ""),
            current_status=data.get("current_status", ""),
            citizenship_countries=data.get("citizenship_countries", ""),
            passport_countries=data.get("passport_countries", ""),
            passport_numbers=data.get("passport_numbers", ""),
            
            # Part 1 - Days Present
            days_2024=data.get("days_2024", 0),
            days_2023=data.get("days_2023", 0),
            days_2022=data.get("days_2022", 0),
            excluded_days=data.get("excluded_days", 0),
            
            # Part 1 - Tax Year
            year_start=data.get("year_start", ""),
            year_end=data.get("year_end", ""),
            alt_year=data.get("alt_year", ""),
            
            # Part 2 - Teachers/Researchers
            teacher_institution=data.get("teacher_institution", ""),
            teacher_address=data.get("teacher_address", ""),
            teacher_phone=data.get("teacher_phone", ""),
            teacher_director=data.get("teacher_director", ""),
            teacher_dir_address=data.get("teacher_dir_address", ""),
            teacher_dir_phone=data.get("teacher_dir_phone", ""),
            
            # Part 2 - Teacher Visa History
            teacher_visa_2018=data.get("teacher_visa_2018", ""),
            teacher_visa_2019=data.get("teacher_visa_2019", ""),
            teacher_visa_2020=data.get("teacher_visa_2020", ""),
            teacher_visa_2021=data.get("teacher_visa_2021", ""),
            teacher_visa_2022=data.get("teacher_visa_2022", ""),
            teacher_visa_2023=data.get("teacher_visa_2023", ""),
            
            # Part 3 - Students
            student_institution=data.get("student_institution", ""),
            student_address=data.get("student_address", ""),
            student_phone=data.get("student_phone", ""),
            student_director=data.get("student_director", ""),
            student_dir_address=data.get("student_dir_address", ""),
            student_dir_phone=data.get("student_dir_phone", ""),
            
            # Part 3 - Student Visa History
            student_visa_2018=data.get("student_visa_2018", ""),
            student_visa_2019=data.get("student_visa_2019", ""),
            student_visa_2020=data.get("student_visa_2020", ""),
            student_visa_2021=data.get("student_visa_2021", ""),
            student_visa_2022=data.get("student_visa_2022", ""),
            student_visa_2023=data.get("student_visa_2023", ""),
            
            # Eligibility Questions
            exempt_2years=data.get("exempt_2years", False),
            exempt_5years=data.get("exempt_5years", False),
            permanent_residence=data.get("permanent_residence", False),
            
            # Permanent Residence Explanation
            residence_explain_1=data.get("residence_explain_1", ""),
            residence_explain_2=data.get("residence_explain_2", ""),
            residence_explain_3=data.get("residence_explain_3", ""),
            
            # Part 4 - Professional Athletes
            sports_event_1=data.get("sports_event_1", ""),
            sports_event_2=data.get("sports_event_2", ""),
            sports_event_3=data.get("sports_event_3", ""),
            charity_org_1=data.get("charity_org_1", ""),
            charity_org_2=data.get("charity_org_2", ""),
            charity_org_3=data.get("charity_org_3", ""),
            
            # Part 5 - Medical Condition
            medical_desc_1=data.get("medical_desc_1", ""),
            medical_desc_2=data.get("medical_desc_2", ""),
            medical_desc_3=data.get("medical_desc_3", ""),
            medical_desc_4=data.get("medical_desc_4", ""),
            intended_leave_date=data.get("intended_leave_date", ""),
            actual_leave_date=data.get("actual_leave_date", "")
        )
            send_pdf_via_gmail("filled/filled_form_8843.pdf")
        return "Form filled successfully"
    except Exception as e:
        print(e)
        return str(e)
