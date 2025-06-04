from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cấu hình thư mục upload
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Danh sách tài khoản mẫu
USERS = {
    "Huân": "admin123",
    "Long": "pass123",
    "Điềm": "pass123",
    "Tuấn": "pass123",
    "Mạnh": "pass123",
    "HEHE": "pass123"
}

# Lưu trữ thông tin file
files = []

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS and USERS[username] == password:
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route('/list_users', methods=['GET'])
def list_users():
    return jsonify(list(USERS.keys()))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    
    file = request.files['file']
    sender = request.form.get('sender')
    receiver = request.form.get('receiver')
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Tính toán SHA-256
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        sha256 = sha256_hash.hexdigest()
        
        # Lưu thông tin file
        file_info = {
            "name": filename,
            "sha256": sha256,
            "sender": sender,
            "receiver": receiver
        }
        files.append(file_info)
        
        return jsonify({
            "status": "uploaded",
            "sha256": sha256
        })

@app.route('/list_files', methods=['GET'])
def list_files():
    return jsonify(files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
