import os
import json
from anthropic import Anthropic

def anomaly_detection(json_data):
    '''
    Function to detect anomalies in the data

    checks for common fields in the data provided upon inserting forms on website and tallies them to check whether the numbers match
    uses Claude wrapper to prevent having to check manually each field
    takes in json data and returns a json object with the anomalies detected
    '''

    try:
        # Initialize Anthropic client
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # System prompt as a separate parameter
        system_prompt = """
You are a tax data anomaly detection tool, the best in the world. You are trained on data from the IRS and other tax authorities. 
You are given a JSON object containing tax data. Your task is to analyze this data for anomalies and return ONLY a JSON response. 
Do NOT hallucinate. Follow the following format:
    {
    "anomalies": [
        {
            "field": "field_name",
            "anomaly_type": "anomaly_type",
            "description": "description of the anomaly"
        },
        ...
    ]
}
"""

        # Create the completion using Claude
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=system_prompt,  # System prompt as a separate parameter
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this tax data for anomalies and return ONLY a JSON response: {json.dumps(json_data)}"
                }
            ],
            temperature=0.3
        )
        
        output = message.content[0].text.strip()
        
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