from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
import re

from app.model import generate_image

app = FastAPI(
    title="Tiny SD API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "tryItOutEnabled": True
    }
)


@app.get("/")
def root():
    return {
        "message": "Tiny SD API is running"
    }

    
@app.get("/generate")
def generate(prompt: str):
    image = generate_image(prompt)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    safe_prompt = re.sub(
        r'[\\/*?:"<>|]',
        "_",
        prompt
    )[:40]

    filename = (
        f"{safe_prompt}-"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    path = output_dir / filename

    image.save(path)

    return FileResponse(
        path=path,
        media_type="image/png",
        filename=filename
    )