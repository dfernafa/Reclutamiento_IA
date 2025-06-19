from app.services.ftp_service import FtpService
from app.services.MongoStorageService import MongoStorageService
from app.services.openIA_services import OpenAIServices
from io import BytesIO
from app.models.diagnosis_IA import diagnosis_IA
import fitz  # PyMuPDF
import json
import os
import time  # <-- No olvides importar esto


class TextoService:
    def __init__(self):
        self.ftp_service = FtpService()
        self.mongo_service = MongoStorageService()
        self.OpenAI_service = OpenAIServices()

    def read_files(self):
        resultados = []
        self.ftp_service.connect()
        try:
            archivos = self.ftp_service.list_pdfs('/HV')
            for archivo in archivos:
                contenido_binario = self.ftp_service.download_file(f'/HV/{archivo}')
                texto_extraido = self.extract_text(contenido_binario)

                # Extraer el nombre del archivo sin la extensión
                nombre_archivo = os.path.splitext(archivo)[0]

                # Obtener el origen desde el nombre (asumiendo formato: documento_<cedula>_<origen>.pdf)
                partes = nombre_archivo.split('_')
                origen = partes[-1] if len(partes) >= 3 else 'desconocido'
                self.mongo_service.save_document(archivo, texto_extraido,origen)
                
                # Definir rutas origen y destino para mover el archivo
                ruta_origen = f'/HV/{archivo}'
                ruta_destino = f'/HV/Analizado/{archivo}'
                self.ftp_service.move_Analizado(ruta_origen, ruta_destino)
                
                # 👇 Aquí copias al FTP ICE en /HV/
                self.ftp_service.mover_y_copiar_a_ftp_destino(ruta_destino)
                resultados.append({"archivo": archivo, "estado": "guardado"})
                self.get_analisys_for_text_mongo()
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
                self.mongo_service.marcar_reclutaia_como_true(doc['_id'])
                self.mongo_service.save_analisys_hv(resultado_json)
                resultados.append(resultado_json)

        return resultados


