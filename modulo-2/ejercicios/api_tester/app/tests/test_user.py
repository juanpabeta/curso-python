from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users",json={
        "id": 1,
        "nombre": "Juan Pablo",
        "email": "Juan@gmail.com"
    })
    assert response.status_code == 201

def test_duplicate_user():
    response = client.post("/users",json={
        "id": 2,
        "nombre": "Juan Pablo",
        "email": "Juan@gmail.com"
    })
    assert response.status_code == 409
    
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    
def test_get_user():
    client.post("/users",json={
        "id": 4,
        "nombre": "Antonio",
        "email": "Juan@gmail.com"
    })
    response = client.get("/users/4")
    assert response.status_code == 200
    assert response.json()['name'] == "Antonio"

def test_user_not_found():
    response = client.get("/users/10")
    assert response.status_code == 404
    
def test_update_user():
    response = client.put("/users/5",json= {
        "id":5,
        "name":"Laura Update",
        "email":"laura_new@gmail.com"
        
    })    
    assert response.status_code == 200
    
def test_update_user_not_found():
    response = client.put("/users/10",json= {
        "id":10,
        "name":"Fernanda",
        "email":"fernanda@gmail.com"
        
    })    
    assert response.status_code == 404

def test_delete_user():
    client.post("/users", json={
        "id": 6,
        "name": "Jesus",
        "email": "jesus@gmail.com"
    })
    
    response = client.delete("/users/6")
    assert response.status_code == 204

def test_delete_user_not_found():    
    response = client.delete("/users/90")
    assert response.status_code == 404
    
def test_full_flow():
    response = client.post("/users", json= {
        "id":7,
        "nombre":"Cristina",
        "email":"cristina@gamil.com"
    })
    
    response = client.get("/users/7")
    assert response.status_code == 200
    
    response = client.put("/users/7", json= {
        "id":7,
        "nombre":"Cristina",
        "email":"cristina@gamil.com"
    })
    assert response.status_code == 200
    
    response = client.delete("/users/7")
    assert response.status_code == 204 
    
    response = client.get("/users/7")
    assert response.status_code == 404