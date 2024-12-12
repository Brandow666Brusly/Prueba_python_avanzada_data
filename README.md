+---------------------------------------------------------------------------------------------+
|                 PROYECTO DE MIGRACIÓN Y ANÁLISIS DE DATOS DE IMÁGENES                        |
+---------------------------------------------------------------------------------------------+

+---------------------------------------+-----------------------------------------------------+
| Descripción del Proyecto     | Este proyecto analiza, migra y clasifica imágenes             |
|                              | (.png) tomando como base un archivo catalogo.txt,             |
|                              | almacenando la información en PostgreSQL y generando          |
|                              | un log con el estado final de cada imagen.                    |
+---------------------------------------+-----------------------------------------------------+

+-----------------------------+---------------------------------------------------------------+
| Objetivos                   | - Cargar datos desde catalogo.txt a PostgreSQL                |
|                             | - Identificar imágenes en el directorio vs. la BD             |
|                             | - Clasificar por categoría e insertar en                     |
|                             |   migracion_propiedades_archivos                              |
|                             | - Generar un log final con estado de las imágenes             |
|                             | - (Opcional) Visualizaciones y dockerización                 |
+-----------------------------+---------------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Requerimientos                    | - Python 3.10+                                          |
|                                   | - PostgreSQL 14+                                        |
|                                   | - Librerías (ver requirements.txt)                      |
|                                   | - Docker (opcional)                                     |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Estructura de Archivos/Directorios|                                                         |
|                                   | raiz_del_proyecto/                                      |
|                                   | ├─ src/                                                 |
|                                   | │  ├─ main.py (principal)                               |
|                                   | │  ├─ logic.py (lógica)                                 |
|                                   | │  ├─ db.py (conexión BD)                               |
|                                   | │  ├─ log.py (generar log final)                        |
|                                   | │  ├─ visualization.py (opcional)                       |
|                                   | │                                                       |
|                                   | ├─ data/ (catalogo.txt, IMAGENES/)                      |
|                                   | ├─ sql/ (create_tables.sql)                             |
|                                   | ├─ docker/ (Dockerfile, docker-compose.yaml)            |
|                                   | ├─ visualizaciones/                                     |
|                                   | ├─ config.ini                                           |
|                                   | ├─ requirements.txt                                     |
|                                   | ├─ README.md                                            |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Instalación Local (Sin Docker)    |                                                         |
|                                   | 1. Clonar repositorio:                                  |
|                                   |    ```                                                 |
|                                   |    git clone https://github.com/usuario/proyecto.git    |
|                                   |    cd proyecto                                          |
|                                   |    ```                                                 |
|                                   |                                                         |
|                                   | 2. Crear entorno virtual:                               |
|                                   |    ```                                                 |
|                                   |    python3 -m venv venv                                 |
|                                   |    source venv/bin/activate (Linux/Mac)                 |
|                                   |    venv\Scripts\activate (Win)                         |
|                                   |    ```                                                 |
|                                   |                                                         |
|                                   | 3. Instalar dependencias:                               |
|                                   |    ```                                                 |
|                                   |    pip install -r requirements.txt                      |
|                                   |    ```                                                 |
|                                   |                                                         |
|                                   | 4. Configurar config.ini (credenciales BD)              |
|                                   |                                                         |
|                                   | 5. Crear tablas:                                        |
|                                   |    ```                                                 |
|                                   |    psql -U postgres -d images_migration -f sql/create_tables.sql |
|                                   |    ```                                                 |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Ejecución del Proyecto (Local)    | Correr proceso completo:                                |
|                                   |    ```                                                 |
|                                   |    python src/main.py                                   |
|                                   |    ```                                                 |
|                                   |                                                         |
|                                   | Generar visualizaciones:                                |
|                                   |    ```                                                 |
|                                   |    python src/visualization.py                          |
|                                   |    ```                                                 |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Ejecución con Docker (Opcional)   | 1. Construir imagen:                                    |
|                                   |    ```                                                 |
|                                   |    docker-compose build                                 |
|                                   |    ```                                                 |
|                                   |                                                         |
|                                   | 2. Levantar servicios:                                  |
|                                   |    ```                                                 |
|                                   |    docker-compose up                                    |
|                                   |    ```                                                 |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Exportar la Base de Datos          | ```                                                    |
|                                   | pg_dump -U postgres -h localhost -p 5432                |
|                                   | -d images_migration -F p -f export/dump.sql             |
|                                   | ```                                                    |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Detalles de Conexión PostgreSQL   | Ajustar config.ini con credenciales correctas.          |
|                                   | Host = localhost (o db en docker), user = postgres, etc.|
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Ejemplos de Uso                   | Log final (ejemplo):                                    |
|                                   | ```                                                    |
|                                   | ===== LOG DE MIGRACIÓN =====                            |
|                                   | *** Imágenes Presentes ***                              |
|                                   | Imagen: 0520...001.png | Categoría: Servicios Adic.     |
|                                   | Estado: Presente                                        |
|                                   | ...                                                    |
|                                   | ===== FIN LOG =====                                     |
|                                   | ```                                                    |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Resolución de Problemas Comunes    | - Si no conecta a BD: revisar config.ini                |
|                                   | - No encuentra catalogo.txt: revisar data_dir en config |
|                                   | - Errores de dependencias: reinstalar requerimientos    |
+-----------------------------------+---------------------------------------------------------+

+-----------------------------------+---------------------------------------------------------+
| Contribuciones y Licencia          | Contributions bienvenidas, Licencia MIT (ejemplo)       |
+-----------------------------------+---------------------------------------------------------+
