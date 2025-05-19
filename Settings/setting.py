# Settings/sql_server.py
import pyodbc

def get_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=DESKTOP-0JUDDFN\\SQLEXPRESS;DATABASE=GESTORTAREAS;UID=;PWD='
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
    
def get_sqlalchemy_uri():
    print('conexion establecida')
    return (
        "mssql+pyodbc://@DESKTOP-0JUDDFN\\SQLEXPRESS/GESTORTAREAS"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )