import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Add startup logging
console.log('📦 Initializing RAG Chatbot frontend application')
console.log(`🌐 Environment: ${import.meta.env.MODE}`)
console.log(`🔗 API URL: ${import.meta.env.VITE_API_URL || 'default backend URL'}`)

// Log when app initialization starts
console.time('⏱️ App rendering time')

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

// Log when app is mounted
console.timeEnd('⏱️ App rendering time')
console.log('✅ Application mounted successfully')
