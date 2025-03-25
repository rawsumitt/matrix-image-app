import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import uuid

def generate_random_matrix(rows, cols, min_val, max_val):
    matrix = np.random.randint(min_val, max_val+1, size=(rows, cols))
    plt.figure(figsize=(5, 5))
    plt.imshow(matrix, cmap='viridis')
    plt.colorbar()
    
    # Save the file and return the path
    path = os.path.join('static/results', f'matrix_{uuid.uuid4()}.png')
    plt.savefig(path)
    plt.close()
    return path 

def apply_operation(image_path, operation, scalar=1):
    matrix = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if operation == 'transpose':
        result = matrix.T
    elif operation == 'scalar_mult':
        result = scalar * matrix
    else:
        result = matrix
    
    plt.figure(figsize=(10, 5))
    plt.imshow(result, cmap='gray')
    path = os.path.join('static', 'results', f'result_{uuid.uuid4()}.png')
    plt.savefig(path)
    plt.close()
    return path

def process_image(image_path, gray_scale=False):
    image = cv2.imread(image_path)
    if gray_scale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        paths = [plot_channel(image, 'gray')]
    else:
        r, g, b = cv2.split(image)
        paths = [
            plot_channel(r, 'Reds'),
            plot_channel(g, 'Greens'),
            plot_channel(b, 'Blues')
        ]
    return paths

def plot_channel(channel, cmap):
    plt.figure(figsize=(8, 6))
    plt.imshow(channel, cmap=cmap)
    plt.colorbar()
    path = os.path.join('static', 'results', f'{cmap}_{uuid.uuid4()}.png')
    plt.savefig(path)
    plt.close()
    return path
