import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://jgxpfqyrqemcyvisgngo.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqd250dm5sbG5idXZva3hrcWpwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE3MjEwMTksImV4cCI6MjA1NzI5NzAxOX0.EM4Be1upI3PL6r3usnOY1obMAKLMu8lZEtojcZ-hfbc'

export const supabase = createClient(supabaseUrl, supabaseKey) 