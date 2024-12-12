import os
import configparser
import pandas as pd
import hashlib

def read_config(config_path='config.ini'):
    """Lee cfg."""
    c = configparser.ConfigParser()
    c.read(config_path)
    return c

def get_filesystem_images(base_path, extension):
    """Obtiene imágenes del FS."""
    fs_images = []
    for raiz, _, archivos in os.walk(base_path):  # Recorre todas las carpetas
        print(f"Explorando carpeta: {os.path.abspath(raiz)}")
        for archivo in archivos:
            print(f"Archivo encontrado: {archivo}")  # Lista todos los archivos
            if archivo.lower().endswith(extension.lower()):  # Ignora mayúsculas/minúsculas
                ruta_completa = os.path.join(raiz, archivo)
                fs_images.append(ruta_completa)
                print(f"Imagen válida encontrada: {ruta_completa}")
    return fs_images

def compare_images(db_images, fs_images):
    """Compara imágenes entre BD y FS."""
    # Convierte ambas listas en conjuntos
    db_images_set = set(db_images)
    fs_images_set = set(fs_images)

    # Calcula las diferencias y la intersección
    presentes = db_images_set.intersection(fs_images_set)
    ausentes = db_images_set.difference(fs_images_set)
    no_cat = fs_images_set.difference(db_images_set)

    return presentes, ausentes, no_cat


def load_hash_for_images(hash_path):
    """Lee hash."""
    # Lee hash.txt
    hashes={}
    if os.path.isfile(hash_path):
        with open(hash_path,'r',encoding='utf-8') as f:
            lines = f.read().splitlines()
        # Asumiendo form: NOMBRE_ARCHIVO|RUTA|HASH
        # Ajustar sep si difiere
        for line in lines[1:]:
            parts=line.split('|')
            if len(parts)>=3:
                nombre_arch=parts[0].strip()
                h=parts[2].strip()
                hashes[nombre_arch.lower()]=h
    return hashes

def generate_hash_for_image(file_path):
    """Gen hash."""
    # Lee binario
    h=hashlib.sha256()
    if os.path.isfile(file_path):
        with open(file_path,'rb') as f:
            content=f.read()
        h.update(content)
        return h.hexdigest()
    else:
        return None

def process_catalogo(catalogo_path, sep, campos):
    """Proc cat."""
    # df = pd.read_csv(catalogo_path, sep=sep, header=0, error_bad_lines=False)
    df = pd.read_csv(catalogo_path, sep=sep, header=0, on_bad_lines='skip')

    # Check cols
    req_cols = [campos['ano_rad_field'], campos['codi_secl_field'], campos['codi_pat_field'], campos['nume_rad_field'], campos['nomb_ima_field']]
    for c in req_cols:
        if c not in df.columns:
            return []
    registros=[]
    for _,row in df.iterrows():
        registros.append({
            'nombre_imagen': row[campos['nomb_ima_field']],
            'ano_rad': row[campos['ano_rad_field']],
            'codi_secl': row[campos['codi_secl_field']],
            'codi_pat': row[campos['codi_pat_field']],
            'nume_rad': row[campos['nume_rad_field']]
        })
    return registros

def get_category_from_path(catalogo_path, data_dir, dir_padre):
    """Cat path."""
    rel=os.path.relpath(catalogo_path, os.path.join(data_dir,dir_padre.strip('/')))
    parts=rel.split(os.sep)
    # Estructura: CATEGORIA_X/.../catalogo.txt
    # penultimo dir antes de catalogo.txt es la categoria final
    if len(parts)>1:
        return parts[-2]
    return 'Desconocida'

def find_catalogos(data_dir, dir_padre, catalogo_filename):
    """Hall catalogos."""
    cat_paths=[]
    base_path=os.path.join(data_dir, dir_padre.strip('/'))
    for raiz,_,archivos in os.walk(base_path):
        for archivo in archivos:
            if archivo.lower()==catalogo_filename.lower():
                cat_paths.append(os.path.join(raiz,archivo))
    return cat_paths
