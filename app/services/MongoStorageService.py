from pymongo import MongoClient
from dotenv import load_dotenv
import os


class MongoStorageService:
    def __init__(self):
        load_dotenv()
        MONGO_HOST = os.getenv("MONGO_HOST")         # Ejemplo: "mongodb://localhost:27017"
        MONGO_DB = os.getenv("DATABASE_MONGO")             # Ejemplo: "mi_base"

        self.client = MongoClient(MONGO_HOST)
        self.db = self.client[MONGO_DB]
        self.collection = self.db["hv_ftp"]
        self.analisys_hv_collection = self.db["analisys_hv"]

    def save_document(self, nombre: str, texto: str):
        self.collection.insert_one({"nombre": nombre, "texto": texto})
    
    def serialize_doc(self,doc):
        doc['_id'] = str(doc['_id'])
        return doc
    
    def get_text_documents(self):
        return [self.serialize_doc(doc) for doc in self.collection.find()]
    
    def save_analisys_hv(self, resultado_json: dict):
        self.analisys_hv_collection.insert_one(resultado_json)