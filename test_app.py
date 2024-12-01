import pytest
from app import app, db, User

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config.TestConfig')  # Use your TestConfig here
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Set up the test database
        yield client  # This is where the test client is used
        with app.app_context():
            db.drop_all()  # Clean up the database after tests

def test_register_user(test_client):
    response = test_client.post('/register', data={
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Check that the user was added to the database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'

    # Optionally, check for flash messages
    response_data = response.data.decode('utf-8')
    assert 'Account created! You can now log in.' in response_data
