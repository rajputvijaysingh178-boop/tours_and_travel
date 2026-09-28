import { Link, useParams } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function TourDetails() {
  const { id } = useParams()

  const packages = [
    {
      id: 'kerala',
      name: 'Kerala Nature Explorer',
      location: 'Kerala',
      days: '5 Days / 4 Nights',
      price: '₹18,000',
      icon: '🌴',
      description:
        'Explore the beautiful landscapes of Kerala including backwaters, beaches, hill stations, and natural attractions.',
      itinerary: [
        'Day 1 - Arrival and local sightseeing',
        'Day 2 - Explore Munnar',
        'Day 3 - Visit waterfalls and tea plantations',
        'Day 4 - Kerala backwater experience',
        'Day 5 - Departure'
      ],
      includes: [
        'Hotel accommodation',
        'Daily breakfast',
        'Transportation',
        'Sightseeing'
      ],
      excludes: [
        'Personal expenses',
        'Travel insurance',
        'Additional activities'
      ]
    },
    {
      id: 'rajasthan',
      name: 'Rajasthan Heritage Tour',
      location: 'Rajasthan',
      days: '6 Days / 5 Nights',
      price: '₹25,000',
      icon: '🏰',
      description:
        'Experience the royal heritage of Rajasthan through historic forts, palaces, culture, and traditional attractions.',
      itinerary: [
        'Day 1 - Arrival in Jaipur',
        'Day 2 - Jaipur sightseeing',
        'Day 3 - Visit historic forts',
        'Day 4 - Travel to Udaipur',
        'Day 5 - Udaipur sightseeing',
        'Day 6 - Departure'
      ],
      includes: [
        'Hotel accommodation',
        'Daily breakfast',
        'Transportation',
        'Sightseeing'
      ],
      excludes: [
        'Personal expenses',
        'Travel insurance',
        'Additional activities'
      ]
    },
    {
      id: 'goa',
      name: 'Goa Beach Holiday',
      location: 'Goa',
      days: '4 Days / 3 Nights',
      price: '₹15,000',
      icon: '🏖️',
      description:
        'Enjoy a relaxing Goa holiday with beautiful beaches, sightseeing, local experiences, and leisure activities.',
      itinerary: [
        'Day 1 - Arrival and beach visit',
        'Day 2 - North Goa sightseeing',
        'Day 3 - South Goa sightseeing',
        'Day 4 - Departure'
      ],
      includes: [
        'Hotel accommodation',
        'Daily breakfast',
        'Transportation',
        'Sightseeing'
      ],
      excludes: [
        'Personal expenses',
        'Travel insurance',
        'Additional activities'
      ]
    },
    {
      id: 'himachal',
      name: 'Himachal Adventure',
      location: 'Himachal Pradesh',
      days: '7 Days / 6 Nights',
      price: '₹30,000',
      icon: '🏔️',
      description:
        'Discover the mountains of Himachal Pradesh with scenic landscapes, adventure experiences, and beautiful valleys.',
      itinerary: [
        'Day 1 - Arrival',
        'Day 2 - Local sightseeing',
        'Day 3 - Mountain exploration',
        'Day 4 - Adventure activities',
        'Day 5 - Valley sightseeing',
        'Day 6 - Local experiences',
        'Day 7 - Departure'
      ],
      includes: [
        'Hotel accommodation',
        'Daily breakfast',
        'Transportation',
        'Sightseeing'
      ],
      excludes: [
        'Personal expenses',
        'Travel insurance',
        'Additional activities'
      ]
    }
  ]

  const tour = packages.find((item) => item.id === id)

  if (!tour) {
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
            {tour.location}
          </p>

          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            {tour.name}
          </h1>

          <p className="mt-4 text-lg text-blue-100">
            {tour.days}
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
              {tour.icon}
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

            {/* Itinerary */}
            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold text-gray-900">
                Tour Itinerary
              </h2>

              <div className="mt-5 space-y-4">
                {tour.itinerary.map((day) => (
                  <div
                    key={day}
                    className="rounded-lg border-l-4 border-blue-600 bg-gray-50 p-4"
                  >
                    <p className="font-medium text-gray-700">
                      {day}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Included / Excluded */}
            <div className="mt-6 grid gap-6 md:grid-cols-2">

              <div className="rounded-xl bg-white p-6 shadow-sm">
                <h2 className="text-xl font-bold text-gray-900">
                  What's Included
                </h2>

                <ul className="mt-4 space-y-3">
                  {tour.includes.map((item) => (
                    <li key={item} className="text-gray-600">
                      ✅ {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-xl bg-white p-6 shadow-sm">
                <h2 className="text-xl font-bold text-gray-900">
                  What's Not Included
                </h2>

                <ul className="mt-4 space-y-3">
                  {tour.excludes.map((item) => (
                    <li key={item} className="text-gray-600">
                      ❌ {item}
                    </li>
                  ))}
                </ul>
              </div>

            </div>
          </div>

          {/* Booking Card */}
          <div>
            <div className="sticky top-6 rounded-xl bg-white p-6 shadow-lg">

              <p className="text-sm text-gray-500">
                Starting from
              </p>

              <p className="mt-1 text-3xl font-bold text-blue-600">
                {tour.price}
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
                    {tour.location}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-500">
                    Duration
                  </span>

                  <span className="font-semibold">
                    {tour.days}
                  </span>
                </div>
              </div>

              <Link
                to={`/booking/${tour.id}`}
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