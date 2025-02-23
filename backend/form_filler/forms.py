from .form_w9 import fill_w9_form
from .form_w4 import fill_w4_form
from .form_w8ben import fill_w8ben_form
from .form_1040 import fill_1040_form
from .form_8863 import fill_8863_form
from .form_8843 import fill_8843_form
import json 
def el_filler(form, data):
    try:
        print("filling form: " + form)
        print(form)
        print(data)
        if form == "W-9":
            fill_w9_form(
                name=data["name"],
                business_name=data["business_name"],
                tax_classification=data["tax_classification"],
                llc_classification=data["llc_classification"],
                address=data["address"],
                city_state_zip=data["city_state_zip"],
                exempt_payee_code=data["exempt_payee_code"],
                fatca_code=data["fatca_code"],
                requester_info=data["requester_info"],
                account_numbers=data["account_numbers"],
                ssn_first=data["ssn_first"],
                ssn_second=data["ssn_second"],
                ssn_third=data["ssn_third"],
                ein_first=data["ein_first"],
                ein_second=data["ein_second"]
            )
        elif form == "W-4":
            print("enetring w4")
            fill_w4_form(
                first_middle_name= data["first_middle_name"],
                last_name= data["last_name"],
                address= data["address"],
                city_state_zip= data["city_state_zip"],
                single_or_married_filing_separately= data["single_or_married_filing_separately"],
                married_filing_jointly= data["married_filing_jointly"],
                head_of_household= data["head_of_household"],
                two_jobs_only= data["two_jobs_only"],
                ssn= data["ssn"],
                child_tax_credits= data["child_tax_credits"],
                dependent_credits= data["dependent_credits"],
                total_credits= data["total_credits"],
                other_income= data["other_income"],
                deductions= data["deductions"],
                extra_withholding= data["extra_withholding"],
                employer_info= data["employer_info"],
                employment_date= data["employment_date"],
                employer_ein= data["employer_ein"],
                pay_periods= data["pay_periods"],
                itemized_deductions= data["itemized_deductions"],
                standard_deduction= data["standard_deduction"],
                deduction_difference= data["deduction_difference"],
                other_adjustments= data["other_adjustments"],
                total_adjustments= data["total_adjustments"],
                two_jobs_value= data["two_jobs_value"],
                three_jobs_highest= data["three_jobs_highest"],
                three_jobs_third= data["three_jobs_third"],
                total_jobs_value= data["total_jobs_value"],
                per_period_value= data["per_period_value"]

            )
        elif form == "W-8BEN":
            fill_w8ben_form(
                name=data["name"],
                country_citizenship=data["country_citizenship"],
                perm_address=data["perm_address"],
                perm_city_state_zip=data["perm_city_state_zip"],
                perm_country=data["perm_country"],
                mailing_address=data["mailing_address"],
                mailing_city_state_zip=data["mailing_city_state_zip"],
                mailing_country=data["mailing_country"],
                ssn_itin=data["ssn_itin"],
                foreign_tax_id=data["foreign_tax_id"],
                date_of_birth=data["date_of_birth"],
                country_residence=data["country_residence"],
                treaty_article=data["treaty_article"],
                withholding_rate=data["withholding_rate"],
                income_type=data["income_type"],
                treaty_article_cite=data["treaty_article_cite"],
                treaty_paragraph=data["treaty_paragraph"]
            )
        elif form == "1040":
            if data["dependents"]:
                data["dependents"] = json.loads(data["dependents"])
            fill_1040_form(
                # Personal Information
                tax_year_begin=data["tax_year_begin"],
                tax_year_end=data["tax_year_end"],
                year_20=data["year_20"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                ssn=data["ssn"],
                spouse_first_name=data["spouse_first_name"],
                spouse_last_name=data["spouse_last_name"],
                spouse_ssn=data["spouse_ssn"],
                home_address=data["home_address"],
                apt_no=data["apt_no"],
                city=data["city"],
                state=data["state"],
                zip_code=data["zip_code"],
                foreign_country=data["foreign_country"],
                foreign_province=data["foreign_province"],
                foreign_postal_code=data["foreign_postal_code"],
                mfs_spouse_name=data["mfs_spouse_name"],
                nonresident_spouse_name=data["nonresident_spouse_name"],

                # Filing Status and Elections
                filing_single=data["filing_single"],
                filing_joint=data["filing_joint"],
                filing_separate=data["filing_separate"],
                nonresident_alien_spouse=data["nonresident_alien_spouse"],
                you_election_fund=data["you_election_fund"],
                spouse_election_fund=data["spouse_election_fund"],

                # Digital Assets
                digital_assets_yes=data["digital_assets_yes"],
                digital_assets_no=data["digital_assets_no"],

                # Standard Deduction
                you_dependent=data["you_dependent"],
                spouse_dependent=data["spouse_dependent"],
                spouse_itemizes=data["spouse_itemizes"],

                # Age/Blindness
                you_born_before_1960=data["you_born_before_1960"],
                you_blind=data["you_blind"],
                spouse_born_before_1960=data["spouse_born_before_1960"],
                spouse_blind=data["spouse_blind"],

                # Dependents
                more_than_four_dependents=data["more_than_four_dependents"],
                dependents=data["dependents"],

                # Dependent Tax Credits
                dependent_1_child_credit=data["dependent_1_child_credit"],
                dependent_1_other_credit=data["dependent_1_other_credit"],
                dependent_2_child_credit=data["dependent_2_child_credit"],
                dependent_2_other_credit=data["dependent_2_other_credit"],
                dependent_3_child_credit=data["dependent_3_child_credit"],
                dependent_3_other_credit=data["dependent_3_other_credit"],
                dependent_4_child_credit=data["dependent_4_child_credit"],
                dependent_4_other_credit=data["dependent_4_other_credit"],

                # Additional Elections
                lump_sum_election=data["lump_sum_election"],
                capital_gain_no_schedule=data["capital_gain_no_schedule"],

                # Income Information
                w2_income=data["w2_income"],
                household_wages=data["household_wages"],
                tip_income=data["tip_income"],
                medicaid_waiver=data["medicaid_waiver"],
                dependent_care_benefits=data["dependent_care_benefits"],
                adoption_benefits=data["adoption_benefits"],
                wages_8919=data["wages_8919"],
                other_earned_income=data["other_earned_income"],
                nontaxable_combat_pay=data["nontaxable_combat_pay"],
                total_income=data["total_income"],

                # Interest and Dividends
                tax_exempt_interest=data["tax_exempt_interest"],
                taxable_interest=data["taxable_interest"],
                qualified_dividends=data["qualified_dividends"],
                ordinary_dividends=data["ordinary_dividends"],

                # Retirement Income
                ira_distributions=data["ira_distributions"],
                ira_taxable_amount=data["ira_taxable_amount"],
                pensions_annuities=data["pensions_annuities"],
                pensions_taxable_amount=data["pensions_taxable_amount"],

                # Social Security Benefits
                social_security_benefits=data["social_security_benefits"],
                social_security_taxable=data["social_security_taxable"],

                # Additional Income
                capital_gain_loss=data["capital_gain_loss"],
                schedule_1_income=data["schedule_1_income"],
                total_income_all=data["total_income_all"],
                adjustments_to_income=data["adjustments_to_income"],
                adjusted_gross_income=data["adjusted_gross_income"],

                # Deductions
                standard_deduction=data["standard_deduction"],
                qbi_deduction=data["qbi_deduction"],
                total_deductions=data["total_deductions"],
                taxable_income=data["taxable_income"],

                # Tax and Credits
                tax_amount=data["tax_amount"],
                schedule_2_line_3=data["schedule_2_line_3"],
                total_tax=data["total_tax"],
                child_tax_credit=data["child_tax_credit"],
                schedule_3_line_8=data["schedule_3_line_8"],
                total_credits=data["total_credits"],
                tax_less_credits=data["tax_less_credits"],
                other_taxes=data["other_taxes"],
                total_tax_due=data["total_tax_due"],

                # Tax Forms Attachments
                form_8814_attached=data["form_8814_attached"],
                form_4972_attached=data["form_4972_attached"],
                other_form=data["other_form"],

                # Payments and Credits
                w2_withholding=data["w2_withholding"],
                form_1099_withholding=data["form_1099_withholding"],
                other_withholding=data["other_withholding"],
                total_withholding=data["total_withholding"],
                estimated_tax_payments=data["estimated_tax_payments"],
                earned_income_credit=data["earned_income_credit"],
                additional_child_tax_credit=data["additional_child_tax_credit"],
                american_opportunity_credit=data["american_opportunity_credit"],
                reserved_future=data["reserved_future"],
                schedule_3_line_15=data["schedule_3_line_15"],
                total_other_payments=data["total_other_payments"],
                total_payments=data["total_payments"],

                # Refund Information
                overpaid_amount=data["overpaid_amount"],
                refund_amount=data["refund_amount"],
                routing_number=data["routing_number"],
                account_number=data["account_number"],
                account_type_checking=data["account_type_checking"],
                account_type_savings=data["account_type_savings"],
                form_8888_attached=data["form_8888_attached"],
                applied_to_estimated_tax=data["applied_to_estimated_tax"],
                amount_you_owe=data["amount_you_owe"],
                estimated_tax_penalty=data["estimated_tax_penalty"],

                # Third Party Designee
                third_party_designee=data["third_party_designee"],
                designee_name=data["designee_name"],
                designee_phone=data["designee_phone"],
                designee_pin=data["designee_pin"],

                # Signature Information
                your_occupation=data["your_occupation"],
                your_identity_pin=data["your_identity_pin"],
                spouse_occupation=data["spouse_occupation"],
                spouse_identity_pin=data["spouse_identity_pin"],
                phone_number=data["phone_number"],
                email_address=data["email_address"],

                # Paid Preparer Information
                preparer_name=data["preparer_name"],
                preparer_ptin=data["preparer_ptin"],
                preparer_self_employed=data["preparer_self_employed"],
                firm_name=data["firm_name"],
                firm_phone=data["firm_phone"],
                firm_address=data["firm_address"],
                firm_ein=data["firm_ein"]
            )
        elif form == "8863":
            fill_8863_form(
            # Basic Taxpayer Information
            taxpayer_name=data["taxpayer_name"],
            taxpayer_ssn=data["taxpayer_ssn"],
            
            # Part I - Credit Calculation
            tentative_credit=data["tentative_credit"],
            income_limit=data["income_limit"],
            modified_agi=data["modified_agi"],
            income_difference=data["income_difference"],
            phase_out_amount=data["phase_out_amount"],
            decimal_amount_1000=data["decimal_amount_1000"],
            decimal_amount_other=data["decimal_amount_other"],
            multiply_result=data["multiply_result"],
            refundable_credit=data["refundable_credit"],
            credit_limit=data["credit_limit"],
            
            # Part II - Nonrefundable Education Credits
            total_expenses=data["total_expenses"],
            smaller_amount=data["smaller_amount"],
            multiply_20_percent=data["multiply_20_percent"],
            married_limit=data["married_limit"],
            form_1040_amount=data["form_1040_amount"],
            subtract_result=data["subtract_result"],
            filing_status_amount=data["filing_status_amount"],
            decimal_amount_2_1000=data["decimal_amount_2_1000"],
            decimal_amount_2_other=data["decimal_amount_2_other"],
            multiply_final=data["multiply_final"],
            nonrefundable_credits=data["nonrefundable_credits"],
            
            # Part III - Student Information
            student_name=data["student_name"],
            student_ssn=data["student_ssn"],
            student_ssn_2=data["student_ssn_2"],
            
            # First Educational Institution
            institution_1_name=data["institution_1_name"],
            institution_1_address=data["institution_1_address"],
            institution_1_ein=data["institution_1_ein"],
            
            # Second Educational Institution
            institution_2_name=data["institution_2_name"],
            institution_2_address=data["institution_2_address"],
            institution_2_ein=data["institution_2_ein"],
            
            # Part III - American Opportunity Credit
            qualified_expenses=data["qualified_expenses"],
            expenses_minus_2000=data["expenses_minus_2000"],
            multiply_25_percent=data["multiply_25_percent"],
            final_amount=data["final_amount"],
            lifetime_learning_credit=data["lifetime_learning_credit"],
            
            # Checkboxes for Student Status
            under_24=data["under_24"],
            
            # Institution 1 Form 1098-T
            received_1098t_inst1=data["received_1098t_inst1"],
            box_7_checked_inst1=data["box_7_checked_inst1"],
            
            # Institution 2 Form 1098-T
            received_1098t_inst2=data["received_1098t_inst2"],
            box_7_checked_inst2=data["box_7_checked_inst2"],
            
            # Additional Eligibility Conditions
            aoc_claimed_prior=data["aoc_claimed_prior"],
            half_time_enrollment=data["half_time_enrollment"],
            completed_first_4_years=data["completed_first_4_years"],
            felony_drug_conviction=data["felony_drug_conviction"]
        )
        elif form == "8843":
            fill_8843_form(
            # Part 1 - Personal Information
            first_name=data["first_name"],
            last_name=data["last_name"],
            us_tax_id=data["us_tax_id"],
            foreign_address=data["foreign_address"],
            us_address=data["us_address"],
            
            # Part 1 - Visa Status
            current_visa=data["current_visa"],
            current_status=data["current_status"],
            citizenship_countries=data["citizenship_countries"],
            passport_countries=data["passport_countries"],
            passport_numbers=data["passport_numbers"],
            
            # Part 1 - Days Present
            days_2024=data["days_2024"],
            days_2023=data["days_2023"],
            days_2022=data["days_2022"],
            excluded_days=data["excluded_days"],
            
            # Part 1 - Tax Year
            year_start=data["year_start"],
            year_end=data["year_end"],
            alt_year=data["alt_year"],
            
            # Part 2 - Teachers/Researchers
            teacher_institution=data["teacher_institution"],
            teacher_address=data["teacher_address"],
            teacher_phone=data["teacher_phone"],
            teacher_director=data["teacher_director"],
            teacher_dir_address=data["teacher_dir_address"],
            teacher_dir_phone=data["teacher_dir_phone"],
            
            # Part 2 - Teacher Visa History
            teacher_visa_2018=data["teacher_visa_2018"],
            teacher_visa_2019=data["teacher_visa_2019"],
            teacher_visa_2020=data["teacher_visa_2020"],
            teacher_visa_2021=data["teacher_visa_2021"],
            teacher_visa_2022=data["teacher_visa_2022"],
            teacher_visa_2023=data["teacher_visa_2023"],
            
            # Part 3 - Students
            student_institution=data["student_institution"],
            student_address=data["student_address"],
            student_phone=data["student_phone"],
            student_director=data["student_director"],
            student_dir_address=data["student_dir_address"],
            student_dir_phone=data["student_dir_phone"],
            
            # Part 3 - Student Visa History
            student_visa_2018=data["student_visa_2018"],
            student_visa_2019=data["student_visa_2019"],
            student_visa_2020=data["student_visa_2020"],
            student_visa_2021=data["student_visa_2021"],
            student_visa_2022=data["student_visa_2022"],
            student_visa_2023=data["student_visa_2023"],
            
            # Eligibility Questions
            exempt_2years=data["exempt_2years"],
            exempt_5years=data["exempt_5years"],
            permanent_residence=data["permanent_residence"],
            
            # Permanent Residence Explanation
            residence_explain_1=data["residence_explain_1"],
            residence_explain_2=data["residence_explain_2"],
            residence_explain_3=data["residence_explain_3"],
            
            # Part 4 - Professional Athletes
            sports_event_1=data["sports_event_1"],
            sports_event_2=data["sports_event_2"],
            sports_event_3=data["sports_event_3"],
            charity_org_1=data["charity_org_1"],
            charity_org_2=data["charity_org_2"],
            charity_org_3=data["charity_org_3"],
            
            # Part 5 - Medical Condition
            medical_desc_1=data["medical_desc_1"],
            medical_desc_2=data["medical_desc_2"],
            medical_desc_3=data["medical_desc_3"],
            medical_desc_4=data["medical_desc_4"],
            intended_leave_date=data["intended_leave_date"],
            actual_leave_date=data["actual_leave_date"]
        )
        return "Form filled successfully"
    except Exception as e:
        print(e)
        return str(e)
