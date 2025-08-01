from openai import OpenAI
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2
import os
from dotenv import load_dotenv


load_dotenv(override=True)
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

messages=[{
             'role': 'system',
                'content': f""""
                You are a tax agent and we are fillion out a form. You will be given the syntax of the form to be filled.
                The user has provided some information and you need to fill out all the fields that you can and replace the rest with "NEEDS INFO" 
                Return a string in the original format and do not remove the comment explanation for each field as these explanations are required by the agent who is filling out the forms
                Make sure you do not infer anything. Only fill out fields that look relly similar
                Exactly return the string in the format as given in the syntax
                """
            }]

def get_formatted_syntax(syntax, user_data):
    # formatted_user_query = f"""
    #     This is the Syntax of the form:\n
    #     {syntax}

    #     The is the information provided by the user:\n
    #     {user_data}
    
    # """
    # messages.append(
    #         {
    #             'role': 'user',
    #             'content': formatted_user_query
    #         })
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=messages,
    # )
    # out = response.choices[0].message.content
    # print("SSSSSSSSSS" + out)
    return syntax
