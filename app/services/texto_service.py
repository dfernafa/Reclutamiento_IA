from app.services.ftp_service import FtpService
from app.services.MongoStorageService import MongoStorageService
from app.services.openIA_services import OpenAIServices
import fitz  # PyMuPDF
import json
from io import BytesIO
from app.models.diagnosis_IA import diagnosis_IA


class TextoService:
    def __init__(self):
        self.ftp_service = FtpService()
        self.mongo_service = MongoStorageService()
        self.OpenAI_service = OpenAIServices()

    def read_files(self):
        resultados = []
        self.ftp_service.connect()
        try:
            archivos = self.ftp_service.list_pdfs('/hv')
            for archivo in archivos:
                contenido_binario = self.ftp_service.download_file(f'/hv/{archivo}')
                texto_extraido = self.extract_text(contenido_binario)
                self.mongo_service.save_document(archivo, texto_extraido)
                resultados.append({"archivo": archivo, "estado": "guardado"})
        finally:
            self.ftp_service.disconnect()
        return resultados

    def extract_text(self, contenido: bytes):
        with fitz.open(stream=contenido, filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        return texto
    
    def get_analisys_for_text_mongo(self):
        resultados = []
        mongo_information = self.mongo_service.get_text_documents()

        for doc in mongo_information:
            # Obtener objeto diagnosis_IA de OpenAI
            diagnosis = self.OpenAI_service.get_completion(doc['texto'])

            # Extraer solo resultado_json
            resultado_json = diagnosis.resultado_json

            if resultado_json:
                self.mongo_service.save_analisys_hv(resultado_json)
                resultados.append(resultado_json)

        return resultados
