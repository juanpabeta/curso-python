import os
os.environ['DATABASE_URL'] = 'sqlite:///./test_universidad.db'
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'
os.environ['JWT_ALGORITHM'] = 'HS256'
os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = '60'

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.database import Base, SessionLocal, engine
from app.users.models import Role, User, UserRole
from app.core.security import hash_password
from app.main import app

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()
try:
    db.query(UserRole).delete()
    db.query(Role).delete()
    db.query(User).delete()
    role = Role(name='Administrador', description='Administrador del sistema')
    db.add(role)
    db.flush()
    user = User(
        email='admin@universidad.test',
        full_name='Admin Test',
        password_hash=hash_password('Secret123!'),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.flush()
    db.add(UserRole(user_id=user.id, role_id=role.id))
    db.commit()
finally:
    db.close()

client = TestClient(app)
resp = client.post('/auth/login', json={'email': 'admin@universidad.test', 'password': 'Secret123!'})
print('STATUS', resp.status_code)
print(resp.text)
