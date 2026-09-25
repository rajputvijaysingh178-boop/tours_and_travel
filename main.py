from fastapi import FastAPI

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

app = FastAPI(title="Travel Management System")

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

@app.get("/health")
def health_check():
    return {"status": "healthy"
            }