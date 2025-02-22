from flask import Flask
from flask_cors import CORS
from document_upload_methods import DocumentHandler
import os

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

UPLOAD_FOLDER = 'uploads'
document_handler = DocumentHandler(UPLOAD_FOLDER)

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
    return document_handler.get_documents()

if __name__ == '__main__':
    print("Server starting... Upload folder:", os.path.abspath(UPLOAD_FOLDER))
    app.run(debug=True, port=5000)