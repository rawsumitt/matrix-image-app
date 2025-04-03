import React from 'react';
import MatrixGenerator from './components/MatrixGenerator';
import MatrixOperations from './components/MatrixOperations';
import ImageUploader from './components/ImageUploader';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Matrix Image Processor</h1>
      </header>
      
      <main className="main-content">
        <div className="tool-section">
          <MatrixGenerator />
        </div>
        
        <div className="tool-section">
          <MatrixOperations />
        </div>
        
        <div className="tool-section">
          <ImageUploader />
        </div>
      </main>
      
      <footer className="app-footer">
        <p>© {new Date().getFullYear()} Matrix Image App</p>
      </footer>
    </div>
  );
}

export default App;