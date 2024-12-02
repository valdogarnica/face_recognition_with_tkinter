import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion import obtener_conexion
import mysql.connector
from tkinter import messagebox


def login(username, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    SELECT usuario, passw
    FROM usuarios
    WHERE usuario = %s AND passw = %s;
    """
    cursor.execute(query, (username, password))  # Reemplaza 'tu_tabla' por el nombre de tu tabla
    resultados = cursor.fetchall()
    if resultados:
        return True
    else:
        False

def mostrar_usuarios_registrados():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, nombre, correo FROM usuarios")  # Reemplaza 'tu_tabla' por el nombre de tu tabla
    resultados = cursor.fetchall()
    
    # Imprimir resultados
    #for fila in resultados:
    #    print(fila)
    if resultados:
        return resultados
    
    # Cerrar cursor y conexión
    cursor.close()
    conexion.close()

from fun_sql.conexion import obtener_conexion

def eliminar_usuario_por_id(user_id):
    """
    Elimina un usuario de la base de datos según su ID utilizando transacciones.
    
    :param user_id: ID del usuario a eliminar.
    :return: True si se elimina correctamente, False en caso de error.
    """
    conexion = None
    try:
        # Obtener la conexión
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Iniciar la transacción
        conexion.start_transaction()
        
        # Ejecutar la consulta de eliminación
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (user_id,))
        
        # Confirmar los cambios
        conexion.commit()
        messagebox.showinfo(title="EXITO!!", message=f"Usuario con ID {user_id} eliminado exitosamente.")
        return True
    except Exception as e:
        # Revertir los cambios en caso de error
        if conexion:
            conexion.rollback()
        print(f"Error al eliminar el usuario: {e}")
        return False
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


#verificar_usuario()
def registrar_usuario(nombre, apellido_p, apellido_m, correo, username, password, path_foto):
    conexion = None
    cursor = None
    try:
        # Obtener la conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Iniciar una transacción
        conexion.start_transaction()

        # Crear la consulta SQL para insertar los datos
        query = """
        INSERT INTO usuarios (nombre, apellidop, apellidom, correo, usuario, passw, foto)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Valores a insertar
        values = (nombre, apellido_p, apellido_m, correo, username, password, path_foto)

        # Ejecutar la consulta
        cursor.execute(query, values)

        # Confirmar los cambios en la base de datos (commit de la transacción)
        conexion.commit()

        messagebox.showinfo(title="Exito!", message="Registro Exitoso")

    except mysql.connector.Error as err:
        # Si ocurre un error, deshacer la transacción
        if conexion:
            conexion.rollback()
        print(f"Error al registrar el usuario: {err}")

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()