import pytest
from app import app, db, User  # Ensure these are imported correctly from your app
from flask import session

@pytest.fixture
def client():
    # Setup test client
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for tests
    app.config['SECRET_KEY'] = 'test_secret_key'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_button(client):
    data = {
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }

    response = client.post('/register', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert "Zaloguj się tutaj" in response.data.decode("utf-8")


def test_register_existing_user(client):
    with app.app_context():
        hashed_password = app.bcrypt.generate_password_hash('password123').decode('utf-8')
        db.session.add(User(username='existinguser', password=hashed_password))
        db.session.commit()

    data = {
        'username': 'existinguser',
        'password': 'password123',
        'confirm_password': 'password123'
    }
    response = client.post('/register', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Username already exists" in response.data
