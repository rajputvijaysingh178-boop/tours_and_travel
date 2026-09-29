import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

import {
  getMyBookings,
  getPackages,
  cancelBooking,
  getHotels,
  getHotelRooms,
  allocateHotelRoom
} from '../services/api'

const API_URL = 'http://127.0.0.1:8000'

function MyBookings() {
  const navigate = useNavigate()

  const [bookings, setBookings] = useState([])
  const [departures, setDepartures] = useState([])
  const [packages, setPackages] = useState([])

  const [hotels, setHotels] = useState([])
  const [selectedHotel, setSelectedHotel] = useState({})
  const [hotelRooms, setHotelRooms] = useState({})
  const [allocatingRoom, setAllocatingRoom] = useState('')

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('access_token')

        if (!token) {
          navigate('/login')
          return
        }

        const [
          bookingData,
          departureResponse,
          packageData,
          hotelData
        ] = await Promise.all([
          getMyBookings(),
          fetch(`${API_URL}/departures`),
          getPackages(),
          getHotels()
        ])

        if (!departureResponse.ok) {
          throw new Error('Failed to fetch departures')
        }

        const departureData =
          await departureResponse.json()

        setBookings(bookingData)
        setDepartures(departureData)
        setPackages(packageData)
        setHotels(hotelData)

      } catch (error) {
        console.error(
          'MY BOOKINGS ERROR:',
          error
        )

        setError(
          error.message ||
          'Failed to load bookings'
        )
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [navigate])

  const getDeparture = (departureId) => {
    return departures.find(
      (departure) =>
        departure.departure_id === departureId
    )
  }

  const getPackage = (packageId) => {
    return packages.find(
      (pkg) =>
        pkg.package_id === packageId
    )
  }

  const handleCancelBooking = async (bookingId) => {
    const reason = window.prompt(
      'Please enter the reason for cancellation:'
    )

    if (!reason || !reason.trim()) {
      return
    }

    const confirmed = window.confirm(
      'Are you sure you want to cancel this booking?'
    )

    if (!confirmed) {
      return
    }

    try {
      await cancelBooking(
        bookingId,
        reason.trim()
      )

      alert(
        'Booking cancelled successfully!'
      )

      const updatedBookings =
        await getMyBookings()

      setBookings(updatedBookings)

    } catch (error) {
      console.error(
        'CANCEL BOOKING ERROR:',
        error
      )

      alert(
        error.message ||
        'Failed to cancel booking'
      )
    }
  }

  const handleHotelChange = async (
    bookingId,
    hotelId
  ) => {
    setSelectedHotel((prev) => ({
      ...prev,
      [bookingId]: hotelId
    }))

    if (!hotelId) {
      return
    }

    try {
      const rooms =
        await getHotelRooms(hotelId)

      setHotelRooms((prev) => ({
        ...prev,
        [bookingId]: rooms
      }))

    } catch (error) {
      console.error(
        'HOTEL ROOMS ERROR:',
        error
      )

      alert(
        error.message ||
        'Failed to load hotel rooms'
      )
    }
  }

  const handleRoomAllocation = async (
    bookingId,
    hotelId,
    roomId
  ) => {
    if (!hotelId || !roomId) {
      alert(
        'Please select a hotel and room'
      )
      return
    }

    const confirmed = window.confirm(
      'Are you sure you want to allocate this room to this booking?'
    )

    if (!confirmed) {
      return
    }

    try {
      setAllocatingRoom(roomId)

      await allocateHotelRoom(
        bookingId,
        hotelId,
        roomId
      )

      alert(
        'Hotel room allocated successfully!'
      )

      const rooms =
        await getHotelRooms(hotelId)

      setHotelRooms((prev) => ({
        ...prev,
        [bookingId]: rooms
      }))

    } catch (error) {
      console.error(
        'HOTEL ALLOCATION ERROR:',
        error
      )

      alert(
        error.message ||
        'Failed to allocate hotel room'
      )

    } finally {
      setAllocatingRoom('')
    }
  }

  return (
    <>
      <Navbar />

      <div className="min-h-[70vh] bg-gray-50 px-6 py-10">

        <div className="mx-auto max-w-5xl">

          {/* Page Heading */}

          <h1 className="mb-8 text-3xl font-bold text-gray-800">
            My Bookings
          </h1>

          {/* Loading */}

          {loading && (
            <div className="rounded-lg bg-white p-6 shadow">

              <p className="text-gray-600">
                Loading your bookings...
              </p>

            </div>
          )}

          {/* Error */}

          {error && !loading && (
            <div className="rounded-lg bg-red-50 p-6 text-red-600">
              {error}
            </div>
          )}

          {/* No Bookings */}

          {!loading &&
            !error &&
            bookings.length === 0 && (

              <div className="rounded-lg bg-white p-8 text-center shadow">

                <h2 className="mb-2 text-xl font-semibold">
                  No bookings yet
                </h2>

                <p className="mb-5 text-gray-600">
                  You haven't booked any tours yet.
                </p>

                <button
                  onClick={() =>
                    navigate('/packages')
                  }
                  className="rounded-lg bg-blue-600 px-5 py-2.5 text-white hover:bg-blue-700"
                >
                  Browse Tour Packages
                </button>

              </div>
            )}

          {/* Bookings */}

          {!loading &&
            !error &&
            bookings.length > 0 && (

              <div className="space-y-6">

                {bookings.map((booking) => {

                  const departure =
                    getDeparture(
                      booking.departure_id
                    )

                  const packageData =
                    departure
                      ? getPackage(
                          departure.package_id
                        )
                      : null

                  return (

                    <div
                      key={booking.booking_id}
                      className="rounded-xl bg-white p-6 shadow-md"
                    >

                      {/* Package Information */}

                      <div className="mb-5 border-b pb-5">

                        <h2 className="text-2xl font-bold text-gray-800">
                          {packageData?.name ||
                            'Tour Package'}
                        </h2>

                        <p className="mt-1 text-gray-600">
                          📍{' '}
                          {packageData?.destination ||
                            'Destination unavailable'}
                        </p>

                      </div>

                      {/* Travel Details */}

                      <div className="grid gap-4 md:grid-cols-2">

                        <div>

                          <p className="text-sm text-gray-500">
                            Travel Dates
                          </p>

                          <p className="font-semibold text-gray-800">
                            {departure?.start_date ||
                              'N/A'}

                            {' → '}

                            {departure?.end_date ||
                              'N/A'}
                          </p>

                        </div>

                        <div>

                          <p className="text-sm text-gray-500">
                            Passengers
                          </p>

                          <p className="font-semibold text-gray-800">
                            {booking.passenger_count}
                          </p>

                        </div>

                        <div>

                          <p className="text-sm text-gray-500">
                            Total Amount
                          </p>

                          <p className="font-semibold text-gray-800">
                            ₹{booking.total_amount}
                          </p>

                        </div>

                        <div>

                          <p className="text-sm text-gray-500">
                            Booking ID
                          </p>

                          <p className="break-all font-semibold text-gray-800">
                            {booking.booking_id}
                          </p>

                        </div>

                      </div>

                      {/* Status */}

                      <div className="mt-6 flex flex-wrap gap-3">

                        <span
                          className={`rounded-full px-4 py-2 text-sm font-medium ${
                            booking.booking_status ===
                            'cancelled'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-blue-100 text-blue-700'
                          }`}
                        >
                          Booking:{' '}
                          {booking.booking_status}
                        </span>

                        <span
                          className={`rounded-full px-4 py-2 text-sm font-medium ${
                            booking.payment_status ===
                            'paid'
                              ? 'bg-green-100 text-green-700'
                              : 'bg-yellow-100 text-yellow-700'
                          }`}
                        >
                          Payment:{' '}
                          {booking.payment_status}
                        </span>

                      </div>

                      {/* Created Date */}

                      <p className="mt-5 text-sm text-gray-500">
                        Booking created:{' '}
                        {booking.created_at}
                      </p>

                      {/* Cancel Button */}

                      {booking.booking_status !==
                        'cancelled' && (

                        <button
                          onClick={() =>
                            handleCancelBooking(
                              booking.booking_id
                            )
                          }
                          className="mt-4 rounded-lg bg-red-600 px-5 py-2.5 text-white hover:bg-red-700"
                        >
                          Cancel Booking
                        </button>

                      )}

                      {/* Cancelled Message */}

                      {booking.booking_status ===
                        'cancelled' && (

                        <p className="mt-4 font-medium text-red-600">
                          This booking has been cancelled.
                        </p>

                      )}

                      {/* Hotel Allocation */}

                      {booking.booking_status !==
                        'cancelled' && (

                        <div className="mt-6 rounded-xl border border-blue-100 bg-blue-50 p-5">

                          <h3 className="text-xl font-bold text-gray-800">
                            🏨 Hotel Accommodation
                          </h3>

                          <p className="mt-1 text-sm text-gray-600">
                            Select a hotel and allocate a room to this booking.
                          </p>

                          {/* Hotel Selection */}

                          <div className="mt-4">

                            <label className="mb-2 block text-sm font-medium text-gray-700">
                              Select Hotel
                            </label>

                            <select
                              value={
                                selectedHotel[
                                  booking.booking_id
                                ] || ''
                              }
                              onChange={(e) =>
                                handleHotelChange(
                                  booking.booking_id,
                                  e.target.value
                                )
                              }
                              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                            >

                              <option value="">
                                Select a hotel
                              </option>

                              {hotels.map(
                                (hotel) => (

                                  <option
                                    key={
                                      hotel.hotel_id
                                    }
                                    value={
                                      hotel.hotel_id
                                    }
                                  >
                                    {hotel.name}
                                    {' - '}
                                    {hotel.location}
                                  </option>

                                )
                              )}

                            </select>

                          </div>

                          {/* Rooms */}

                          {selectedHotel[
                            booking.booking_id
                          ] && (

                            <div className="mt-5">

                              <label className="mb-3 block text-sm font-medium text-gray-700">
                                Select Room
                              </label>

                              <div className="space-y-3">

                                {(
                                  hotelRooms[
                                    booking.booking_id
                                  ] || []
                                ).map((room) => (

                                  <div
                                    key={
                                      room.room_id
                                    }
                                    className="flex flex-col gap-4 rounded-lg bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between"
                                  >

                                    <div>

                                      <p className="font-semibold text-gray-800">
                                        {room.room_type}
                                      </p>

                                      <p className="text-sm text-gray-500">
                                        Capacity:{' '}
                                        {room.capacity}{' '}
                                        guests
                                      </p>

                                      <p className="text-sm text-gray-500">
                                        Price: ₹
                                        {Number(
                                          room.price
                                        ).toLocaleString(
                                          'en-IN'
                                        )}
                                      </p>

                                      <p className="text-xs text-gray-400">
                                        {room.available_from}
                                        {' → '}
                                        {room.available_to}
                                      </p>

                                    </div>

                                    <button
                                      onClick={() =>
                                        handleRoomAllocation(
                                          booking.booking_id,
                                          selectedHotel[
                                            booking.booking_id
                                          ],
                                          room.room_id
                                        )
                                      }
                                      disabled={
                                        allocatingRoom ===
                                        room.room_id
                                      }
                                      className="rounded-lg bg-blue-600 px-5 py-2.5 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                                    >
                                      {allocatingRoom ===
                                      room.room_id
                                        ? 'Allocating...'
                                        : 'Allocate Room'}
                                    </button>

                                  </div>

                                ))}

                              </div>

                            </div>

                          )}

                        </div>

                      )}

                    </div>

                  )

                })}

              </div>

            )}

        </div>

      </div>

      <Footer />
    </>
  )
}

export default MyBookings