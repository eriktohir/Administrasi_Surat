# ==============================================================================
# SCRIPT STRUKTUR DATABASE MYSQL (TUUD_SURAT)
# ==============================================================================
# Script ini merepresentasikan struktur tabel final yang digunakan oleh aplikasi
# untuk keperluan migrasi, backup, maupun inisialisasi phpMyAdmin.
# ==============================================================================

DATABASE_SCHEMA_SQL = """
CREATE DATABASE IF NOT EXISTS tuud_surat;
USE tuud_surat;

-- 1. TABEL ROLES
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_role VARCHAR(50) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert Default Roles jika belum ada
INSERT IGNORE INTO roles (id, nama_role) VALUES 
(1, 'admin'), 
(2, 'staf'), 
(3, 'pimpinan'), 
(4, 'arsiparis');

-- 2. TABEL USERS
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert Default Admin (Password: admin123) jika belum ada
INSERT IGNORE INTO users (id, username, password_hash, role_id) VALUES 
(1, 'admin', '$2b$12$Rf4mxqK6DGbXtF0mmq1n/O.g.BBvnIV/5nShLwPzp3EkVGkqyLtGq', 1);

-- 3. TABEL UTAMA: DOKUMEN (Mengakomodir Surat Masuk & Surat Keluar)
CREATE TABLE IF NOT EXISTS dokumen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_dokumen VARCHAR(100) UNIQUE DEFAULT NULL,
    arah ENUM('masuk', 'keluar') NOT NULL,
    asal_tujuan VARCHAR(255) DEFAULT NULL,
    perihal TEXT DEFAULT NULL,
    tanggal DATE DEFAULT NULL,
    file_path VARCHAR(255) DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'Diterima',
    user_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 4. TABEL DISPOSISI
CREATE TABLE IF NOT EXISTS disposisi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dokumen_id INT NOT NULL,
    dari_user_id INT NOT NULL,
    untuk_user_id INT DEFAULT NULL,
    instruksi TEXT DEFAULT NULL,
    tanggal_disposisi DATE DEFAULT NULL,
    catatan TEXT DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'Proses',
    file_path VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (dokumen_id) REFERENCES dokumen(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (dari_user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (untuk_user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 5. TABEL TRACKING DOKUMEN (Riwayat Perubahan Status)
CREATE TABLE IF NOT EXISTS tracking_dokumen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dokumen_id INT NOT NULL,
    status VARCHAR(50) DEFAULT NULL,
    catatan TEXT DEFAULT NULL,
    updated_by INT DEFAULT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dokumen_id) REFERENCES dokumen(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 6. TABEL ARSIP
CREATE TABLE IF NOT EXISTS arsip (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dokumen_id INT NOT NULL,
    kategori VARCHAR(100) DEFAULT NULL,
    keterangan TEXT DEFAULT NULL,
    tanggal_arsip DATE DEFAULT NULL,
    file_path VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (dokumen_id) REFERENCES dokumen(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 7. TABEL AUDIT LOGS (Keamanan & Tracking Aktivitas Staf/User)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    aktivitas VARCHAR(255) DEFAULT NULL,
    tabel_terkait VARCHAR(50) DEFAULT NULL,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ==============================================================================
-- INDEX OPTIMASI QUERY (Dashboard Statistik & Pencarian)
-- ==============================================================================
CREATE INDEX idx_dokumen_user_tanggal ON dokumen(user_id, tanggal);
CREATE INDEX idx_dokumen_arah_status ON dokumen(arah, status);
CREATE INDEX idx_disposisi_dokumen ON disposisi(dokumen_id);
"""