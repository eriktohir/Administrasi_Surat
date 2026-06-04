from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Request
from typing import Optional
from ..database import get_db_connection
from ..auth import get_current_user
from ..utils import save_upload_file, log_audit, get_client_ip

router = APIRouter()


@router.get('/')
def list_dokumen(arah: Optional[str] = None, limit: Optional[int] = None):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    query = 'SELECT id, nomor_dokumen, arah, asal_tujuan, perihal, tanggal, file_path, status, user_id, created_at FROM dokumen'
    params = []
    if arah:
        query += ' WHERE arah = %s'
        params.append(arah)
    query += ' ORDER BY created_at DESC'
    if limit is not None and limit > 0:
        query += ' LIMIT %s'
        params.append(limit)

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@router.get('/count')
def count_dokumen(arah: Optional[str] = None):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    query = 'SELECT COUNT(*) AS count FROM dokumen'
    params = []
    if arah:
        query += ' WHERE arah = %s'
        params.append(arah)

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    count = cursor.fetchone()['count']
    cursor.close()
    conn.close()
    return {'count': count}


@router.post('/')
def create_dokumen(
    request: Request,
    current_user: dict = Depends(get_current_user),
    arah: str = Form(...),
    asal_tujuan: str = Form(...),
    perihal: str = Form(...),
    tanggal: str = Form(...),
    file: Optional[UploadFile] = File(None),
):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    file_path = save_upload_file(file)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO dokumen (arah, asal_tujuan, perihal, tanggal, file_path, user_id) VALUES (%s, %s, %s, %s, %s, %s)',
        (arah, asal_tujuan, perihal, tanggal, file_path, current_user['user_id'])
    )
    conn.commit()
    dokumen_id = cursor.lastrowid
    cursor.close()
    log_audit(conn, current_user['user_id'], f'Create dokumen id={dokumen_id}', 'dokumen', get_client_ip(request))
    conn.close()
    return {'id': dokumen_id}


@router.put('/{dokumen_id}')
def update_dokumen(
    dokumen_id: int,
    request: Request,
    current_user: dict = Depends(get_current_user),
    arah: Optional[str] = Form(None),
    asal_tujuan: Optional[str] = Form(None),
    perihal: Optional[str] = Form(None),
    tanggal: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id FROM dokumen WHERE id = %s', (dokumen_id,))
    dokumen = cursor.fetchone()
    if not dokumen:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dokumen tidak ditemukan')

    fields = []
    params = []
    if arah is not None:
        fields.append('arah = %s')
        params.append(arah)
    if asal_tujuan is not None:
        fields.append('asal_tujuan = %s')
        params.append(asal_tujuan)
    if perihal is not None:
        fields.append('perihal = %s')
        params.append(perihal)
    if tanggal is not None:
        fields.append('tanggal = %s')
        params.append(tanggal)
    if file is not None:
        file_path = save_upload_file(file)
        fields.append('file_path = %s')
        params.append(file_path)
    if fields:
        params.append(dokumen_id)
        query = f"UPDATE dokumen SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, tuple(params))
        conn.commit()

    cursor.close()
    log_audit(conn, current_user['user_id'], f'Update dokumen id={dokumen_id}', 'dokumen', get_client_ip(request))
    conn.close()
    return {'id': dokumen_id}


@router.delete('/{dokumen_id}')
def delete_dokumen(dokumen_id: int, request: Request, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor()
    cursor.execute('DELETE FROM dokumen WHERE id = %s', (dokumen_id,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dokumen tidak ditemukan')

    conn.commit()
    cursor.close()
    log_audit(conn, current_user['user_id'], f'Delete dokumen id={dokumen_id}', 'dokumen', get_client_ip(request))
    conn.close()
    return {'id': dokumen_id}
