from fastapi import FastAPI
from app.routes import status_routes

app = FastAPI(
    title="API de Análisis de Hojas de Vida",
    description="Conexión a MongoDB, FTP y análisis con OpenAI.",
    version="1.0.0"
)

app.include_router(status_routes.router)