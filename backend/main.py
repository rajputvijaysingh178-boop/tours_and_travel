from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.departure_routes import router as departure_router
from routes.auth_routes import router as auth_router
from routes.customer_routes import router as customer_router
from routes.booking_routes import router as booking_router
from routes.passanger_routes import router as passanger_router
from routes.payment_routes import router as payment_router
from routes.invoice_routes import router as invoice_router
from routes.refund_routes import router as refund_router
from routes.transportass_routes import router as transportass_router
from routes.guide_routes import router as guide_router
from routes.driver_routes import router as driver_router
from routes.vehicle_routes import router as vehicle_router
from routes.package_routes import router as package_router
from routes.itinerary_routes import router as itinerary_router
from routes.hotel_routes import router as hotel_router
from routes.trip_cart_routes import router as trip_cart_router
from routes.activity_routes import router as activity_router
from routes.inventory_hold_routes import router as inventory_hold_router
from routes.payment_order_routes import router as payment_order_router
from routes.checkout_routes import router as checkout_router
from routes.destination_routes import router as destination_router
from routes.admin_routes import router as admin_router
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://tours-and-travel-zp24.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(booking_router)
app.include_router(passanger_router)
app.include_router(payment_router)
app.include_router(invoice_router)
app.include_router(refund_router)
app.include_router(transportass_router)
app.include_router(guide_router)
app.include_router(driver_router)
app.include_router(vehicle_router)
app.include_router(package_router)
app.include_router(itinerary_router)
app.include_router(hotel_router)
app.include_router(departure_router)
app.include_router(trip_cart_router)
app.include_router(activity_router)
app.include_router(inventory_hold_router)
app.include_router(payment_order_router)
app.include_router(checkout_router)
app.include_router(destination_router)
app.include_router(admin_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}