import { BrowserRouter, Routes, Route } from 'react-router-dom'

import Home from './pages/Home'
import Packages from './pages/Packages'
import TourDetails from './pages/TourDetails'
import Booking from './pages/Booking'
import Login from './pages/Login'
import Register from './pages/Register'

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Home Page */}
        <Route path="/" element={<Home />} />

        {/* Tour Packages */}
        <Route path="/packages" element={<Packages />} />

        {/* Tour Details */}
        <Route
          path="/packages/:id"
          element={<TourDetails />}
        />

        {/* Booking */}
        <Route
          path="/booking/:id"
          element={<Booking />}
        />

        {/* Authentication */}
        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

      </Routes>
    </BrowserRouter>
  )
}

export default App