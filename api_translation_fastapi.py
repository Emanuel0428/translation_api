# api_translation_fastapi.py
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pdf2docx import Converter
from docx import Document
from googletrans import Translator
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()
translator = Translator()
templates = Jinja2Templates(directory="templates")

# Montar la carpeta estática para los estilos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Crear carpeta de archivos temporales si no existe para guardar los archivos temporalmente por la sesion
TEMP_FOLDER = "temp_files"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def render_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/translate")
async def translate_file(
        file: UploadFile = File(...),
        src_lang: str = Form(...),
        dest_lang: str = Form(...)
):
    extension = file.filename.split(".")[-1].lower()

    # Validar que los idiomas seleccionados sean válidos!
    if not src_lang or not dest_lang:
        return {"error": "Por favor selecciona ambos, idioma de la fuente y el destino."}

    if extension == "pdf":
        return await translate_pdf_to_docx(file, src_lang, dest_lang)
    elif extension == "docx":
        return await translate_docx(file, src_lang, dest_lang)
    else:
        return {"error": "Tipo de archivo no soportado :/. Por favor sube un archivo .pdf o .docx."}

# Función para traducir un archivo PDF
async def translate_pdf_to_docx(file: UploadFile, src_lang: str, dest_lang: str):
    # Guardar archivo PDF temporalmente
    input_pdf_path = os.path.join(TEMP_FOLDER, f"temp_{file.filename}")
    with open(input_pdf_path, "wb") as temp_file:
        temp_file.write(await file.read())

    # Convertir PDF a DOCX para usarlo
    output_docx_path = os.path.join(TEMP_FOLDER, f"temp_{file.filename.rsplit('.', 1)[0]}.docx")
    cv = Converter(input_pdf_path)
    cv.convert(output_docx_path, start=0, end=None)
    cv.close()

    # Traducir el archivo DOCX generado a partir del PDF
    translated_docx_path = await translate_docx_internal(output_docx_path, src_lang, dest_lang)

    # Eliminar archivos temporales generados durante el proceso
    os.remove(input_pdf_path)
    os.remove(output_docx_path)

    return FileResponse(
        translated_docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"translated_{file.filename.rsplit('.', 1)[0]}.docx",
    )

# Función para traducir un archivo DOCX
async def translate_docx(file: UploadFile, src_lang: str, dest_lang: str):
    # Guardar archivo DOCX temporalmente para usarlo
    input_docx_path = os.path.join(TEMP_FOLDER, f"temp_{file.filename}")
    with open(input_docx_path, "wb") as temp_file:
        temp_file.write(await file.read())

    # Traducir el archivo DOCX y obtener la ruta del archivo traducido
    translated_docx_path = await translate_docx_internal(input_docx_path, src_lang, dest_lang)

    # Eliminar archivo original temporal generado durante el proceso
    os.remove(input_docx_path)

    return FileResponse(
        translated_docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"translated_{file.filename}",
    )

# Función para traducir el contenido de un archivo DOCX
async def translate_docx_internal(input_docx_path, src_lang, dest_lang):

    document = Document(input_docx_path)

    translated_docx_path = os.path.join("translated_files", os.path.basename(input_docx_path.replace("temp_", "translated_")))

    os.makedirs(os.path.dirname(translated_docx_path), exist_ok=True)

    # Traducir el contenido
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            translated_text = translator.translate(paragraph.text, src=src_lang, dest=dest_lang).text
            paragraph.text = translated_text

    # Guardar el archivo traducido
    document.save(translated_docx_path)

    return translated_docx_path

