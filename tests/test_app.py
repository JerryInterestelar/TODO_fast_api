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
