import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Transport from './pages/Transport'
import MyBookings from './pages/MyBookings'
import Home from './pages/Home'
import Packages from './pages/Packages'
import TourDetails from './pages/TourDetails'
import Booking from './pages/Booking'
import Login from './pages/Login'
import Register from './pages/Register'
import Hotels from './pages/Hotels'
import TourGuide from "./pages/TourGuide";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/packages"
          element={<Packages />}
        />

        <Route
          path="/packages/:id"
          element={<TourDetails />}
        />

        <Route
          path="/booking/:id"
          element={<Booking />}
        />

        <Route
          path="/my-bookings"
          element={<MyBookings />}
        />

        <Route
          path="/hotels"
          element={<Hotels />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />
        <Route
          path="/transport"
          element={<Transport />}
         />
         <Route path="/tour-guides" element={<TourGuide />} />

      </Routes>

    </BrowserRouter>
  )
}

export default App