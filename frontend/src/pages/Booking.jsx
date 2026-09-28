import { Link, useParams } from 'react-router-dom'
import { useState } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function Booking() {
  const { id } = useParams()

  const [travelDate, setTravelDate] = useState('')
  const [passengers, setPassengers] = useState(1)

  const [passengerDetails, setPassengerDetails] = useState({
    name: '',
    age: '',
    email: '',
    phone: '',
    address: '',
  })

  const packages = {
    kerala: {
      name: 'Kerala Nature Explorer',
      location: 'Kerala',
      days: '5 Days / 4 Nights',
      price: 18000,
      icon: '🌴',
    },

    rajasthan: {
      name: 'Rajasthan Heritage Tour',
      location: 'Rajasthan',
      days: '6 Days / 5 Nights',
      price: 25000,
      icon: '🏰',
    },

    goa: {
      name: 'Goa Beach Holiday',
      location: 'Goa',
      days: '4 Days / 3 Nights',
      price: 15000,
      icon: '🏖️',
    },

    himachal: {
      name: 'Himachal Adventure',
      location: 'Himachal Pradesh',
      days: '7 Days / 6 Nights',
      price: 30000,
      icon: '🏔️',
    },
  }

  const tour = packages[id]

  const totalPrice = tour ? tour.price * passengers : 0

  if (!tour) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />

        <div className="px-6 py-20 text-center">
          <h1 className="text-3xl font-bold text-gray-900">
            Tour Package Not Found
          </h1>

          <Link
            to="/packages"
            className="mt-6 inline-block rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
          >
            Back to Packages
          </Link>
        </div>

        <Footer />
      </div>
    )
  }

  const handlePassengerChange = (field, value) => {
    setPassengerDetails({
      ...passengerDetails,
      [field]: value,
    })
  }

  const handleCheckAvailability = () => {
    if (!travelDate) {
      alert('Please select a travel date.')
      return
    }

    if (!passengerDetails.name) {
      alert('Please enter passenger name.')
      return
    }

    if (!passengerDetails.email) {
      alert('Please enter passenger email.')
      return
    }

    if (!passengerDetails.phone) {
      alert('Please enter passenger phone number.')
      return
    }

    alert(
      `Availability check requested for ${passengers} passenger(s) on ${travelDate}.`
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Header */}
      <section className="bg-blue-600 px-6 py-12 text-white">
        <div className="mx-auto max-w-7xl">
          <p className="text-blue-200">
            Complete Your Booking
          </p>

          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            {tour.name}
          </h1>

          <p className="mt-3 text-blue-100">
            {tour.location} • {tour.days}
          </p>
        </div>
      </section>

      <main className="mx-auto max-w-7xl px-6 py-12">
        <div className="grid gap-8 lg:grid-cols-3">

          {/* LEFT SIDE */}
          <div className="lg:col-span-2">

            {/* Travel Details */}
            <div className="rounded-xl bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold text-gray-900">
                Travel Details
              </h2>

              <p className="mt-2 text-gray-500">
                Select your travel date and number of passengers.
              </p>

              <div className="mt-6 grid gap-5 md:grid-cols-2">

                {/* Travel Date */}
                <div>
                  <label className="mb-2 block font-medium text-gray-700">
                    Travel Date
                  </label>

                  <input
                    type="date"
                    value={travelDate}
                    onChange={(e) => setTravelDate(e.target.value)}
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Passengers */}
                <div>
                  <label className="mb-2 block font-medium text-gray-700">
                    Number of Passengers
                  </label>

                  <select
                    value={passengers}
                    onChange={(e) =>
                      setPassengers(Number(e.target.value))
                    }
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="1">1 Passenger</option>
                    <option value="2">2 Passengers</option>
                    <option value="3">3 Passengers</option>
                    <option value="4">4 Passengers</option>
                    <option value="5">5 Passengers</option>
                    <option value="6">6 Passengers</option>
                  </select>
                </div>

              </div>
            </div>

            {/* Passenger Information */}
            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold text-gray-900">
                Passenger Information
              </h2>

              <p className="mt-2 text-gray-500">
                Enter the details of the primary passenger.
              </p>

              <div className="mt-6 grid gap-5 md:grid-cols-2">

                {/* Name */}
                <div>
                  <label className="mb-2 block font-medium text-gray-700">
                    Full Name
                  </label>

                  <input
                    type="text"
                    placeholder="Enter full name"
                    value={passengerDetails.name}
                    onChange={(e) =>
                      handlePassengerChange('name', e.target.value)
                    }
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Age */}
                <div>
                  <label className="mb-2 block font-medium text-gray-700">
                    Age
                  </label>

                  <input
                    type="number"
                    placeholder="Enter age"
                    min="1"
                    value={passengerDetails.age}
                    onChange={(e) =>
                      handlePassengerChange('age', e.target.value)
                    }
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
                    placeholder="Enter email"
                    value={passengerDetails.email}
                    onChange={(e) =>
                      handlePassengerChange('email', e.target.value)
                    }
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
                    placeholder="Enter phone number"
                    value={passengerDetails.phone}
                    onChange={(e) =>
                      handlePassengerChange('phone', e.target.value)
                    }
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

              </div>

              {/* Address */}
              <div className="mt-5">
                <label className="mb-2 block font-medium text-gray-700">
                  Address
                </label>

                <textarea
                  rows="3"
                  placeholder="Enter your address"
                  value={passengerDetails.address}
                  onChange={(e) =>
                    handlePassengerChange('address', e.target.value)
                  }
                  className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Availability */}
            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
              <h2 className="text-xl font-bold text-gray-900">
                Check Availability
              </h2>

              <p className="mt-2 text-gray-500">
                Check whether this tour is available for your
                selected travel date and number of passengers.
              </p>

              <button
                type="button"
                onClick={handleCheckAvailability}
                className="mt-5 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
              >
                Check Availability
              </button>
            </div>

          </div>

          {/* RIGHT SIDE - BOOKING SUMMARY */}
          <div>
            <div className="sticky top-6 rounded-xl bg-white p-6 shadow-lg">

              {/* Package Icon */}
              <div className="flex h-32 items-center justify-center rounded-lg bg-blue-100 text-7xl">
                {tour.icon}
              </div>

              {/* Package Name */}
              <h2 className="mt-5 text-xl font-bold text-gray-900">
                {tour.name}
              </h2>

              <p className="mt-2 text-gray-500">
                📍 {tour.location}
              </p>

              <p className="mt-2 text-gray-500">
                🗓️ {tour.days}
              </p>

              <div className="my-6 border-t" />

              {/* Price Per Person */}
              <div className="flex justify-between">
                <span className="text-gray-500">
                  Price per person
                </span>

                <span className="font-semibold">
                  ₹{tour.price.toLocaleString('en-IN')}
                </span>
              </div>

              {/* Passenger Count */}
              <div className="mt-4 flex justify-between">
                <span className="text-gray-500">
                  Passengers
                </span>

                <span className="font-semibold">
                  {passengers}
                </span>
              </div>

              {/* Travel Date */}
              <div className="mt-4 flex justify-between">
                <span className="text-gray-500">
                  Travel Date
                </span>

                <span className="font-semibold">
                  {travelDate || 'Not selected'}
                </span>
              </div>

              <div className="my-6 border-t" />

              {/* Total */}
              <div className="flex justify-between text-lg">
                <span className="font-bold">
                  Total
                </span>

                <span className="font-bold text-blue-600">
                  ₹{totalPrice.toLocaleString('en-IN')}
                </span>
              </div>

              {/* Payment Button */}
              <button
                type="button"
                onClick={() => {
                  alert(
                    'Please check availability before continuing to payment.'
                  )
                }}
                className="mt-6 w-full rounded-lg bg-green-600 px-6 py-3 font-semibold text-white hover:bg-green-700"
              >
                Continue to Payment
              </button>

              {/* Back */}
              <Link
                to={`/packages/${id}`}
                className="mt-3 block text-center text-sm font-medium text-blue-600 hover:underline"
              >
                ← Back to Tour Details
              </Link>

            </div>
          </div>

        </div>
      </main>

      <Footer />
    </div>
  )
}

export default Booking