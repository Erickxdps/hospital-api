import pytest # type: ignore

def test_get_patients(test_client, admin_auth_headers):
    # El usuario con el rol de "admin" debería poder obtener la lista de patientos
    response = test_client.get("/api/patients", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json == []


def test_create_patient(test_client, admin_auth_headers):
    # El usuario con el rol de "admin" debería poder crear un nuevo pacientes
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


def test_get_patient(test_client, admin_auth_headers):
    response = test_client.get("/api/patients/1", headers=admin_auth_headers)
    assert response.status_code == 200
    assert "name" in response.json


def test_get_nonexistent_patient(test_client, admin_auth_headers):
    response = test_client.get("/api/patients/999", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Paciente no encontrado"


def test_create_patient_invalid_data(test_client, admin_auth_headers):
    data = {"name": "Carlos"}  
    # El usuario con el rol de "admin" debería recibir un error al intentar crear un patiento con datos inválidos
    response = test_client.post("/api/patients", json=data, headers=admin_auth_headers)
    assert response.status_code == 400
    assert response.json["error"] == "Faltan datos requeridos"


def test_update_patient(test_client, admin_auth_headers):
    # El usuario con el rol de "admin" debería poder actualizar un patiento existente
    data = {
        "name": "Erick",
        "lastname": "Perez",
        "ci" : "32425",
        "birth_date" : "12/12/2010"	
    }
    response = test_client.put("/api/patients/1", json=data, headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json["name"]== "Erick"
    assert response.json["lastname"]== "Perez"
    assert response.json["ci"]== "32425"
    assert response.json["birth_date"]== "12/12/2010"


def test_update_nonexistent_patient(test_client, admin_auth_headers):
    # El usuario con el rol de "admin" debería recibir un error al intentar actualizar un patiento inexistente
    data = {
        "name": "Joaquin",
        "lastname": "Otich",
        "ci":"253252",
        "birth_date":"12/12/2014"
    }
    response = test_client.put(
        "/api/patients/999", json=data, headers=admin_auth_headers
    )
    # Verifica que el patiento no ha sido actualizado
    assert response.status_code == 404
    assert response.json["error"] == "Paciente no encontrado"


def test_delete_patient(test_client, admin_auth_headers):
    # El usuario con el rol de "admin" debería poder eliminar un patiento existente
    response = test_client.delete("/api/patients/1", headers=admin_auth_headers)
    assert response.status_code == 204

    # Verifica que el patiento ha sido eliminado
    response = test_client.get("/api/patients/1", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Paciente no encontrado"


def test_delete_nonexistent_patient(test_client, admin_auth_headers):
    # El usuario con el rol de "admin" debería recibir un error al intentar eliminar un patiento inexistente
    response = test_client.delete("/api/patients/999", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Paciente no encontrado"
