// frontend/src/components/HybridForm.jsx
import React, { useState } from 'react'

function HybridForm({ onGenerate, isGenerating }) {
  const [file, setFile] = useState(null)
  const [formData, setFormData] = useState({
    research_topic: '',
    research_context: '',
    minutes_context: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!file) {
      alert('Please select a meeting minutes file')
      return
    }

    const data = new FormData()
    data.append('file', file)
    data.append('research_topic', formData.research_topic)
    if (formData.research_context) data.append('research_context', formData.research_context)
    if (formData.minutes_context) data.append('minutes_context', formData.minutes_context)

    onGenerate('/api/newsletter/generate/hybrid', data)
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  return (
    <div className="form-container">
      <h2>Generate Combined Newsletter</h2>
      <p className="form-description">
        Combine meeting minutes with research on a current topic to create a comprehensive newsletter that connects local activities with broader issues.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>📄 Meeting Minutes</h3>
          
          <div className="form-group">
            <label htmlFor="file">Upload Minutes *</label>
            <input
              type="file"
              id="file"
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx,.txt"
              required
              disabled={isGenerating}
            />
            {file && (
              <div className="file-info">
                ✓ Selected: {file.name}
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="minutes_context">Minutes Context</label>
            <textarea
              id="minutes_context"
              name="minutes_context"
              value={formData.minutes_context}
              onChange={handleChange}
              placeholder="Additional context about the meeting..."
              rows="3"
              disabled={isGenerating}
            />
          </div>
        </div>

        <div className="form-section">
          <h3>📊 Research Topic</h3>
          
          <div className="form-group">
            <label htmlFor="research_topic">Topic to Research *</label>
            <input
              type="text"
              id="research_topic"
              name="research_topic"
              value={formData.research_topic}
              onChange={handleChange}
              placeholder="e.g., Virginia education policy updates"
              required
              disabled={isGenerating}
            />
            <small>This will provide broader context for the meeting updates</small>
          </div>

          <div className="form-group">
            <label htmlFor="research_context">Research Context</label>
            <textarea
              id="research_context"
              name="research_context"
              value={formData.research_context}
              onChange={handleChange}
              placeholder="Specific angles or connections to explore..."
              rows="3"
              disabled={isGenerating}
            />
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={isGenerating || !file}>
          {isGenerating ? 'Generating...' : 'Generate Combined Newsletter'}
        </button>
      </form>
    </div>
  )
}

export default HybridForm