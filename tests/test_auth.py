from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
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
        '/auth/token',
        data={
            'username': 'username_errado',
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect Username or Password'}


def test_get_token_error_senha_errada(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.username,
            'password': 'Senha_errada',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect Username or Password'}
