import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../utils/supabaseClient'

const AuthContext = createContext({})

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    console.log('AuthProvider: Initializing...')
    
    // Check active sessions and sets the user
    supabase.auth.getSession().then(({ data: { session }, error }) => {
      console.log('AuthProvider: Initial session check:', { session, error })
      setUser(session?.user ?? null)
      setLoading(false)
    })

    // Listen for changes on auth state (sign in, sign out, etc.)
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      console.log('AuthProvider: Auth state changed:', { event, session })
      setUser(session?.user ?? null)
      setLoading(false)
    })

    return () => subscription.unsubscribe()
  }, [])

  const value = {
    signUp: async (data) => {
      console.log('AuthProvider: Signing up...', data)
      const result = await supabase.auth.signUp(data)
      console.log('AuthProvider: Sign up result:', result)
      return result
    },
    signIn: async (data) => {
      console.log('AuthProvider: Signing in...', data)
      // 1. Đăng nhập (signIn): Nếu nhập đúng email bypass@gmail.com và password bypass thì bypass, còn lại dùng Supabase.
      if (data.email === 'bypass@gmail.com' && data.password === 'bypass') {
        const mockUser = {
          id: 'bypass-user-id',
          email: 'bypass@gmail.com',
          user_metadata: {},
          app_metadata: {},
          aud: 'authenticated',
          role: 'authenticated'
        }
        setUser(mockUser)
        return { data: { user: mockUser, session: { user: mockUser } }, error: null }
      }
      const result = await supabase.auth.signInWithPassword(data)
      console.log('AuthProvider: Sign in result:', result)
      return result
    },
    signOut: async () => {
      // 2. Đăng xuất (signOut): Nếu user hiện tại là bypass@gmail.com thì chỉ xóa local, không gọi Supabase
      if (user && user.email === 'bypass@gmail.com') {
        setUser(null)
        return { error: null }
      }
      // Ngược lại, dùng Supabase như bình thường
      const result = await supabase.auth.signOut()
      console.log('AuthProvider: Sign out result:', result)
      return result
    },
    user,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  return useContext(AuthContext)
} 