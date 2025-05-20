from fastapi import APIRouter

from app.api.user import user_router as user_router
from app.api.auth import auth_router as auth_router
from app.api.item import item_router as item_router
from app.api.order_item import order_item_router as order_item_router
from app.api.order import order_router as order_router
from app.api.mission import mission_router as mission_router
from app.api.notification import notification_router as notification_router
from app.api.vehicle import vehicle_router as vehicle_router
from app.api.routing import routing_router as routing_router
from app.api.audit_log import audit_log_router as audit_log_router
from app.api.mission_assignment_log import mission_assignment_log_router as mission_assignment_log_router
from app.api.report import report_router as report_router

api_router = APIRouter()

# Include all routers with their respective prefixes
api_router.include_router(user_router, prefix="/users")
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(item_router, prefix="/items")
api_router.include_router(order_item_router, prefix="/order-items")
api_router.include_router(order_router, prefix="/orders")
api_router.include_router(mission_router, prefix="/missions")
api_router.include_router(notification_router, prefix="/notifications")
api_router.include_router(vehicle_router, prefix="/vehicles")
api_router.include_router(routing_router, prefix="/routes")
api_router.include_router(audit_log_router, prefix="/audit-logs")
api_router.include_router(mission_assignment_log_router, prefix="/mission-assignment-logs")
api_router.include_router(report_router, prefix="/reports")
