import os
from flask import Flask, jsonify

# Flask must be imported and initialized
app = Flask(__name__) 

# --- Configuration ---
# Get the directory where this script (server.py) is located (/API)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate UP two levels to the /Your_Gallery_Project/public/images/ folder
# Vercel suggests serving static content from /public, so we must point the logic to find files there.
IMAGE_DIR = os.path.join(SCRIPT_DIR, '..', 'public', 'images') 

ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')

# --------------------------------------------------------------------

@app.route('/API/list-images', methods=['GET'])
def list_images():
    """
    The sole API endpoint, accessible via: http://<host>:<port>/API/list-images
    """
    try:
        # Check if the directory exists (it should, inside the Vercel deployment structure)
        if not os.path.isdir(IMAGE_DIR):
            # This error is critical, means the deployment structure is wrong
            return jsonify({'error': f"Image directory not found at: {IMAGE_DIR}"}), 500

        # Read all files in the directory
        all_files = os.listdir(IMAGE_DIR)
        
        # Filter for allowed image files
        image_list = [
            f for f in all_files 
            if os.path.isfile(os.path.join(IMAGE_DIR, f)) and f.lower().endswith(ALLOWED_EXTENSIONS)
        ]
        
        # Return the list of image file names as JSON
        return jsonify(image_list)

    except Exception as e:
        # Generic error handling
        return jsonify({'error': str(e)}), 500

# The standard __name__ == '__main__' block is omitted, 
# as Vercel imports and runs the 'app' instance directly.
