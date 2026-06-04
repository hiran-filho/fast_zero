from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings


def test_jwt():
    # Create a token
    data = {'sub': 'test_user'}
    token = create_access_token(data)
    # Decode the token
    decoded = decode(
        jwt=token, key=Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )
    # Verify the contents
    assert decoded['sub'] == data['sub']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalidtoken'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_invalid_email(client):
    # Create a token
    data = {'sub': 'test_user'}
    token = create_access_token(data)
    # Attempt to access a protected endpoint with the token
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    # The user with email 'test_user' does not exist,
    # so we expect an unauthorized error
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_without_email(client):
    # Create a token
    data = {'sub': ''}
    token = create_access_token(data)
    # Attempt to access a protected endpoint with the token
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    # The user with email '' does not exist,
    # so we expect an unauthorized error
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
