from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
# Import seluruh rute backend
from app.routes import auth, surat_masuk, surat_keluar, disposisi

# Jalankan skema pembuatan tabel database relasional otomatis
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistem API Administrasi Surat - TUUD",
    description="Backend Server untuk Capstone Project Manajemen Surat Masuk, Keluar, dan Disposisi",
    version="1.0.0"
)

# Konfigurasi Akses Lintas Origin (CORS) agar Front-End Ionic bisa melakukan Request API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup direktori penyimpanan berkas statis
UPLOAD_DIR = "app/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/static/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Registrasi Router Endpoints Terpadu
app.include_router(auth.router)
app.include_router(surat_masuk.router)
app.include_router(surat_keluar.router)
app.include_router(disposisi.router)

@app.get("/", tags=["Sistem"])
def read_root():
    return {
        "status": "Online",
        "aplikasi": "API Administrasi Surat TUUD",
        "pesan": "Gunakan endpoint /docs untuk melihat dokumentasi interaktif Swagger OpenAPI."
    }