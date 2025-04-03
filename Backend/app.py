from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from utils import generate_random_matrix, apply_operation, process_image
import logging
import uuid

app = Flask(__name__)

# Configure CORS with specific settings
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/generate_matrix', methods=['POST'])
def api_generate_matrix():
    try:
        data = request.get_json()
        if not all(key in data for key in ['rows', 'cols', 'min_val', 'max_val']):
            raise ValueError("Missing required parameters")
            
        matrix_path = generate_random_matrix(
            int(data['rows']),
            int(data['cols']),
            int(data['min_val']),
            int(data['max_val'])
        )
        return jsonify({
            'success': True,
            'data': {
                'image_url': f"/api/results/{os.path.basename(matrix_path)}",
                'matrix_path': matrix_path
            },
            'error': None
        })
    except Exception as e:
        app.logger.error(f"Error in generate_matrix: {str(e)}")
        return jsonify({
            'success': False,
            'data': None,
            'error': str(e)
        }), 400

@app.route('/api/upload_image', methods=['POST'])
def api_upload_image():
    try:
        if 'image' not in request.files:
            raise ValueError("No image file provided")
            
        file = request.files['image']
        if file.filename == '':
            raise ValueError("No selected file")
            
        if not allowed_file(file.filename):
            raise ValueError("File type not allowed")
            
        gray_scale = request.form.get('gray_scale', 'false').lower() == 'true'
        
        # Secure file handling
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(upload_path)
        
        # Process image
        output_paths = process_image(upload_path, gray_scale)
        return jsonify({
            'success': True,
            'data': {
                'paths': [f"/api/results/{os.path.basename(p)}" for p in output_paths],
                'original_path': upload_path
            },
            'error': None
        })
    except Exception as e:
        app.logger.error(f"Error in upload_image: {str(e)}")
        return jsonify({
            'success': False,
            'data': None,
            'error': str(e)
        }), 500

@app.route('/api/matrix_operation', methods=['POST'])
def api_matrix_operation():
    try:
        if 'matrix' not in request.files:
            raise ValueError("No matrix file provided")
            
        file = request.files['matrix']
        if file.filename == '':
            raise ValueError("No selected file")
            
        if not allowed_file(file.filename):
            raise ValueError("File type not allowed")
            
        operation = request.form.get('operation')
        if not operation:
            raise ValueError("No operation specified")
            
        scalar = int(request.form.get('scalar', 1))
        
        # Secure file handling
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(file_path)
        
        # Apply operation
        result_path = apply_operation(file_path, operation, scalar)
        return jsonify({
            'success': True,
            'data': {
                'image_url': f"/api/results/{os.path.basename(result_path)}",
                'result_path': result_path
            },
            'error': None
        })
    except Exception as e:
        app.logger.error(f"Error in matrix_operation: {str(e)}")
        return jsonify({
            'success': False,
            'data': None,
            'error': str(e)
        }), 500

@app.route('/api/results/<filename>')
def serve_result(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        app.logger.error(f"Error serving file {filename}: {str(e)}")
        return jsonify({
            'success': False,
            'data': None,
            'error': "File not found"
        }), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {str(error)}")
    return jsonify({
        'success': False,
        'data': None,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(port=5000, debug=True)