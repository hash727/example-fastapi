import pytest
from app import schemas

from jose import jwt
from app.config import settings
    

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Hello World"
#     assert res.status_code == 200



def test_create_user(client):
    res = client.post("/users/", json = {"email":"test112@gmail.com", "password":"test123"})
    #print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test112@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data = {"username":test_user['email'], "password":test_user['password']})
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secrete_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "Bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ("test123@gmail.com", "WrongPassword", 403),
    ("wronguser@gmail.com", "test123", 403),
    ("wronguser@gmail.com", "WrongPassword", 403),
    ("test123@gmail.com", None, 422),
    (None, "WrongPassword", 422)
])
def test_error_login_user(client, test_user, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password":password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials !"