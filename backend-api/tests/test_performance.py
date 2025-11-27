import time

def test_response_time_register(client):
    """Performance: Tiempo de registro < 1s"""
    start = time.time()
    client.post("/register", json={"email": f"perf{time.time()}@test.com", "password": "pass"})
    duration = time.time() - start
    assert duration < 1.0

def test_response_time_login(client):
    """Performance: Tiempo de login < 1s"""
    email = f"perf{time.time()}@test.com"
    client.post("/register", json={"email": email, "password": "pass"})
    
    start = time.time()
    client.post("/login", json={"email": email, "password": "pass"})
    duration = time.time() - start
    assert duration < 1.0