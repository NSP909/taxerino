from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import os

class DocumentHandler:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

    def handle_document(self, filename):
        file_path = os.path.join(self.upload_folder, filename)
        
        if request.method == 'GET':
            try:
                return send_from_directory(
                    self.upload_folder,
                    filename,
                    mimetype='application/pdf',
                    as_attachment=False
                )
            except Exception as e:
                print(f"Preview error: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        elif request.method == 'DELETE':
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return jsonify({'message': 'File deleted successfully'}), 200
                else:
                    return jsonify({'error': 'File not found'}), 404
            except Exception as e:
                print(f"Delete error: {str(e)}")
                return jsonify({'error': str(e)}), 500

    def upload_file(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(f"{timestamp}_{file.filename}")
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'path': file_path,
                'size': os.path.getsize(file_path),
                'uploadedAt': timestamp
            }), 200
        except Exception as e:
            print(f"Upload error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    def get_documents(self):
        try:
            files = []
            for filename in os.listdir(self.upload_folder):
                file_path = os.path.join(self.upload_folder, filename)
                files.append({
                    'filename': filename,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'uploadedAt': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                })
            return jsonify(files), 200
        except Exception as e:
            print(f"List documents error: {str(e)}")
            return jsonify({'error': str(e)}), 500 