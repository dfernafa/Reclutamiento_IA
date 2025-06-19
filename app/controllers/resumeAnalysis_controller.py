from fastapi import APIRouter
from app.services.ftp_service import FtpService 
from app.services.texto_service import TextoService 
from app.services.MongoStorageService import MongoStorageService
from app.services.openIA_services import OpenAIServices 
from app.services.Sql_server import Sql_serverSql_server

ftp_service = FtpService()
texto_service = TextoService() 
sqlconteciot = Sql_serverSql_server() 
router = APIRouter(prefix="/ftp", tags=["ftp_process"])

@router.get("/getDocsftp")
def get_ftp_docs():
    ftp_service = FtpService()
    try:
        archivos = ftp_service.list_files('/HV')  # Se entra directamente en 'hv'
        return {"archivos": archivos}
    finally:
        ftp_service.disconnect()
        
@router.get("/ftp_texto_mongo")
def text_for_mongo():
    texto_service = TextoService()
    return texto_service.read_files()

@router.get("/analysis")
def analysis_text_for_mongo():
    texto_service = TextoService()
    return texto_service.get_analisys_for_text_mongo()

@router.get("/sqlConnecet")
def ConectionSql():
    sqlconteciot = FtpService()
    return sqlconteciot.connectICE()
