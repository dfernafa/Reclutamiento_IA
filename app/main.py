from fastapi import FastAPI
from app.routes import status_routes
from app.services.texto_service import TextoService
import asyncio

app = FastAPI(
    title="API de Análisis de Hojas de Vida",
    description="Conexión a MongoDB, FTP y análisis con OpenAI.",
    version="1.0.0"
)

app.include_router(status_routes.router)

@app.on_event("startup")
async def iniciar_monitoreo_ftp():
    texto_service = TextoService()

    async def loop_ftp():
        while True:
            try:
                print("🔄 Revisando archivos en FTP...")
                resultados = texto_service.read_files()
                if resultados:
                    print(f"✅ Archivos nuevos: {[r['archivo'] for r in resultados]}")
                    texto_service.get_analisys_for_text_mongo()
                else:
                    print("📭 No hay archivos nuevos.")
            except Exception as e:
                print(f"❌ Error en el loop FTP: {e}")
            await asyncio.sleep(60)

    asyncio.create_task(loop_ftp())