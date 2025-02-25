from flask import Flask, request, send_file, send_from_directory
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import io

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

# Helper function to pad data
def pad(data):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data)
    padded_data += padder.finalize()
    return padded_data

# Helper function to unpad data
def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data)
    unpadded_data += unpadder.finalize()
    return unpadded_data

# Encrypt image using AES
def encrypt_image(image_data, password):
    key = password.ljust(32)[:32].encode()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = pad(image_data)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

# Decrypt image using AES
def decrypt_image(encrypted_data, password):
    key = password.ljust(32)[:32].encode()
    iv = encrypted_data[:16]
    actual_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(actual_data) + decryptor.finalize()
    return unpad(decrypted_padded_data)

# Serve the frontend
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

# Route for encrypting an image
@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return "File or password missing", 400

    file = request.files['file']
    password = request.form['password']

    if file.filename == '':
        return "No file selected", 400

    image_data = file.read()
    try:
        encrypted_data = encrypt_image(image_data, password)
        return send_file(
            io.BytesIO(encrypted_data),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name='encrypted_image.bin'
        )
    except Exception as e:
        return f"Encryption failed: {str(e)}", 500

# Route for decrypting an image
@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files or 'password' not in request.form:
        return "File or password missing", 400

    file = request.files['file']
    password = request.form['password']

    if file.filename == '':
        return "No file selected", 400
    
    if not file.filename.endswith('.bin'):
        return "Invalid file format. Please upload a .bin file", 400

    encrypted_data = file.read()
    try:
        decrypted_data = decrypt_image(encrypted_data, password)
        return send_file(
            io.BytesIO(decrypted_data),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='decrypted_image.jpg'
        )
    except Exception as e:
        return f"Decryption failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
