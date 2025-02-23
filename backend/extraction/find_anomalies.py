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

    try:
        completion = client.chat.completions.create(
            model="gpt-4",  # Changed from gpt-4o to gpt-4
            messages=[
                {
                    "role": "system", 
                    "content": """You are an expert financial data analyst with exceptional attention to detail. Your task is to analyze financial JSON data files and identify discrepancies or anomalies between related fields across documents. 

Key Requirements:
1. Compare matching fields across all provided documents and identify any inconsistencies
2. Generate a detailed anomaly report in JSON format
3. Only include fields with detected anomalies in the output
4. For numerical values, calculate and show the differences
5. For non-numerical identifiers (like EIN, account numbers), simply indicate "mismatch detected"
6. For scenarios where like net pay, calculate the total tax and then subtract. Do some mathematical operations yourself, be flexible like a human

Output Format:
{
    "field_with_anomaly": {
        "source_details": {
            "document_1": {
                "value": "<value>",
                "metadata": "<relevant context>"
            },
            "document_2": {
                "value": "<value>",
                "metadata": "<relevant context>"
            }
        },
        "anomaly_details": {
            "type": "numerical_difference",
            "difference": "<calculated difference for numerical values>",
            "description": "<clear explanation of the anomaly>"
        }
    }
}

IMPORTANT: 
1. Return ONLY valid JSON data
2. Do not include any markdown formatting or additional text
3. Ensure all values are properly quoted in the JSON
4. Make sure the response is a complete, valid JSON object"""
                },
                {
                    "role": "user",
                    "content": f"Analyze this tax data for anomalies and return ONLY a JSON response: {json.dumps(json_data)}"
                }
            ],
            temperature=0.2  # Lower temperature for more consistent output
        )
        
        output = completion.choices[0].message.content.strip()
        
        # Remove any potential markdown formatting
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "```" in output:
            output = output.split("```")[1].split("```")[0].strip()
            
        # Ensure we have a valid JSON string
        if not output.startswith("{"):
            print("Invalid JSON format, missing opening brace")
            return {}
            
        if not output.endswith("}"):
            print("Invalid JSON format, missing closing brace")
            return {}
            
        # Parse the JSON
        try:
            anomalies = json.loads(output)
            if not isinstance(anomalies, dict):
                print("Invalid response format: not a dictionary")
                return {}
            return anomalies
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            print(f"Raw output: {output}")
            return {}
            
    except Exception as e:
        print(f"Error in anomaly detection: {str(e)}")
        return {}
