// frontend/src/components/ResearchForm.jsx
import React, { useState } from 'react'

function ResearchForm({ onGenerate, isGenerating }) {
  const [formData, setFormData] = useState({
    topic: '',
    context: '',
    sources: '',
    word_count: 800
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const data = {
      topic: formData.topic,
      context: formData.context || null,
      sources: formData.sources ? formData.sources.split('\n').filter(s => s.trim()) : [],
      word_count: parseInt(formData.word_count)
    }

    onGenerate('/api/newsletter/generate/research', data)
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="form-container">
      <h2>Generate Newsletter from Research</h2>
      <p className="form-description">
        Provide a topic and the AI will research current information to create a comprehensive newsletter article.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="topic">Topic *</label>
          <input
            type="text"
            id="topic"
            name="topic"
            value={formData.topic}
            onChange={handleChange}
            placeholder="e.g., Recent Virginia election law changes"
            required
            disabled={isGenerating}
          />
          <small>What should the newsletter cover?</small>
        </div>

        <div className="form-group">
          <label htmlFor="context">Additional Context</label>
          <textarea
            id="context"
            name="context"
            value={formData.context}
            onChange={handleChange}
            placeholder="Any specific angles, local connections, or background information..."
            rows="4"
            disabled={isGenerating}
          />
          <small>Optional: Provide specific context or direction for the research</small>
        </div>

        <div className="form-group">
          <label htmlFor="sources">Priority Sources</label>
          <textarea
            id="sources"
            name="sources"
            value={formData.sources}
            onChange={handleChange}
            placeholder="https://example.com/article1&#10;https://example.com/article2"
            rows="4"
            disabled={isGenerating}
          />
          <small>Optional: Specific URLs to include (one per line)</small>
        </div>

        <div className="form-group">
          <label htmlFor="word_count">Target Word Count</label>
          <input
            type="number"
            id="word_count"
            name="word_count"
            value={formData.word_count}
            onChange={handleChange}
            min="400"
            max="2000"
            step="100"
            disabled={isGenerating}
          />
          <small>Recommended: 600-1200 words</small>
        </div>

        <button type="submit" className="btn btn-primary" disabled={isGenerating}>
          {isGenerating ? 'Generating...' : 'Generate Newsletter'}
        </button>
      </form>
    </div>
  )
}

export default ResearchForm