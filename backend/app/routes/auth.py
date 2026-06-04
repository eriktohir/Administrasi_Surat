from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from app.database import get_db
from app import models, schemas, utils
from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Autentikasi Pengguna"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ==========================================
# ENDPOINT: LOGIN & GENERATE TOKEN JWT
# ==========================================
@router.post("/login", response_model=schemas.Token)
def login_user(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    # Cari pengguna berdasarkan username
    user = db.query(models.User).filter(models.User.username == user_in.username).first()
    
    # Validasi keberadaan user dan kesesuaian password
    if not user or not utils.verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password yang Anda masukkan salah.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Siapkan data payload yang akan dibungkus di dalam Token JWT
    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role
    }
    
    # Buat token akses JWT
    access_token = utils.create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================
# ENDPOINT: REGISTER USER
# ==========================================
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Cek apakah username sudah terdaftar
    existing = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username tersebut sudah terdaftar di dalam sistem."
        )

    # Enkripsi password sebelum disimpan
    hashed_pwd = utils.hash_password(user_in.password)

    # Buat objek user baru sesuai model
    new_user = models.User(
        username=user_in.username,
        password_hash=hashed_pwd,
        role=(user_in.role or "staf").lower()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ==========================================
# HELPER: FUNGSI CEK USER AKTIF (ROUTE GUARD)
# ==========================================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Fungsi helper untuk memproteksi halaman internal."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesi Anda telah berakhir atau token tidak sah. Silakan login kembali.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Dekripsi token JWT
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user