def test_search_kmp_success(client, mock_motor_success):
    """Integración: Búsqueda KMP exitosa"""
    client.post("/register", json={"email": "search@test.com", "password": "pass"})
    token = client.post("/login", json={"email": "search@test.com", "password": "pass"}).json()["access_token"]
    
    response = client.post("/search",
        headers={"Authorization": f"Bearer {token}"},
        data={"pattern": "ATCG", "algorithm": "kmp"},
        files={"csv_file": ("test.csv", b"Joy,ATCGATCG", "text/csv")}
    )
    assert response.status_code == 200
    assert response.json()["match_count"] == 1

def test_search_rabin_karp_success(client, mock_motor_success):
    """Integración: Búsqueda Rabin-Karp"""
    client.post("/register", json={"email": "search2@test.com", "password": "pass"})
    token = client.post("/login", json={"email": "search2@test.com", "password": "pass"}).json()["access_token"]
    
    response = client.post("/search",
        headers={"Authorization": f"Bearer {token}"},
        data={"pattern": "GCTA", "algorithm": "rabin_karp"},
        files={"csv_file": ("test.csv", b"User,GCTAGCTA", "text/csv")}
    )
    assert response.status_code == 200

def test_search_invalid_algorithm(client):
    """Caja negra: Algoritmo inválido"""
    client.post("/register", json={"email": "search3@test.com", "password": "pass"})
    token = client.post("/login", json={"email": "search3@test.com", "password": "pass"}).json()["access_token"]
    
    response = client.post("/search",
        headers={"Authorization": f"Bearer {token}"},
        data={"pattern": "ATCG", "algorithm": "invalid"},
        files={"csv_file": ("test.csv", b"Name,ATCG", "text/csv")}
    )
    assert response.status_code == 400

def test_search_saves_history(client, mock_motor_success):
    """Sistema: Guardar en historial"""
    client.post("/register", json={"email": "hist@test.com", "password": "pass"})
    token = client.post("/login", json={"email": "hist@test.com", "password": "pass"}).json()["access_token"]
    
    client.post("/search",
        headers={"Authorization": f"Bearer {token}"},
        data={"pattern": "TEST", "algorithm": "kmp"},
        files={"csv_file": ("test.csv", b"Name,ATCG", "text/csv")}
    )
    
    history = client.get("/history", headers={"Authorization": f"Bearer {token}"})
    assert history.json()["total"] >= 1