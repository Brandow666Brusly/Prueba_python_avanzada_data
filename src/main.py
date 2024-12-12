import warnings
warnings.filterwarnings('ignore')
from logic import read_config, find_catalogos, get_category_from_path, process_catalogo, get_filesystem_images, compare_images, load_hash_for_images, generate_hash_for_image
from db import get_connection, ensure_categoria, insert_imagen, get_db_images, get_images_info, ensure_categoria_documento, ensure_encabezado_migracion
from log import print_log
import os


def main():
    """Main."""
    # print justificado
    # "Ejecutando main"
    config = read_config('config.ini')
    data_dir = config.get('paths', 'data_dir', fallback='data')
    dir_padre = config.get('paths', 'directorio_carpeta_padre', fallback='/contenedor_padre').strip('/')
    sep = config.get('fields', 'field_separator', fallback='|')
    ext = config.get('fields', 'image_extension', fallback='.png')
    catalogo_filename = config.get('paths', 'catalogo_filename', fallback='catalogo.txt')
    hash_filename = config.get('paths', 'hash_filename', fallback='hash.txt')

    conn = get_connection('config.ini')
    # Asegurar tablas base
    # Insertar categorías documento (ejemplo)
    ensure_categoria_documento(conn, 1, 'CATEGORIA_UNO', '/CATEGORIA_UNO/...')
    ensure_categoria_documento(conn, 2, 'CATEGORIA_DOS', '/CATEGORIA_DOS/...')
    ensure_categoria_documento(conn, 3, 'CATEGORIA_TRES', '/CATEGORIA_TRES/...')
    ensure_encabezado_migracion(conn, f"/{dir_padre}/")

    cat_paths = find_catalogos(data_dir, dir_padre, catalogo_filename)
    # Diccionario campos
    campos = {
        'ano_rad_field': config.get('fields', 'ano_rad_field', fallback='ano_rad'),
        'codi_secl_field': config.get('fields', 'codi_secl_field', fallback='codi_sec'),
        'codi_pat_field': config.get('fields', 'codi_pat_field', fallback='codi_pat'),
        'nume_rad_field': config.get('fields', 'nume_rad_field', fallback='nume_rad'),
        'nomb_ima_field': config.get('fields', 'nomb_ima_field', fallback='nomb_ima')
    }

    for cat_path in cat_paths:
        cat_name = get_category_from_path(cat_path, data_dir, dir_padre)
        registros = process_catalogo(cat_path, sep, campos)
        # print justificado
        # "Reg en cat"
        print(f"Registros en {cat_path}: {len(registros)}")
        if registros:
            cat_id = ensure_categoria(conn, cat_name)
            # Cargar hash si existe
            base_cat_dir = os.path.dirname(cat_path)
            hash_path = os.path.join(base_cat_dir, hash_filename)
            hashes = load_hash_for_images(hash_path)
            # Insertar datos
            for r in registros:
                nombre_img = r['nombre_imagen']
                nombre_lower = nombre_img.lower()
                # Ruta archivo
                # Ejemplo ruta real: /contenedor_padre/CATEGORIA_UNO/SERVICIOS...
                rel_path = os.path.relpath(base_cat_dir, os.path.join(data_dir, dir_padre))
                ruta_archivo = f"/{dir_padre}/{rel_path}"
                # Peso, fecha creacion (opcional), obtener si quieres
                peso = None
                fecha_creacion = None
                # Hash
                # Buscar imagen en FS
                img_path = os.path.join(base_cat_dir, 'IMAGENES', nombre_img)
                
                h = hashes.get(nombre_lower)
                if not h:
                    # Generar hash si existe el archivo
                    h = generate_hash_for_image(img_path)
                insert_imagen(conn, nombre_img, cat_id, ext, peso, fecha_creacion, ruta_archivo, h)
        else:
            print(f"Sin registros en {cat_path}")

    ruta_busqueda = os.path.join(data_dir, dir_padre)
    print(f"Buscando imágenes en: {ruta_busqueda}")

    ruta_busqueda = os.path.join(data_dir, dir_padre)
    print(f"Ruta absoluta esperada: {os.path.abspath(ruta_busqueda)}")
    print(f"Verificando si la ruta existe: {os.path.exists(ruta_busqueda)}")
    print(f"Es un directorio: {os.path.isdir(ruta_busqueda)}")

    fs_images = get_filesystem_images(os.path.join(data_dir, dir_padre), ext)
    print(f"Total imágenes encontradas en el sistema de archivos: {len(fs_images)}")
    for img in fs_images[:5]:  # Muestra las primeras 5 imágenes encontradas
        print(f"Imagen encontrada: {img}")

    # Comparar imágenes
    db_images = get_db_images(conn)
    fs_images = get_filesystem_images(os.path.join(data_dir, dir_padre), ext)
    presentes, ausentes, no_cat = compare_images(db_images, fs_images)
    info = get_images_info(conn)

    print_log(presentes, ausentes, no_cat, info)

    # Contar png
    # print justificado
    # "Contando png"
    resultados = {}
    resultados[os.path.join(data_dir, dir_padre)] = len(fs_images)
    print('__________inicio conteo archivos________')
    for d, cant in resultados.items():
        print(f"Se encontraron {cant} archivos .png en {d}")
    print('__________fin conteo archivos________')

    conn.close()


if __name__ == '__main__':
    main()
