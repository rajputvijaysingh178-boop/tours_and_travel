import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function Packages() {
  const packages = [
    {
      id: 'kerala',
      name: 'Kerala Nature Explorer',
      location: 'Kerala',
      days: '5 Days / 4 Nights',
      price: '₹18,000',
      icon: '🌴',
      description:
        'Explore beautiful backwaters, hill stations, beaches, and natural landscapes.',
    },
    {
      id: 'rajasthan',
      name: 'Rajasthan Heritage Tour',
      location: 'Rajasthan',
      days: '6 Days / 5 Nights',
      price: '₹25,000',
      icon: '🏰',
      description:
        'Experience royal palaces, historic forts, culture, and traditional Rajasthan.',
    },
    {
      id: 'goa',
      name: 'Goa Beach Holiday',
      location: 'Goa',
      days: '4 Days / 3 Nights',
      price: '₹15,000',
      icon: '🏖️',
      description:
        'Enjoy beautiful beaches, relaxing stays, and exciting coastal experiences.',
    },
    {
      id: 'himachal',
      name: 'Himachal Adventure',
      location: 'Himachal Pradesh',
      days: '7 Days / 6 Nights',
      price: '₹30,000',
      icon: '🏔️',
      description:
        'Discover mountains, adventure activities, valleys, and scenic landscapes.',
    },
  ]

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

        {/* Package Cards */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">

          {packages.map((tour) => (
            <div
              key={tour.id}
              className="overflow-hidden rounded-xl bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-xl"
            >

              {/* Image / Icon */}
              <div className="flex h-44 items-center justify-center bg-blue-100 text-7xl">
                {tour.icon}
              </div>

              {/* Package Information */}
              <div className="p-5">

                <span className="text-sm font-semibold text-blue-600">
                  {tour.location}
                </span>

                <h3 className="mt-2 text-xl font-bold text-gray-800">
                  {tour.name}
                </h3>

                <p className="mt-2 text-sm text-gray-500">
                  {tour.description}
                </p>

                <p className="mt-4 text-sm font-medium text-gray-600">
                  🗓️ {tour.days}
                </p>

                {/* Price + Button */}
                <div className="mt-5 flex items-center justify-between">

                  <div>
                    <p className="text-xs text-gray-500">
                      Starting from
                    </p>

                    <p className="text-xl font-bold text-blue-600">
                      {tour.price}
                    </p>
                  </div>

                  <Link
                    to={`/packages/${tour.id}`}
                    className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                  >
                    View Details
                  </Link>

                </div>

              </div>
            </div>
          ))}

        </div>
      </section>

      <Footer />
    </div>
  )
}

export default Packages