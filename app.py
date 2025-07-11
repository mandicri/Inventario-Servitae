from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import time

app = FastAPI()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".bmp", ".webp", ".png"}
BASE_UPLOADS_DIR = Path("uploads")

@app.post("/upload/{marketplace}")
async def upload_barcode(marketplace: str, file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    dest_dir = BASE_UPLOADS_DIR / marketplace
    dest_dir.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time() * 1000)
    dest_file = dest_dir / f"{marketplace}_{timestamp}{ext}"

    with dest_file.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"marketplace": marketplace, "filename": dest_file.name}
