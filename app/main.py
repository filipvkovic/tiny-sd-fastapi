from datetime import datetime
from pathlib import Path
from urllib.parse import quote
import re

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.model import generate_image
from app.schemas import GenerateRequest, GenerateResponse

app = FastAPI(
    title="Tiny SD API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"tryItOutEnabled": True},
)

# Persistent folder inside HF Space workspace
OUTPUT_DIR = Path("/workspace/persistent_outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Serve generated files publicly
app.mount("/outputs", StaticFiles(directory=str(OUTPUT_DIR)), name="outputs")


@app.get("/")
def root():
    return {"message": "Tiny SD API is running"}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest, request: Request):
    prompt = req.prompt
    image = generate_image(prompt)

    # Sanitize filename
    safe_prompt = re.sub(r'[\\/*?:"<>|]', "_", prompt)[:40]
    filename = f"{safe_prompt}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = OUTPUT_DIR / filename

    # Save image locally
    image.save(path)

    # URL-encode filename for safe HTTP URL
    encoded_filename = quote(filename, safe="")
    base_url = str(request.base_url).rstrip("/")

    return GenerateResponse(
        filename=filename, url=f"{base_url}/outputs/{encoded_filename}"
    )
