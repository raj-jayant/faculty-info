from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    admin = User(
        username='prerak',
        password=generate_password_hash('prerak'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()