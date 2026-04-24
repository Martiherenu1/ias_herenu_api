from app.main import app

def test_health_check():
    # Configuramos el cliente de pruebas de Flask
    client = app.test_client()
    
    # Hacemos una petición GET al endpoint
    response = client.get('/health')
    
    # Verificamos que el código de estado sea 200 y el status sea 'ok'
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "message": "El servicio está funcionando"}