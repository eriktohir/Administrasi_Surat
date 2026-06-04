from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import datetime

# ==========================================
# SCHEMAS UNTUK USER & AUTENTIKASI
# ==========================================
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str
class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(UserBase):
    id: int
    created_at: datetime.date
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

# ==========================================
# SCHEMAS UNTUK DISPOSISI
# ==========================================
class DisposisiBase(BaseModel):
    diteruskan_kepada: str
    catatan: str
    status: str = "Proses"

class DisposisiCreate(DisposisiBase):
    surat_masuk_id: int

class DisposisiResponse(DisposisiBase):
    id: int
    surat_masuk_id: int
    tanggal_disposisi: datetime.date
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# SCHEMAS UNTUK SURAT MASUK
# ==========================================
class SuratMasukBase(BaseModel):
    no_surat: str
    asal_surat: str
    perihal: str
    status_arsip: str = "Aktif"

class SuratMasukCreate(SuratMasukBase):
    tanggal_masuk: datetime.date

class SuratMasukResponse(SuratMasukBase):
    id: int
    tanggal_masuk: datetime.date
    file_path: Optional[str] = None
    # Menyertakan list instruksi disposisi yang terikat secara otomatis (Nested Relational)
    disposisi_list: List[DisposisiResponse] = []
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# SCHEMAS UNTUK SURAT KELUAR
# ==========================================
class SuratKeluarBase(BaseModel):
    no_surat: str
    tujuan_surat: str
    perihal: str
    status_arsip: str = "Aktif"

class SuratKeluarCreate(SuratKeluarBase):
    tanggal_keluar: datetime.date

class SuratKeluarResponse(SuratKeluarBase):
    id: int
    tanggal_keluar: datetime.date
    file_path: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)