from ftplib import FTP
from dotenv import load_dotenv
import os


class FtpService():
    def __init__(self):
        load_dotenv(override=True)
        load_dotenv()
        self.ftp_host = os.getenv("FTP_HOST")
        self.ftp_user = os.getenv("FTP_USER")
        self.ftp_pass = os.getenv("FTP_PASS")
        self.ftp_port = int(os.getenv("FTP_PORT", 21))
        self.timeout = 15
        self.ftp = None

    def connect(self):
        self.ftp = FTP()
        self.ftp.connect(host=self.ftp_host, port=self.ftp_port, timeout=self.timeout)
        self.ftp.login(user=self.ftp_user, passwd=self.ftp_pass)
        self.ftp.set_pasv(True)
        print(f"Conectado a {self.ftp_host}")

    def list_files(self, directory: str = "/HV"):
        self.connect()
        self.ftp.cwd(directory)
        return [f for f in self.ftp.nlst() if f.lower().endswith('.pdf')]

    def list_pdfs(self, path: str):
            self.ftp.cwd(path)
            archivos = self.ftp.nlst()
            return [f for f in archivos if f.lower().endswith(".pdf")]

    def download_file(self, remote_path: str):
        from io import BytesIO
        buffer = BytesIO()
        self.ftp.retrbinary(f"RETR {remote_path}", buffer.write)
        buffer.seek(0)
        return buffer
    
    def move_Analizado(self,ruta_origen,ruta_destino):
        self.ftp.rename(ruta_origen, ruta_destino)
        
    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            self.ftp = None
