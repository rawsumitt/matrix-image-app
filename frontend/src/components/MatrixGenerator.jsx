import { useState } from 'react'
import axios from 'axios'

export default function MatrixGenerator() {
  const [matrix, setMatrix] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setMatrix(null)

    try {
      const formData = {
        rows: e.target.rows.value,
        cols: e.target.cols.value,
        min_val: e.target.min_val.value,
        max_val: e.target.max_val.value
      }

      // Validate input
      if (formData.rows > 100 || formData.cols > 100) {
        throw new Error("Maximum size is 100x100")
      }

      const res = await axios.post('/api/generate_matrix', formData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      })
      
      if (!res.data.success) {
        throw new Error(res.data.error || "Failed to generate matrix")
      }
      
      setMatrix(res.data.data.image_url)
    } catch (err) {
      setError(err.response?.data?.error || 
              err.message || 
              'An unknown error occurred')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="section">
      <h2>Generate Matrix</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Rows:</label>
          <input name="rows" type="number" min="1" max="100" defaultValue="5" required />
        </div>
        <div className="form-group">
          <label>Columns:</label>
          <input name="cols" type="number" min="1" max="100" defaultValue="5" required />
        </div>
        <div className="form-group">
          <label>Min Value:</label>
          <input name="min_val" type="number" defaultValue="0" required />
        </div>
        <div className="form-group">
          <label>Max Value:</label>
          <input name="max_val" type="number" defaultValue="100" required />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Matrix'}
        </button>
      </form>
      
      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
        </div>
      )}
      
      {matrix && (
        <div className="matrix-result">
          <h3>Generated Matrix:</h3>
          <img 
            src={matrix} 
            alt="Generated matrix" 
            onError={(e) => {
              e.target.style.display = 'none';
              setError('Failed to load matrix image');
            }}
          />
        </div>
      )}
    </div>
  )
}