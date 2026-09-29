import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

const API_URL = 'http://127.0.0.1:8000'

function Hotels() {
  const [hotels, setHotels] = useState([])
  const [selectedHotel, setSelectedHotel] = useState(null)
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [roomsLoading, setRoomsLoading] = useState(false)
  const [error, setError] = useState('')
  const [roomError, setRoomError] = useState('')

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        const response = await fetch(
          `${API_URL}/hotels`
        )

        if (!response.ok) {
          throw new Error(
            'Failed to fetch hotels'
          )
        }

        const data = await response.json()

        setHotels(data)

      } catch (error) {
        console.error(
          'HOTELS ERROR:',
          error
        )

        setError(
          error.message ||
          'Failed to load hotels'
        )

      } finally {
        setLoading(false)
      }
    }

    fetchHotels()
  }, [])

  const handleViewRooms = async (hotel) => {
    setSelectedHotel(hotel)
    setRooms([])
    setRoomError('')
    setRoomsLoading(true)

    try {
      const response = await fetch(
        `${API_URL}/hotels/${hotel.hotel_id}/availability`
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail ||
          'Failed to fetch rooms'
        )
      }

      setRooms(data)

    } catch (error) {
      console.error(
        'ROOMS ERROR:',
        error
      )

      setRoomError(
        error.message ||
        'Failed to load rooms'
      )

    } finally {
      setRoomsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">

      <Navbar />

      {/* Header */}

      <section className="bg-blue-600 px-6 py-16 text-white">

        <div className="mx-auto max-w-7xl">

          <p className="font-semibold uppercase tracking-wider text-blue-200">
            Accommodation
          </p>

          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            Hotels
          </h1>

          <p className="mt-4 max-w-2xl text-lg text-blue-100">
            Explore hotels and available rooms for your tour.
          </p>

        </div>

      </section>

      {/* Hotels */}

      <main className="mx-auto max-w-7xl px-6 py-12">

        {loading && (
          <div className="rounded-xl bg-white p-8 text-center shadow">

            <p className="text-gray-500">
              Loading hotels...
            </p>

          </div>
        )}

        {error && !loading && (
          <div className="rounded-xl bg-red-50 p-6 text-red-600">
            {error}
          </div>
        )}

        {!loading &&
          !error &&
          hotels.length === 0 && (

            <div className="rounded-xl bg-white p-8 text-center shadow">

              <h2 className="text-xl font-semibold">
                No hotels available
              </h2>

              <p className="mt-2 text-gray-500">
                There are currently no hotels to display.
              </p>

            </div>
          )}

        {!loading &&
          !error &&
          hotels.length > 0 && (

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

              {hotels.map((hotel) => (

                <div
                  key={hotel.hotel_id}
                  className="overflow-hidden rounded-xl bg-white shadow-md transition hover:-translate-y-1 hover:shadow-xl"
                >

                  <div className="flex h-48 items-center justify-center bg-blue-100 text-7xl">
                    🏨
                  </div>

                  <div className="p-6">

                    <span className="text-sm font-semibold text-blue-600">
                      {hotel.status}
                    </span>

                    <h2 className="mt-2 text-2xl font-bold text-gray-800">
                      {hotel.name}
                    </h2>

                    <p className="mt-2 text-gray-600">
                      📍 {hotel.location}
                    </p>

                    <p className="mt-3 text-sm text-gray-500">
                      📞 {hotel.contact_details}
                    </p>

                    <button
                      onClick={() =>
                        handleViewRooms(hotel)
                      }
                      className="mt-6 w-full rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
                    >
                      View Available Rooms
                    </button>

                  </div>

                </div>

              ))}

            </div>
          )}

        {/* Rooms */}

        {selectedHotel && (

          <section className="mt-12">

            <div className="mb-6">

              <h2 className="text-3xl font-bold text-gray-900">
                Rooms at {selectedHotel.name}
              </h2>

              <p className="mt-2 text-gray-500">
                Available accommodation options.
              </p>

            </div>

            {roomsLoading && (
              <div className="rounded-xl bg-white p-8 text-center shadow">

                <p className="text-gray-500">
                  Loading rooms...
                </p>

              </div>
            )}

            {roomError && !roomsLoading && (
              <div className="rounded-xl bg-red-50 p-6 text-red-600">
                {roomError}
              </div>
            )}

            {!roomsLoading &&
              !roomError &&
              rooms.length === 0 && (

                <div className="rounded-xl bg-white p-8 text-center shadow">

                  <h3 className="text-xl font-semibold">
                    No rooms available
                  </h3>

                  <p className="mt-2 text-gray-500">
                    This hotel currently has no rooms listed.
                  </p>

                </div>
              )}

            {!roomsLoading &&
              !roomError &&
              rooms.length > 0 && (

                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

                  {rooms.map((room) => (

                    <div
                      key={room.room_id}
                      className="rounded-xl bg-white p-6 shadow-md"
                    >

                      <div className="flex h-24 items-center justify-center rounded-lg bg-gray-100 text-5xl">
                        🛏️
                      </div>

                      <h3 className="mt-5 text-xl font-bold text-gray-800">
                        {room.room_type}
                      </h3>

                      <div className="mt-4 space-y-3">

                        <div className="flex justify-between">
                          <span className="text-gray-500">
                            Capacity
                          </span>

                          <span className="font-semibold">
                            {room.capacity} guests
                          </span>
                        </div>

                        <div className="flex justify-between">
                          <span className="text-gray-500">
                            Price
                          </span>

                          <span className="font-semibold text-blue-600">
                            ₹
                            {Number(
                              room.price
                            ).toLocaleString('en-IN')}
                          </span>
                        </div>

                        <div className="flex justify-between">
                          <span className="text-gray-500">
                            Available From
                          </span>

                          <span className="font-semibold">
                            {room.available_from}
                          </span>
                        </div>

                        <div className="flex justify-between">
                          <span className="text-gray-500">
                            Available To
                          </span>

                          <span className="font-semibold">
                            {room.available_to}
                          </span>
                        </div>

                      </div>

                      <div className="mt-5 rounded-lg bg-green-50 px-4 py-3 text-center font-medium text-green-700">
                        Available
                      </div>

                    </div>

                  ))}

                </div>
              )}

          </section>
        )}

      </main>

      <Footer />

    </div>
  )
}

export default Hotels