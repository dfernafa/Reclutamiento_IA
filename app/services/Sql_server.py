import pyodbc
import os
from dotenv import load_dotenv

class Sql_serverSql_server:
    def __init__(self):
        load_dotenv()
        connection_string = os.getenv("SQLSERVER_CONNECTION_STRING")
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def get_credenciales(self):
        try:
            query = "SELECT [User], [Password] FROM [KeyIceberg]"
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row:
                return {"User": row[0], "Password": row[1]}
            else:
                print("⚠️ No se encontraron credenciales en KeyIceberg")
                return None
        except Exception as e:
            print(f"❌ Error al obtener credenciales: {e}")
            return None