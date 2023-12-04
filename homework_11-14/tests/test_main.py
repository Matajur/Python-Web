from fastapi.testclient import TestClient

import main


client = TestClient(main.app)

# pytest tests/ <- to run tests
# pytest tests/ -s <- to run test with enabled print()


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_main_docs():
    response = client.get("/docs")
    assert response.status_code == 200
