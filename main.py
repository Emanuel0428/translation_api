# main.py
from fastapi import FastAPI
from api_translation_fastapi import app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_translation_fastapi:app", host="0.0.0.0", port=8000, reload=True)
