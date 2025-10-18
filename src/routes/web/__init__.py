from .root import router as root_router
from .dashboard import router as dashboard_router

from fastapi import APIRouter

router = APIRouter()
router.include_router(root_router)
router.include_router(dashboard_router)
