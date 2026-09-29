import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

import {
  getAvailableVehicles,
  getDrivers,
  createVehicle,
  createDriver,
  createTransportAssignment
} from '../services/api'

const API_URL = 'http://127.0.0.1:8000'

function Transport() {
  const [vehicles, setVehicles] = useState([])
  const [drivers, setDrivers] = useState([])
  const [departures, setDepartures] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  // ==============================
  // VEHICLE FORM
  // ==============================

  const [vehicleForm, setVehicleForm] = useState({
    vehicle_type: '',
    capacity: '',
    status: 'available',
    maintenance_details: ''
  })

  // ==============================
  // DRIVER FORM
  // ==============================

  const [driverForm, setDriverForm] = useState({
    name: '',
    phone: '',
    license_number: '',
    availability: true
  })

  // ==============================
  // ASSIGNMENT FORM
  // ==============================

  const [assignmentForm, setAssignmentForm] = useState({
    vehicle_id: '',
    driver_id: '',
    departure_id: ''
  })

  // ==============================
  // LOAD DATA
  // ==============================

  useEffect(() => {
    loadTransportData()
  }, [])

  const loadTransportData = async () => {
    try {
      setLoading(true)
      setError('')

      const [
        vehicleData,
        driverData,
        departureResponse
      ] = await Promise.all([
        getAvailableVehicles(),
        getDrivers(),
        fetch(`${API_URL}/departures`)
      ])

      if (!departureResponse.ok) {
        throw new Error('Failed to fetch departures')
      }

      const departureData =
        await departureResponse.json()

      setVehicles(vehicleData)
      setDrivers(driverData)
      setDepartures(departureData)

    } catch (error) {
      console.error(
        'TRANSPORT ERROR:',
        error
      )

      setError(
        error.message ||
        'Failed to load transport data'
      )

    } finally {
      setLoading(false)
    }
  }

  // ==============================
  // VEHICLE FORM
  // ==============================

  const handleVehicleChange = (e) => {
    const { name, value } = e.target

    setVehicleForm((prev) => ({
      ...prev,
      [name]: value
    }))
  }

  const handleCreateVehicle = async (e) => {
    e.preventDefault()

    try {
      const result = await createVehicle({
        vehicle_type:
          vehicleForm.vehicle_type,

        capacity:
          Number(vehicleForm.capacity),

        status:
          vehicleForm.status,

        maintenance_details:
          vehicleForm.maintenance_details ||
          null
      })

      alert(
        result.message ||
        'Vehicle created successfully'
      )

      setVehicleForm({
        vehicle_type: '',
        capacity: '',
        status: 'available',
        maintenance_details: ''
      })

      const updatedVehicles =
        await getAvailableVehicles()

      setVehicles(updatedVehicles)

    } catch (error) {
      alert(
        error.message ||
        'Failed to create vehicle'
      )
    }
  }

  // ==============================
  // DRIVER FORM
  // ==============================

  const handleDriverChange = (e) => {
    const { name, value } = e.target

    setDriverForm((prev) => ({
      ...prev,
      [name]: value
    }))
  }

  const handleCreateDriver = async (e) => {
    e.preventDefault()

    try {
      const result = await createDriver({
        name: driverForm.name,
        phone: driverForm.phone,
        license_number:
          driverForm.license_number,
        availability:
          driverForm.availability
      })

      alert(
        result.message ||
        'Driver created successfully'
      )

      setDriverForm({
        name: '',
        phone: '',
        license_number: '',
        availability: true
      })

      // Refresh driver list
      const updatedDrivers =
        await getDrivers()

      setDrivers(updatedDrivers)

    } catch (error) {
      alert(
        error.message ||
        'Failed to create driver'
      )
    }
  }

  // ==============================
  // ASSIGNMENT FORM
  // ==============================

  const handleAssignmentChange = (e) => {
    const { name, value } = e.target

    setAssignmentForm((prev) => ({
      ...prev,
      [name]: value
    }))
  }

  const handleAssignTransport = async (e) => {
    e.preventDefault()

    if (
      !assignmentForm.vehicle_id ||
      !assignmentForm.driver_id ||
      !assignmentForm.departure_id
    ) {
      alert(
        'Please select vehicle, driver and departure'
      )

      return
    }

    try {
      const result =
        await createTransportAssignment(
          assignmentForm
        )

      setMessage(
        result.message ||
        'Transport assigned successfully'
      )

      alert(
        result.message ||
        'Transport assigned successfully'
      )

      setAssignmentForm({
        vehicle_id: '',
        driver_id: '',
        departure_id: ''
      })

    } catch (error) {
      setMessage('')

      alert(
        error.message ||
        'Failed to assign transport'
      )
    }
  }

  // ==============================
  // UI
  // ==============================

  return (
    <div className="min-h-screen bg-gray-50">

      <Navbar />

      {/* HEADER */}

      <section className="bg-blue-600 px-6 py-16 text-white">

        <div className="mx-auto max-w-7xl">

          <p className="font-semibold uppercase tracking-wider text-blue-200">
            Transportation
          </p>

          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            Transport Management
          </h1>

          <p className="mt-4 max-w-2xl text-lg text-blue-100">
            Manage vehicles, drivers and transport assignments.
          </p>

        </div>

      </section>

      <main className="mx-auto max-w-7xl px-6 py-12">

        {/* ERROR */}

        {error && (
          <div className="mb-8 rounded-lg bg-red-50 p-5 text-red-600">
            {error}
          </div>
        )}

        {/* ============================== */}
        {/* AVAILABLE VEHICLES */}
        {/* ============================== */}

        <section>

          <div className="mb-6">

            <h2 className="text-2xl font-bold text-gray-900">
              Available Vehicles
            </h2>

            <p className="mt-1 text-gray-500">
              Vehicles currently available for assignment.
            </p>

          </div>

          {loading ? (

            <div className="rounded-xl bg-white p-8 text-center shadow">

              <p className="text-gray-500">
                Loading transport data...
              </p>

            </div>

          ) : vehicles.length === 0 ? (

            <div className="rounded-xl bg-white p-8 text-center shadow">

              <p className="text-gray-500">
                No available vehicles found.
              </p>

            </div>

          ) : (

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

              {vehicles.map((vehicle) => (

                <div
                  key={vehicle.vehicle_id}
                  className="rounded-xl bg-white p-6 shadow-md"
                >

                  <div className="flex h-24 items-center justify-center rounded-lg bg-blue-100 text-5xl">
                    🚐
                  </div>

                  <h3 className="mt-5 text-xl font-bold text-gray-800">
                    {vehicle.vehicle_type}
                  </h3>

                  <div className="mt-4 space-y-2">

                    <p className="text-gray-600">
                      Capacity:{' '}

                      <span className="font-semibold">
                        {vehicle.capacity}
                      </span>
                    </p>

                    <p className="text-gray-600">
                      Status:{' '}

                      <span className="font-semibold text-green-600">
                        {vehicle.status}
                      </span>
                    </p>

                    {vehicle.maintenance_details && (

                      <p className="text-sm text-gray-500">
                        Maintenance:{' '}
                        {vehicle.maintenance_details}
                      </p>

                    )}

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>


        {/* ============================== */}
        {/* CREATE VEHICLE */}
        {/* ============================== */}

        <section className="mt-12 rounded-xl bg-white p-6 shadow-md">

          <h2 className="text-2xl font-bold text-gray-900">
            Add Vehicle
          </h2>

          <form
            onSubmit={handleCreateVehicle}
            className="mt-6 grid gap-4 md:grid-cols-2"
          >

            <input
              name="vehicle_type"
              value={vehicleForm.vehicle_type}
              onChange={handleVehicleChange}
              placeholder="Vehicle Type"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              name="capacity"
              type="number"
              min="1"
              value={vehicleForm.capacity}
              onChange={handleVehicleChange}
              placeholder="Capacity"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <select
              name="status"
              value={vehicleForm.status}
              onChange={handleVehicleChange}
              className="rounded-lg border bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value="available">
                Available
              </option>

              <option value="inactive">
                Inactive
              </option>

              <option value="maintenance">
                Maintenance
              </option>

            </select>

            <input
              name="maintenance_details"
              value={
                vehicleForm.maintenance_details
              }
              onChange={handleVehicleChange}
              placeholder="Maintenance Details (optional)"
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700 md:col-span-2"
            >
              Add Vehicle
            </button>

          </form>

        </section>


        {/* ============================== */}
        {/* CREATE DRIVER */}
        {/* ============================== */}

        <section className="mt-8 rounded-xl bg-white p-6 shadow-md">

          <h2 className="text-2xl font-bold text-gray-900">
            Add Driver
          </h2>

          <form
            onSubmit={handleCreateDriver}
            className="mt-6 grid gap-4 md:grid-cols-2"
          >

            <input
              name="name"
              value={driverForm.name}
              onChange={handleDriverChange}
              placeholder="Driver Name"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              name="phone"
              value={driverForm.phone}
              onChange={handleDriverChange}
              placeholder="Phone Number"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              name="license_number"
              value={
                driverForm.license_number
              }
              onChange={handleDriverChange}
              placeholder="License Number"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <select
              name="availability"
              value={
                driverForm.availability
                  ? 'true'
                  : 'false'
              }
              onChange={(e) =>
                setDriverForm((prev) => ({
                  ...prev,
                  availability:
                    e.target.value === 'true'
                }))
              }
              className="rounded-lg border bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value="true">
                Available
              </option>

              <option value="false">
                Not Available
              </option>

            </select>

            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700 md:col-span-2"
            >
              Add Driver
            </button>

          </form>

        </section>


        {/* ============================== */}
        {/* ASSIGN TRANSPORT */}
        {/* ============================== */}

        <section className="mt-8 rounded-xl bg-white p-6 shadow-md">

          <h2 className="text-2xl font-bold text-gray-900">
            Assign Transport
          </h2>

          <p className="mt-1 text-gray-500">
            Assign a vehicle and driver to a departure.
          </p>

          <form
            onSubmit={handleAssignTransport}
            className="mt-6 space-y-4"
          >

            {/* VEHICLE */}

            <select
              name="vehicle_id"
              value={
                assignmentForm.vehicle_id
              }
              onChange={handleAssignmentChange}
              required
              className="w-full rounded-lg border bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value="">
                Select Vehicle
              </option>

              {vehicles.map((vehicle) => (

                <option
                  key={vehicle.vehicle_id}
                  value={vehicle.vehicle_id}
                >
                  {vehicle.vehicle_type}
                  {' - Capacity: '}
                  {vehicle.capacity}
                </option>

              ))}

            </select>


            {/* DRIVER */}

            <select
              name="driver_id"
              value={
                assignmentForm.driver_id
              }
              onChange={handleAssignmentChange}
              required
              className="w-full rounded-lg border bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value="">
                Select Driver
              </option>

              {drivers.map((driver) => (

                <option
                  key={driver.driver_id}
                  value={driver.driver_id}
                >
                  {driver.name}
                  {' - '}
                  {driver.phone}
                </option>

              ))}

            </select>


            {/* DEPARTURE */}

            <select
              name="departure_id"
              value={
                assignmentForm.departure_id
              }
              onChange={handleAssignmentChange}
              required
              className="w-full rounded-lg border bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value="">
                Select Departure
              </option>

              {departures.map((departure) => (

                <option
                  key={departure.departure_id}
                  value={departure.departure_id}
                >
                  {departure.start_date}
                  {' → '}
                  {departure.end_date}
                </option>

              ))}

            </select>


            {/* ASSIGN BUTTON */}

            <button
              type="submit"
              className="w-full rounded-lg bg-green-600 px-5 py-3 font-semibold text-white hover:bg-green-700"
            >
              Assign Transport
            </button>

          </form>


          {message && (
            <div className="mt-5 rounded-lg bg-green-50 p-4 text-green-700">
              {message}
            </div>
          )}

        </section>

      </main>

      <Footer />

    </div>
  )
}

export default Transport