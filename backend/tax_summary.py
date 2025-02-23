from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_tax_summary(tax_data):
    """
    Generate a comprehensive tax summary using OpenAI based on the extracted tax data.
    """
    try:
        # Create a well-structured prompt for the LLM
        prompt = f"""As an expert tax advisor, analyze the following tax data and provide a direct, specific tax summary with concrete recommendations. Use definitive language and exact figures whenever possible.
        
        Tax Data:
        {tax_data}

        You must respond with a valid JSON object containing two main sections:
        1. A detailed summary section with thorough analysis of all tax aspects
        2. A prioritized list of recommended documents needed for better analysis

        Your response must be a valid JSON object with this exact structure:
        {{
            "summary": {{
                "overview": {{
                    "total_income": "Your total income for the tax year is £X. This includes £Y from salary and £Z from other sources.",
                    "filing_status": "Based on your circumstances, you should file as X. This is optimal because Y.",
                    "tax_bracket": "You fall in the X% tax bracket for income between £Y and £Z."
                }},
                "implications": {{
                    "tax_liability": "Your estimated tax liability is £X, calculated as follows: Y",
                    "marginal_rate": "Your marginal tax rate is X%. This means each additional pound earned is taxed at Y%",
                    "state_tax_impact": "Your state tax obligation is X% based on Y"
                }},
                "deductions": {{
                    "standard_vs_itemized": "You should take the X deduction because Y. This will save you £Z.",
                    "available_deductions": "You qualify for the following deductions: X, Y, Z",
                    "estimated_savings": "These deductions will save you approximately £X"
                }},
                "credits": {{
                    "eligible_credits": "You qualify for X, Y, and Z credits",
                    "requirements": "To claim these credits, you need X, Y, Z",
                    "estimated_benefit": "These credits will reduce your tax by £X"
                }},
                "deadlines": {{
                    "filing_deadline": "Your next important deadline is DATE for REASON. You must complete X by this date.",
                    "estimated_tax": "Your next estimated tax payment of £X is due on Y",
                    "extension_options": "You can extend until X by doing Y"
                }},
                "recommendations": {{
                    "immediate_actions": "Your most important next step is: X. This will help you Y.",
                    "tax_planning": "Implement these strategies: X, Y, Z",
                    "savings_opportunities": "You can save £X by doing Y"
                }},
                "concerns": {{
                    "risk_areas": "These items need attention: X, Y, Z",
                    "missing_information": "You must provide X, Y, Z",
                    "compliance_issues": "Address these compliance requirements: X, Y, Z"
                }},
                "retirement_planning": {{
                    "contribution_limits": "You can contribute up to £X to your retirement accounts",
                    "tax_advantages": "This will save you £X in taxes this year",
                    "recommendations": "Maximize your contributions by doing X, Y, Z"
                }},
                "investment_tax": {{
                    "capital_gains": "Your capital gains tax rate is X%. This applies to £Y in gains",
                    "loss_harvesting": "You can offset £X in gains by harvesting losses",
                    "investment_strategies": "Implement these tax-efficient strategies: X, Y, Z"
                }}
            }},
            "recommended_documents": [
                {{
                    "type": "string",
                    "name": "Document name",
                    "description": "Specific reason why this document is needed",
                    "priority": "high|medium|low",
                    "deadline": "Submit by X to ensure Y"
                }}
            ]
        }}

        Important Guidelines:
        - Always include exact monetary values with pound signs (£)
        - Format all monetary values with proper commas and decimals (e.g., £1,234.56)
        - For the overview section, ensure total_income, filing_status, and tax_bracket are always present
        - For deadlines, always specify exact dates in DD/MM/YYYY format
        - For immediate_actions, provide one clear, specific action
        - Use direct, definitive language
        - Keep explanations clear and professional
        - Focus on definitive statements rather than possibilities
        - Ensure all JSON fields are present even if data is limited"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a tax advisor providing analysis in JSON format. Always respond with valid JSON that matches the specified structure exactly. Do not include any text before or after the JSON object. Do not use markdown or special formatting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        # Parse the response to verify it's valid JSON before returning
        import json
        content = response.choices[0].message.content
        parsed_content = json.loads(content)  # Verify JSON is valid
        
        return {
            "summary": content,
            "status": "success"
        }
    except Exception as e:
        print(f"Error generating tax summary: {str(e)}")
        return {
            "summary": "Error generating tax summary. Please try again later.",
            "status": "error",
            "error": str(e)
        } 