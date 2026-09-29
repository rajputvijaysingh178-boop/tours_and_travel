import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="border-b bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 md:px-6">

        {/* Logo */}
        <Link
          to="/"
          className="shrink-0 text-xl font-bold text-blue-600 md:text-2xl"
        >
          ✈️ TravelEase
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-3 md:gap-5">

          <Link
            to="/"
            className="hidden text-gray-700 hover:text-blue-600 sm:block"
          >
            Home
          </Link>

          <Link
            to="/packages"
            className="text-sm text-gray-700 hover:text-blue-600 md:text-base"
          >
            Packages
          </Link>

          <Link
            to="/hotels"
            className="text-sm text-gray-700 hover:text-blue-600 md:text-base"
          >
            Hotels
          </Link>

          <Link
            to="/my-bookings"
            className="hidden text-gray-700 hover:text-blue-600 lg:block"
          >
            My Bookings
          </Link>

          <Link
            to="/login"
            className="hidden text-gray-700 hover:text-blue-600 sm:block"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="shrink-0 rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700 md:px-5 md:py-2.5 md:text-base"
          >
            Register
          </Link>
           
          <Link
           to="/transport"
           className="text-sm text-gray-700 hover:text-blue-600 md:text-base"
          >
          Transport
          </Link>

        </div>
      </div>
    </nav>
  )
}

export default Navbar