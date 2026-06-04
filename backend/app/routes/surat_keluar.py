from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import time
import shutil
import datetime

from app.database import get_db
from app import models, schemas
from app.routes.auth import get_current_user

router = APIRouter(
    prefix="/surat-keluar",
    tags=["Manajemen Surat Keluar"]
)

UPLOAD_DIR = "app/uploads"

# 1. TAMBAH SURAT KELUAR BARU
@router.post("/", response_model=schemas.SuratKeluarResponse, status_code=status.HTTP_201_CREATED)
async def create_surat_keluar(
    no_surat: str = Form(...),
    tujuan_surat: str = Form(...),
    perihal: str = Form(...),
    tanggal_keluar: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    existing_surat = db.query(models.SuratKeluar).filter(models.SuratKeluar.no_surat == no_surat).first()
    if existing_surat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Surat keluar dengan Nomor {no_surat} sudah terdaftar di sistem."
        )

    try:
        parsed_date = datetime.datetime.strptime(tanggal_keluar, "%Y-%m-%d").date()
    except ValueError:
        parsed_date = datetime.date.today()

    saved_filename = None
    if file:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".png", ".jpg", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Format file tidak valid.")
        
        clean_filename = file.filename.replace(" ", "_")
        saved_filename = f"{int(time.time())}_{clean_filename}"
        with open(os.path.join(UPLOAD_DIR, saved_filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    new_surat = models.SuratKeluar(
        no_surat=no_surat,
        tujuan_surat=tujuan_surat,
        perihal=perihal,
        tanggal_keluar=parsed_date,
        file_path=saved_filename
    )
    db.add(new_surat)
    db.commit()
    db.refresh(new_surat)
    return new_surat

# 2. AMBIL SEMUA DATA SURAT KELUAR
@router.get("/", response_model=List[schemas.SuratKeluarResponse])
def get_all_surat_keluar(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.SuratKeluar).order_by(models.SuratKeluar.tanggal_keluar.desc()).all()

# 3. AMBIL DETAIL SURAT KELUAR BY ID
@router.get("/{id}", response_model=schemas.SuratKeluarResponse)
def get_surat_keluar_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    surat = db.query(models.SuratKeluar).filter(models.SuratKeluar.id == id).first()
    if not surat:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    return surat

# 4. UPDATE DATA SURAT KELUAR
@router.put("/{id}", response_model=schemas.SuratKeluarResponse)
async def update_surat_keluar(
    id: int,
    no_surat: str = Form(...),
    tujuan_surat: str = Form(...),
    perihal: str = Form(...),
    tanggal_keluar: str = Form(...),
    status_arsip: str = Form("Aktif"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    surat = db.query(models.SuratKeluar).filter(models.SuratKeluar.id == id).first()
    if not surat:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")

    try:
        parsed_date = datetime.datetime.strptime(tanggal_keluar, "%Y-%m-%d").date()
    except ValueError:
        parsed_date = surat.tanggal_keluar

    if file:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in [".pdf", ".png", ".jpg", ".jpeg"]:
            if surat.file_path:
                old_path = os.path.join(UPLOAD_DIR, surat.file_path)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            clean_filename = file.filename.replace(" ", "_")
            saved_filename = f"{int(time.time())}_{clean_filename}"
            with open(os.path.join(UPLOAD_DIR, saved_filename), "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            surat.file_path = saved_filename

    surat.no_surat = no_surat
    surat.tujuan_surat = tujuan_surat
    surat.perihal = perihal
    surat.tanggal_keluar = parsed_date
    surat.status_arsip = status_arsip

    db.commit()
    db.refresh(surat)
    return surat

# 5. HAPUS DATA SURAT KELUAR
@router.delete("/{id}")
def delete_surat_keluar(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    surat = db.query(models.SuratKeluar).filter(models.SuratKeluar.id == id).first()
    if not surat:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    
    if surat.file_path:
        old_path = os.path.join(UPLOAD_DIR, surat.file_path)
        if os.path.exists(old_path):
            os.remove(old_path)

    db.delete(surat)
    db.commit()
    return {"message": "Data surat keluar berhasil dihapus."}