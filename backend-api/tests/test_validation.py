def test_upload_csv_valid_format(client):
    """Funcional: CSV válido"""
    client.post("/register", json={"email": "up@test.com", "password": "pass"})
    token = client.post("/login", json={"email": "up@test.com", "password": "pass"}).json()["access_token"]
    
    response = client.post("/upload-csv",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", b"Name,ATCG", "text/csv")}
    )
    assert response.status_code == 200

def test_upload_csv_wrong_extension(client):
    """Funcional: Extensión incorrecta"""
    client.post("/register", json={"email": "up2@test.com", "password": "pass"})
    token = client.post("/login", json={"email": "up2@test.com", "password": "pass"}).json()["access_token"]
    
    response = client.post("/upload-csv",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", b"data", "text/plain")}
    )
    assert response.status_code == 400

def test_upload_csv_invalid_chars(client):
    """Caja negra: Caracteres inválidos"""
    client.post("/register", json={"email": "up3@test.com", "password": "pass"})
    token = client.post("/login", json={"email": "up3@test.com", "password": "pass"}).json()["access_token"]
    
    response = client.post("/upload-csv",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("bad.csv", b"Name,XYZ123", "text/csv")}
    )
    assert response.status_code == 200