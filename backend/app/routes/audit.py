from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..database import get_db_connection
from ..auth import get_current_user
from ..utils import log_audit, get_client_ip

router = APIRouter()


@router.get('/')
def list_audit(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user.get('role_id') != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Administrator access required')

    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT a.id, a.user_id, u.username AS username, a.aktivitas, a.tabel_terkait, a.ip_address, a.waktu '
        'FROM audit_logs a LEFT JOIN users u ON a.user_id = u.id ORDER BY a.waktu DESC'
    )
    rows = cursor.fetchall()
    cursor.close()
    log_audit(conn, current_user['user_id'], 'Read audit logs', 'audit_logs', get_client_ip(request))
    conn.close()
    return rows
