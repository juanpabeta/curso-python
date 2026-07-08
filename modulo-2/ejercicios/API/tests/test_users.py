from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users",json={
        "id" : 1,
        "name": "Maria",
        "email":"maria@gmail.com"
    })
    assert response.status_code == 201

def test_duplicate_user():
    client.post("/users",json={
        "id": 2,
        "name": "Ana",
        "email": "ana@gmail.com"
    })

    response = client.post("/users", json={
        "id" : 3,
        "name":" Ana Torres",
        "email":"ana@gmail.com"

    })

    assert response.status_code == 409

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user():
    client.post("/users",json={
        "id": 4,
        "name": "carlos",
        "email": "carlos@gmail.com"
    })

    response = client.get("/users/4")
    assert response.status_code==200
    assert response.json() ["name"] == "carlos" 

def test_user_not_found():
    response= client.get("/users/10")
    assert response.status_code == 404

def test_update_user():
    client.post("/users", json={ 
        "id": 5,
        "name": "Laura",
        "email": "laura@gmail.com"
    })

    response = client.put("/users/5", json={
        "id": 5,
        "name": "Laura Update",
        "email": "laura_new@gmail.com"
    })

    assert response.status_code == 200
    assert response.json() ["name"] == "Laura Update"

def test_update_user_not_found():
    response = response = client.put("/users/10", json={
        "id": 10,
        "name": "Fernanda",
        "email": "fernanda@gmail.com"
    })

    assert response.status_code == 404

def test_delete_user():
    client.post("/users", json={
        "id": 6,
        "name": "Pedro",
        "email": "pedro@gmail.com"
    })
    
    response = client.delete("/users/6")
    assert response.status_code == 204

def test_delete_user_not_found():
    response = client.delete("/users/10")
    assert response.status_code == 404

def test_full_flow():
    response = client.post("/users", json={
        "id": 7,
        "name": "Daniela",
        "email": "daniela@gmail.com"
    })
    
    assert response.status_code == 201

    response = client.get("/users/7")
    assert response.status_code==200

    response = client.put("/users/7", json={
        "id": 7,
        "name": "Daniela Rodriguez",
        "email":"dani@gmail.com"
    })

    assert response.status_code == 200
  
    response = client.delete("/users/7")
    assert response.status_code == 204

    response = client.get("/users/7")
    assert response.status_code == 404




