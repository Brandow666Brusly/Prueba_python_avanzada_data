import configparser
import psycopg2

def get_config(config_path='config.ini', section='database'):
    """Lee config seccion."""
    # Lee config
    c = configparser.ConfigParser()
    c.read(config_path)
    return c[section]

def get_connection(config_path='config.ini'):
    """Conecta BD."""
    # Lee DB config
    dbconf = get_config(config_path, 'database')
    conn = psycopg2.connect(
        dbname=dbconf.get('dbname'),
        user=dbconf.get('user'),
        password=dbconf.get('password'),
        host=dbconf.get('host'),
        port=dbconf.get('port')
    )
    return conn

def ensure_categoria_documento(conn, codigo, nombre, ruta):
    """Asegura catdoc."""
    # Sin var global
    with conn.cursor() as cur:
        # catdoc
        cur.execute("SELECT codigo_categoria FROM categoria_documento WHERE codigo_categoria=%s",(codigo,))
        row=cur.fetchone()
        if not row:
            # Insertar
            cur.execute("INSERT INTO categoria_documento (codigo_categoria,nombre_categoria,ruta_categoria) VALUES (%s,%s,%s)",
                        (codigo,nombre,ruta))
            conn.commit()

def ensure_encabezado_migracion(conn, ruta_base):
    """Encabezado mig."""
    with conn.cursor() as cur:
        cur.execute("SELECT id_migracion FROM encabezado_migracion WHERE id_migracion=1")
        row = cur.fetchone()
        if not row:
            cur.execute("INSERT INTO encabezado_migracion (id_migracion,ruta_carpeta_base) VALUES (%s,%s)",(1,ruta_base))
            conn.commit()

def ensure_categoria(conn, cat_name):
    """Asegura cat."""
    with conn.cursor() as cur:
        cur.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria=%s",(cat_name,))
        r=cur.fetchone()
        if r:
            return r[0]
        else:
            cur.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s) RETURNING id_categoria",(cat_name,))
            new_id=cur.fetchone()[0]
            conn.commit()
            return new_id

def insert_imagen(conn, nombre_archivo, categoria_id, extension, peso, fecha_creacion, ruta_archivo, llave, hash_archivo):
    """Inserta imagen."""
    # Insert imagenes_catalogo
    with conn.cursor() as cur:
        cur.execute("INSERT INTO imagenes_catalogo (nombre_imagen,categoria_id) VALUES (%s,%s) RETURNING id_imagen",
                    (nombre_archivo,categoria_id))
        id_img = cur.fetchone()[0]
        # Insert migracion_propiedades_archivos
        cur.execute("""INSERT INTO migracion_propiedades_archivos 
        (id_migracion,nombre_archivo,extension_archivo,peso_archivo,fecha_creacion,ruta_archivo,llave,hash_archivo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (1,nombre_archivo,extension,peso,fecha_creacion,ruta_archivo,llave,hash_archivo))
        conn.commit()

def get_db_images(conn):
    """Imgs BD."""
    with conn.cursor() as cur:
        cur.execute("SELECT nombre_archivo FROM migracion_propiedades_archivos")
        rows=cur.fetchall()
    return set(r[0] for r in rows)

def get_images_info(conn):
    """Info imgs."""
    with conn.cursor() as cur:
        cur.execute("SELECT nombre_archivo,llave FROM migracion_propiedades_archivos")
        rows=cur.fetchall()
    return {r[0]: r[1] for r in rows}
