import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://jgxpfqyrqemcyvisgngo.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpneHBmcXlycWVtY3l2aXNnbmdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyOTQ5NDUsImV4cCI6MjA1OTg3MDk0NX0.JAxQ20Dnfn7LGVKoH7TYYxXHkVQ8JzNV5CQrhlXsF_g'

console.log('Supabase URL:', supabaseUrl)
// log ra 3 ký tự cuối của supabaseKey
console.log('Supabase Key:', supabaseKey.slice(-3))

const supabase = createClient(supabaseUrl, supabaseKey)

// Test connection
supabase.auth.getSession().then(({ data, error }) => {
  if (error) {
    console.error('Supabase connection error:', error)
  } else {
    console.log('Supabase connection successful:', data)
  }
})

export { supabase } 