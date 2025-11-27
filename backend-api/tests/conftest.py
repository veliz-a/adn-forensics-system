import pytest
from fastapi.testclient import TestClient
from app.main import app
import tempfile
import os

@pytest.fixture
def client():
    """Cliente de prueba sin BD"""
    return TestClient(app)

@pytest.fixture
def mock_motor_success(monkeypatch):
    """Mock del motor C++ exitoso"""
    import subprocess
    import json
    
    def mock_run(*args, **kwargs):
        class MockResult:
            returncode = 0
            stdout = json.dumps({
                "success": True,
                "algorithm": "kmp",
                "pattern": "ATCG",
                "total_sequences": 3,
                "matches": [{"name": "Joy Williamson", "positions": [0, 10]}],
                "match_count": 1,
                "execution_time_ms": 50,
                "threads_used": 1,
                "hash_collisions": 0
            })
            stderr = ""
        return MockResult()
    
    monkeypatch.setattr(subprocess, "run", mock_run)

@pytest.fixture
def valid_csv_file():
    """Archivo CSV válido temporal"""
    content = b"Joy Williamson,ATCGATCGATCG\nShannon Burns,GCTAGCTAGCTA\nTest User,TTTTAAAACCCC"
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as f:
        f.write(content)
        path = f.name
    yield path
    os.unlink(path)