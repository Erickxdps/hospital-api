def test_get_patients_as_user(test_client, user_auth_headers):
    # El usuario con el rol de "user" debería poder obtener la lista de pacientes
    response = test_client.get("/api/patients", headers=user_auth_headers)
    assert response.status_code == 200
    assert response.json == []


def test_create_product(test_client, admin_auth_headers):
    # El usuario con el rol de "admin" debería poder crear un nuevo producto
    data = {
        "name": "Javis",
        "lastname" : "Perez",
        "ci" : "123456",
        "birth_date" : "12/12/2021"
    }
    response = test_client.post("/api/patients", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    assert response.json["name"] == "Javis"
    assert response.json["lastname"] == "Perez"
    assert response.json["ci"] == "123456"
    assert response.json["birth_date"] == "12/12/2021"


def test_create_product_as_user(test_client, user_auth_headers):
    # El usuario con el rol de "user" no debería poder crear un producto
    data = {
        "name": "Pakin",
        "lastname": "Otich",
        "ci":"1234",
        "birth_date":"12/12/2001"
    }
    response = test_client.post("/api/patients", json=data, headers=user_auth_headers)
    assert response.status_code == 403


def test_get_product_as_user(test_client, user_auth_headers):
    # El usuario con el rol de "user" debería poder obtener un producto específico
    # Este test asume que existe al menos un producto en la base de datos
    response = test_client.get("/api/patients/1", headers=user_auth_headers)
    assert response.status_code == 200
    assert "name" in response.json
    assert "lastname" in response.json
    assert "ci" in response.json
    assert "birth_date" in response.json


def test_update_product_as_user(test_client, user_auth_headers):
    # El usuario con el rol de "user" no debería poder actualizar un producto
    data = {
        "name": "Cris",
        "lastname": "Ortega",
        "ci":"32875",
        "birth_date":"12/12/1990"
    }
    response = test_client.put("/api/patients/1", json=data, headers=user_auth_headers)
    assert response.status_code == 403


def test_delete_product_as_user(test_client, user_auth_headers):
    # El usuario con el rol de "user" no debería poder eliminar un producto
    response = test_client.delete("/api/patients/1", headers=user_auth_headers)
    assert response.status_code == 403
