from flask import Flask, render_template, request, send_from_directory
import os
from utils import generate_random_matrix, apply_operation, process_image

app = Flask(__name__, template_folder="templates")  
app.config['UPLOAD_FOLDER'] = 'static/results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/generate_matrix', methods=['POST'])
def generate_matrix():
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])
    min_val = int(request.form['min_val'])
    max_val = int(request.form['max_val'])
    
    matrix_path = generate_random_matrix(rows, cols, min_val, max_val)
    filename = os.path.basename(matrix_path)
    
    return {'image_url': f"/static/results/{filename}"}

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    gray_scale = 'gray_scale' in request.form
    
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(upload_path)
    
    output_paths = process_image(upload_path, gray_scale)
    return {'paths': [f"/{path}" for path in output_paths]}  # Ensure paths are properly formatted

@app.route('/matrix_operation', methods=['POST'])
def matrix_operation():
    operation = request.form['operation']
    scalar = int(request.form.get('scalar', 1))
    
    file = request.files['matrix']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    result_path = apply_operation(file_path, operation, scalar)
    filename = os.path.basename(result_path)
    
    return {'image_url': f"/static/results/{filename}"}

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
