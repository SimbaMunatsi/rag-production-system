def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_user(client):
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_secure_query_endpoint_without_token(client):
    response = client.post(
        "/query",
        json={"query": "What is the capital?", "session_id": "123"}
    )
    # Should fail because no token was provided
    assert response.status_code == 401