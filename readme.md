# Traductor de Documentos API

Este proyecto consiste en una API REST construida con **FastAPI** que permite traducir documentos en formatos **PDF** y **DOCX** de un idioma a otro. La API utiliza el servicio de Google Translate para realizar la traducción y permite la conversión de archivos PDF a DOCX antes de la traducción.

## Funcionalidades

- Subir un archivo PDF o DOCX para su traducción.
- Convertir documentos PDF a DOCX antes de traducirlos.
- Traducir el contenido del archivo a un idioma deseado, con la opción de seleccionar el idioma de origen y el de destino.
- Descargar el archivo traducido como un nuevo documento DOCX.

## Requisitos

- Python 3.8+
- Las siguientes bibliotecas de Python:
  - FastAPI
  - Uvicorn (para el servidor de desarrollo)
  - googletrans==4.0.0-rc1 (para traducción)
  - pdf2docx (para conversión de PDF a DOCX)
  - python-docx (para manipulación de archivos DOCX)

## Instalación

1. **Clonar el repositorio**:

    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    ```

2. **Crear un entorno virtual** (opcional pero recomendado):

    ```bash
    python -m venv venv
    ```

3. **Activar el entorno virtual**:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Ejecutar la aplicación**:

    ```bash
    uvicorn main:app --reload
    ```

    La API estará disponible en `http://127.0.0.1:8000`.

## Uso de la API

1. **Acceder al formulario de traducción**:

   Abre tu navegador y ve a `http://127.0.0.1:8000`. Allí podrás subir el archivo que deseas traducir.

2. **Subir un archivo**:

   Selecciona un archivo PDF o DOCX y selecciona el idioma de origen y destino. Luego haz clic en **Traducir**.

3. **Descargar el archivo traducido**:

   Después de realizar la traducción, el archivo traducido estará disponible para su descarga.

## Aspectos a mejorar y en desarrollo

Mantener el formato original y realizar la traducción conservando los elementos esteticos (muy pronto)...

