import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getPackages } from '../services/api'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function Packages() {
  const [packages, setPackages] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getPackages()
      .then((data) => {
        setPackages(data)
      })
      .catch((err) => {
        console.error(err)
        setError('Failed to load packages')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Page Header */}
      <section className="bg-blue-600 px-6 py-16 text-white">
        <div className="mx-auto max-w-7xl">
          <p className="font-semibold uppercase tracking-wider text-blue-200">
            Explore India
          </p>

          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            Tour Packages
          </h1>

          <p className="mt-4 max-w-2xl text-lg text-blue-100">
            Discover exciting destinations and choose a tour package
            that matches your travel plans.
          </p>
        </div>
      </section>

      {/* Packages */}
      <section className="mx-auto max-w-7xl px-6 py-12">

        <div className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-center">

          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Available Packages
            </h2>

            <p className="mt-1 text-gray-500">
              Choose from our popular travel experiences.
            </p>
          </div>

          <select className="rounded-lg border bg-white px-4 py-3 text-gray-700 outline-none focus:ring-2 focus:ring-blue-500">
            <option>All Destinations</option>
            <option>Kerala</option>
            <option>Rajasthan</option>
            <option>Goa</option>
            <option>Himachal Pradesh</option>
          </select>

        </div>

        {/* Loading */}
        {loading && (
          <p className="py-10 text-center text-gray-500">
            Loading packages...
          </p>
        )}

        {/* Error */}
        {error && (
          <p className="py-10 text-center text-red-500">
            {error}
          </p>
        )}

        {/* Package Cards */}
        {!loading && !error && (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">

            {packages.map((tour) => (
              <div
                key={tour.package_id}
                className="overflow-hidden rounded-xl bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-xl"
              >

                {/* Image / Icon */}
                <div className="flex h-44 items-center justify-center bg-blue-100 text-7xl">
                  🌴
                </div>

                {/* Package Information */}
                <div className="p-5">

                  <span className="text-sm font-semibold text-blue-600">
                    {tour.destination}
                  </span>

                  <h3 className="mt-2 text-xl font-bold text-gray-800">
                    {tour.name}
                  </h3>

                  <p className="mt-2 text-sm text-gray-500">
                    {tour.description}
                  </p>

                  <p className="mt-4 text-sm font-medium text-gray-600">
                    🗓️ {tour.duration} Days
                  </p>

                  {/* Price + Button */}
                  <div className="mt-5 flex items-center justify-between">

                    <div>
                      <p className="text-xs text-gray-500">
                        Starting from
                      </p>

                      <p className="text-xl font-bold text-blue-600">
                        ₹{tour.base_price}
                      </p>
                    </div>

                    <Link
                      to={`/packages/${tour.package_id}`}
                      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                    >
                      View Details
                    </Link>

                  </div>

                </div>
              </div>
            ))}

          </div>
        )}

      </section>

      <Footer />
    </div>
  )
}

export default Packages