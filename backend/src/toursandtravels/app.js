const API_URL = "http://127.0.0.1:8000";

let packages = [];
let departures = [];

async function loadData() {
    try {
        const packageResponse = await fetch(`${API_URL}/packages`);
        const departureResponse = await fetch(`${API_URL}/departures`);

        if (!packageResponse.ok || !departureResponse.ok) {
            throw new Error("Unable to load travel data");
        }

        packages = await packageResponse.json();
        departures = await departureResponse.json();

        displayPackages();

    } catch (error) {
        console.error(error);

        document.getElementById("package-container").innerHTML = `
            <p>Unable to load packages.</p>
        `;
    }
}

function displayPackages() {
    const container = document.getElementById("package-container");

    container.innerHTML = "";

    packages.forEach(pkg => {

        const card = document.createElement("div");

        card.className = "package-card";

        card.innerHTML = `
            <h3>${pkg.name}</h3>

            <p>
                <strong>Destination:</strong>
                ${pkg.destination}
            </p>

            <p>
                <strong>Duration:</strong>
                ${pkg.duration} Days
            </p>

            <p>
                <strong>Price:</strong>
                ₹${pkg.base_price}
            </p>

            <button onclick="showPackageDetails('${pkg.package_id}')">
                View Details
            </button>
        `;

        container.appendChild(card);
    });
}

function showPackageDetails(packageId) {

    const pkg = packages.find(
        p => p.package_id === packageId
    );

    if (!pkg) {
        alert("Package not found.");
        return;
    }

    const section = document.getElementById("package-details");
    const container = document.getElementById("details-container");

    const packageDepartures = departures.filter(
        d => d.package_id === packageId
    );

    section.classList.remove("hidden");

    let departureHTML = "";

    if (packageDepartures.length === 0) {

        departureHTML = `
            <p>No upcoming departures available.</p>
        `;

    } else {

        departureHTML = packageDepartures.map(departure => `
            <div class="departure-card">

                <p>
                    <strong>Departure:</strong>
                    ${departure.start_date}
                </p>

                <p>
                    <strong>Return:</strong>
                    ${departure.end_date}
                </p>

                <p>
                    <strong>Available Seats:</strong>
                    ${departure.capacity}
                </p>

                <p>
                    <strong>Status:</strong>
                    ${departure.status}
                </p>

                <button onclick="startBooking('${departure.departure_id}')">
                    Book Now
                </button>

            </div>
        `).join("");
    }

    container.innerHTML = `
        <div class="details-card">

            <h3>${pkg.name}</h3>

            <p>
                <strong>Destination:</strong>
                ${pkg.destination}
            </p>

            <p>
                <strong>Description:</strong>
                ${pkg.description}
            </p>

            <p>
                <strong>Duration:</strong>
                ${pkg.duration} Days
            </p>

            <p>
                <strong>Price:</strong>
                ₹${pkg.base_price}
            </p>

            <h4>Available Departures</h4>

            ${departureHTML}

        </div>
    `;

    section.scrollIntoView({
        behavior: "smooth"
    });
}

function startBooking(departureId) {

    const token = localStorage.getItem("access_token");

    if (!token) {
        alert("Please login before booking.");

        document.getElementById("login").scrollIntoView({
            behavior: "smooth"
        });

        return;
    }

    const container = document.getElementById("details-container");

    container.innerHTML += `
        <div class="booking-box">

            <h3>Book Your Trip</h3>

            <label>Number of Passengers</label>

            <input
                type="number"
                id="passenger-count"
                min="1"
                value="1"
            >

            <button onclick="confirmBooking('${departureId}')">
                Confirm Booking
            </button>

        </div>
    `;
}

async function confirmBooking(departureId) {

    const passengerCount =
        document.getElementById("passenger-count").value;

    if (passengerCount < 1) {
        alert("Passenger count must be at least 1.");
        return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
        alert("Please login first.");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/bookings?departure_id=${departureId}&passenger_count=${passengerCount}`,
            {
                method: "POST",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Booking failed"
            );
        }

        alert(
            `Booking successful!\nTotal Amount: ₹${data.total_amount}`
        );

    } catch (error) {

        console.error(error);

        alert(error.message);
    }
}

document.getElementById("login-form").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const email =
            document.getElementById("login-email").value;

        const password =
            document.getElementById("login-password").value;

        const message =
            document.getElementById("login-message");

        try {

            const response = await fetch(
                `${API_URL}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Login failed"
                );
            }

            localStorage.setItem(
                "access_token",
                data.access_token
            );

            if (data.refresh_token) {
                localStorage.setItem(
                    "refresh_token",
                    data.refresh_token
                );
            }

            message.textContent =
                "Login successful.";

        } catch (error) {

            console.error(error);

            message.textContent =
                error.message;
        }
    }
);

document.getElementById("register-form").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const name =
            document.getElementById("register-name").value;

        const email =
            document.getElementById("register-email").value;

        const password =
            document.getElementById("register-password").value;

        const message =
            document.getElementById("register-message");

        try {

            const response = await fetch(
                `${API_URL}/auth/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password,
                        phone: "9876543210",
                        address: "Hyderabad",
                        emergency_contact: "9876543211"
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Registration failed"
                );
            }

            message.textContent =
                "Registration successful.";

            document
                .getElementById("register-form")
                .reset();

        } catch (error) {

            console.error(error);

            message.textContent =
                error.message;
        }
    }
);

function scrollToPackages() {

    document
        .getElementById("packages")
        .scrollIntoView({
            behavior: "smooth"
        });
}

loadData();