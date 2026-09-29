import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

import {
  createGuide,
  getAvailableGuides,
  assignGuide,
  getGuideTours
} from '../services/api'

function TourGuide() {

  // ==============================
  // GUIDES
  // ==============================

  const [guides, setGuides] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')


  // ==============================
  // CREATE GUIDE FORM
  // ==============================

  const [guideForm, setGuideForm] = useState({
    name: '',
    phone: '',
    languages: '',
    destination_expertise: '',
    availability: true,
    workload: 0
  })


  // ==============================
  // ASSIGNMENT FORM
  // ==============================

  const [assignmentForm, setAssignmentForm] = useState({
    guide_id: '',
    departure_id: ''
  })


  // ==============================
  // GUIDE TOURS
  // ==============================

  const [tourGuideId, setTourGuideId] = useState('')
  const [guideTours, setGuideTours] = useState([])
  const [tourLoading, setTourLoading] = useState(false)


  // ==============================
  // LOAD GUIDES
  // ==============================

  useEffect(() => {
    loadGuides()
  }, [])


  const loadGuides = async () => {

    try {

      setLoading(true)
      setError('')

      const data =
        await getAvailableGuides()

      setGuides(data)

    } catch (error) {

      console.error(
        'GUIDE ERROR:',
        error
      )

      setError(
        error.message ||
        'Failed to load guides'
      )

    } finally {

      setLoading(false)

    }
  }


  // ==============================
  // GUIDE FORM CHANGE
  // ==============================

  const handleGuideChange = (e) => {

    const { name, value, type, checked } = e.target

    setGuideForm((prev) => ({
      ...prev,
      [name]:
        type === 'checkbox'
          ? checked
          : value
    }))
  }


  // ==============================
  // CREATE GUIDE
  // ==============================

  const handleCreateGuide = async (e) => {

    e.preventDefault()

    setError('')
    setMessage('')

    try {

      const guideData = {

        name:
          guideForm.name,

        phone:
          guideForm.phone,

        languages:
          guideForm.languages
            .split(',')
            .map((item) => item.trim())
            .filter(Boolean),

        destination_expertise:
          guideForm.destination_expertise
            .split(',')
            .map((item) => item.trim())
            .filter(Boolean),

        availability:
          guideForm.availability,

        workload:
          Number(guideForm.workload)

      }


      const result =
        await createGuide(guideData)


      setMessage(
        result.message ||
        'Guide created successfully'
      )


      setGuideForm({
        name: '',
        phone: '',
        languages: '',
        destination_expertise: '',
        availability: true,
        workload: 0
      })


      await loadGuides()

    } catch (error) {

      console.error(
        'CREATE GUIDE ERROR:',
        error
      )

      setError(
        error.message ||
        'Failed to create guide'
      )
    }
  }


  // ==============================
  // ASSIGNMENT FORM CHANGE
  // ==============================

  const handleAssignmentChange = (e) => {

    const { name, value } = e.target

    setAssignmentForm((prev) => ({
      ...prev,
      [name]: value
    }))
  }


  // ==============================
  // ASSIGN GUIDE
  // ==============================

  const handleAssignGuide = async (e) => {

    e.preventDefault()

    setError('')
    setMessage('')


    if (
      !assignmentForm.guide_id ||
      !assignmentForm.departure_id
    ) {

      setError(
        'Please select a guide and enter departure ID'
      )

      return
    }


    try {

      const result =
        await assignGuide(
          assignmentForm.guide_id,
          assignmentForm.departure_id
        )


      setMessage(
        result.message ||
        'Guide assigned successfully'
      )


      setAssignmentForm({
        guide_id: '',
        departure_id: ''
      })


      await loadGuides()

    } catch (error) {

      console.error(
        'ASSIGN GUIDE ERROR:',
        error
      )

      setError(
        error.message ||
        'Failed to assign guide'
      )
    }
  }


  // ==============================
  // GET GUIDE TOURS
  // ==============================

  const handleGetGuideTours = async (e) => {

    e.preventDefault()

    setError('')
    setMessage('')
    setGuideTours([])


    if (!tourGuideId) {

      setError(
        'Please enter guide ID'
      )

      return
    }


    try {

      setTourLoading(true)

      const data =
        await getGuideTours(
          tourGuideId
        )

      setGuideTours(data)

    } catch (error) {

      console.error(
        'GUIDE TOURS ERROR:',
        error
      )

      setError(
        error.message ||
        'Failed to fetch guide tours'
      )

    } finally {

      setTourLoading(false)

    }
  }


  return (

    <div className="min-h-screen bg-gray-50">

      <Navbar />


      {/* ============================== */}
      {/* HEADER */}
      {/* ============================== */}

      <section className="bg-blue-600 px-6 py-16 text-white">

        <div className="mx-auto max-w-7xl">

          <p className="font-semibold uppercase tracking-wider text-blue-200">
            Tour Management
          </p>

          <h1 className="mt-2 text-4xl font-bold md:text-5xl">
            Tour Guide Management
          </h1>

          <p className="mt-4 max-w-2xl text-lg text-blue-100">
            Manage tour guides, their availability and
            assignments to tour departures.
          </p>

        </div>

      </section>


      <main className="mx-auto max-w-7xl px-6 py-12">


        {/* ============================== */}
        {/* MESSAGES */}
        {/* ============================== */}

        {error && (

          <div className="mb-8 rounded-lg bg-red-50 p-5 text-red-600">

            {error}

          </div>

        )}


        {message && (

          <div className="mb-8 rounded-lg bg-green-50 p-5 text-green-600">

            {message}

          </div>

        )}


        {/* ============================== */}
        {/* AVAILABLE GUIDES */}
        {/* ============================== */}

        <section>

          <div className="mb-6">

            <h2 className="text-2xl font-bold text-gray-900">
              Available Tour Guides
            </h2>

            <p className="mt-1 text-gray-500">
              Guides currently available for assignment.
            </p>

          </div>


          {loading ? (

            <div className="rounded-xl bg-white p-8 text-center shadow">

              <p className="text-gray-500">
                Loading guides...
              </p>

            </div>

          ) : guides.length === 0 ? (

            <div className="rounded-xl bg-white p-8 text-center shadow">

              <p className="text-gray-500">
                No available guides found.
              </p>

            </div>

          ) : (

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

              {guides.map((guide) => (

                <div
                  key={guide.guide_id}
                  className="rounded-xl bg-white p-6 shadow-md"
                >

                  <div className="flex h-24 items-center justify-center rounded-lg bg-blue-100 text-5xl">
                    🧑‍🏫
                  </div>


                  <h3 className="mt-5 text-xl font-bold text-gray-800">

                    {guide.name}

                  </h3>


                  <div className="mt-4 space-y-2">

                    <p className="text-gray-600">

                      Phone:{' '}

                      <span className="font-semibold">
                        {guide.phone}
                      </span>

                    </p>


                    <p className="text-gray-600">

                      Languages:{' '}

                      <span className="font-semibold">

                        {guide.languages?.join(', ')}

                      </span>

                    </p>


                    <p className="text-gray-600">

                      Expertise:{' '}

                      <span className="font-semibold">

                        {guide.destination_expertise?.join(
                          ', '
                        )}

                      </span>

                    </p>


                    <p className="text-gray-600">

                      Workload:{' '}

                      <span className="font-semibold">

                        {guide.workload}

                      </span>

                    </p>


                    <p className="text-gray-600">

                      Status:{' '}

                      <span className="font-semibold text-green-600">

                        Available

                      </span>

                    </p>

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>


        {/* ============================== */}
        {/* CREATE GUIDE */}
        {/* ============================== */}

        <section className="mt-12 rounded-xl bg-white p-6 shadow-md">

          <h2 className="text-2xl font-bold text-gray-900">
            Add Tour Guide
          </h2>

          <p className="mt-1 text-gray-500">
            Create a new tour guide profile.
          </p>


          <form
            onSubmit={handleCreateGuide}
            className="mt-6 grid gap-4 md:grid-cols-2"
          >

            <input
              name="name"
              value={guideForm.name}
              onChange={handleGuideChange}
              placeholder="Guide Name"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />


            <input
              name="phone"
              value={guideForm.phone}
              onChange={handleGuideChange}
              placeholder="Phone Number"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />


            <input
              name="languages"
              value={guideForm.languages}
              onChange={handleGuideChange}
              placeholder="Languages: English, Hindi, Telugu"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />


            <input
              name="destination_expertise"
              value={
                guideForm.destination_expertise
              }
              onChange={handleGuideChange}
              placeholder="Expertise: Goa, Kerala, Kashmir"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />


            <input
              name="workload"
              type="number"
              min="0"
              value={guideForm.workload}
              onChange={handleGuideChange}
              placeholder="Workload"
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />


            <label className="flex items-center gap-3 rounded-lg border px-4 py-3 text-gray-700">

              <input
                name="availability"
                type="checkbox"
                checked={
                  guideForm.availability
                }
                onChange={handleGuideChange}
                className="h-4 w-4"
              />

              <span>
                Available for assignment
              </span>

            </label>


            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700 md:col-span-2"
            >

              Add Tour Guide

            </button>

          </form>

        </section>


        {/* ============================== */}
        {/* ASSIGN GUIDE */}
        {/* ============================== */}

        <section className="mt-8 rounded-xl bg-white p-6 shadow-md">

          <h2 className="text-2xl font-bold text-gray-900">
            Assign Guide
          </h2>

          <p className="mt-1 text-gray-500">
            Assign an available guide to a departure.
          </p>


          <form
            onSubmit={handleAssignGuide}
            className="mt-6 grid gap-4 md:grid-cols-2"
          >

            <select
              name="guide_id"
              value={
                assignmentForm.guide_id
              }
              onChange={handleAssignmentChange}
              required
              className="rounded-lg border bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            >

              <option value="">
                Select Guide
              </option>

              {guides.map((guide) => (

                <option
                  key={guide.guide_id}
                  value={guide.guide_id}
                >

                  {guide.name}

                </option>

              ))}

            </select>


            <input
              name="departure_id"
              value={
                assignmentForm.departure_id
              }
              onChange={handleAssignmentChange}
              placeholder="Departure ID"
              required
              className="rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />


            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700 md:col-span-2"
            >

              Assign Guide

            </button>

          </form>

        </section>


        {/* ============================== */}
        {/* GUIDE TOURS */}
        {/* ============================== */}

        <section className="mt-8 rounded-xl bg-white p-6 shadow-md">

          <h2 className="text-2xl font-bold text-gray-900">
            Guide Tours
          </h2>

          <p className="mt-1 text-gray-500">
            View departures assigned to a specific guide.
          </p>


          <form
            onSubmit={handleGetGuideTours}
            className="mt-6 flex flex-col gap-4 md:flex-row"
          >

            <input
              value={tourGuideId}
              onChange={(e) =>
                setTourGuideId(e.target.value)
              }
              placeholder="Enter Guide ID"
              required
              className="flex-1 rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />


            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
            >

              {tourLoading
                ? 'Loading...'
                : 'Get Guide Tours'}

            </button>

          </form>


          {guideTours.length > 0 && (

            <div className="mt-6 space-y-4">

              {guideTours.map((tour) => (

                <div
                  key={tour.assignment_id}
                  className="rounded-lg border bg-gray-50 p-5"
                >

                  <div className="grid gap-4 md:grid-cols-3">

                    <div>

                      <p className="text-sm text-gray-500">
                        Assignment ID
                      </p>

                      <p className="mt-1 break-all font-semibold text-gray-800">
                        {tour.assignment_id}
                      </p>

                    </div>


                    <div>

                      <p className="text-sm text-gray-500">
                        Guide ID
                      </p>

                      <p className="mt-1 break-all font-semibold text-gray-800">
                        {tour.guide_id}
                      </p>

                    </div>


                    <div>

                      <p className="text-sm text-gray-500">
                        Departure ID
                      </p>

                      <p className="mt-1 break-all font-semibold text-gray-800">
                        {tour.departure_id}
                      </p>

                    </div>

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>


      <Footer />

    </div>

  )
}

export default TourGuide