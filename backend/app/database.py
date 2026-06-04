from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Cek apakah koneksi menggunakan sqlite atau mysql untuk penyesuaian parameter khusus
IS_SQLITE = settings.DATABASE_URL.startswith("sqlite")

if IS_SQLITE:
    # Parameter 'check_same_thread' khusus diperlukan untuk SQLite di Android/Lokal
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Engine standar untuk koneksi MySQL di server
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Fungsi Dependency untuk menyuntikkan session database ke setiap API Endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()