from app.main import app

def test_get_users():
    client = app.test_client()
    response = client.get('/users')
    
    # Verificamos la integración básica del endpoint de usuarios
    assert response.status_code == 200
    assert "users" in response.get_json()