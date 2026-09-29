import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

const API_URL = 'http://127.0.0.1:8000'

function Login() {
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()

    setError('')

    if (!email || !password) {
      setError('Please enter email and password.')
      return
    }

    try {
      setLoading(true)

      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      })

      const data = await response.json()

      console.log('Login status:', response.status)
      console.log('Login response:', data)

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed')
      }

      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)

      alert('Login successful!')

      navigate('/packages')
    } catch (error) {
      console.error('LOGIN ERROR:', error)

      if (error instanceof TypeError) {
        setError(
          'Cannot connect to the backend. Make sure FastAPI is running on http://127.0.0.1:8000'
        )
      } else {
        setError(error.message || 'Unable to login.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="flex min-h-[calc(100vh-160px)] items-center justify-center px-6 py-12">
        <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">

          {/* Header */}
          <div className="text-center">
            <div className="text-5xl">
              ✈️
            </div>

            <h1 className="mt-4 text-3xl font-bold text-gray-900">
              Welcome Back
            </h1>

            <p className="mt-2 text-gray-500">
              Login to manage your travel bookings
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-6 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
              {error}
            </div>
          )}

          {/* Login Form */}
          <form
            onSubmit={handleLogin}
            className="mt-8 space-y-5"
          >

            {/* Email */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Email
              </label>

              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Password */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Password
              </label>

              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Remember Me */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 text-gray-600">
                <input type="checkbox" />
                Remember me
              </label>

              <button
                type="button"
                className="font-medium text-blue-600 hover:underline"
              >
                Forgot Password?
              </button>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>

          </form>

          {/* Register */}
          <p className="mt-6 text-center text-gray-600">
            Don't have an account?{' '}

            <Link
              to="/register"
              className="font-semibold text-blue-600 hover:underline"
            >
              Create Account
            </Link>
          </p>

        </div>
      </main>

      <Footer />
    </div>
  )
}

export default Login