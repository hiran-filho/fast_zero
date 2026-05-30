from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


# def test_exercicio_ola_mundo_em_html():
#     client = TestClient(app)

#     response = client.get('/exercicio-html')

#     assert response.status_code == HTTPStatus.OK
#     assert '<h1> Olá Mundo </h1>' in response.text


def test_create_user(client):
    # client = TestClient(app)

    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'securepassword',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_read_users(client):
    # client = TestClient(app)

    # Primeiro, criamos um usuário para garantir que ele exista
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'alice',
                'email': 'alice@example.com',
            }
        ]
    }


def test_update_user(client):
    # client = TestClient(app)

    # Primeiro, criamos um usuário para garantir que ele exista
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'securepassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


# exercio Aula 03 - Teste listar user, está antes do delete deviso a
# interdependência dos testes
def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_delete_user(client):
    # client = TestClient(app)

    # Primeiro, criamos um usuário para garantir que ele exista
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


# Exercio Aula 03 - Teste de erro ao atualizar usuário inexistente
def test_update_nonexistent_user(client):
    # client = TestClient(app)

    response = client.put(
        '/users/999',
        json={
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'securepassword',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário com id 999 não encontrado.'}


# Exercio Aula 03 - Teste de erro ao deletar usuário inexistente
def test_delete_nonexistent_user(client):
    # client = TestClient(app)

    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário com id 999 não encontrado.'}


def test_read_user_exception(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário com id 999 não encontrado.'}
