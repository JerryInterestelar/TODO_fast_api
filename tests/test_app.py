from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # Sem a fixture ficaria assim
    #   client = TestClient(app)

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}
