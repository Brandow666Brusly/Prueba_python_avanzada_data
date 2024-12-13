import os
import matplotlib.pyplot as plt
from db import obtener_conexion_bd, obtener_informacion_imagenes
from logic import leer_configuracion, buscar_archivos_catalogo, obtener_categoria_desde_ruta, procesar_catalogo, obtener_imagenes_directorio, comparar_imagenes, cargar_hashes, generar_hash_imagen
from log import imprimir_log

def main():
    """Función principal del script para la migración y análisis de datos."""

    # Leer configuración
    configuracion = leer_configuracion('config.ini')
    directorio_datos = configuracion.get('paths', 'data_dir', fallback='data')
    carpeta_padre = configuracion.get('paths', 'directorio_carpeta_padre', fallback='/contenedor_padre').strip('/')
    separador_campos = configuracion.get('fields', 'field_separator', fallback='|')
    extension_imagen = configuracion.get('fields', 'image_extension', fallback='.png')
    nombre_catalogo = configuracion.get('paths', 'catalogo_filename', fallback='catalogo.txt')
    nombre_hash = configuracion.get('paths', 'hash_filename', fallback='hash.txt')

    # Conexión a la base de datos
    conexion = obtener_conexion_bd('config.ini')

    # Buscar archivos de catálogo
    rutas_catalogos = buscar_archivos_catalogo(directorio_datos, carpeta_padre, nombre_catalogo)

    if not rutas_catalogos:
        print("No se encontraron archivos catalogo.txt. Verifica la estructura del directorio.")
        return

    # Procesar catálogos
    campos = {
        'ano_rad_field': configuracion.get('fields', 'ano_rad_field', fallback='ano_rad'),
        'codi_secl_field': configuracion.get('fields', 'codi_secl_field', fallback='codi_sec'),
        'codi_pat_field': configuracion.get('fields', 'codi_pat_field', fallback='codi_pat'),
        'nume_rad_field': configuracion.get('fields', 'nume_rad_field', fallback='nume_rad'),
        'nomb_ima_field': configuracion.get('fields', 'nomb_ima_field', fallback='nomb_ima')
    }

    for ruta_catalogo in rutas_catalogos:
        try:
            registros = procesar_catalogo(ruta_catalogo, separador_campos, campos)
            if registros:
                categoria = obtener_categoria_desde_ruta(ruta_catalogo, directorio_datos, carpeta_padre)
                print(f"Categoría procesada: {categoria}")
                # Continuar con el procesamiento adicional según sea necesario.
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_catalogo}: {e}")

    # Comparar imágenes
    imagenes_fs = obtener_imagenes_directorio(os.path.join(directorio_datos, carpeta_padre), extension_imagen)
    print(f"Imágenes en el sistema de archivos: {len(imagenes_fs)}")

    imagenes_bd = obtener_informacion_imagenes(conexion)
    presentes, ausentes, no_catalogadas = comparar_imagenes(imagenes_bd.keys(), imagenes_fs)

    # Generar log
    imprimir_log(presentes, ausentes, no_catalogadas, imagenes_bd)

    conexion.close()

    resultados = {}
    resultados[os.path.join(directorio_datos, carpeta_padre)] = len(imagenes_fs)
    print('__________inicio conteo archivos________')
    for d, cant in resultados.items():
        print(f"Se encontraron {cant} archivos .png en {d}")
    print('__________fin conteo archivos________')

if __name__ == '__main__':
    main()
