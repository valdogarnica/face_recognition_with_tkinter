import mysql.connector
from mysql.connector import Error

# Configuración de la conexión
config = {
    'host': 'localhost',        # Dirección del servidor (puede ser una IP o dominio)
    'user': 'root',             # Tu nombre de usuario de MySQL
    'password': 'root',         # Tu contraseña de MySQL
    'database': 'tienda'        # Nombre de la base de datos a la que deseas conectarte
}

def obtener_conexion():
    try:
        # Intentar establecer la conexión
        conexion = mysql.connector.connect(**config)

        # Verificar si la conexión fue exitosa
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos MySQL")
            return conexion  # Retorna la conexión si es exitosa
        else:
            print("No se pudo conectar a la base de datos")
            return None  # Retorna None si no se pudo conectar

    except Error as err:
        # Manejo de excepciones en caso de error
        print(f"Error: {err}")
        return None  # Retorna None si ocurrió un error


