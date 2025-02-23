from flask import Flask
from flask_cors import CORS
from document_upload_methods import DocumentHandler
import os
import base64
from openai import OpenAI
from pdf2image import convert_from_path
from dotenv import load_dotenv
import json
app = Flask(__name__)
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

UPLOAD_FOLDER = 'uploads'
document_handler = DocumentHandler(UPLOAD_FOLDER)
def pdf_to_images(pdf_path, dpi=200, output_folder="temp_images"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Convert PDF pages to a list of PIL Image objects
    images = convert_from_path(pdf_path, dpi=dpi)
    image_files = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(image_path, "PNG")
        image_files.append(image_path)
    return image_files
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def extract_text_from_pdf(pdf_path):
    # Convert PDF to images
    images_array = pdf_to_images(pdf_path)
    responses = []

    # Process each image
    for image_path in images_array:
        # Encode the image
        base64_image = encode_image(image_path)
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Correct model name
                messages=[
                    {
                        "role": "system",
                        "content": """You are a tax expert. You will be provided with a document image, and your task is to extract all the text from it. 
                        Please don't add any additional information. Also only extract information from documents which are in the form of tax documents/bank statments etc instead of just plain text.
                        Also I want you to process the output in the form of a json schema with as many fields as possible with values. 
                        There is no defined schema you need to extract as much info as you can in a json schema."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract all the info from this and give me back a json and not a string"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )

            # Extract content from the response object correctly
            responses.append(response.choices[0].message.content)
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            
    # Clean up temporary image files
    for image_path in images_array:
        try:
            os.remove(image_path)
        except Exception as e:
            print(f"Error removing temporary file {image_path}: {str(e)}")
    # Join text from all pages
    extracted_text = "\n\n".join(responses)
    return extracted_text[7:len(extracted_text)-3]

# Handle GET and DELETE requests for documents
@app.route('/api/documents/<filename>', methods=['GET', 'DELETE'])
def handle_document(filename):
    return document_handler.handle_document(filename)

# Handle POST requests for uploading files
@app.route('/api/upload', methods=['POST'])
def upload_file():
    return document_handler.upload_file()

# Handle GET requests for listing documents
@app.route('/api/documents', methods=['GET'])
def get_documents():
    print("Getting documents...")
    # print(document_handler.get_documents()[0].get_json()[0]['path'])
    # data = document_handler.get_documents()[0].get_json()
    return document_handler.get_documents()
@app.route('/api/documents/data', methods=['GET'])
def get_documents_data():
    upload_folder = '/Users/abhyudaygoyal/Desktop/HACKLYTICS/taxerino/backend/uploads'
    all_data = {}
    pdf_files = [f for f in os.listdir(upload_folder) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(upload_folder, pdf_file)
        extracted_text = extract_text_from_pdf(pdf_path)
        data = json.loads(extracted_text)
        all_data.update(data)
    # print(document_handler.get_documents()[0].get_json()[0]['path'])
    # path = document_handler.get_documents()[0].get_json()[0]['path']
    # data = extract_text_from_pdf(path)
    # print(data)
    print(all_data)
    return all_data
if __name__ == '__main__':
    print("Server starting... Upload folder:", os.path.abspath(UPLOAD_FOLDER))
    app.run(debug=True, port=5000)