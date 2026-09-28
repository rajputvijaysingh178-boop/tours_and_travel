import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function Login() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="flex min-h-[calc(100vh-160px)] items-center justify-center px-6 py-12">
        <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">

          <div className="text-center">
            <div className="text-5xl">✈️</div>

            <h1 className="mt-4 text-3xl font-bold text-gray-900">
              Welcome Back
            </h1>

            <p className="mt-2 text-gray-500">
              Login to manage your travel bookings
            </p>
          </div>

          <form className="mt-8 space-y-5">

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

            <div>
              <label className="mb-2 block font-medium text-gray-700">
                Password
              </label>

              <input
                type="password"
                placeholder="Enter your password"
                className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

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

            <button
              type="submit"
              className="w-full rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
            >
              Login
            </button>

          </form>

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