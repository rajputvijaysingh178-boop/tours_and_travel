function Footer() {
  return (
    <footer className="bg-gray-900 px-6 py-10 text-white">
      <div className="mx-auto grid max-w-7xl gap-8 md:grid-cols-3">

        {/* Company */}
        <div>
          <h2 className="text-2xl font-bold text-blue-400">
            ✈️ TravelEase
          </h2>

          <p className="mt-3 text-gray-400">
            Your trusted platform for discovering and booking
            unforgettable travel experiences.
          </p>
        </div>

        {/* Quick Links */}
        <div>
          <h3 className="font-semibold">
            Quick Links
          </h3>

          <div className="mt-3 space-y-2 text-gray-400">
            <p className="cursor-pointer hover:text-white">
              Home
            </p>

            <p className="cursor-pointer hover:text-white">
              Tour Packages
            </p>

            <p className="cursor-pointer hover:text-white">
              About Us
            </p>

            <p className="cursor-pointer hover:text-white">
              Contact
            </p>
          </div>
        </div>

        {/* Contact */}
        <div>
          <h3 className="font-semibold">
            Contact
          </h3>

          <div className="mt-3 space-y-2 text-gray-400">
            <p>📧 support@travelease.com</p>
            <p>📞 +91 98765 43210</p>
            <p>📍 Hyderabad, India</p>
          </div>
        </div>

      </div>

      {/* Copyright */}
      <div className="mx-auto mt-8 max-w-7xl border-t border-gray-700 pt-6 text-center text-sm text-gray-500">
        © 2026 TravelEase Tours. All rights reserved.
      </div>
    </footer>
  )
}

export default Footer