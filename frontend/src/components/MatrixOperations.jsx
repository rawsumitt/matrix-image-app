import { useState } from 'react'
import axios from 'axios'

export default function MatrixOperations() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('matrix', e.target.matrix.files[0])
      formData.append('operation', e.target.operation.value)
      formData.append('scalar', e.target.scalar.value)

      const res = await axios.post('/api/matrix_operation', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Accept': 'application/json'
        }
      })
      
      if (!res.data.success) {
        throw new Error(res.data.error || "Operation failed")
      }
      
      setResult(res.data.data.image_url)
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
      <h2>Matrix Operations</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Matrix Image:</label>
          <input 
            type="file" 
            name="matrix" 
            accept="image/*" 
            required
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label>Operation:</label>
          <select name="operation" disabled={loading}>
            <option value="transpose">Transpose</option>
            <option value="scalar_mult">Scalar Multiply</option>
          </select>
        </div>
        <div className="form-group">
          <label>Scalar Value:</label>
          <input 
            type="number" 
            name="scalar" 
            defaultValue="1"
            disabled={loading}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Apply Operation'}
        </button>
      </form>
      
      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
        </div>
      )}
      
      {result && (
        <div className="operation-result">
          <h3>Operation Result:</h3>
          <img 
            src={result} 
            alt="Operation result" 
            onError={(e) => {
              e.target.style.display = 'none';
              setError('Failed to load result image');
            }}
          />
        </div>
      )}
    </div>
  )
}