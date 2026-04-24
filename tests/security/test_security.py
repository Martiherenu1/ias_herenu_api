import os
from app.main import app

def test_debug_is_false():
    # Verificamos que el modo debug no esté activado por defecto por seguridad
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    assert debug_mode is False