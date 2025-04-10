import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [isSignUp, setIsSignUp] = useState(false)
  const { signIn, signUp } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    try {
      if (isSignUp) {
        const { error } = await signUp({ email, password })
        if (error) throw error
        alert('Vui lòng kiểm tra email để xác thực tài khoản!')
      } else {
        const { error } = await signIn({ email, password })
        if (error) throw error
        navigate('/')
      }
    } catch (error) {
      setError(error.message)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-purple-900">
      <div className="max-w-md w-full space-y-8 p-10 bg-white/10 dark:bg-slate-800/50 backdrop-blur-xl rounded-2xl shadow-xl transition-all duration-300 hover:shadow-2xl hover:scale-[1.02] border border-white/20">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
            {isSignUp ? 'Đăng ký tài khoản' : 'Đăng nhập'}
          </h2>
          <p className="mt-2 text-center text-sm text-gray-200">
            {isSignUp ? 'Tạo tài khoản mới để trải nghiệm' : 'Chào mừng bạn trở lại'}
          </p>
        </div>
        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <div className="rounded-md -space-y-px">
            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium text-gray-200 mb-1">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                className="appearance-none relative block w-full px-4 py-3 border bg-slate-800/50 border-gray-600 placeholder-gray-400 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm transition-all duration-300 hover:border-indigo-400"
                placeholder="Nhập địa chỉ email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-200 mb-1">
                Mật khẩu
              </label>
              <input
                id="password"
                type="password"
                required
                className="appearance-none relative block w-full px-4 py-3 border bg-slate-800/50 border-gray-600 placeholder-gray-400 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm transition-all duration-300 hover:border-indigo-400"
                placeholder="Nhập mật khẩu"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {error && (
            <div className="text-red-300 text-sm text-center bg-red-900/50 p-3 rounded-lg border border-red-500/50">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-800 focus:ring-indigo-500 transition-all duration-300 hover:scale-[1.02] shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50"
            >
              <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                <svg className="h-5 w-5 text-indigo-300 group-hover:text-indigo-200" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                </svg>
              </span>
              {isSignUp ? 'Đăng ký' : 'Đăng nhập'}
            </button>
          </div>
        </form>

        <div className="text-center">
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-indigo-300 hover:text-indigo-200 font-medium transition-colors duration-300"
          >
            {isSignUp 
              ? 'Đã có tài khoản? Đăng nhập' 
              : 'Chưa có tài khoản? Đăng ký'}
          </button>
        </div>
      </div>
    </div>
  )
} 