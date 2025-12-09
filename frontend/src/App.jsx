// frontend/src/App.jsx
import React, { useState, useEffect } from 'react'
import ResearchForm from './components/ResearchForm'
import MinutesForm from './components/MinutesForm'
import HybridForm from './components/HybridForm'
import GenerationStatus from './components/GenerationStatus'
import axios from 'axios'

function App() {
  const [activeTab, setActiveTab] = useState('research')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationResult, setGenerationResult] = useState(null)
  const [error, setError] = useState(null)
  const [wpConnected, setWpConnected] = useState(false)

  useEffect(() => {
    checkWordPressConnection()
  }, [])

  const checkWordPressConnection = async () => {
    try {
      const response = await axios.get('/api/wordpress/test-connection')
      setWpConnected(response.data.success)
    } catch (err) {
      console.error('WordPress connection failed:', err)
      setWpConnected(false)
    }
  }

  const handleGenerate = async (endpoint, data) => {
    setIsGenerating(true)
    setError(null)
    setGenerationResult(null)

    try {
      const response = await axios.post(endpoint, data, {
        headers: {
          'Content-Type': data instanceof FormData ? 'multipart/form-data' : 'application/json'
        }
      })

      setGenerationResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Generation failed')
      console.error('Generation error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>🦅 Goochland GOP Newsletter Agent</h1>
          <p className="subtitle">AI-Powered Newsletter Generation System</p>
          <div className={`connection-status ${wpConnected ? 'connected' : 'disconnected'}`}>
            {wpConnected ? '✓ WordPress Connected' : '✗ WordPress Disconnected'}
          </div>
        </div>
      </header>

      <main className="container main-content">
        {!wpConnected && (
          <div className="alert alert-warning">
            <strong>Warning:</strong> WordPress connection not established. Please check your configuration.
          </div>
        )}

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'research' ? 'active' : ''}`}
            onClick={() => setActiveTab('research')}
          >
            📊 Research Topic
          </button>
          <button
            className={`tab ${activeTab === 'minutes' ? 'active' : ''}`}
            onClick={() => setActiveTab('minutes')}
          >
            📄 Meeting Minutes
          </button>
          <button
            className={`tab ${activeTab === 'hybrid' ? 'active' : ''}`}
            onClick={() => setActiveTab('hybrid')}
          >
            🔗 Combined
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'research' && (
            <ResearchForm onGenerate={handleGenerate} isGenerating={isGenerating} />
          )}
          {activeTab === 'minutes' && (
            <MinutesForm onGenerate={handleGenerate} isGenerating={isGenerating} />
          )}
          {activeTab === 'hybrid' && (
            <HybridForm onGenerate={handleGenerate} isGenerating={isGenerating} />
          )}
        </div>

        {error && (
          <div className="alert alert-error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {isGenerating && (
          <GenerationStatus status="generating" />
        )}

        {generationResult && !isGenerating && (
          <GenerationStatus status="complete" result={generationResult} />
        )}
      </main>

      <footer className="footer">
        <div className="container">
          <p>&copy; 2024 Goochland County Republican Committee. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default App