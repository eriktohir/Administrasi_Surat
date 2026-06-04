from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from ..database import get_db_connection
from ..auth import get_current_user, get_password_hash
from ..models import UserCreate, UserUpdate
from ..utils import log_audit, get_client_ip
from fastapi import Request

router = APIRouter()


def admin_required(current_user: Dict):
    if current_user.get('role_id') != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Administrator access required')


@router.get('/')
def list_users(current_user: dict = Depends(get_current_user)):
    admin_required(current_user)
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, username, role_id, created_at FROM users ORDER BY created_at DESC')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@router.post('/')
def create_user(user: UserCreate, request: Request, current_user: dict = Depends(get_current_user)):
    admin_required(current_user)
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    password_hash = get_password_hash(user.password)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (username, password_hash, role_id) VALUES (%s, %s, %s)',
        (user.username, password_hash, user.role_id)
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    log_audit(conn, current_user['user_id'], f'Create user id={user_id}', 'users', get_client_ip(request))
    conn.close()
    return {'id': user_id}


@router.put('/{user_id}')
def update_user(user_id: int, user: UserUpdate, request: Request, current_user: dict = Depends(get_current_user)):
    admin_required(current_user)
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id FROM users WHERE id = %s', (user_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User tidak ditemukan')

    fields = []
    params = []
    if user.username is not None:
        fields.append('username = %s')
        params.append(user.username)
    if user.password:
        fields.append('password_hash = %s')
        params.append(get_password_hash(user.password))
    if user.role_id is not None:
        fields.append('role_id = %s')
        params.append(user.role_id)

    if fields:
        params.append(user_id)
        cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = %s", tuple(params))
        conn.commit()

    cursor.close()
    log_audit(conn, current_user['user_id'], f'Update user id={user_id}', 'users', get_client_ip(request))
    conn.close()
    return {'id': user_id}


@router.delete('/{user_id}')
def delete_user(user_id: int, request: Request, current_user: dict = Depends(get_current_user)):
    admin_required(current_user)
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database connection failed')

    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User tidak ditemukan')

    conn.commit()
    cursor.close()
    log_audit(conn, current_user['user_id'], f'Delete user id={user_id}', 'users', get_client_ip(request))
    conn.close()
    return {'id': user_id}
