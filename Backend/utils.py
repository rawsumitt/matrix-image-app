import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import uuid
from werkzeug.utils import secure_filename
import logging

def generate_random_matrix(rows, cols, min_val, max_val):
    try:
        # Validate input
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive integers")
        if min_val >= max_val:
            raise ValueError("Min value must be less than max value")
            
        matrix = np.random.randint(min_val, max_val+1, size=(rows, cols))
        plt.figure(figsize=(5, 5))
        plt.imshow(matrix, cmap='viridis')
        plt.colorbar()
        plt.title('Generated Matrix')
        
        filename = f"matrix_{uuid.uuid4()}.png"
        path = os.path.join('static/results', filename)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        return path
    except Exception as e:
        logging.error(f"Error in generate_random_matrix: {str(e)}")
        raise

def apply_operation(image_path, operation, scalar=1):
    try:
        # Validate operation
        valid_operations = ['transpose', 'scalar_mult']
        if operation not in valid_operations:
            raise ValueError(f"Invalid operation. Must be one of: {valid_operations}")
            
        matrix = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if matrix is None:
            raise ValueError("Could not read the image file")
            
        if operation == 'transpose':
            result = matrix.T
            title = 'Matrix Transpose'
        elif operation == 'scalar_mult':
            result = scalar * matrix
            title = f'Scalar Multiplication (×{scalar})'
            
        plt.figure(figsize=(10, 5))
        plt.imshow(result, cmap='gray')
        plt.title(title)
        plt.colorbar()
        
        filename = f"result_{uuid.uuid4()}.png"
        path = os.path.join('static/results', filename)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        return path
    except Exception as e:
        logging.error(f"Error in apply_operation: {str(e)}")
        raise

def process_image(image_path, gray_scale=False):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read the image file")
            
        if gray_scale:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return [plot_channel(image, 'gray', 'Grayscale')]
        else:
            b, g, r = cv2.split(image)
            return [
                plot_channel(r, 'Reds', 'Red Channel'),
                plot_channel(g, 'Greens', 'Green Channel'),
                plot_channel(b, 'Blues', 'Blue Channel')
            ]
    except Exception as e:
        logging.error(f"Error in process_image: {str(e)}")
        raise

def plot_channel(channel, cmap, title):
    try:
        plt.figure(figsize=(8, 6))
        plt.imshow(channel, cmap=cmap)
        plt.colorbar()
        plt.title(title)
        
        filename = f"{cmap}_{uuid.uuid4()}.png"
        path = os.path.join('static/results', filename)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        return path
    except Exception as e:
        logging.error(f"Error in plot_channel: {str(e)}")
        raise