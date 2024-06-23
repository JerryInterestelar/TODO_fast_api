from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # Sem a fixture ficaria assim
    #   client = TestClient(app)

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_create_user_deve_retornar_created_e_no_modelo_certo(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test_user',
        'email': 'test_user@example.com',
    }


def test_read_users_deve_retornar_ok_e_uma_lista(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'test_user',
                'email': 'test_user@example.com',
            }
        ]
    }


def test_update_users_deve_retornar_ok_e_atualizar_usuario(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'test_user_updated',
            'email': 'test_user_2@example.com',
            'password': 'test_password_2',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test_user_updated',
        'email': 'test_user_2@example.com',
    }


def test_update_users_error_not_found(client):
    response = client.put(
        '/users/15',
        json={
            'username': 'test_user_updated',
            'email': 'test_user_2@example.com',
            'password': 'test_password_2',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_delete_users_deve_retornar_ok_e_usuario_deletado(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_users_error_not_found(client):
    response = client.delete('/users/15')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}
