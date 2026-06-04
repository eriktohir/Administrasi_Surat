from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

class User(Base):
    """Tabel untuk autentikasi dan manajemen hak akses pengguna."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="staf", nullable=False) # e.g., 'pimpinan', 'tuud', 'staf'
    created_at = Column(Date, default=datetime.date.today)

class SuratMasuk(Base):
    """Tabel untuk menyimpan data arsip dan operasional Surat Masuk."""
    __tablename__ = "surat_masuk"

    id = Column(Integer, primary_key=True, index=True)
    no_surat = Column(String(100), unique=True, index=True, nullable=False)
    asal_surat = Column(String(150), nullable=False)
    perihal = Column(Text, nullable=False)
    tanggal_masuk = Column(Date, default=datetime.date.today, nullable=False)
    file_path = Column(String(255), nullable=True) # Menyimpan nama file dokumen fisik (PDF/Gambar)
    status_arsip = Column(String(20), default="Aktif", nullable=False) # 'Aktif' atau 'Diarsipkan'

    # Relasi satu ke banyak (Satu Surat Masuk bisa memiliki beberapa instruksi Disposisi)
    disposisi_list = relationship("Disposisi", back_populates="surat", cascade="all, delete-orphan")

class SuratKeluar(Base):
    """Tabel untuk menyimpan data arsip dan operasional Surat Keluar."""
    __tablename__ = "surat_keluar"

    id = Column(Integer, primary_key=True, index=True)
    no_surat = Column(String(100), unique=True, index=True, nullable=False)
    tujuan_surat = Column(String(150), nullable=False)
    perihal = Column(Text, nullable=False)
    tanggal_keluar = Column(Date, default=datetime.date.today, nullable=False)
    file_path = Column(String(255), nullable=True)
    status_arsip = Column(String(20), default="Aktif", nullable=False) # 'Aktif' atau 'Diarsipkan'

class Disposisi(Base):
    """Tabel untuk pelacakan alur penugasan dan instruksi pimpinan."""
    __tablename__ = "disposisi"

    id = Column(Integer, primary_key=True, index=True)
    # Menghubungkan disposisi secara spesifik ke ID Surat Masuk
    surat_masuk_id = Column(Integer, ForeignKey("surat_masuk.id", ondelete="CASCADE"), nullable=False)
    diteruskan_kepada = Column(String(100), nullable=False) # Nama jabatan/staf penerima tugas
    catatan = Column(Text, nullable=False) # Instruksi pimpinan
    status = Column(String(20), default="Proses", nullable=False) # 'Proses' atau 'Selesai'
    tanggal_disposisi = Column(Date, default=datetime.date.today)

    # Menghubungkan balik ke model SuratMasuk
    surat = relationship("SuratMasuk", back_populates="disposisi_list")