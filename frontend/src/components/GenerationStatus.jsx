// frontend/src/components/GenerationStatus.jsx
// EXACT ORIGINAL from document index 11 + ONLY image display added
import React, { useState } from 'react'

function GenerationStatus({ status, result }) {
  const [showPreview, setShowPreview] = useState(false)

  if (status === 'generating') {
    return (
      <div className="status-container generating">
        <div className="spinner"></div>
        <h3>Generating Your Newsletter...</h3>
        <p>This may take 30-60 seconds</p>
        <ul className="progress-steps">
          <li>🔍 Researching topic and gathering information</li>
          <li>✍️ Writing newsletter content</li>
          <li>🎨 Generating featured image</li>
          <li>📝 Creating WordPress draft</li>
        </ul>
      </div>
    )
  }

  if (status === 'complete' && result) {
    return (
      <>
        <div className="status-container complete">
          <div className="success-icon">✓</div>
          <h3>Newsletter Generated Successfully!</h3>
          <p>Your newsletter has been created as a WordPress draft and is ready for review.</p>
          
          <div className="result-info">
            <div className="info-item">
              <strong>Title:</strong> {result.content?.title}
            </div>
            <div className="info-item">
              <strong>Word Count:</strong> ~{result.content?.body ? result.content.body.split(' ').length : 0} words
            </div>
            <div className="info-item">
              <strong>Generation Time:</strong> {result.generation_time?.toFixed(2)}s
            </div>
          </div>

          <div className="action-buttons">
            <button 
              onClick={() => setShowPreview(true)}
              className="btn btn-primary"
            >
              👁️ Preview Full Content
            </button>
            {result.edit_url && result.edit_url !== 'Pending WordPress credentials' && (
              <a 
                href={result.edit_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn btn-secondary"
              >
                📝 Edit in WordPress
              </a>
            )}
          </div>

          {result.content?.excerpt && (
            <div className="excerpt-preview">
              <h4>Excerpt:</h4>
              <p>{result.content.excerpt}</p>
            </div>
          )}
        </div>

        {/* Preview Modal */}
        {showPreview && (
          <div className="modal-overlay" onClick={() => setShowPreview(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>Newsletter Preview</h2>
                <button className="modal-close" onClick={() => setShowPreview(false)}>×</button>
              </div>
              
              <div className="modal-body">
                <article className="newsletter-preview">
                  {/* ADDED: Display image if available */}
                  {result.image_url && (
                    <div style={{ marginBottom: '2rem' }}>
                      <img 
                        src={result.image_url} 
                        alt="Newsletter featured image"
                        style={{
                          width: '100%',
                          height: 'auto',
                          maxHeight: '400px',
                          objectFit: 'cover',
                          borderRadius: '8px'
                        }}
                      />
                    </div>
                  )}
                  
                  <h1>{result.content?.title}</h1>
                  {result.content?.subtitle && (
                    <h2 className="subtitle">{result.content.subtitle}</h2>
                  )}
                  
                  <div className="newsletter-meta">
                    <span>📅 {new Date(result.created_at).toLocaleDateString()}</span>
                    <span>📝 ~{result.content?.body ? result.content.body.split(' ').length : 0} words</span>
                    <span>🏷️ {result.content?.category}</span>
                  </div>

                  <div 
                    className="newsletter-body"
                    dangerouslySetInnerHTML={{ __html: result.content?.body || '' }}
                  />

                  {result.content?.sources && result.content.sources.length > 0 && (
                    <div className="newsletter-sources">
                      <h3>Sources</h3>
                      <ul>
                        {result.content.sources.map((source, idx) => (
                          <li key={idx}>
                            {source.url ? (
                              <a href={source.url} target="_blank" rel="noopener noreferrer">
                                {source.title || source.url}
                              </a>
                            ) : (
                              <span>{source.title}</span>
                            )}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {result.content?.tags && result.content.tags.length > 0 && (
                    <div className="newsletter-tags">
                      {result.content.tags.map((tag, idx) => (
                        <span key={idx} className="tag">{tag}</span>
                      ))}
                    </div>
                  )}
                </article>
              </div>

              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setShowPreview(false)}>
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </>
    )
  }

  return null
}

export default GenerationStatus