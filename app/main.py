from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.database import engine
from app.utils.logger import log_info
import uvicorn
import pkgutil
import importlib

# Import all API routers
from app.api.user import user_router
from app.api.auth import auth_router
from app.api.order import order_router
from app.api.order_item import order_item_router
from app.api.vehicle import vehicle_router
from app.api.mission import mission_router
from app.api.notification import notification_router
from app.api.routing import routing_router
from app.api.audit_log import audit_log_router
from app.api.mission_assignment_log import mission_assignment_log_router
from app.api.item import item_router

app = FastAPI(
    title="Tire Recycling and Fleet Management App",
    description="A comprehensive system for managing tire recycling and fleet operations.",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mounting static files
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Automatically import all models to ensure registration
def import_all_models():
    package = "app.models"
    for _, name, _ in pkgutil.iter_modules([package.replace(".", "/")]):
        importlib.import_module(f"{package}.{name}")

# Event handler for application startup
@app.on_event("startup")
async def startup_event():
    log_info("Starting Tire Recycling and Fleet Management App...")
    print("Importing all models...")
    import_all_models()
    print("Creating database tables...")
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)  # Ensure tables are created
    print("Database tables created successfully.")
    print("Application started successfully.")

# Including the API routers directly
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(order_router, prefix="/api", tags=["Orders"])
app.include_router(order_item_router, prefix="/api", tags=["Orders"])
app.include_router(vehicle_router, prefix="/api", tags=["Vehicles"])
app.include_router(mission_router, prefix="/api", tags=["Missions"])
app.include_router(notification_router, prefix="/api", tags=["Notifications"])
app.include_router(routing_router, prefix="/api", tags=["Routes"])
app.include_router(audit_log_router, prefix="/api", tags=["Audit Logs"])
app.include_router(mission_assignment_log_router, prefix="/api", tags=["Mission Assignment Logs"])
app.include_router(item_router, prefix="/api", tags=["Items"])

# Event handler for application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    log_info("Shutting down the application...")
    print("Application shutdown complete.")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
