import os
from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask
app = Flask(__name__)
# Enable CORS to allow index.html (which might be loaded directly or from a different port) 
# to fetch data from this API.
CORS(app) 

# --- Configuration ---
# Get the directory where this script (app.py) is located (/API)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate UP one level (..) and THEN into the 'images' folder
# This correctly targets /Your_Gallery_Project/images/
IMAGE_DIR = os.path.join(SCRIPT_DIR, '..', 'images') 

ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')

# --------------------------------------------------------------------

@app.route('/list-images', methods=['GET'])
def list_images():
    """
    API endpoint to scan the IMAGE_DIR and return a list of image file names.
    This will be accessed via http://<server-ip>:<port>/list-images
    """
    try:
        # 1. Ensure the directory exists
        if not os.path.isdir(IMAGE_DIR):
            return jsonify({'error': f"Image directory not found at: {IMAGE_DIR}"}), 500

        # 2. Read all files in the directory
        all_files = os.listdir(IMAGE_DIR)
        
        # 3. Filter for allowed image files
        image_list = [
            f for f in all_files 
            if os.path.isfile(os.path.join(IMAGE_DIR, f)) and f.lower().endswith(ALLOWED_EXTENSIONS)
        ]
        
        # 4. Return the list of image file names as JSON
        return jsonify(image_list)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# --------------------------------------------------------------------

if __name__ == '__main__':
    # Make sure the 'images' directory exists before starting
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"Created images directory at: {IMAGE_DIR}")

    # Run the Flask app on host 0.0.0.0 (accessible externally) and port 5000
    # Note: When run like this, the API path is simply http://127.0.0.1:5000/list-images
    print("Starting Flask API server...")
    app.run(host='0.0.0.0', port=5000)
