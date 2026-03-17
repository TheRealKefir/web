import requests

from data.db_session import global_init, create_session
from data.users import User
import pytest

BASE_URL = 'http://localhost:5000/api/v2'

@pytest.fixture
def create_conn():
    global_init('db/mass_explorer.db')
    sess = create_session()
    yield sess
    sess.close()

def test_post_user(create_conn):
    response = requests.post(BASE_URL + '/users', json={
        'name': 'John',
        "surname": "Doe",
        'email': 'john.doe@example.com',
        'password': '123456'
    })
    assert response.status_code == 200
    uid = response.json()['id']
    create_conn.get('User', uid)
    user = create_conn.get(User, uid)
    assert user.email == 'john.doe@example.com'

def test_get_users(create_conn):
    response = requests.get(BASE_URL + '/users')
    assert response.status_code == 200
    users = [item.to_dict(only=('id', 'name', 'surname', 'email'))
            for item in create_conn.query(User).all()]
    assert response.json() == users


def test_get_one_user(create_conn):
    response = requests.get(BASE_URL + '/users/1')
    assert response.status_code == 200
    user = create_conn.get(User, 1).to_dict(max_serilization_depth=0)
    assert response.json() == {'user': user}


def test_get_wrong_user_id():
    response = requests.get(BASE_URL + '/users/100000')
    assert response.status_code == 404
    assert response.json() == {'error': f"User 100000 not found"}


def test_get_str_user_id():
    response = requests.get(BASE_URL + '/users/asd')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_post_empty_user():
    response = requests.post(BASE_URL + '/users', json={})
    assert response.status_code == 400
    assert response.json() == {'error': 'Empty request'}


def test_post_bad_user():
    response = requests.post(BASE_URL + '/users', json={'name': 'jhkahfvewkaf'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Bad request'}


def test_delete_user():
    response = requests.delete(BASE_URL + '/users/1')
    assert response.status_code == 200
    assert response.json() == {'success': 'OK'}


def test_delete_nonexistent_user():
    response = requests.delete(BASE_URL + '/users/100000')
    assert response.status_code == 404
    assert response.json() == {'error': 'User 100000 not found'}


def test_delete_str_user():
    response = requests.delete(BASE_URL + '/users/asd')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}

