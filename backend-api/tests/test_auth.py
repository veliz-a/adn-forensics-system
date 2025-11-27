def test_register_new_user(client):
    """Unitaria: Registro exitoso"""
    response = client.post("/register", json={
        "email": "test0@example.com",
        "password": "securepass12345"
    })
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_register_duplicate_email(client):
    """Unitaria: Email duplicado"""
    client.post("/register", json={"email": "dup@test.com", "password": "pass"})
    response = client.post("/register", json={"email": "dup@test.com", "password": "pass"})
    assert response.status_code == 400

def test_login_correct_credentials(client):
    """Funcional: Login exitoso"""
    client.post("/register", json={"email": "user@test.com", "password": "mypass"})
    response = client.post("/login", json={"email": "user@test.com", "password": "mypass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    """Funcional: Password incorrecta"""
    client.post("/register", json={"email": "user@test.com", "password": "correct"})
    response = client.post("/login", json={"email": "user@test.com", "password": "wrong"})
    assert response.status_code == 401

def test_protected_route_no_token(client):
    """Funcional: Endpoint protegido sin token"""
    response = client.get("/history")
    assert response.status_code == 401

def test_protected_route_invalid_token(client):
    """Funcional: Token inválido"""
    response = client.get("/history", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401