from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile, Request
from typing import Optional
from ..database import get_db_connection
from ..auth import get_current_user
from ..utils import save_upload_file, log_audit, get_client_ip

router = APIRouter()


@router.get('/')
def list_arsip():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT a.id, a.dokumen_id, a.kategori, a.keterangan, a.tanggal_arsip, d.nomor_dokumen, d.asal_tujuan, d.perihal, d.file_path '
        'FROM arsip a LEFT JOIN dokumen d ON a.dokumen_id = d.id ORDER BY a.tanggal_arsip DESC'
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@router.post('/')
def create_arsip(
    request: Request,
    current_user: dict = Depends(get_current_user),
    dokumen_id: int = Form(...),
    kategori: str = Form(...),
    keterangan: str = Form(None),
    tanggal_arsip: str = Form(...),
    file: Optional[UploadFile] = File(None),
):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    file_path = save_upload_file(file)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO arsip (dokumen_id, kategori, keterangan, tanggal_arsip) VALUES (%s, %s, %s, %s)',
        (dokumen_id, kategori, keterangan, tanggal_arsip)
    )
    conn.commit()
    arsip_id = cursor.lastrowid
    if file_path:
        cursor.execute('UPDATE dokumen SET file_path = %s WHERE id = %s', (file_path, dokumen_id))
        conn.commit()
    cursor.close()
    log_audit(conn, current_user['user_id'], f'Create arsip id={arsip_id}', 'arsip', get_client_ip(request))
    conn.close()
    return {'id': arsip_id}


@router.delete('/{arsip_id}')
def delete_arsip(arsip_id: int, request: Request, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor()
    cursor.execute('DELETE FROM arsip WHERE id = %s', (arsip_id,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Arsip tidak ditemukan')

    conn.commit()
    cursor.close()
    log_audit(conn, current_user['user_id'], f'Delete arsip id={arsip_id}', 'arsip', get_client_ip(request))
    conn.close()
    return {'id': arsip_id}
