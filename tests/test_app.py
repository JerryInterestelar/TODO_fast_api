from http import HTTPStatus

from fast_zero.schemas import UserSchemaPublic
from fast_zero.security import create_access_token


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


def test_create_user_username_duplicado(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user',  # Mesmo username
            'email': 'test_user_02@example.com',
            'password': 'test_password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_duplicado(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user_02',
            'email': 'test_user@example.com',  # Mesmo email
            'password': 'test_password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users_sem_usuarios(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_com_usuarios(client, user):
    user_schema = UserSchemaPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_deve_retornar_ok_e_um_usuario(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test_user',
        'email': 'test_user@example.com',
    }


def test_read_user_error_not_found(client):
    response = client.get('/users/15')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_users_deve_retornar_ok_e_atualizar_usuario(
    client,
    user,
    token,
):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_user_updated',
            'email': 'test_user_2@example.com',
            'password': 'test_password_2',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'test_user_updated',
        'email': 'test_user_2@example.com',
    }


def test_update_users_error_atualizar_outro_user(
    client,
    user,
    token,
):
    response = client.put(
        '/users/5',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_user_updated',
            'email': 'test_user_2@example.com',
            'password': 'test_password_2',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_users_error_token_com_user_nulo(
    client,
    user,
    token,
):
    wrong_token = create_access_token(data={'sub': ''})

    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {wrong_token}'},
        json={
            'username': 'test_user_updated',
            'email': 'test_user_2@example.com',
            'password': 'test_password_2',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_update_users_error_token_com_user_invalido(
    client,
    user,
    token,
):
    wrong_token = create_access_token(data={'sub': 'user_invalid'})

    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {wrong_token}'},
        json={
            'username': 'test_user_updated',
            'email': 'test_user_2@example.com',
            'password': 'test_password_2',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_users_deve_retornar_ok_e_usuario_deletado(
    client,
    user,
    token,
):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_users_error_deletar_outro_user(
    client,
    user,
    token,
):
    response = client.delete(
        '/users/5',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token


def test_get_token_error_username_errado(client, user):
    response = client.post(
        '/token',
        data={
            'username': 'username_errado',
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect Username or Password'}


def test_get_token_error_senha_errada(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.username,
            'password': 'Senha_errada',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect Username or Password'}
