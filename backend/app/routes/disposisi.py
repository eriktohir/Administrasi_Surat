from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.routes.auth import get_current_user

router = APIRouter(
    prefix="/disposisi",
    tags=["Manajemen Lembar Disposisi"]
)

# 1. BUAT INSTRUKSI DISPOSISI BARU (TERIKAT PADA SURAT MASUK)
@router.post("/", response_model=schemas.DisposisiResponse, status_code=status.HTTP_201_CREATED)
def create_disposisi(
    disposisi_in: schemas.DisposisiCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Validasi: Pastikan ID Surat Masuk yang dirujuk benar-asli eksis di database MySQL
    surat = db.query(models.SuratMasuk).filter(models.SuratMasuk.id == disposisi_in.surat_masuk_id).first()
    if not surat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gagal menerbitkan disposisi. Surat Masuk dengan ID {disposisi_in.surat_masuk_id} tidak ditemukan."
        )

    new_disposisi = models.Disposisi(
        surat_masuk_id=disposisi_in.surat_masuk_id,
        diteruskan_kepada=disposisi_in.diteruskan_kepada,
        catatan=disposisi_in.catatan,
        status=disposisi_in.status
    )
    db.add(new_disposisi)
    db.commit()
    db.refresh(new_disposisi)
    return new_disposisi

# 2. AMBIL SEMUA DATA RIWAYAT DISPOSISI
@router.get("/", response_model=List[schemas.DisposisiResponse])
def get_all_disposisi(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Disposisi).order_by(models.Disposisi.tanggal_disposisi.desc()).all()

# 3. AMBIL DETAIL DISPOSISI BERDASARKAN ID
@router.get("/{id}", response_model=schemas.DisposisiResponse)
def get_disposisi_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    disposisi = db.query(models.Disposisi).filter(models.Disposisi.id == id).first()
    if not disposisi:
        raise HTTPException(status_code=404, detail="Lembar instruksi disposisi tidak ditemukan.")
    return disposisi

# 4. UPDATE CATATAN / STATUS PEMROSESAN DISPOSISI
@router.put("/{id}", response_model=schemas.DisposisiResponse)
def update_disposisi(
    id: int,
    disposisi_update: schemas.DisposisiBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    disposisi = db.query(models.Disposisi).filter(models.Disposisi.id == id).first()
    if not disposisi:
        raise HTTPException(status_code=404, detail="Lembar disposisi tidak ditemukan.")

    disposisi.diteruskan_kepada = disposisi_update.diteruskan_kepada
    disposisi.catatan = disposisi_update.catatan
    disposisi.status = disposisi_update.status

    db.commit()
    db.refresh(disposisi)
    return disposisi

# 5. HAPUS DISPOSISI
@router.delete("/{id}")
def delete_disposisi(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    disposisi = db.query(models.Disposisi).filter(models.Disposisi.id == id).first()
    if not disposisi:
        raise HTTPException(status_code=404, detail="Lembar disposisi tidak ditemukan.")
    
    db.delete(disposisi)
    db.commit()
    return {"message": "Lembar disposisi berhasil dihapus dari sistem pelacakan."}