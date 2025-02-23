from flask import Flask, request, jsonify
from flask_cors import CORS
from document_upload_methods import DocumentHandler
import os
import base64
from openai import OpenAI
from pdf2image import convert_from_path
from dotenv import load_dotenv
import json
from pymongo import MongoClient
from datetime import datetime
from tax_summary import generate_tax_summary
from extraction.pdf_json_to_plot_data import generate_plot_values_from_provided_data
from benford import analyze_benfords_law
from anthropic import Anthropic
from extraction.find_anomalies import anomaly_detection

app = Flask(__name__)
load_dotenv()

# Initialize MongoDB client with URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")
try:
    mongo_client = MongoClient(MONGO_URI)
    # Test the connection
    mongo_client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")
    raise e

db = mongo_client['taxerino']
tax_data_collection = db['tax_data']
file_data_collection = db['file_data']  # New collection to track file-data mapping

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
CACHE_FOLDER = 'cache'
SUMMARY_CACHE_FILE = os.path.join(CACHE_FOLDER, 'tax_summary.json')

# Create cache folder if it doesn't exist
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)

document_handler = DocumentHandler(UPLOAD_FOLDER)

def save_summary_cache(summary):
    """Save tax summary to cache file"""
    try:
        with open(SUMMARY_CACHE_FILE, 'w') as f:
            json.dump(summary, f)
    except Exception as e:
        print(f"Error saving summary cache: {str(e)}")

def get_summary_cache():
    """Get tax summary from cache file"""
    try:
        if os.path.exists(SUMMARY_CACHE_FILE):
            with open(SUMMARY_CACHE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading summary cache: {str(e)}")
    return None

def clear_summary_cache():
    """Clear the tax summary cache"""
    try:
        if os.path.exists(SUMMARY_CACHE_FILE):
            os.remove(SUMMARY_CACHE_FILE)
    except Exception as e:
        print(f"Error clearing summary cache: {str(e)}")

def update_tax_data(data, filename):
    """
    Upsert tax data into MongoDB and track which file it came from.
    """
    try:
        # Store the mapping of file to its extracted fields
        file_data_collection.update_one(
            {'filename': filename},
            {
                '$set': {
                    'fields': list(data.keys()),
                    'last_updated': datetime.utcnow()
                }
            },
            upsert=True
        )
        
        # Add timestamp for tracking
        data['last_updated'] = datetime.utcnow()
        
        # Upsert the data
        result = tax_data_collection.update_one(
            {'_id': 'current_tax_data'},
            {'$set': data},
            upsert=True
        )
        
        print(f"MongoDB upsert successful. Modified: {result.modified_count}, Upserted: {result.upserted_id is not None}")
        return True
    except Exception as e:
        print(f"Error updating MongoDB: {str(e)}")
        return False

def remove_file_data(filename):
    """
    Remove data associated with a specific file from MongoDB.
    """
    try:
        # Remove the file mapping
        file_data_collection.delete_one({'filename': filename})
        
        # Check if there are any remaining files
        remaining_files = file_data_collection.count_documents({})
        if remaining_files == 0:
            # If no files left, delete all tax data
            tax_data_collection.delete_many({})
            # Clear the summary cache
            clear_summary_cache()
            print(f"No files remaining, cleared all tax data and cache")
        
        print(f"Successfully removed data for file: {filename}")
        update_info_json()
        return True
    except Exception as e:
        print(f"Error removing file data: {str(e)}")
        return False

def get_current_tax_data():
    try:
        data = tax_data_collection.find_one(
            {'_id': 'current_tax_data'},
            projection={'timestamp': 0}  # Exclude timestamp if you don't need it
        )
        if data:
            # Remove MongoDB's _id field
            data.pop('_id', None)
            
            # Convert any remaining datetime objects to ISO format strings
            for key, value in dict(data).items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                    
            # Remove empty fields
            return {k: v for k, v in data.items() if v}
        return {}
    except Exception as e:
        print(f"Error retrieving from MongoDB: {str(e)}")
        return {}

def update_info_json():
    data = get_current_tax_data()
    with open("info.json", 'w') as file:
        json.dump(data, file, indent=4)

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
    anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Process each image
    for image_path in images_array:
        # Encode the image
        base64_image = encode_image(image_path)
        
        try:
            response = anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """You are a tax expert. You will be provided with a document image, and your task is to extract all the text from it. 
                                Please don't add any additional information. Also only extract information from documents which are in the form of tax documents/bank statements etc instead of just plain text.
                                Also I want you to process the output in the form of a json schema with as many fields as possible with values. 
                                There is no defined schema you need to extract as much info as you can in a json schema. Only return the information
                                that exists as a NUMERICAL VALUE. If the value is not a number, then don't include it.
                                BE AS PRECISE AS POSSIBLE.
                                Take your time, the decision is yours, extract all the info CORRECTLY from this and give me back a json and not a string"""
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            )

            # Extract content from the response
            responses.append(response.content[0].text)
            
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

# Handle GET and DELETE requests for documents
@app.route('/api/documents/<filename>', methods=['GET', 'DELETE'])
def handle_document(filename):
    if request.method == 'DELETE':
        # First remove the data from MongoDB
        remove_file_data(filename)
    # Then handle the file deletion
    return document_handler.handle_document(filename)

# Handle POST requests for uploading files
@app.route('/api/upload', methods=['POST'])
def upload_file():
    result = document_handler.upload_file()
    
    if result[1] == 200:  # If upload was successful
        try:
            # Extract filename from the response
            response_data = json.loads(result[0].get_data(as_text=True))
            filename = response_data.get('filename')
            
            if filename:
                pdf_path = os.path.join(UPLOAD_FOLDER, filename)
                extracted_text = extract_text_from_pdf(pdf_path)
                data = json.loads(extracted_text)
                
                # Update MongoDB with the new data and track the file
                update_tax_data(data, filename)
                # Clear the summary cache since we have new data
                clear_summary_cache()
            update_info_json()
            
        except Exception as e:
            print(f"Error processing uploaded file: {str(e)}")
    
    return result

# Handle GET requests for listing documents
@app.route('/api/documents', methods=['GET'])
def get_documents():
    print("Getting documents...")
    # print(document_handler.get_documents()[0].get_json()[0]['path'])
    # data = document_handler.get_documents()[0].get_json()
    return document_handler.get_documents()

@app.route('/api/documents/data', methods=['GET'])
def get_documents_data():
    # Return data from MongoDB instead of processing files again
    return get_current_tax_data()

@app.route('/api/tax-summary', methods=['GET'])
def get_tax_summary():
    """
    Generate a comprehensive summary of all tax data using LLM.
    """
    try:
        # First check if we have a cached summary
        cached_summary = get_summary_cache()
        if cached_summary:
            return cached_summary, 200

        # If no cache, generate new summary
        tax_data = get_current_tax_data()
        if not tax_data:
            empty_response = {"summary": "No tax data available yet.", "status": "empty"}
            save_summary_cache(empty_response)
            return empty_response, 200
            
        # Generate summary using OpenAI
        summary = generate_tax_summary(tax_data)
        # Cache the summary
        save_summary_cache(summary)
        return summary, 200
        
    except Exception as e:
        print(f"Error in tax summary endpoint: {str(e)}")
        error_response = {"error": "Failed to generate tax summary", "status": "error"}
        save_summary_cache(error_response)
        return error_response, 500
    
@app.route('/api/get-benford-data', methods=['GET'])
def get_benford_data():
    """
    Generate plot data from the tax data using LLM.
    """
    try:
        # Get current tax data
        update_info_json()

        with open("info.json", 'r') as file:
            tax_data = json.load(file)
        plot_data = analyze_benfords_law(tax_data)
        print("Benford analysis plot_data:", json.dumps(plot_data, indent=2))  # Debug log
        
        # Generate summary using OpenAI
        similarity_score = plot_data['similarity_score']
        risk_level = "normal" if similarity_score >= 0.8 else "moderate" if similarity_score >= 0.5 else "high"
        
        prompt = f"""Analyze this Benford's Law data and provide a concise summary:
- Similarity Score: {similarity_score}
- Risk Level: {risk_level}
- Number of data points: {len(plot_data['first_digits'])}

Focus on implications and recommendations. Keep it brief and clear."""

        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analysis expert providing concise summaries of Benford's Law analysis results."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        summary = summary_response.choices[0].message.content
        
        return {
            "benford_data": plot_data,
            "summary": summary,
            "status": "success"
        }, 200
        
    except Exception as e:
        print(f"Error in Benford analysis: {str(e)}")
        return {
            "error": str(e),
            "status": "error"
        }, 500
    
@app.route('/api/tax-plots', methods=['GET'])
def get_tax_plots():
    """
    Generate plot data from the tax data using LLM.
    """
    try:
        # Get current tax data
        tax_data = get_current_tax_data()
        if not tax_data:
            return {"error": "No tax data available yet.", "status": "empty"}, 200

        # Generate plot data using the LLM
        plot_data = generate_plot_values_from_provided_data(tax_data)
        print("Generated plot data:", json.dumps(plot_data, indent=2))  # Debug log
        
        return {
            "plot_data": plot_data,
            "status": "success"
        }, 200
        
    except Exception as e:
        print(f"Error in tax plots endpoint: {str(e)}")
        return {
            "error": "Failed to generate plot data",
            "status": "error",
            "details": str(e)
        }, 500

def save_debug_json(raw_data, normalized_data):
    """Save raw and normalized JSON data to debug files in both frontend and backend"""
    try:
        # Backend paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        backend_debug_folder = os.path.join(base_dir, CACHE_FOLDER, 'debug')
        
        # Frontend paths (relative to backend)
        frontend_debug_folder = os.path.join(base_dir, '..', 'frontend', 'src', 'debug')
        
        # Create directories if they don't exist
        os.makedirs(backend_debug_folder, exist_ok=True)
        os.makedirs(frontend_debug_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save files in backend location
        backend_raw_file = os.path.join(backend_debug_folder, f'raw_plot_data_{timestamp}.json')
        backend_norm_file = os.path.join(backend_debug_folder, f'normalized_plot_data_{timestamp}.json')
        
        # Save files in frontend location
        frontend_raw_file = os.path.join(frontend_debug_folder, f'raw_plot_data_{timestamp}.json')
        frontend_norm_file = os.path.join(frontend_debug_folder, f'normalized_plot_data_{timestamp}.json')
        
        # Save to backend location
        with open(backend_raw_file, 'w') as f:
            json.dump(raw_data, f, indent=2)
        with open(backend_norm_file, 'w') as f:
            json.dump(normalized_data, f, indent=2)
            
        # Save to frontend location
        with open(frontend_raw_file, 'w') as f:
            json.dump(raw_data, f, indent=2)
        with open(frontend_norm_file, 'w') as f:
            json.dump(normalized_data, f, indent=2)
            
        print(f"Debug files saved at:")
        print(f"Backend raw data: {backend_raw_file}")
        print(f"Backend normalized data: {backend_norm_file}")
        print(f"Frontend raw data: {frontend_raw_file}")
        print(f"Frontend normalized data: {frontend_norm_file}")
        return True
    except Exception as e:
        print(f"Error saving debug files: {str(e)}")
        print(f"Attempted to save in backend directory: {backend_debug_folder}")
        print(f"Attempted to save in frontend directory: {frontend_debug_folder}")
        return False

@app.route('/api/debug/save-plot-data', methods=['POST'])
def save_plot_debug_data():
    """
    Save raw and normalized plot data for debugging.
    """
    try:
        data = request.get_json()
        if not data or 'raw_data' not in data or 'normalized_data' not in data:
            return {"error": "Missing required data"}, 400

        save_debug_json(data['raw_data'], data['normalized_data'])
        return {"status": "success", "message": "Debug data saved"}, 200
    except Exception as e:
        print(f"Error in save plot debug data endpoint: {str(e)}")
        return {"error": "Failed to save debug data", "details": str(e)}, 500
    
@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    """
    Get anomalies from the tax data using LLM.
    """
    try:
        # Update info.json with current data
        print("Starting anomaly detection...")
        update_info_json()
        
        # Check if info.json exists and read its contents
        if not os.path.exists("info.json"):
            print("info.json does not exist")
            return jsonify({
                "status": "empty",
                "message": "No tax data available for analysis"
            })
        
        # Load tax data
        try:
            with open("info.json", 'r') as file:
                tax_data = json.load(file)
                print("Loaded tax data:", json.dumps(tax_data, indent=2))
        except json.JSONDecodeError as e:
            print(f"Error parsing info.json: {str(e)}")
            return jsonify({
                "status": "error",
                "error": "Invalid tax data format"
            })
        
        # Check if tax data is empty
        if not tax_data:
            print("Tax data is empty")
            return jsonify({
                "status": "empty",
                "message": "No tax data available for analysis"
            })

        # Get anomalies
        try:
            anomalies = anomaly_detection(tax_data)
            print("Generated anomalies:", json.dumps(anomalies, indent=2))
            
            if not isinstance(anomalies, dict):
                print("Invalid anomalies format: not a dictionary")
                return jsonify({
                    "status": "error",
                    "error": "Invalid anomalies format returned from analysis"
                })

            if not anomalies:  # Check if anomalies is empty
                print("No anomalies detected")
                return jsonify({
                    "status": "success",
                    "data": {}
                })

            # Validate anomalies structure
            for field, data in anomalies.items():
                if not isinstance(data, dict) or 'source_details' not in data or 'anomaly_details' not in data:
                    print(f"Invalid anomaly structure for field {field}")
                    return jsonify({
                        "status": "error",
                        "error": f"Invalid anomaly structure for field {field}"
                    })

            # Return the response
            return jsonify({
                "status": "success",
                "data": anomalies
            })
        except Exception as e:
            print(f"Error in anomaly detection: {str(e)}")
            return jsonify({
                "status": "error",
                "error": f"Error in anomaly detection: {str(e)}"
            })

    except Exception as e:
        print(f"Error in anomalies endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        })
    
if __name__ == '__main__':
    print("Server starting... Upload folder:", os.path.abspath(UPLOAD_FOLDER))
    app.run(debug=True, port=5000)