from http import HTTPStatus

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fast_zero.app import app

app = FastAPI()

# def test2():
#     client = TestClient(app)
#     response = client.get('/exercicio-html')

#     assert response.status_code == HTTPStatus.OK
#     assert '<h1> Olá Mundo </h1>' in response.text


@pytest.fixture
def client():
    return TestClient(app)


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_create_user():
    client = TestClient(app)

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }
