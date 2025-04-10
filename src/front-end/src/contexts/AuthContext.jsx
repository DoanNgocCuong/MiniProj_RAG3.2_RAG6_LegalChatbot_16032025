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
      const result = await supabase.auth.signInWithPassword(data)
      console.log('AuthProvider: Sign in result:', result)
      return result
    },
    signOut: async () => {
      console.log('AuthProvider: Signing out...')
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