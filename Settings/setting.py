# Settings/sql_server.py
import pyodbc
import os
from dotenv import load_dotenv
import urllib.parse
load_dotenv()

def get_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=VS1\\INTEL;DATABASE=GESTORTAREASUTP;UID=;PWD='
        )
        cursor=connection.cursor()
        cursor.execute("select @@VERSION")
        row = cursor.fetchone()
        print(row)
        print("Conexión exitosa.")
        return connection
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return None

#CONEXION DE VERONIKA  
# def get_sqlalchemy_uri():
#     print('conexion establecida')
#     db_server_name = os.getenv('DB_SERVER_NAME')
#     db_user_name = os.getenv('DB_USER_NAME')

#     return (
#         f"mssql+pyodbc://{db_user_name}@{db_server_name}/GESTORTAREASUTP"
#         "?driver=ODBC+Driver+17+for+SQL+Server"
#         "&trusted_connection=yes"
#     )

#CONEXION DE JHAIR
def get_sqlalchemy_uri():
    # Retorna el URI de conexión para SQLAlchemy con pyodbc
    db_name = "GESTORTAREASUTP"
    server_name = "DESKTOP-0JUDDFN\\SQLEXPRESS"
    return (
        f"mssql+pyodbc://@{server_name}/{db_name}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )