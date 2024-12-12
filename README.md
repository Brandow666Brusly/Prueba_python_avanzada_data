# **Prueba Python Avanzada - Migración y Análisis de Datos**

## **Descripción del Proyecto**
Este proyecto es una solución técnica que utiliza Python y PostgreSQL para realizar la migración y análisis de datos relacionados con imágenes. El objetivo principal es clasificar, procesar y almacenar información sobre imágenes presentes en un sistema de archivos, comparándolas con los datos existentes en un archivo `catalogo.txt` y subiendo esta información a una base de datos PostgreSQL.

---

## **Objetivos**
- Leer el archivo `catalogo.txt` y cargar las imágenes y sus categorías en PostgreSQL.
- Identificar imágenes presentes físicamente en el sistema de archivos.
- Comparar las imágenes con los datos en la base de datos.
- Generar un log detallado de la migración que incluya:
  - Imágenes presentes (en sistema de archivos y base de datos).
  - Imágenes ausentes (en base de datos pero no en el sistema de archivos).
  - Imágenes no catalogadas (en el sistema de archivos pero no en la base de datos).

---

## **Requerimientos**
### **Software Necesario**
- Python 3.10 o superior.
- PostgreSQL 13 o superior.
- Git para control de versiones.

### **Dependencias de Python**
Las dependencias necesarias están listadas en `requirements.txt`. Puedes instalarlas ejecutando:
```bash
pip install -r requirements.txt
```
---

## **Estructura del Proyecto**
```
raiz_del_proyecto/
├── src/
│   ├── main.py              # Script principal.
│   ├── logic.py             # Lógica principal.
│   ├── db.py                # Funciones para base de datos.
│   ├── log.py               # Generación de logs.
│   ├── visualization.py     # Generación de visualizaciones.
├── data/                    # Carpeta de datos (incluye catalogo.txt e imágenes).
├── config.ini               # Archivo de configuración.
├── requirements.txt         # Dependencias de Python.
├── README.md                # Documentación del proyecto.
```
---

## **Instalación y Configuración**
### **1. Clonar el Repositorio**
```bash
git clone https://github.com/Brandow666Brusly/Prueba_python_avanzada_data.git
cd Prueba_python_avanzada_data
```

### **2. Configurar el Entorno Virtual**
```bash
python -m venv env
source env/bin/activate   # En Linux/Mac
env\Scripts\activate     # En Windows
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar PostgreSQL**
- Importa la base de datos exportada que se incluye en este proyecto.
  Para ello, utiliza el archivo SQL proporcionado (por ejemplo, `exported_db.sql`) con el siguiente comando:
  ```bash
  psql -U postgres -d images_migration -f exported_db.sql
  ```

- Configura `config.ini` con los detalles de tu conexión a PostgreSQL:
  ```ini
  [database]
  host = localhost
  user = postgres
  password = Pollito
  port = 5432
  dbname = images_migration

  [paths]
  data_dir = data
  directorio_carpeta_padre = contenedor_padre
  ```

---

## **Ejecución del Proyecto**
1. Ejecuta el script principal:
   ```bash
   python src/main.py
   ```
2. Los resultados de la migración se mostrarán en la consola y se generará un log con los detalles.

---

## **Resultados Esperados**
- Log detallado en consola con el estado de las imágenes.
- Visualización generada en la carpeta `visualizaciones/`.
- Datos migrados exitosamente a la base de datos PostgreSQL.

---

## **Contacto**
- **Autor:** Brandow666Brusly
- **Email:** bruslybrandow@gmail.com
- **Repositorio:** [GitHub](https://github.com/Brandow666Brusly/Prueba_python_avanzada_data)
