// Simple logger utility for consistent logging
const logger = {
  info: (message, data) => {
    console.log(`ℹ️ ${message}`, data ? data : '')
  },
  warn: (message, data) => {
    console.warn(`⚠️ ${message}`, data ? data : '')
  },
  error: (message, error) => {
    console.error(`❌ ${message}`, error ? error : '')
  },
  debug: (message, data) => {
    if (import.meta.env.DEV) {
      console.log(`🔍 ${message}`, data ? data : '')
    }
  },
  apiRequest: (endpoint, method) => {
    if (import.meta.env.DEV) {
      console.log(`🔄 API ${method} request to: ${endpoint}`)
    }
  },
  apiResponse: (endpoint, status) => {
    if (import.meta.env.DEV) {
      const icon = status >= 200 && status < 300 ? '✅' : '❌'
      console.log(`${icon} API response from ${endpoint}: ${status}`)
    }
  }
}

export default logger 