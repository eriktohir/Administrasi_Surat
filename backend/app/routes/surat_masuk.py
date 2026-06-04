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
    prefix="/surat-masuk",
    tags=["Manajemen Surat Masuk"]
)

# Tentukan lokasi penyimpanan folder upload berkas fisik
UPLOAD_DIR = "app/uploads"

# =========================================================================
# 1. ENDPOINT: TAMBAH SURAT MASUK BARU + UPLOAD FILE
# =========================================================================
@router.post("/", response_model=schemas.SuratMasukResponse, status_code=status.HTTP_201_CREATED)
async def create_surat_masuk(
    no_surat: str = Form(...),
    asal_surat: str = Form(...),
    perihal: str = Form(...),
    tanggal_masuk: str = Form(...), # Diterima dalam format string YYYY-MM-DD dari form Ionic
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Proteksi Token JWT[cite: 1]
):
    # Validasi: Cek apakah nomor surat sudah pernah diinput sebelumnya
    existing_surat = db.query(models.SuratMasuk).filter(models.SuratMasuk.no_surat == no_surat).first()
    if existing_surat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Surat masuk dengan Nomor {no_surat} sudah terdaftar di sistem."
        )

    # Konversi string tanggal dari frontend menjadi objek date Python
    try:
        parsed_date = datetime.datetime.strptime(tanggal_masuk, "%Y-%m-%d").date()
    except ValueError:
        parsed_date = datetime.date.today()

    # Proses penyimpanan berkas fisik jika ada file yang diunggah
    saved_filename = None
    if file:
        # Validasi ekstensi berkas demi keamanan server
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".png", ".jpg", ".jpeg"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format file tidak didukung. Hanya diizinkan berkas .pdf, .png, .jpg, atau .jpeg"
            )
        
        # Penamaan ulang file agar unik: kombinasi timestamp + nama file asli bersih
        clean_filename = file.filename.replace(" ", "_")
        saved_filename = f"{int(time.time())}_{clean_filename}"
        file_path = os.path.join(UPLOAD_DIR, saved_filename)
        
        # Simpan file secara biner ke dalam folder penyimpanan server
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Simpan record data ke database MySQL
    new_surat = models.SuratMasuk(
        no_surat=no_surat,
        asal_surat=asal_surat,
        perihal=perihal,
        tanggal_masuk=parsed_date,
        file_path=saved_filename
    )
    
    db.add(new_surat)
    db.commit()
    db.refresh(new_surat)
    return new_surat

# =========================================================================
# 2. ENDPOINT: AMBIL SEMUA DATA SURAT MASUK (UNTUK TABEL UTAMA)
# =========================================================================
@router.get("/", response_model=List[schemas.SuratMasukResponse])
def get_all_surat_masuk(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Harus login[cite: 1]
):
    # Menarik seluruh data surat masuk diurutkan dari yang paling baru diterima
    return db.query(models.SuratMasuk).order_by(models.SuratMasuk.tanggal_masuk.desc()).all()

# =========================================================================
# 3. ENDPOINT: AMBIL DETAIL DATA BERDASARKAN ID SURAT (UNTUK MODE EDIT)
# =========================================================================
@router.get("/{id}", response_model=schemas.SuratMasukResponse)
def get_surat_masuk_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    surat = db.query(models.SuratMasuk).filter(models.SuratMasuk.id == id).first()
    if not surat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data surat masuk tidak ditemukan.")
    return surat

# =========================================================================
# 4. ENDPOINT: UPDATE DATA SURAT MASUK
# =========================================================================
@router.put("/{id}", response_model=schemas.SuratMasukResponse)
async def update_surat_masuk(
    id: int,
    no_surat: str = Form(...),
    asal_surat: str = Form(...),
    perihal: str = Form(...),
    tanggal_masuk: str = Form(...),
    status_arsip: str = Form("Aktif"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    surat = db.query(models.SuratMasuk).filter(models.SuratMasuk.id == id).first()
    if not surat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data surat tidak ditemukan.")
    
    # Validasi perubahan tanggal
    try:
        parsed_date = datetime.datetime.strptime(tanggal_masuk, "%Y-%m-%d").date()
    except ValueError:
        parsed_date = surat.tanggal_masuk

    # Update berkas dokumen jika ada file baru yang diunggah
    if file:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in [".pdf", ".png", ".jpg", ".jpeg"]:
            # Hapus berkas fisik lama dari server jika sebelumnya ada
            if surat.file_path:
                old_file_path = os.path.join(UPLOAD_DIR, surat.file_path)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            # Simpan berkas fisik baru
            clean_filename = file.filename.replace(" ", "_")
            saved_filename = f"{int(time.time())}_{clean_filename}"
            new_file_path = os.path.join(UPLOAD_DIR, saved_filename)
            with open(new_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            surat.file_path = saved_filename

    # Update field data teks lainnya
    surat.no_surat = no_surat
    surat.asal_surat = asal_surat
    surat.perihal = perihal
    surat.tanggal_masuk = parsed_date
    surat.status_arsip = status_arsip

    db.commit()
    db.refresh(surat)
    return surat

# =========================================================================
# 5. ENDPOINT: HAPUS DATA SURAT MASUK (CASCADE DISPOSISI OTOMATIS)
# =========================================================================
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_surat_masuk(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    surat = db.query(models.SuratMasuk).filter(models.SuratMasuk.id == id).first()
    if not surat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data surat masuk tidak ditemukan.")
    
    # Hapus file fisik dari penyimpanan server agar tidak memenuhi memori penyimpanan
    if surat.file_path:
        file_to_delete = os.path.join(UPLOAD_DIR, surat.file_path)
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
            
    db.delete(surat)
    db.commit()
    return {"message": f"Data surat masuk dengan ID {id} beserta berkas fisiknya berhasil dihapus secara permanen."}