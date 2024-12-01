import pytest
from app import app, db, User


@pytest.fixture(scope='module')
def test_client():
    # Configure the app for testing with a separate test database
    app.config.from_object('config.TestConfig')
    with app.test_client() as client:
        # Establish an application context for the tests
        with app.app_context():
            # Create the database tables
            db.create_all()
        yield client
        # Clean up after tests by dropping tables
        with app.app_context():
            db.drop_all()


def test_register_user(test_client):
    response = test_client.post('/register', data={
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200

    response_data = response.data.decode('utf-8')
    assert 'Zaloguj się' in response_data

    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'
