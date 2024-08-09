from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
import gridfs
import os
from io import BytesIO

app = Flask(__name__)

# MongoDB connection string
URL = "mongodb+srv://sudhrshan18:NaZFjUKdKlr2JrZF@cluster0.ma0bt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def mongo_conn():
    """Create a MongoDB connection"""
    try:
        conn = MongoClient(URL)
        print("MongoDB Connected")
        return conn['Ytube']
    except Exception as err:
        print(f"Error in MongoDB connection: {err}")
        return None

# Initialize MongoDB connection and GridFS
db = mongo_conn()
fs = gridfs.GridFS(db, collection="youtube")

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to MongoDB"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file to GridFS
    fs.put(file.read(), filename=file.filename)
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file from MongoDB"""
    try:
        file = fs.find_one({'filename': filename})
        if file is None:
            return jsonify({"error": "File not found"}), 404

        file_content = file.read()
        return send_file(BytesIO(file_content), as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
