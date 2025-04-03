import React, { useState } from 'react';
import axios from 'axios';

export default function ImageUploader() {
    const [images, setImages] = useState([]);
    const [grayScale, setGrayScale] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        setLoading(true);
        setError(null);
        setImages([]);

        try {
            // Validate file
            if (!file.type.match('image.*')) {
                throw new Error("Only image files are allowed");
            }
            if (file.size > 5 * 1024 * 1024) {  // 5MB limit
                throw new Error("File size must be less than 5MB");
            }

            const formData = new FormData();
            formData.append('image', file);
            formData.append('gray_scale', grayScale.toString());

            const response = await axios.post('/api/upload_image', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Accept': 'application/json'
                }
            });

            if (!response.data.success) {
                throw new Error(response.data.error || "Upload failed");
            }

            setImages(response.data.data.paths);
        } catch (err) {
            console.error("Image upload error:", {
                error: err.message,
                response: err.response?.data
            });
            setError(err.response?.data?.error || err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="section">
            <h2>Image Processing</h2>
            
            <div className="upload-controls">
                <input 
                    type="file" 
                    id="image-upload"
                    accept="image/*"
                    onChange={handleUpload}
                    disabled={loading}
                    style={{ display: 'none' }}
                />
                <label htmlFor="image-upload" className={`upload-button ${loading ? 'disabled' : ''}`}>
                    {loading ? 'Processing...' : 'Select Image'}
                </label>
                
                <div className="checkbox-group">
                    <input
                        type="checkbox"
                        id="grayscale-toggle"
                        checked={grayScale}
                        onChange={() => setGrayScale(!grayScale)}
                        disabled={loading}
                    />
                    <label htmlFor="grayscale-toggle">Convert to Grayscale</label>
                </div>
            </div>
            
            {error && (
                <div className="error-message">
                    <p>Error: {error}</p>
                </div>
            )}
            
            {images.length > 0 && (
                <div className="image-results">
                    <h3>Processed Results:</h3>
                    <div className="image-grid">
                        {images.map((img, index) => (
                            <div key={index} className="image-container">
                                <img 
                                    src={img}
                                    alt={`Processed result ${index + 1}`}
                                    onError={() => setError("Failed to load processed image")}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}