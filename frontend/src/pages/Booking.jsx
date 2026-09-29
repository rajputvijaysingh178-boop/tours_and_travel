import { Link, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

import {
  getAvailableGuides,
  assignGuide,
} from '../services/api'


const API_URL = 'http://127.0.0.1:8000'


function Booking() {

  const { id } = useParams()


  // -----------------------------------
  // PACKAGE
  // -----------------------------------

  const [tour, setTour] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')


  // -----------------------------------
  // TRAVEL DETAILS
  // -----------------------------------

  const [travelDate, setTravelDate] = useState('')
  const [passengers, setPassengers] = useState(1)
  const [selectedDeparture, setSelectedDeparture] = useState(null)


  // -----------------------------------
  // BOOKING
  // -----------------------------------

  const [booking, setBooking] = useState(null)


  // -----------------------------------
  // PAYMENT
  // -----------------------------------

  const [paymentLoading, setPaymentLoading] = useState(false)
  const [paymentCompleted, setPaymentCompleted] = useState(false)


  // -----------------------------------
  // PASSENGER DETAILS
  // -----------------------------------

  const [passengerDetails, setPassengerDetails] = useState({
    name: '',
    age: '',
    email: '',
    phone: '',
    address: '',
  })


  // -----------------------------------
  // TOUR GUIDE
  // -----------------------------------

  const [availableGuides, setAvailableGuides] = useState([])
  const [selectedGuide, setSelectedGuide] = useState('')
  const [guideLoading, setGuideLoading] = useState(false)
  const [guideAssigned, setGuideAssigned] = useState(false)


  // -----------------------------------
  // TOTAL PRICE
  // -----------------------------------

  const totalPrice = tour
    ? Number(tour.base_price || 0) * passengers
    : 0


  // -----------------------------------
  // LOAD PACKAGE
  // -----------------------------------

  useEffect(() => {

    const loadPackage = async () => {

      try {

        setLoading(true)
        setError('')


        const response =
          await fetch(
            `${API_URL}/packages/${id}`
          )


        if (!response.ok) {
          throw new Error(
            'Package not found'
          )
        }


        const data =
          await response.json()


        setTour(data)

      } catch (err) {

        console.error(
          'Package loading error:',
          err
        )

        setError(
          'Tour Package Not Found'
        )

      } finally {

        setLoading(false)

      }
    }


    if (id) {
      loadPackage()
    }

  }, [id])


  // -----------------------------------
  // PASSENGER DETAILS
  // -----------------------------------

  const handlePassengerChange = (
    field,
    value
  ) => {

    setPassengerDetails(
      (previous) => ({
        ...previous,
        [field]: value,
      })
    )

  }


  // -----------------------------------
  // CHECK AVAILABILITY
  // -----------------------------------

  const handleCheckAvailability =
    async () => {

      if (
        !passengerDetails.name.trim()
      ) {

        alert(
          'Please enter passenger name.'
        )

        return
      }


      if (
        !passengerDetails.email.trim()
      ) {

        alert(
          'Please enter passenger email.'
        )

        return
      }


      if (
        !passengerDetails.phone.trim()
      ) {

        alert(
          'Please enter passenger phone number.'
        )

        return
      }


      if (!travelDate) {

        alert(
          'Please select your travel date.'
        )

        return
      }


      try {

        const response =
          await fetch(
            `${API_URL}/departures`
          )


        if (!response.ok) {

          throw new Error(
            'Failed to fetch departures'
          )

        }


        const departures =
          await response.json()


        // Find capacity/departure record
        // connected to this package.

        const departure =
          departures.find(
            (item) =>
              item.package_id ===
                tour.package_id &&
              typeof item.status ===
                'string'
          )


        if (!departure) {

          setSelectedDeparture(null)

          alert(
            'No capacity is configured for this package.'
          )

          return
        }


        const capacity =
          Number(
            departure.capacity || 0
          )


        if (capacity <= 0) {

          setSelectedDeparture(null)

          alert(
            'No passenger capacity is available for this package.'
          )

          return
        }


        if (passengers > capacity) {

          setSelectedDeparture(null)

          alert(
            `Only ${capacity} passengers can be accommodated.`
          )

          return
        }


        setSelectedDeparture(
          departure
        )


        alert(
          `Tour is available for ${travelDate}!\n\n` +
          `${passengers} passenger(s) can be accommodated.`
        )

      } catch (error) {

        console.error(
          'Availability error:',
          error
        )


        setSelectedDeparture(null)


        alert(
          error.message ||
          'Unable to check availability. Please try again.'
        )

      }

    }


  // -----------------------------------
  // CREATE BOOKING
  // -----------------------------------

  const handleCreateBooking =
    async () => {

      if (!selectedDeparture) {

        alert(
          'Please check availability first.'
        )

        return
      }


      if (!travelDate) {

        alert(
          'Please select your travel date.'
        )

        return
      }


      const token =
        localStorage.getItem(
          'access_token'
        )


      if (!token) {

        alert(
          'Please login before booking.'
        )

        return
      }


      try {

        const response =
          await fetch(
            `${API_URL}/bookings?package_id=${encodeURIComponent(
              tour.package_id
            )}&travel_date=${encodeURIComponent(
              travelDate
            )}&passenger_count=${passengers}`,
            {
              method: 'POST',

              headers: {
                Authorization:
                  `Bearer ${token}`,
              },
            }
          )


        const data =
          await response.json()


        if (!response.ok) {

          throw new Error(
            data.detail ||
            'Booking failed'
          )

        }


        setBooking(data)


        alert(
          `Booking created successfully!\n\n` +
          `Booking ID: ${data.booking_id}\n` +
          `Total Amount: ₹${Number(
            data.total_amount
          ).toLocaleString('en-IN')}`
        )

      } catch (error) {

        console.error(
          'Booking error:',
          error
        )


        alert(
          error.message ||
          'Unable to create booking.'
        )

      }

    }


  // -----------------------------------
  // LOAD AVAILABLE GUIDES
  // -----------------------------------

  const loadAvailableGuides =
    async () => {

      try {

        const guides =
          await getAvailableGuides()


        setAvailableGuides(
          Array.isArray(guides)
            ? guides
            : []
        )

      } catch (error) {

        console.error(
          'Guide loading error:',
          error
        )


        setAvailableGuides([])


        alert(
          error.message ||
          'Unable to load available tour guides.'
        )

      }

    }


  // -----------------------------------
  // PAYMENT
  // -----------------------------------

  const handlePayment =
    async () => {

      if (!booking) {

        alert(
          'Please create your booking first.'
        )

        return
      }


      try {

        setPaymentLoading(true)


        const paymentReference =
          `MOCK-PAY-${Date.now()}`


        const response =
          await fetch(
            `${API_URL}/bookings/${booking.booking_id}/payments`,
            {
              method: 'POST',

              headers: {
                'Content-Type':
                  'application/json',
              },

              body: JSON.stringify({
                booking_id:
                  booking.booking_id,

                payment_reference:
                  paymentReference,

                amount:
                  booking.total_amount,
              }),
            }
          )


        const data =
          await response.json()


        if (!response.ok) {

          throw new Error(
            data.detail ||
            'Payment failed'
          )

        }


        // Payment completed
        setPaymentCompleted(true)


        // Load available guides
        // immediately after payment.
        await loadAvailableGuides()


        alert(
          `Payment successful!\n\n` +
          `Payment ID: ${data.payment_id}\n` +
          `Reference: ${paymentReference}`
        )

      } catch (error) {

        console.error(
          'Payment error:',
          error
        )


        alert(
          error.message ||
          'Unable to process payment.'
        )

      } finally {

        setPaymentLoading(false)

      }

    }


  // -----------------------------------
  // ASSIGN TOUR GUIDE
  // -----------------------------------

  const handleAssignGuide =
    async () => {

      if (!selectedGuide) {

        alert(
          'Please select a tour guide.'
        )

        return
      }


      if (!selectedDeparture) {

        alert(
          'Departure information is missing.'
        )

        return
      }


      try {

        setGuideLoading(true)


        await assignGuide(
          selectedGuide,
          selectedDeparture.departure_id
        )


        setGuideAssigned(true)


        // Remove assigned guide
        // from available list.
        setAvailableGuides(
          (previous) =>
            previous.filter(
              (guide) =>
                guide.guide_id !==
                selectedGuide
            )
        )


        alert(
          'Tour guide assigned successfully!'
        )

      } catch (error) {

        console.error(
          'Guide assignment error:',
          error
        )


        alert(
          error.message ||
          'Failed to assign tour guide.'
        )

      } finally {

        setGuideLoading(false)

      }

    }


  // -----------------------------------
  // LOADING
  // -----------------------------------

  if (loading) {

    return (

      <div className="min-h-screen bg-gray-50">

        <Navbar />


        <div className="mx-auto max-w-7xl px-6 py-20 text-center">

          <p className="text-lg text-gray-500">
            Loading booking details...
          </p>

        </div>


        <Footer />

      </div>

    )

  }


  // -----------------------------------
  // ERROR
  // -----------------------------------

  if (error || !tour) {

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


  // -----------------------------------
  // MAIN UI
  // -----------------------------------

  return (

    <div className="min-h-screen bg-gray-50">

      <Navbar />


      {/* HEADER */}

      <section className="bg-blue-600 px-6 py-12 text-white">

        <div className="mx-auto max-w-7xl">

          <p className="text-blue-200">
            Complete Your Booking
          </p>


          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            {tour.name}
          </h1>


          <p className="mt-3 text-blue-100">
            {tour.destination} • {tour.duration} Days
          </p>

        </div>

      </section>


      <main className="mx-auto max-w-7xl px-6 py-12">

        <div className="grid gap-8 lg:grid-cols-3">


          {/* =====================================
              LEFT SIDE
          ===================================== */}

          <div className="lg:col-span-2">


            {/* TRAVEL DETAILS */}

            <div className="rounded-xl bg-white p-6 shadow-sm">

              <h2 className="text-2xl font-bold text-gray-900">
                Travel Details
              </h2>


              <p className="mt-2 text-gray-500">
                Select your own travel date and number
                of passengers.
              </p>


              <div className="mt-6 grid gap-5 md:grid-cols-2">


                {/* DATE */}

                <div>

                  <label className="mb-2 block font-medium text-gray-700">
                    Travel Date
                  </label>


                  <input
                    type="date"
                    value={travelDate}
                    onChange={(e) => {

                      setTravelDate(
                        e.target.value
                      )

                      setSelectedDeparture(
                        null
                      )

                      setBooking(null)

                      setPaymentCompleted(
                        false
                      )

                      setGuideAssigned(
                        false
                      )

                    }}
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />

                </div>


                {/* PASSENGERS */}

                <div>

                  <label className="mb-2 block font-medium text-gray-700">
                    Number of Passengers
                  </label>


                  <select
                    value={passengers}
                    onChange={(e) => {

                      setPassengers(
                        Number(
                          e.target.value
                        )
                      )

                      setSelectedDeparture(
                        null
                      )

                      setBooking(null)

                      setPaymentCompleted(
                        false
                      )

                      setGuideAssigned(
                        false
                      )

                    }}
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  >

                    {Array.from(
                      {
                        length: Math.min(
                          Number(
                            tour.max_passengers ||
                            6
                          ),
                          6
                        ),
                      },
                      (_, index) =>
                        index + 1
                    ).map(
                      (number) => (

                        <option
                          key={number}
                          value={number}
                        >

                          {number}
                          {' '}
                          Passenger
                          {number > 1
                            ? 's'
                            : ''}

                        </option>

                      )
                    )}

                  </select>

                </div>

              </div>

            </div>


            {/* PASSENGER INFORMATION */}

            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">

              <h2 className="text-2xl font-bold text-gray-900">
                Passenger Information
              </h2>


              <p className="mt-2 text-gray-500">
                Enter the details of the primary passenger.
              </p>


              <div className="mt-6 grid gap-5 md:grid-cols-2">


                {/* NAME */}

                <div>

                  <label className="mb-2 block font-medium text-gray-700">
                    Full Name
                  </label>


                  <input
                    type="text"
                    placeholder="Enter full name"
                    value={
                      passengerDetails.name
                    }
                    onChange={(e) =>
                      handlePassengerChange(
                        'name',
                        e.target.value
                      )
                    }
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />

                </div>


                {/* AGE */}

                <div>

                  <label className="mb-2 block font-medium text-gray-700">
                    Age
                  </label>


                  <input
                    type="number"
                    placeholder="Enter age"
                    min="1"
                    value={
                      passengerDetails.age
                    }
                    onChange={(e) =>
                      handlePassengerChange(
                        'age',
                        e.target.value
                      )
                    }
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />

                </div>


                {/* EMAIL */}

                <div>

                  <label className="mb-2 block font-medium text-gray-700">
                    Email
                  </label>


                  <input
                    type="email"
                    placeholder="Enter email"
                    value={
                      passengerDetails.email
                    }
                    onChange={(e) =>
                      handlePassengerChange(
                        'email',
                        e.target.value
                      )
                    }
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />

                </div>


                {/* PHONE */}

                <div>

                  <label className="mb-2 block font-medium text-gray-700">
                    Phone Number
                  </label>


                  <input
                    type="tel"
                    placeholder="Enter phone number"
                    value={
                      passengerDetails.phone
                    }
                    onChange={(e) =>
                      handlePassengerChange(
                        'phone',
                        e.target.value
                      )
                    }
                    className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  />

                </div>

              </div>


              {/* ADDRESS */}

              <div className="mt-5">

                <label className="mb-2 block font-medium text-gray-700">
                  Address
                </label>


                <textarea
                  rows="3"
                  placeholder="Enter your address"
                  value={
                    passengerDetails.address
                  }
                  onChange={(e) =>
                    handlePassengerChange(
                      'address',
                      e.target.value
                    )
                  }
                  className="w-full rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                />

              </div>

            </div>


            {/* AVAILABILITY */}

            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">

              <h2 className="text-xl font-bold text-gray-900">
                Check Availability
              </h2>


              <p className="mt-2 text-gray-500">
                Check whether this package is available
                for your selected date.
              </p>


              <button
                type="button"
                onClick={
                  handleCheckAvailability
                }
                className="mt-5 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
              >
                Check Availability
              </button>


              {selectedDeparture && (

                <div className="mt-4 rounded-lg bg-green-50 p-4">

                  <p className="font-semibold text-green-700">
                    ✓ Tour Available
                  </p>


                  <p className="mt-1 text-green-600">

                    {passengers}
                    {' '}
                    passenger
                    {passengers > 1
                      ? 's'
                      : ''}
                    {' '}
                    can travel on{' '}
                    {travelDate}.

                  </p>

                </div>

              )}

            </div>


            {/* PAYMENT */}

            {booking &&
              !paymentCompleted && (

                <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">

                  <h2 className="text-xl font-bold text-gray-900">
                    Payment
                  </h2>


                  <p className="mt-2 text-gray-500">
                    This is a mock payment for project
                    demonstration.
                  </p>


                  <div className="mt-5 rounded-lg bg-gray-50 p-4">

                    <div className="flex justify-between">

                      <span className="text-gray-500">
                        Booking ID
                      </span>


                      <span className="font-medium">
                        {booking.booking_id}
                      </span>

                    </div>


                    <div className="mt-3 flex justify-between">

                      <span className="text-gray-500">
                        Travel Date
                      </span>


                      <span className="font-medium">
                        {booking.travel_date}
                      </span>

                    </div>


                    <div className="mt-3 flex justify-between">

                      <span className="text-gray-500">
                        Amount
                      </span>


                      <span className="font-bold text-blue-600">

                        ₹
                        {Number(
                          booking.total_amount
                        ).toLocaleString(
                          'en-IN'
                        )}

                      </span>

                    </div>

                  </div>


                  <button
                    type="button"
                    onClick={
                      handlePayment
                    }
                    disabled={
                      paymentLoading
                    }
                    className="mt-5 w-full rounded-lg bg-green-600 px-6 py-3 font-semibold text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
                  >

                    {paymentLoading
                      ? 'Processing Payment...'
                      : 'Pay Now'}

                  </button>

                </div>

              )}


            {/* PAYMENT SUCCESS */}

            {paymentCompleted && (

              <div className="mt-6 rounded-xl bg-green-50 p-6">

                <h2 className="text-2xl font-bold text-green-700">
                  ✓ Payment Successful
                </h2>


                <p className="mt-2 text-green-600">
                  Your booking payment has been
                  completed successfully.
                </p>


                <div className="mt-4 rounded-lg bg-white p-4">

                  <p className="text-sm text-gray-500">
                    Booking ID
                  </p>


                  <p className="font-semibold text-gray-900">
                    {booking.booking_id}
                  </p>


                  <p className="mt-3 text-sm text-gray-500">
                    Travel Date
                  </p>


                  <p className="font-semibold text-gray-900">
                    {booking.travel_date}
                  </p>


                  <p className="mt-3 text-sm text-gray-500">
                    Amount Paid
                  </p>


                  <p className="font-bold text-green-600">

                    ₹
                    {Number(
                      booking.total_amount
                    ).toLocaleString(
                      'en-IN'
                    )}

                  </p>

                </div>

              </div>

            )}


            {/* =====================================
                TOUR GUIDE SELECTION
            ===================================== */}

            {paymentCompleted &&
              !guideAssigned && (

                <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">

                  <h2 className="text-2xl font-bold text-gray-900">
                    Select Your Tour Guide
                  </h2>


                  <p className="mt-2 text-gray-500">
                    Your payment is complete.
                    Select an available tour guide
                    for your trip.
                  </p>


                  {availableGuides.length === 0 ? (

                    <div className="mt-5 rounded-lg bg-yellow-50 p-4 text-yellow-700">

                      No tour guides are currently
                      available.

                    </div>

                  ) : (

                    <div className="mt-5 space-y-4">

                      {availableGuides.map(
                        (guide) => (

                          <label
                            key={
                              guide.guide_id
                            }
                            className={`block cursor-pointer rounded-lg border p-5 transition ${
                              selectedGuide ===
                              guide.guide_id
                                ? 'border-blue-600 bg-blue-50'
                                : 'border-gray-200 hover:border-blue-400'
                            }`}
                          >

                            <div className="flex gap-4">

                              <input
                                type="radio"
                                name="tourGuide"
                                value={
                                  guide.guide_id
                                }
                                checked={
                                  selectedGuide ===
                                  guide.guide_id
                                }
                                onChange={(e) =>
                                  setSelectedGuide(
                                    e.target.value
                                  )
                                }
                                className="mt-1 h-4 w-4"
                              />


                              <div>

                                <h3 className="text-lg font-semibold text-gray-900">
                                  {guide.name}
                                </h3>


                                <p className="mt-1 text-sm text-gray-500">

                                  📞{' '}
                                  {guide.phone}

                                </p>


                                <p className="mt-1 text-sm text-gray-500">

                                  🗣️{' '}
                                  {guide.languages?.join(
                                    ', '
                                  )}

                                </p>


                                <p className="mt-1 text-sm text-gray-500">

                                  📍{' '}
                                  {guide.destination_expertise?.join(
                                    ', '
                                  )}

                                </p>


                                <p className="mt-1 text-sm text-gray-500">

                                  Workload:{' '}
                                  {guide.workload}

                                </p>

                              </div>

                            </div>

                          </label>

                        )
                      )}


                      <button
                        type="button"
                        onClick={
                          handleAssignGuide
                        }
                        disabled={
                          guideLoading ||
                          !selectedGuide
                        }
                        className="w-full rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                      >

                        {guideLoading
                          ? 'Assigning Guide...'
                          : 'Confirm Tour Guide'}

                      </button>

                    </div>

                  )}

                </div>

              )}


            {/* GUIDE ASSIGNED */}

            {guideAssigned && (

              <div className="mt-6 rounded-xl bg-green-50 p-6">

                <h2 className="text-2xl font-bold text-green-700">
                  ✓ Tour Guide Assigned
                </h2>


                <p className="mt-2 text-green-600">
                  Your tour guide has been
                  successfully assigned to this trip.
                </p>

              </div>

            )}

          </div>


          {/* =====================================
              RIGHT SIDE
          ===================================== */}

          <div>

            <div className="sticky top-6 rounded-xl bg-white p-6 shadow-lg">


              {/* IMAGE PLACEHOLDER */}

              <div className="flex h-32 items-center justify-center rounded-lg bg-blue-100 text-7xl">
                🌴
              </div>


              {/* PACKAGE */}

              <h2 className="mt-5 text-xl font-bold text-gray-900">
                {tour.name}
              </h2>


              <p className="mt-2 text-gray-500">
                📍 {tour.destination}
              </p>


              <p className="mt-2 text-gray-500">
                🗓️ {tour.duration} Days
              </p>


              <div className="my-6 border-t" />


              {/* PRICE */}

              <div className="flex justify-between">

                <span className="text-gray-500">
                  Price per person
                </span>


                <span className="font-semibold">

                  ₹
                  {Number(
                    tour.base_price
                  ).toLocaleString(
                    'en-IN'
                  )}

                </span>

              </div>


              {/* PASSENGERS */}

              <div className="mt-4 flex justify-between">

                <span className="text-gray-500">
                  Passengers
                </span>


                <span className="font-semibold">
                  {passengers}
                </span>

              </div>


              {/* DATE */}

              <div className="mt-4 flex justify-between">

                <span className="text-gray-500">
                  Travel Date
                </span>


                <span className="font-semibold">
                  {travelDate ||
                    'Not selected'}
                </span>

              </div>


              <div className="my-6 border-t" />


              {/* TOTAL */}

              <div className="flex justify-between text-lg">

                <span className="font-bold">
                  Total
                </span>


                <span className="font-bold text-blue-600">

                  ₹
                  {Number(
                    totalPrice
                  ).toLocaleString(
                    'en-IN'
                  )}

                </span>

              </div>


              {/* CREATE BOOKING */}

              {!booking && (

                <button
                  type="button"
                  onClick={
                    handleCreateBooking
                  }
                  className="mt-6 w-full rounded-lg bg-green-600 px-6 py-3 font-semibold text-white hover:bg-green-700"
                >
                  Continue to Payment
                </button>

              )}


              {/* BOOKING CREATED */}

              {booking &&
                !paymentCompleted && (

                  <div className="mt-6 rounded-lg bg-blue-50 p-4 text-center">

                    <p className="font-semibold text-blue-700">
                      Booking Created
                    </p>


                    <p className="mt-1 text-sm text-blue-600">
                      Complete the payment below.
                    </p>

                  </div>

                )}


              {/* PAYMENT COMPLETED */}

              {paymentCompleted && (

                <div className="mt-6 rounded-lg bg-green-50 p-4 text-center">

                  <p className="font-semibold text-green-700">
                    Payment Completed
                  </p>

                </div>

              )}


              {/* BACK */}

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