from app.database import SessionLocal
from app import models, utils
import traceback

db = SessionLocal()
try:
    hashed = utils.hash_password('password_for_test')
    new_user = models.User(username='test_user_probe', password_hash=hashed, role='staf')
    db.add(new_user)
    db.commit()
    print('created', new_user.id)
except Exception as e:
    traceback.print_exc()
finally:
    db.close()
