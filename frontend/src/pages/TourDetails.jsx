import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

const API_URL = 'http://127.0.0.1:8000'

function TourDetails() {
  const { id } = useParams()

  const [tour, setTour] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`${API_URL}/packages/${id}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Package not found')
        }

        return response.json()
      })
      .then((data) => {
        setTour(data)
      })
      .catch((err) => {
        console.error(err)
        setError('Tour Package Not Found')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />

        <div className="mx-auto max-w-7xl px-6 py-20 text-center">
          <p className="text-lg text-gray-500">
            Loading tour details...
          </p>
        </div>

        <Footer />
      </div>
    )
  }

  if (error || !tour) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />

        <div className="mx-auto max-w-7xl px-6 py-20 text-center">
          <h1 className="text-3xl font-bold text-gray-900">
            Tour Package Not Found
          </h1>

          <Link
            to="/packages"
            className="mt-6 inline-block rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white"
          >
            Back to Packages
          </Link>
        </div>

        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Header */}
      <section className="bg-blue-600 px-6 py-16 text-white">
        <div className="mx-auto max-w-7xl">
          <p className="text-blue-200">
            {tour.destination}
          </p>

          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            {tour.name}
          </h1>

          <p className="mt-4 text-lg text-blue-100">
            {tour.duration} Days
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-6 py-12">

        <div className="grid gap-8 lg:grid-cols-3">

          {/* Left Content */}
          <div className="lg:col-span-2">

            {/* Image */}
            <div className="flex h-72 items-center justify-center rounded-2xl bg-blue-100 text-9xl">
              🌴
            </div>

            {/* Description */}
            <div className="mt-8 rounded-xl bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold text-gray-900">
                About This Tour
              </h2>

              <p className="mt-4 leading-7 text-gray-600">
                {tour.description}
              </p>
            </div>

            {/* Tour Information */}
            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold text-gray-900">
                Tour Information
              </h2>

              <div className="mt-5 space-y-4">

                <div className="flex justify-between border-b pb-3">
                  <span className="text-gray-500">
                    Destination
                  </span>

                  <span className="font-semibold">
                    {tour.destination}
                  </span>
                </div>

                <div className="flex justify-between border-b pb-3">
                  <span className="text-gray-500">
                    Duration
                  </span>

                  <span className="font-semibold">
                    {tour.duration} Days
                  </span>
                </div>

                <div className="flex justify-between border-b pb-3">
                  <span className="text-gray-500">
                    Maximum Passengers
                  </span>

                  <span className="font-semibold">
                    {tour.max_passengers}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-500">
                    Status
                  </span>

                  <span className="font-semibold capitalize">
                    {tour.status}
                  </span>
                </div>

              </div>
            </div>

            {/* Cancellation Policy */}
            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold text-gray-900">
                Cancellation Policy
              </h2>

              <p className="mt-4 leading-7 text-gray-600">
                {tour.cancellation_policy || 'Please contact us for cancellation details.'}
              </p>
            </div>

          </div>

          {/* Booking Card */}
          <div>
            <div className="sticky top-6 rounded-xl bg-white p-6 shadow-lg">

              <p className="text-sm text-gray-500">
                Starting from
              </p>

              <p className="mt-1 text-3xl font-bold text-blue-600">
                ₹{tour.base_price}
              </p>

              <p className="mt-2 text-gray-500">
                per person
              </p>

              <div className="my-6 border-t" />

              <div className="space-y-4">

                <div className="flex justify-between">
                  <span className="text-gray-500">
                    Destination
                  </span>

                  <span className="font-semibold">
                    {tour.destination}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-500">
                    Duration
                  </span>

                  <span className="font-semibold">
                    {tour.duration} Days
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-500">
                    Capacity
                  </span>

                  <span className="font-semibold">
                    {tour.max_passengers}
                  </span>
                </div>

              </div>

              <Link
                to={`/booking/${tour.package_id}`}
                className="mt-8 block w-full rounded-lg bg-blue-600 px-6 py-3 text-center font-semibold text-white hover:bg-blue-700"
              >
                Book This Tour
              </Link>

              <Link
                to="/packages"
                className="mt-3 block w-full rounded-lg border border-gray-300 px-6 py-3 text-center font-semibold text-gray-700 hover:bg-gray-50"
              >
                Back to Packages
              </Link>

            </div>
          </div>

        </div>
      </main>

      <Footer />
    </div>
  )
}

export default TourDetails