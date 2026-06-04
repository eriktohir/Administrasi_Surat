from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List
from ..database import get_db_connection
from ..auth import get_current_user

router = APIRouter()

@router.get('/staf')
def statistik_staf_per_bulan(tahun: int = 2026, current_user: dict = Depends(get_current_user)):
    if current_user.get('role_id') != 1:
        raise HTTPException(status_code=403, detail="Hanya admin")
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB error")
    cursor = conn.cursor(dictionary=True)
    # Ambil semua user dengan role_id = 2 (staf)
    cursor.execute("SELECT id, username FROM users WHERE role_id = 2")
    stafs = cursor.fetchall()
    
    result = []
    for staf in stafs:
        data_per_bulan = []
        for bulan in range(1, 13):
            # hitung surat masuk yang dibuat oleh staf ini
            cursor.execute("""
                SELECT COUNT(*) as jumlah FROM dokumen 
                WHERE arah = 'masuk' AND user_id = %s AND YEAR(tanggal) = %s AND MONTH(tanggal) = %s
            """, (staf['id'], tahun, bulan))
            masuk = cursor.fetchone()['jumlah']
            cursor.execute("""
                SELECT COUNT(*) as jumlah FROM dokumen 
                WHERE arah = 'keluar' AND user_id = %s AND YEAR(tanggal) = %s AND MONTH(tanggal) = %s
            """, (staf['id'], tahun, bulan))
            keluar = cursor.fetchone()['jumlah']
            data_per_bulan.append({'masuk': masuk, 'keluar': keluar})
        result.append({
            'user_id': staf['id'],
            'username': staf['username'],
            'data': data_per_bulan
        })
    cursor.close()
    conn.close()
    return result