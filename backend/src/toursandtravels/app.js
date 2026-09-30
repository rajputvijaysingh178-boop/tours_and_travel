const API_URL = "http://127.0.0.1:8000";

let packages = [];
let departures = [];
let destinations = [];

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
        fetch(`${API_URL}/destinations`)
            .then(async response => {
                if (!response.ok) return;
                destinations = await response.json();
                displayPackages();
            })
            .catch(error => console.error(error));

    } catch (error) {
        console.error(error);

        document.getElementById("package-container").innerHTML = `
            <p>Unable to load packages.</p>
        `;
    }
}

function packageDestination(pkg) {
    const destination = destinations.find(
        item => item.destination_id === pkg.destination_id
    );
    return destination?.name || pkg.destination || "Destination unavailable";
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
                ${packageDestination(pkg)}
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
                ${packageDestination(pkg)}
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

    const departure = departures.find(
        item => item.departure_id === departureId
    );

    if (!departure) {
        alert("Departure not found.");
        return;
    }

    const container = document.getElementById("details-container");
    container.querySelector(".booking-box")?.remove();

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

    const passengerCount = Number(
        document.getElementById("passenger-count").value
    );

    const departure = departures.find(
        item => item.departure_id === departureId
    );

    if (!Number.isInteger(passengerCount) || passengerCount < 1) {
        alert("Passenger count must be at least 1.");
        return;
    }

    if (!departure?.package_id || !departure.start_date) {
        alert("The selected departure is missing package or date information.");
        return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
        alert("Please login first.");
        return;
    }

    try {

        const query = new URLSearchParams({
            package_id: departure.package_id,
            travel_date: departure.start_date,
            passenger_count: String(passengerCount)
        });

        const response = await fetch(
            `${API_URL}/bookings?${query}`,
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

        const pkg = packages.find(
            item => item.package_id === departure.package_id
        );
        showBookingResult({
            ...data,
            package_name: data.package_name || pkg?.name,
            destination: data.destination || (pkg ? packageDestination(pkg) : null),
            travel_date: data.travel_date || departure.start_date,
            end_date: data.end_date || departure.end_date,
            passenger_count: data.passenger_count || passengerCount,
            booking_status: data.booking_status || "pending",
            payment_status: data.payment_status || "pending"
        });
        await loadMyBookings();

    } catch (error) {

        console.error(error);

        alert(error.message);
    }
}

let currentBookings = [];
let bookingToCancel = null;

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

function formatDate(value) {
    if (!value) return "Date unavailable";
    const date = /^\d{4}-\d{2}-\d{2}$/.test(value)
        ? new Date(`${value}T00:00:00`)
        : new Date(value);
    if (Number.isNaN(date.getTime())) return escapeHtml(value);
    return new Intl.DateTimeFormat("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric"
    }).format(date);
}

function formatAmount(amount) {
    const numericAmount = Number(amount);
    if (!Number.isFinite(numericAmount)) return "Amount unavailable";
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        minimumFractionDigits: 2
    }).format(numericAmount);
}

function displayDateRange(startDate, endDate) {
    if (!startDate && !endDate) return "Travel dates unavailable";
    if (!endDate) return formatDate(startDate);
    if (!startDate) return formatDate(endDate);
    return `${formatDate(startDate)} → ${formatDate(endDate)}`;
}

function showBookingResult(booking) {
    const confirmed = ["confirmed", "CONFIRMED"].includes(
        booking.booking_status
    );
    document.getElementById("booking-result-title").textContent = confirmed
        ? "Booking Confirmed"
        : "Booking request received";
    document.getElementById("booking-result-summary").innerHTML = `
        <p><strong>Package:</strong> ${escapeHtml(booking.package_name || "Package details unavailable")}</p>
        <p><strong>Destination:</strong> ${escapeHtml(booking.destination || "Destination unavailable")}</p>
        <p><strong>Travel dates:</strong> ${displayDateRange(booking.travel_date, booking.end_date)}</p>
        <p><strong>Passengers:</strong> ${escapeHtml(booking.passenger_count ?? "Not available")}</p>
        <p><strong>Total:</strong> ${formatAmount(booking.total_amount ?? booking.amount)}</p>
        <p><strong>Booking ID:</strong> ${escapeHtml(booking.booking_id || "Not available")}</p>
        ${confirmed ? "" : `<p><strong>Payment status:</strong> ${escapeHtml(booking.payment_status || "pending")}</p>`}
    `;
    document.getElementById("booking-result").classList.remove("hidden");
    document.getElementById("booking-result").scrollIntoView({
        behavior: "smooth"
    });
}

async function loadMyBookings() {
    const container = document.getElementById("booking-list");
    const token = localStorage.getItem("access_token");
    if (!token) {
        currentBookings = [];
        container.innerHTML = '<p>Sign in to view your bookings.</p>';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/bookings`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Unable to load bookings");
        currentBookings = Array.isArray(data) ? data : [];
        renderBookings();
    } catch (error) {
        console.error(error);
        container.innerHTML = `<p>${escapeHtml(error.message)}</p>`;
    }
}

function renderBookings() {
    const container = document.getElementById("booking-list");
    if (currentBookings.length === 0) {
        container.innerHTML = "<p>No bookings found.</p>";
        return;
    }

    container.innerHTML = currentBookings.map(booking => {
        const status = String(booking.booking_status || "unknown");
        const cancelled = status.toLowerCase() === "cancelled";
        const canCancel = ["pending", "confirmed"].includes(status.toLowerCase());
        const bookingId = escapeHtml(booking.booking_id || "");
        const cancelButton = canCancel
            ? `<div class="booking-actions"><button type="button" class="button-danger" data-action="cancel" data-booking-id="${bookingId}">Cancel Booking</button></div>`
            : "";
        return `
            <article class="booking-card ${cancelled ? "is-cancelled" : ""}">
                <div class="booking-card-heading">
                    <span class="booking-status ${cancelled ? "is-cancelled" : ""}">${escapeHtml(status.toUpperCase())}</span>
                    <span class="booking-amount">${formatAmount(booking.total_amount)}</span>
                </div>
                <h3>${escapeHtml(booking.package_name || "Package details unavailable")}</h3>
                <p class="booking-destination">${escapeHtml([booking.destination, booking.destination_state].filter(Boolean).join(", ") || "Destination unavailable")}</p>
                <div class="booking-meta">
                    <span>${displayDateRange(booking.travel_date, booking.end_date)}</span>
                    <span>${escapeHtml(booking.passenger_count ?? "Passenger count unavailable")} ${Number(booking.passenger_count) === 1 ? "Passenger" : "Passengers"}</span>
                </div>
                <p><strong>Booking ID:</strong> ${bookingId || "Unavailable"}</p>
                <p><strong>Payment:</strong> ${escapeHtml(booking.payment_status || "Status unavailable")}</p>
                ${cancelButton}
            </article>
        `;
    }).join("");
}

function requestBookingCancellation(bookingId) {
    bookingToCancel = currentBookings.find(
        booking => booking.booking_id === bookingId
    );
    if (!bookingToCancel) return;

    document.getElementById("cancel-booking-summary").innerHTML = `
        <p><strong>${escapeHtml(bookingToCancel.package_name || "Package details unavailable")}</strong></p>
        <p>${escapeHtml(formatAmount(bookingToCancel.total_amount))}</p>
    `;
    document.getElementById("cancel-reason").value = "";
    document.getElementById("additional-reason").value = "";
    document.getElementById("confirm-cancel-button").disabled = true;
    document.getElementById("cancel-booking-dialog").showModal();
}

async function confirmBookingCancellation() {
    if (!bookingToCancel) return;
    const token = localStorage.getItem("access_token");
    const button = document.getElementById("confirm-cancel-button");
    const reason = document.getElementById("cancel-reason").value;
    if (!reason) return;
    button.disabled = true;

    try {
        const response = await fetch(
            `${API_URL}/bookings/${encodeURIComponent(bookingToCancel.booking_id)}/cancel`,
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    reason,
                    additional_reason: document.getElementById("additional-reason").value.trim() || null
                })
            }
        );
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Cancellation failed");
        closeDialog("cancel-booking-dialog");
        bookingToCancel = null;
        await loadMyBookings();
        if (data.payment_status === "refund_pending") {
            alert("Booking cancelled. Refund pending provider processing.");
        }
    } catch (error) {
        console.error(error);
        alert(error.message);
    } finally {
        button.disabled = false;
    }
}

async function loadMyInvoices() {
    const container = document.getElementById("invoice-list");
    const token = localStorage.getItem("access_token");
    if (!token) {
        container.innerHTML = '<p>Sign in to view your invoices.</p>';
        return;
    }

    container.innerHTML = "<p>Loading invoices...</p>";
    try {
        const bookingsResponse = await fetch(`${API_URL}/bookings`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const bookings = await bookingsResponse.json();
        if (!bookingsResponse.ok) throw new Error(bookings.detail || "Unable to load bookings");

        const invoices = await Promise.all((bookings || []).map(async booking => {
            const response = await fetch(
                `${API_URL}/bookings/${encodeURIComponent(booking.booking_id)}/invoice`,
                { headers: { "Authorization": `Bearer ${token}` } }
            );
            if (!response.ok) return null;
            return { ...await response.json(), booking };
        }));
        const available = invoices.filter(Boolean);
        if (available.length === 0) {
            container.innerHTML = "<p>No invoices found.</p>";
            return;
        }

        container.innerHTML = available.map(invoice => `
            <article class="booking-card">
                <div class="booking-card-heading">
                    <span class="booking-status">${escapeHtml(invoice.status || "INVOICE")}</span>
                    <span class="booking-amount">${formatAmount(invoice.total_amount ?? invoice.amount)}</span>
                </div>
                <h3>${escapeHtml(invoice.package_name || invoice.booking.package_name || "Package details unavailable")}</h3>
                <p><strong>Destination:</strong> ${escapeHtml(invoice.destination || invoice.booking.destination || "Destination unavailable")}</p>
                <p><strong>Invoice:</strong> ${escapeHtml(invoice.invoice_number || "Not available")}</p>
                <p><strong>Customer:</strong> ${escapeHtml(invoice.customer_name || "Not available")}</p>
                <p><strong>Booking ID:</strong> ${escapeHtml(invoice.booking_id || "Not available")}</p>
                <p><strong>Invoice date:</strong> ${formatDate(invoice.generated_at)}</p>
                <p><strong>Payment status:</strong> ${escapeHtml(invoice.payment_status || "Not available")}</p>
                <p><strong>Passengers:</strong> ${escapeHtml((invoice.passengers || []).map(passenger => passenger.name).filter(Boolean).join(", ") || invoice.booking.passenger_count || "Not available")}</p>
            </article>
        `).join("");
    } catch (error) {
        console.error(error);
        container.innerHTML = `<p>${escapeHtml(error.message)}</p>`;
    }
}

function openMyBookings() {
    document.getElementById("my-bookings").scrollIntoView({ behavior: "smooth" });
    loadMyBookings();
}

function closeDialog(dialogId) {
    document.getElementById(dialogId).close();
}

document.getElementById("booking-list").addEventListener("click", event => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    if (button.dataset.action === "cancel") {
        requestBookingCancellation(button.dataset.bookingId);
    }
});

document.getElementById("cancel-reason").addEventListener("change", event => {
    document.getElementById("confirm-cancel-button").disabled = !event.target.value;
});

document.getElementById("confirm-cancel-button").addEventListener(
    "click",
    confirmBookingCancellation
);

document.querySelector('a[href="#my-invoices"]').addEventListener(
    "click",
    loadMyInvoices
);

if (localStorage.getItem("access_token")) {
    loadMyBookings();
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