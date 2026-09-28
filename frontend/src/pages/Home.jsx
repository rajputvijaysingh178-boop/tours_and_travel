import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function Home() {
  return (
    <div className="min-h-screen bg-gray-50">

      <Navbar />

      {/* Hero Section */}
      <section className="bg-blue-600 px-6 py-24 text-white">
        <div className="mx-auto max-w-7xl">

          <div className="max-w-3xl">

            <p className="mb-4 font-semibold uppercase tracking-wider text-blue-200">
              Explore • Travel • Experience
            </p>

            <h1 className="text-5xl font-bold leading-tight md:text-6xl">
              Discover Your Next
              <span className="text-yellow-300">
                {' '}Adventure
              </span>
            </h1>

            <p className="mt-6 text-lg text-blue-100">
              Explore amazing destinations, discover exciting tour
              packages, and create unforgettable memories with TravelEase.
            </p>

            <div className="mt-8 flex flex-wrap gap-4">

              <Link
                to="/packages"
                className="rounded-lg bg-white px-7 py-3 font-semibold text-blue-600 hover:bg-gray-100"
              >
                Explore Tours
              </Link>

              <Link
                to="/register"
                className="rounded-lg border border-white px-7 py-3 font-semibold text-white hover:bg-blue-700"
              >
                Create Account
              </Link>

            </div>

          </div>

        </div>
      </section>


      {/* Search Section */}
      <section className="relative -mt-10 px-6">

        <div className="mx-auto max-w-6xl rounded-xl bg-white p-6 shadow-xl">

          <h2 className="text-xl font-bold text-gray-800">
            Find Your Perfect Tour
          </h2>

          <div className="mt-5 grid gap-4 md:grid-cols-4">

            <input
              type="text"
              placeholder="Destination"
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <select className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500">
              <option>Any Duration</option>
              <option>1 - 3 Days</option>
              <option>4 - 6 Days</option>
              <option>7+ Days</option>
            </select>

            <input
              type="date"
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700">
              Search Tours
            </button>

          </div>

        </div>

      </section>


      {/* Popular Destinations */}
      <section className="mx-auto max-w-7xl px-6 py-20">

        <div className="text-center">

          <p className="font-semibold text-blue-600">
            EXPLORE
          </p>

          <h2 className="mt-2 text-3xl font-bold text-gray-900">
            Popular Destinations
          </h2>

          <p className="mt-3 text-gray-600">
            Explore some of the most exciting destinations.
          </p>

        </div>


        <div className="mt-10 grid gap-6 md:grid-cols-4">

          {[
            'Kerala',
            'Rajasthan',
            'Goa',
            'Himachal Pradesh'
          ].map((destination) => (

            <div
              key={destination}
              className="cursor-pointer rounded-xl bg-white p-8 text-center shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
            >

              <div className="text-5xl">
                🌴
              </div>

              <h3 className="mt-4 text-xl font-bold text-gray-800">
                {destination}
              </h3>

              <p className="mt-2 text-gray-500">
                Explore amazing experiences
              </p>

            </div>

          ))}

        </div>

      </section>


      {/* Featured Packages */}
      <section className="bg-gray-100 px-6 py-20">

        <div className="mx-auto max-w-7xl">

          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">

            <div>

              <p className="font-semibold text-blue-600">
                FEATURED TOURS
              </p>

              <h2 className="mt-2 text-3xl font-bold text-gray-900">
                Popular Tour Packages
              </h2>

            </div>

            <Link
              to="/packages"
              className="font-semibold text-blue-600 hover:text-blue-700"
            >
              View All Tours →
            </Link>

          </div>


          <div className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-4">

            {[
              {
                name: 'Kerala Nature Explorer',
                days: '5 Days',
                price: '₹18,000'
              },
              {
                name: 'Rajasthan Heritage Tour',
                days: '6 Days',
                price: '₹25,000'
              },
              {
                name: 'Goa Beach Holiday',
                days: '4 Days',
                price: '₹15,000'
              },
              {
                name: 'Himachal Adventure',
                days: '7 Days',
                price: '₹30,000'
              }
            ].map((tour) => (

              <div
                key={tour.name}
                className="overflow-hidden rounded-xl bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
              >

                <div className="flex h-40 items-center justify-center bg-blue-100 text-6xl">
                  🏔️
                </div>

                <div className="p-5">

                  <h3 className="text-lg font-bold text-gray-800">
                    {tour.name}
                  </h3>

                  <p className="mt-2 text-gray-500">
                    🗓️ {tour.days}
                  </p>

                  <div className="mt-5 flex items-center justify-between">

                    <span className="text-xl font-bold text-blue-600">
                      {tour.price}
                    </span>

                    <Link
                      to="/packages"
                      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                    >
                      View
                    </Link>

                  </div>

                </div>

              </div>

            ))}

          </div>

        </div>

      </section>


      {/* Why TravelEase */}
      <section className="mx-auto max-w-7xl px-6 py-20">

        <div className="text-center">

          <p className="font-semibold text-blue-600">
            WHY TRAVELEASE
          </p>

          <h2 className="mt-2 text-3xl font-bold text-gray-900">
            Everything You Need for Your Journey
          </h2>

        </div>


        <div className="mt-10 grid gap-6 md:grid-cols-3">

          {[
            {
              icon: '🧳',
              title: 'Wide Range of Tours',
              text: 'Choose from exciting destinations and carefully planned tour packages.'
            },
            {
              icon: '🔒',
              title: 'Secure Booking',
              text: 'Your booking information is handled through a secure platform.'
            },
            {
              icon: '💬',
              title: 'Complete Support',
              text: 'Manage bookings, itineraries, payments, and travel information in one place.'
            }
          ].map((item) => (

            <div
              key={item.title}
              className="rounded-xl bg-white p-8 text-center shadow-sm"
            >

              <div className="text-5xl">
                {item.icon}
              </div>

              <h3 className="mt-5 text-xl font-bold text-gray-800">
                {item.title}
              </h3>

              <p className="mt-3 text-gray-600">
                {item.text}
              </p>

            </div>

          ))}

        </div>

      </section>


      <Footer />

    </div>
  )
}

export default Home
