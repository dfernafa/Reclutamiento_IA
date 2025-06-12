import time
from fastapi import APIRouter
from datetime import datetime

start_time = time.time()
start_datetime = datetime.now()

router = APIRouter()

@router.get("/", tags=["Health Check"])
def get_status():
    uptime = round(time.time() - start_time, 2)
    return {
        "status": "success",
        "message": "✅ API funcionando correctamente",
        "version": "1.0.0",
        "started_at": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime_seconds": uptime
    }
