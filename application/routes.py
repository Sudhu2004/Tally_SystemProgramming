from application import app, db
from flask import request, jsonify, send_file
from bson.objectid import ObjectId
import gridfs
from io import BytesIO

# Initialize GridFS
fs = gridfs.GridFS(db)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_id = fs.put(file, filename=file.filename)
    return jsonify({'message': 'File uploaded successfully', 'file_id': str(file_id)}), 201

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        file = fs.get(ObjectId(file_id))
        return send_file(BytesIO(file.read()), attachment_filename=file.filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

