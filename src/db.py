import os
import configparser
import psycopg2

def leer_configuracion_bd(ruta_configuracion='config.ini', seccion='database'):
    """Leer la configuración de la base de datos desde el archivo de configuración."""
    configuracion = configparser.ConfigParser()
    configuracion.read(ruta_configuracion)
    return configuracion[seccion]

def obtener_conexion_bd(ruta_configuracion='config.ini'):
    """Establecer una conexión con la base de datos PostgreSQL."""
    configuracion_bd = leer_configuracion_bd(ruta_configuracion)
    conexion = psycopg2.connect(
        dbname=configuracion_bd.get('dbname'),
        user=configuracion_bd.get('user'),
        password=configuracion_bd.get('password'),
        host=configuracion_bd.get('host'),
        port=configuracion_bd.get('port')
    )
    return conexion

def asegurar_categoria_documento(conexion, codigo, nombre, ruta):
    """Asegurar que exista la categoría en la tabla categoria_documento."""
    with conexion.cursor() as cursor:
        cursor.execute("SELECT codigo_categoria FROM categoria_documento WHERE codigo_categoria=%s", (codigo,))
        fila = cursor.fetchone()
        if not fila:
            cursor.execute(
                "INSERT INTO categoria_documento (codigo_categoria, nombre_categoria, ruta_categoria) VALUES (%s, %s, %s)",
                (codigo, nombre, ruta)
            )
            conexion.commit()

def asegurar_encabezado_migracion(conexion, ruta_base):
    """Asegurar que exista el encabezado de migración."""
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_migracion FROM encabezado_migracion WHERE id_migracion=1")
        fila = cursor.fetchone()
        if not fila:
            cursor.execute(
                "INSERT INTO encabezado_migracion (id_migracion, ruta_carpeta_base) VALUES (%s, %s)",
                (1, ruta_base)
            )
            conexion.commit()

def asegurar_categoria(conexion, nombre_categoria):
    """Asegurar que exista la categoría en la tabla categorias."""
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria=%s", (nombre_categoria,))
        fila = cursor.fetchone()
        if fila:
            return fila[0]
        else:
            cursor.execute(
                "INSERT INTO categorias (nombre_categoria) VALUES (%s) RETURNING id_categoria",
                (nombre_categoria,)
            )
            id_nueva_categoria = cursor.fetchone()[0]
            conexion.commit()
            return id_nueva_categoria

def insertar_imagen(conexion, nombre_archivo, id_categoria, extension, peso, fecha_creacion, ruta_archivo, llave, hash_archivo):
    """Insertar información de la imagen en las tablas imagenes_catalogo y migracion_propiedades_archivos."""
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO imagenes_catalogo (nombre_imagen, categoria_id) VALUES (%s, %s) RETURNING id_imagen",
            (nombre_archivo, id_categoria)
        )
        id_imagen = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO migracion_propiedades_archivos 
            (id_migracion, nombre_archivo, extension_archivo, peso_archivo, fecha_creacion, ruta_archivo, llave, hash_archivo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (1, nombre_archivo, extension, peso, fecha_creacion, ruta_archivo, llave, hash_archivo)
        )
        conexion.commit()

def obtener_imagenes_bd(conexion):
    """Obtener los nombres de las imágenes registrados en la base de datos."""
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombre_archivo FROM migracion_propiedades_archivos")
        filas = cursor.fetchall()
    return set(fila[0] for fila in filas)

def obtener_informacion_imagenes(conexion):
    """Obtener información detallada de las imágenes desde la base de datos."""
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombre_archivo, llave FROM migracion_propiedades_archivos")
        filas = cursor.fetchall()
    return {fila[0]: fila[1] for fila in filas}
