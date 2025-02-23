import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def anomaly_detection(json_data):
    '''
    Function to detect anomalies in the data

    checks for common fields in the data provided upon inserting forms on webiste and tallies them to check whether the numbers match
    uses gpt wrapper prevent having to check manually each field
    takes in json data and returns a json object with the anomalies detected
    '''

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": 
                """
                    You are an expert financial data analyst with exceptional attention to detail. Your task is to analyze financial JSON data files and identify discrepancies or anomalies between related fields across documents. 

Key Requirements:

1. Compare matching fields across all provided documents and identify any inconsistencies
2. Generate a detailed anomaly report in JSON format
3. Only include fields with detected anomalies in the output
4. For numerical values, calculate and show the differences
5. For non-numerical identifiers (like EIN, account numbers), simply indicate "mismatch detected"
6. For scenarios where like net pay, calculate the total tax and then subtract. Do some mathematical operations yourself, be flexible like a humna

Output Format:
{
    "field_with_anomaly": {
        "source_details": {
            "document_1": {
                "value": <value>,
                "metadata": <relevant context>
            },
            "document_2": {
                "value": <value>,
                "metadata": <relevant context>
            }
        },
        "anomaly_details": {
            "type": "numerical_difference" | "mismatch",
            "difference": <calculated difference for numerical values>,
            "description": <clear explanation of the anomaly>
        }
    }
}

Example:
{
    "annual_salary": {
        "source_details": {
            "w2_form": {
                "value": 75000,
                "reporting_year": "2024"
            },
            "employment_contract": {
                "value": 80000,
                "effective_date": "2024-01-01"
            }
        },
        "anomaly_details": {
            "type": "numerical_difference",
            "difference": 5000,
            "description": "Salary amount differs between W2 and employment contract"
        }
    },
    "employer_id": {
        "source_details": {
            "w2_form": {
                "value": "12-3456789"
            },
            "1099_form": {
                "value": "12-3456780"
            }
        },
        "anomaly_details": {
            "type": "mismatch",
            "description": "EIN does not match across tax documents"
        }
    }
}"
                """
            },
            {
                "role": "user",
                "content": str(json_data)
            }
        ]
    )
    output = completion.choices[0].message.content
    return json.loads(output[7:len(output)-3])
