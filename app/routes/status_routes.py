from fastapi import APIRouter
from app.controllers import status_controller, resumeAnalysis_controller

router = APIRouter()
router.include_router(status_controller.router)
router.include_router(resumeAnalysis_controller.router)