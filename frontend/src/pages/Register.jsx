import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function Register() {
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

          <form className="mt-8 space-y-5">

            {/* Full Name */}
            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Full Name
              </label>

              <input
                type="text"
                placeholder="Enter your full name"
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
                placeholder="Enter your email"
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
                placeholder="Enter your phone number"
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
                placeholder="Create a password"
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
                placeholder="Confirm your password"
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Terms */}
            <label className="flex items-start gap-2 text-sm text-gray-600">
              <input
                type="checkbox"
                className="mt-1"
              />

              <span>
                I agree to the terms and conditions.
              </span>
            </label>

            {/* Register */}
            <button
              type="submit"
              className="w-full rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
            >
              Create Account
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