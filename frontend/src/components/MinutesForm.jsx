// frontend/src/components/MinutesForm.jsx
import React, { useState } from 'react'

function MinutesForm({ onGenerate, isGenerating }) {
  const [file, setFile] = useState(null)
  const [additionalContext, setAdditionalContext] = useState('')
  const [highlightItems, setHighlightItems] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!file) {
      alert('Please select a file')
      return
    }

    const formData = new FormData()
    formData.append('file', file)
    if (additionalContext) formData.append('additional_context', additionalContext)
    if (highlightItems) formData.append('highlight_items', highlightItems)

    onGenerate('/api/newsletter/generate/minutes', formData)
  }

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  return (
    <div className="form-container">
      <h2>Generate Newsletter from Meeting Minutes</h2>
      <p className="form-description">
        Upload meeting minutes (PDF, Word, or text) and the AI will transform them into an engaging newsletter article.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="file">Meeting Minutes File *</label>
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
              ✓ Selected: {file.name} ({(file.size / 1024).toFixed(2)} KB)
            </div>
          )}
          <small>Accepted formats: PDF, Word (.docx), Text (.txt)</small>
        </div>

        <div className="form-group">
          <label htmlFor="additional_context">Additional Context</label>
          <textarea
            id="additional_context"
            value={additionalContext}
            onChange={(e) => setAdditionalContext(e.target.value)}
            placeholder="Any additional context or emphasis for the newsletter..."
            rows="4"
            disabled={isGenerating}
          />
          <small>Optional: Provide context not in the minutes</small>
        </div>

        <div className="form-group">
          <label htmlFor="highlight_items">Items to Highlight</label>
          <input
            type="text"
            id="highlight_items"
            value={highlightItems}
            onChange={(e) => setHighlightItems(e.target.value)}
            placeholder="fundraiser, new members, upcoming events"
            disabled={isGenerating}
          />
          <small>Optional: Comma-separated items to emphasize</small>
        </div>

        <button type="submit" className="btn btn-primary" disabled={isGenerating || !file}>
          {isGenerating ? 'Generating...' : 'Generate Newsletter'}
        </button>
      </form>
    </div>
  )
}

export default MinutesForm