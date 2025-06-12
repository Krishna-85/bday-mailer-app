from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "server/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, "employees.xlsx")
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "File uploaded successfully!"}
