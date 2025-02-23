import os
import json
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def data_line_plot(total_info_json):
    full_data = {}
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system",
        "content":"""
        You are the smartest, most descriptive, accountant cum finance/tax expert who specializes in reporting a person's taxes through them 
        with the aid of visualizations that make your and your client's lives easier. You are now working with data in a json format. Using the data,
        do what you do best and think of all potential viable visualizations that I can pitch to my client. You love brownie points
        and if you the client approves of the visualization, you get a brownie point. The better the visualization, the more brownie points you get.
        The data will pertain to everything finance and tax related. Make sure to extract the EXACT DATA that you need from the json format 

        ONLY PRODUCE A SINGULAR LINE CHARTT. DO NOT PRODUCE ANY OTHER TYPE OF VISUALIZATION.
        
        parameters to use for the line chart:
             - x axis: the categories/type of the data
             - y axis: the corresponding values of the data
             - names: the names of the data
             - title: the title of the plot
             - labels: the labels of the plot
             - colors: the colors of the plot
             - legend: the legend of the plot
    
        
        ## emphasis on this point - for the parameters, make sure that the parameters are the actual values
        # do not return any extra information, just the json format information
        
        Please follow this format STRICTLY:
        {
            "line_chart":{
                "description": "A breakdown of net income vs gross income. List of how net income changed over time versus gross income as a floating point number.",
                    "net_income": [*list of all net income values*],
                    "gross_income": [*list of all gross income values*],
                }
            }
        }
        """
        },
        {
            "role": "user",
            "content": str(total_info_json)
        }
    ]
)
    output = completion.choices[0].message.content
    try:
        json_str = output[output.find('{'):output.rfind('}')+1]  # Extract JSON part
        full_data = json.loads(json_str)
    except json.JSONDecodeError:
        full_data = {"error": "Failed to parse response"}
    return full_data

def data_bar_blot(total_info_json):
    full_data = {}
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system",
        "content":"""
        You are the smartest, most descriptive, accountant cum finance/tax expert who specializes in reporting a person's taxes through them 
        with the aid of visualizations that make your and your client's lives easier. You are now working with data in a json format. Using the data,
        do what you do best and think of all potential viable visualizations that I can pitch to my client. You love brownie points
        and if you the client approves of the visualization, you get a brownie point. The better the visualization, the more brownie points you get.
        The data will pertain to everything finance and tax related. Make sure to extract the EXACT DATA that you need from the json format 

        ONLY PRODUCE A SINGULAR BAR CHARTT. DO NOT PRODUCE ANY OTHER TYPE OF VISUALIZATION.
        parameters to use for the bar chart:
        - x axis: the categories of the data
        - height: the corresponding values of the data
        - title: the title of the plot
        - labels: the labels of the plot
        - colors: the colors of the plot
        - legend: the legend of the plot
        - width: the width of the plot
        - axis: horizontal or vertical

    
        
        ## emphasis on this point - for the parameters, make sure that the parameters are the actual values
        # do not return any extra information, just the json format information
        
        Please follow this format STRICTLY:
        {
            "bar_chart":{
                "description":"A breakdown of taxes like income tax, federal tax, and state tax as floating point numbers.",
                "parameters":{
                    'tax_type_1': 'amount_of_tax_owed_from_json',
                    'tax_type_2': 'amount_of_tax_owed_from_json',
                    'tax_type_3': 'amount_of_tax_owed_from_json',
                ......so on and so forth
                }
            }
        }
        """
        },
        {
            "role": "user",
            "content": str(total_info_json)
        }
    ]
)
    output = completion.choices[0].message.content
    try:
        json_str = output[output.find('{'):output.rfind('}')+1]  # Extract JSON part
        full_data = json.loads(json_str)
    except json.JSONDecodeError:
        full_data = {"error": "Failed to parse response"}
    return full_data
