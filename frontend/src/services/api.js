const API_URL = "http://127.0.0.1:8000";


// ==============================
// PACKAGES
// ==============================

export async function getPackages() {
    const response = await fetch(
        `${API_URL}/packages`
    );

    if (!response.ok) {
        throw new Error(
            "Failed to fetch packages"
        );
    }

    return response.json();
}


// ==============================
// BOOKINGS
// ==============================

export async function getMyBookings() {
    const token =
        localStorage.getItem("access_token");

    if (!token) {
        throw new Error(
            "Please login first"
        );
    }

    const response = await fetch(
        `${API_URL}/bookings`,
        {
            headers: {
                Authorization:
                    `Bearer ${token}`,
            },
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch bookings"
        );
    }

    return data;
}


// ==============================
// CANCEL BOOKING
// ==============================

export async function cancelBooking(
    bookingId,
    reason
) {
    const token =
        localStorage.getItem("access_token");

    if (!token) {
        throw new Error(
            "Please login first"
        );
    }

    const response = await fetch(
        `${API_URL}/bookings/${bookingId}/cancel?reason=${encodeURIComponent(reason)}`,
        {
            method: "POST",
            headers: {
                Authorization:
                    `Bearer ${token}`,
            },
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to cancel booking"
        );
    }

    return data;
}


// ==============================
// HOTELS
// ==============================

export async function getHotels() {
    const response = await fetch(
        `${API_URL}/hotels`
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch hotels"
        );
    }

    return data;
}


// ==============================
// HOTEL ROOMS
// ==============================

export async function getHotelRooms(
    hotelId
) {
    const response = await fetch(
        `${API_URL}/hotels/${hotelId}/availability`
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch rooms"
        );
    }

    return data;
}


// ==============================
// HOTEL ROOM ALLOCATION
// ==============================

export async function allocateHotelRoom(
    bookingId,
    hotelId,
    roomId
) {
    const response = await fetch(
        `${API_URL}/bookings/${bookingId}/hotel-allocation?hotel_id=${encodeURIComponent(hotelId)}&room_id=${encodeURIComponent(roomId)}`,
        {
            method: "POST",
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to allocate hotel room"
        );
    }

    return data;
}


// ==============================
// VEHICLES
// ==============================

export async function getAvailableVehicles() {
    const response = await fetch(
        `${API_URL}/vehicles/available`
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch available vehicles"
        );
    }

    return data;
}


// ==============================
// CREATE VEHICLE
// ==============================

export async function createVehicle(
    vehicleData
) {
    const response = await fetch(
        `${API_URL}/vehicles`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(
                vehicleData
            ),
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to create vehicle"
        );
    }

    return data;
}


// ==============================
// CREATE DRIVER
// ==============================

export async function createDriver(
    driverData
) {
    const response = await fetch(
        `${API_URL}/drivers`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(
                driverData
            ),
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to create driver"
        );
    }

    return data;
}


// ==============================
// GET ALL DRIVERS
// ==============================

export async function getDrivers() {
    const response = await fetch(
        `${API_URL}/drivers`
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch drivers"
        );
    }

    return data;
}


// ==============================
// TRANSPORT ASSIGNMENT
// ==============================

export async function createTransportAssignment(
    assignmentData
) {
    const response = await fetch(
        `${API_URL}/transport-assignments`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(
                assignmentData
            ),
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to assign transport"
        );
    }

    return data;
}


// ==============================
// GET TRANSPORT ASSIGNMENT
// ==============================

export async function getTransportAssignment(
    assignmentId
) {
    const response = await fetch(
        `${API_URL}/transport-assignments/${assignmentId}`
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch transport assignment"
        );
    }

    return data;
}


// ==============================
// TOUR GUIDES
// ==============================

// CREATE GUIDE

export async function createGuide(
    guideData
) {
    const response = await fetch(
        `${API_URL}/guides`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(
                guideData
            ),
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to create guide"
        );
    }

    return data;
}


// ==============================
// GET AVAILABLE GUIDES
// ==============================

export async function getAvailableGuides() {
    const response = await fetch(
        `${API_URL}/guides/available`
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch available guides"
        );
    }

    return data;
}


// ==============================
// ASSIGN GUIDE
// ==============================

export async function assignGuide(
    guideId,
    departureId
) {
    const response = await fetch(
        `${API_URL}/guides/${guideId}/assign?departure_id=${encodeURIComponent(departureId)}`,
        {
            method: "POST",
        }
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to assign guide"
        );
    }

    return data;
}


// ==============================
// GET GUIDE TOURS
// ==============================

export async function getGuideTours(
    guideId
) {
    const response = await fetch(
        `${API_URL}/guides/${guideId}/tours`
    );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to fetch guide tours"
        );
    }

    return data;
}