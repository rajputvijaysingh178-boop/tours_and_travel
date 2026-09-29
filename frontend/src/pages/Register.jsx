import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function Register() {
  const navigate = useNavigate()

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    address: '',
    emergency_contact: '',
  })

  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  async function handleSubmit(e) {
    e.preventDefault()

    setMessage('')
    setError('')

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    setLoading(true)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/auth/register',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: formData.name,
            email: formData.email,
            password: formData.password,
            phone: formData.phone,
            address: formData.address,
            emergency_contact: formData.emergency_contact,
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed')
      }

      setMessage(data.message || 'Registration successful!')

      setFormData({
        name: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
        address: '',
        emergency_contact: '',
      })

      setTimeout(() => {
        navigate('/login')
      }, 1500)

    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="flex min-h-[calc(100vh-160px)] items-center justify-center px-6 py-12">

        <div className="w-full max-w-lg rounded-2xl bg-white p-8 shadow-lg">

          <div className="text-center">
            <div className="text-5xl">🌍</div>

            <h1 className="mt-4 text-3xl font-bold text-gray-900">
              Create Your Account
            </h1>

            <p className="mt-2 text-gray-500">
              Join TravelEase and start exploring
            </p>
          </div>

          {message && (
            <div className="mt-6 rounded-lg bg-green-100 px-4 py-3 text-center text-green-700">
              {message}
            </div>
          )}

          {error && (
            <div className="mt-6 rounded-lg bg-red-100 px-4 py-3 text-center text-red-700">
              {error}
            </div>
          )}

          <form
            onSubmit={handleSubmit}
            className="mt-8 space-y-5"
          >

            {/* Full Name */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Full Name
              </label>

              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter your full name"
                required
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Email */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Email
              </label>

              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
                required
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Phone */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Phone Number
              </label>

              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="Enter your phone number"
                required
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Address */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Address
              </label>

              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Enter your address"
                required
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Emergency Contact */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Emergency Contact
              </label>

              <input
                type="tel"
                name="emergency_contact"
                value={formData.emergency_contact}
                onChange={handleChange}
                placeholder="Enter emergency contact"
                required
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
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Create a password"
                required
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Confirm Password */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Confirm Password
              </label>

              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Confirm your password"
                required
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Terms */}
            <label className="flex items-start gap-2 text-sm text-gray-600">
              <input
                type="checkbox"
                required
                className="mt-1"
              />

              <span>
                I agree to the terms and conditions.
              </span>
            </label>

            {/* Register */}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>

          </form>

          <p className="mt-6 text-center text-gray-600">
            Already have an account?{' '}

            <Link
              to="/login"
              className="font-semibold text-blue-600 hover:underline"
            >
              Login
            </Link>
          </p>

        </div>
      </main>

      <Footer />
    </div>
  )
}

export default Register