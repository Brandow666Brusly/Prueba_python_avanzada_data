import os
import matplotlib.pyplot as plt
from db import obtener_conexion_bd, obtener_informacion_imagenes

def generar_visualizacion():
    """Generar una visualización de la cantidad de imágenes por categoría."""
    # Establecer conexión con la base de datos
    conexion = obtener_conexion_bd('config.ini')
    info_imagenes = obtener_informacion_imagenes(conexion)

    # Contar las imágenes por categoría
    from collections import Counter
    contador_categorias = Counter(info_imagenes.values())
    categorias = list(contador_categorias.keys())
    cantidades = list(contador_categorias.values())

    # Crear el gráfico
    figura, eje = plt.subplots()
    eje.bar(categorias, cantidades, color='skyblue')
    eje.set_title('Cantidad de imágenes por categoría')
    eje.set_xlabel('Categoría')
    eje.set_ylabel('Cantidad')
    plt.tight_layout()

    # Guardar la visualización en un archivo
    directorio_visualizaciones = os.path.join(os.path.dirname(__file__), '..', 'visualizaciones')
    if not os.path.exists(directorio_visualizaciones):
        os.makedirs(directorio_visualizaciones)

    ruta_salida = os.path.join(directorio_visualizaciones, 'imagenes_por_categoria.png')
    plt.savefig(ruta_salida)
    plt.close()
    conexion.close()

    print(f"Visualización generada en: {ruta_salida}")

if __name__ == '__main__':
    generar_visualizacion()
