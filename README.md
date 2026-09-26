# tours-travel-management-system
a project on travel and tours management 
# Tours and Travel Management System

A FastAPI backend for managing customers, tour bookings, passengers, payments,
refunds, invoices, guides, drivers, vehicles, and transport assignments.

The application exposes a REST API and stores data in MongoDB. Interactive API
documentation is available through FastAPI at `/docs` and `/redoc` when the
server is running.

## Features

- Customer registration and login with JWT access and refresh tokens
- Customer profile management and booking history
- Booking creation, lookup, confirmation, and cancellation
- Passenger, payment, refund, and invoice workflows for bookings
- Guide availability and tour assignment
- Driver and vehicle registration
- Transport assignment management
- MongoDB persistence through PyMongo
- Automatic OpenAPI documentation through FastAPI

## Architecture

The project follows a small layered architecture:

```text
Client
	|
	v
FastAPI application (main.py)
	|
	+-- routes/       HTTP endpoints, validation, and HTTP error mapping
	+-- services/     Business operations and MongoDB writes/queries
	+-- schemas/      Pydantic request and response models
	+-- database.py   MongoClient and collection access
	+-- security.py   Password hashing and JWT creation/decoding
	+-- config.py     Environment-backed application settings
	|
	v
MongoDB database: travel_management
```

`main.py` creates the FastAPI application and includes one router for each
domain. Route handlers delegate most business operations to a matching service
module. `database.py` exposes named MongoDB collections, while `security.py`
handles bcrypt password hashing and HS256 JWT tokens.

### Repository layout

```text
.
|-- main.py                         Application entry point
|-- config.py                       Environment and JWT settings
|-- database.py                     MongoDB connection and collections
|-- security.py                     Password and token utilities
|-- models.py                       Legacy/general Pydantic models
|-- routes/                         FastAPI routers
|-- services/                       Domain service functions
|-- schemas/                        Pydantic request/response schemas
|-- pyproject.toml                  Python project metadata
`-- src/toursandtravels/             Package scaffold
```

## Technology Stack

- Python `>=3.14` (as specified in `pyproject.toml`)
- FastAPI
- Pydantic and Pydantic EmailStr validation
- PyMongo
- MongoDB
- PyJWT
- Passlib with bcrypt
- python-dotenv
- Uvicorn (ASGI development server)
- `uv` project/build tooling

The current `pyproject.toml` does not yet list the runtime packages used by the
source code. Install them explicitly during setup, or add them to the project
dependency list before building or deploying the package.

## Getting Started

### Prerequisites

- Python 3.14 or newer
- A running MongoDB instance
- `pip` or `uv`

### Install dependencies

Using pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi "pydantic[email]" pymongo pyjwt passlib[bcrypt] python-dotenv uvicorn
```

Using uv:

```powershell
uv venv
uv pip install fastapi "pydantic[email]" pymongo pyjwt passlib[bcrypt] python-dotenv uvicorn
```

### Configure environment

Create a `.env` file in the project root:

```dotenv
MONGO_URI=mongodb://localhost:27017
JWT_SECRET_KEY=replace-with-a-long-random-secret
```

The application uses the `travel_management` database. The configured MongoDB
URI defaults to `mongodb://localhost:27017` when `MONGO_URI` is not provided.

### Run the API

```powershell
uvicorn main:app --reload
```

The API is then available at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

## Authentication

Register and log in through the authentication endpoints. Login returns an
access token and a refresh token. Protected endpoints expect the access token
in the standard HTTP Bearer header:

```http
Authorization: Bearer <access_token>
```

Access tokens expire after 15 minutes and refresh tokens expire after 7 days.
The current implementation validates the access-token type and loads the user
from MongoDB. There is no refresh-token endpoint in the current API.

## API Endpoints

All paths below are relative to the API base URL, for example
`http://127.0.0.1:8000`.

### System and authentication

| Method | Path | Description | Input |
| --- | --- | --- | --- |
| GET | `/health` | Check API health | None |
| POST | `/auth/register` | Register a customer and linked customer profile | JSON: `name`, `email`, `password`, `phone`, `address`, `emergency_contact` |
| POST | `/auth/login` | Authenticate a user | JSON: `email`, `password` |

### Customers

| Method | Path | Description | Input |
| --- | --- | --- | --- |
| GET | `/customers/me` | Get the authenticated customer's profile | Bearer token |
| PUT | `/customers/me` | Update the authenticated customer's profile | Bearer token; JSON fields: `phone`, `address`, `emergency_contact` |
| GET | `/customers/{customer_id}/bookings` | List bookings for a customer | Path: `customer_id` |

### Bookings

| Method | Path | Description | Input |
| --- | --- | --- | --- |
| POST | `/bookings` | Create a booking | Query parameters: `customer_id`, `departure_id`, `passenger_count`, `total_amount` |
| GET | `/bookings` | List a customer's bookings | Query parameter: `customer_id` |
| GET | `/bookings/{booking_id}` | Get one booking | Path: `booking_id` |
| PATCH | `/bookings/{booking_id}/confirm` | Confirm a booking | Path: `booking_id` |
| POST | `/bookings/{booking_id}/cancel` | Cancel a booking | Path: `booking_id`; query parameter: `reason` |

### Booking passengers, payments, refunds, and invoices

| Method | Path | Description | Input |
| --- | --- | --- | --- |
| POST | `/bookings/{booking_id}/passengers` | Add a passenger | JSON: `name`, `age`, `gender`, `emergency_contact` |
| GET | `/bookings/{booking_id}/passengers` | List passengers | Path: `booking_id` |
| POST | `/bookings/{booking_id}/payments` | Create a payment | JSON: `booking_id`, `amount` |
| GET | `/bookings/{booking_id}/payments` | List payments | Path: `booking_id` |
| GET | `/bookings/{booking_id}/invoice` | Get a booking invoice | Path: `booking_id` |
| POST | `/bookings/{booking_id}/refund` | Create a refund | JSON: `booking_id`, `payment_id`, `reason` |
| GET | `/bookings/{booking_id}/refund` | Get a booking refund | Path: `booking_id` |

### Guides

| Method | Path | Description | Input |
| --- | --- | --- | --- |
| POST | `/guides` | Create a guide | JSON: `name`, `phone`, `languages`, `destination_expertise`, `availability`, `workload` |
| GET | `/guides/available` | List available guides | None |
| POST | `/guides/{guide_id}/assign` | Assign a guide to a departure | Path: `guide_id`; query parameter: `departure_id` |
| GET | `/guides/{guide_id}/tours` | List tours assigned to a guide | Path: `guide_id` |

### Drivers, vehicles, and transport

| Method | Path | Description | Input |
| --- | --- | --- | --- |
| POST | `/drivers` | Create a driver | JSON: `name`, `phone`, `license_number`, `availability` |
| POST | `/vehicles` | Create a vehicle | JSON: `vehicle_type`, `capacity`, `status`, optional `maintenance_details` |
| GET | `/vehicles/available` | List available vehicles | None |
| POST | `/transport-assignments` | Assign transport to a departure | JSON: `vehicle_id`, `driver_id`, `departure_id` |
| GET | `/transport-assignments/{assignment_id}` | Get a transport assignment | Path: `assignment_id` |

### Response and error behavior

- Successful responses return JSON produced by the corresponding service.
- Invalid credentials return `401 Unauthorized`.
- Missing or inactive users return `401 Unauthorized`.
- Non-admin access is rejected by the available admin dependency with `403`
	(the current route modules do not currently attach this dependency).
- Service-level missing-resource errors are generally returned as `404 Not Found`.
- Registration conflicts return `400 Bad Request`.
- FastAPI validation errors return `422 Unprocessable Entity`.

## MongoDB Collections

The application uses these collections in the `travel_management` database:

`users`, `customers`, `sessions`, `vehicles`, `drivers`, `guides`,
`transport_assignments`, `tour_assignments`, `bookings`, `passengers`,
`payments`, `invoices`, and `refunds`.

## Development Notes

- MongoDB is pinged when the database collection objects are initialized. Make
	sure MongoDB is reachable before starting the application.
- The default JWT secret in `config.py` is intended only for local development;
	set `JWT_SECRET_KEY` in every deployed environment.
- Route files currently use both validated JSON schemas and primitive query
	parameters. The generated OpenAPI document at `/docs` is the authoritative
	request-shape reference for the running code.
- There are similarly named files such as `passanger_routes.py` and
	`passanger_service.py`; the spelling is retained for compatibility with the
	current imports.
