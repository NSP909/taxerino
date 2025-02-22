import os
from openai import OpenAI
from pdf2image import convert_from_path
from dotenv import load_dotenv
import base64

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract all text from this document image."},
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
    return extracted_text

# Usage
pdf_path = "/Users/abhyudaygoyal/Desktop/HACKLYTICS/taxerino/backend/GTech booking.pdf"
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)