import os
from flask import Flask, jsonify, send_file, send_from_directory

app = Flask(__name__)
# CORS is no longer strictly necessary since we are serving everything from the same origin,
# but keeping it out for cleanliness in this single-origin setup.

# --- Configuration ---
# Get the directory where this script (app.py) is located (/API)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate UP one level to the project root (/)
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')

# Absolute paths based on the project root
IMAGE_DIR = os.path.join(PROJECT_ROOT, 'images') 
INDEX_HTML_PATH = os.path.join(PROJECT_ROOT, 'index.html') 

ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')

# --------------------------------------------------------------------

@app.route('/')
def serve_html():
    """
    1. Serves the index.html file when accessing the root URL (http://<host>:<port>/)
    """
    try:
        return send_file(INDEX_HTML_PATH)
    except FileNotFoundError:
        return "Error: index.html not found in the project root.", 404

@app.route('/API/list-images', methods=['GET'])
def list_images():
    """
    2. API endpoint to scan the IMAGE_DIR and return a list of image file names.
    Accessed via: http://<host>:<port>/API/list-images
    """
    try:
        if not os.path.isdir(IMAGE_DIR):
            return jsonify({'error': f"Image directory not found at: {IMAGE_DIR}"}), 500

        all_files = os.listdir(IMAGE_DIR)
        image_list = [
            f for f in all_files 
            if os.path.isfile(os.path.join(IMAGE_DIR, f)) and f.lower().endswith(ALLOWED_EXTENSIONS)
        ]
        
        return jsonify(image_list)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    """
    3. Endpoint to serve the actual image files from the /images/ path.
    Accessed via: http://<host>:<port>/images/my_photo.jpg
    """
    # Securely serves the file from the IMAGE_DIR
    return send_from_directory(IMAGE_DIR, filename)

# --------------------------------------------------------------------

if __name__ == '__main__':
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"Created images directory at: {IMAGE_DIR}")

    # The server will run and handle all routes (/, /API/list-images, /images/*)
    print("Starting Flask server for single-origin hosting...")
    print(f"Access the gallery at: http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', port=5000)
    
