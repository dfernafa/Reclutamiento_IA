from ftplib import FTP
from dotenv import load_dotenv
from app.services.Sql_server import Sql_serverSql_server
import os

class FtpService():
    def __init__(self):
        load_dotenv(override=True)
        load_dotenv()
        self.ftp_host = os.getenv("FTP_HOST")
        self.ftp_user = os.getenv("FTP_USER")
        self.ftp_pass = os.getenv("FTP_PASS")
        self.ftp_port = int(os.getenv("FTP_PORT", 21))
        
        self.ftp_host_ice = os.getenv("FTP_HOST_ICE")
        self.ftp_port_ice = int(os.getenv("FTP_PORT_ICE", 99))
        self.timeout = 15
        self.ftp = None

    def connect(self):
        self.ftp = FTP()
        self.ftp.connect(host=self.ftp_host, port=self.ftp_port, timeout=self.timeout)
        self.ftp.login(user=self.ftp_user, passwd=self.ftp_pass)
        self.ftp.set_pasv(True)
        print(f"Conectado a {self.ftp_host}")

    def connectICE(self):
        sql =  Sql_serverSql_server()
        cred = sql.get_credenciales()
        self.ftp = FTP()
        self.ftp.connect(host=self.ftp_host_ice, port=self.ftp_port_ice, timeout=self.timeout)
        self.ftp.login(user=cred["User"], passwd=cred["Password"])
        self.ftp.set_pasv(True)
        print(f"Conectado a {self.ftp_host_ice}")
        
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
            
    def mover_y_copiar_a_ftp_destino(self, ruta_ya_analizado):

        try:

            self.connect()
            buffer = os.BytesIO()
            self.ftp.retrbinary(f"RETR {ruta_ya_analizado}", buffer.write)
            buffer.seek(0)
            print(f"📥 Archivo descargado desde {ruta_ya_analizado}")

            # 3. Conectarse al FTP ICE con las credenciales
            self.connectICE()
            # 4. Subir a /HV/ en el FTP ICE con el mismo nombre del archivo
            nombre_archivo = os.path.basename(ruta_ya_analizado)
            ruta_destino_ftp_ice = "/HV"

            # Asegurar que el directorio /HV exista
            try:
                self.ftp.cwd(ruta_destino_ftp_ice)
            except:
                partes = ruta_destino_ftp_ice.strip('/').split('/')
                actual = ""
                for p in partes:
                    actual += f"/{p}"
                    try:
                        self.ftp.mkd(actual)
                    except:
                        pass
                self.ftp.cwd(ruta_destino_ftp_ice)

            self.ftp.storbinary(f"STOR {nombre_archivo}", buffer)
            print(f"✅ Archivo copiado al FTP ICE en {ruta_destino_ftp_ice}/{nombre_archivo}")

        except Exception as e:
            print(f"❌ Error en el proceso de copiar a FTP ICE: {e}")
        finally:
            self.disconnect()

        