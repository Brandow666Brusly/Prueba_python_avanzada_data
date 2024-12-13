import os
import configparser
import pandas as pd
import hashlib

def leer_configuracion(ruta_configuracion='config.ini'):
    """Leer archivo de configuración."""
    configuracion = configparser.ConfigParser()
    configuracion.read(ruta_configuracion)
    return configuracion

def obtener_imagenes_directorio(ruta_base, extension):
    """Obtener todas las imágenes con una extensión dada desde el sistema de archivos."""
    imagenes = []
    for raiz, _, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if archivo.lower().endswith(extension.lower()):
                ruta_completa = os.path.join(raiz, archivo)
                imagenes.append(ruta_completa)
    return imagenes

def comparar_imagenes(imagenes_bd, imagenes_fs):
    """Comparar imágenes entre la base de datos y el sistema de archivos."""
    set_bd = set(imagenes_bd)
    set_fs = set(imagenes_fs)

    presentes = set_bd.intersection(set_fs)
    ausentes = set_bd.difference(set_fs)
    no_catalogadas = set_fs.difference(set_bd)

    return presentes, ausentes, no_catalogadas

def cargar_hashes(ruta_hashes):
    """Cargar los hashes de las imágenes desde un archivo."""
    hashes = {}
    if os.path.isfile(ruta_hashes):
        with open(ruta_hashes, 'r', encoding='utf-8') as archivo:
            lineas = archivo.read().splitlines()
        for linea in lineas[1:]:
            partes = linea.split('|')
            if len(partes) >= 3:
                nombre_archivo = partes[0].strip().lower()
                hash_valor = partes[2].strip()
                hashes[nombre_archivo] = hash_valor
    return hashes

def generar_hash_imagen(ruta_imagen):
    """Generar el hash SHA-256 de una imagen."""
    hash_obj = hashlib.sha256()
    if os.path.isfile(ruta_imagen):
        with open(ruta_imagen, 'rb') as archivo:
            contenido = archivo.read()
        hash_obj.update(contenido)
        return hash_obj.hexdigest()
    return None

def procesar_catalogo(ruta_catalogo, separador, campos):
    """Procesar un archivo de catálogo para extraer información."""
    try:
        #df = pd.read_csv(ruta_catalogo, sep=separador, header=0, on_bad_lines='skip')
        df = pd.read_csv(ruta_catalogo, sep=separador, header=0, on_bad_lines='skip', engine='python')

        columnas_requeridas = [
            campos['ano_rad_field'],
            campos['codi_secl_field'],
            campos['codi_pat_field'],
            campos['nume_rad_field'],
            campos['nomb_ima_field']
        ]
        for columna in columnas_requeridas:
            if columna not in df.columns:
                return []
        registros = [
            {
                'nombre_imagen': fila[campos['nomb_ima_field']],
                'ano_rad': fila[campos['ano_rad_field']],
                'codi_secl': fila[campos['codi_secl_field']],
                'codi_pat': fila[campos['codi_pat_field']],
                'nume_rad': fila[campos['nume_rad_field']]
            }
            for _, fila in df.iterrows()
        ]
        return registros
    except Exception as e:
        print(f"Error al procesar el catálogo: {e}")
        return []

def obtener_categoria_desde_ruta(ruta_catalogo, data_dir, dir_padre):
    """Obtener la categoría desde la estructura de la ruta del catálogo."""
    ruta_relativa = os.path.relpath(ruta_catalogo, os.path.join(data_dir, dir_padre.strip('/')))
    partes = ruta_relativa.split(os.sep)
    if len(partes) > 1:
        return partes[-2]
    return 'Desconocida'

def buscar_archivos_catalogo(data_dir, dir_padre, nombre_catalogo):
    """Buscar todos los archivos de catálogo en las subcarpetas especificadas."""
    rutas_catalogos = []
    ruta_base = os.path.join(data_dir, dir_padre.strip('/'))
    for raiz, _, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if archivo.lower() == nombre_catalogo.lower():
                rutas_catalogos.append(os.path.join(raiz, archivo))
    return rutas_catalogos
