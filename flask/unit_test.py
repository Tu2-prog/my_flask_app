import pytest
from models import app 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client 
    
class TestSomething:
    def test_index(self, client):
        res = client.get('/')
        assert res.status_code