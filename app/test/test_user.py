from fastapi.datastructures import FormData
from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_main():
    response = client.get('/')
    assert response.status_code == 200
    
def test_login():
    payload = {
        "email": "sebastian2405lucero@hotmail.com",
        "password": "@asdaw@qweDb"
    }
    response = client.post("/api/v1/login", json=payload)
    if response.status_code == 202:
        assert "detail" in response.json()
        assert "token" in response.json()['detail']
        assert "nombre" in response.json()['detail']
        assert "apellido" in response.json()['detail']
        assert "rol" in response.json()['detail']
        assert "email" in response.json()['detail']
        assert "id" in response.json()['detail']
    elif response.status_code == 409:
        assert "Necesitas activar tu cuenta revisa tu correo para confirmar" in response.json()['detail']['msg']


def get_auth_token():
    payload = {
        "email": "sebastian2405lucero@hotmail.com",
        "password": "@asdaw@qweDb"
    }
    response = client.post("/api/v1/login", json=payload)
    if response.status_code == 202:
        return response.json()['detail']['token']
    elif response.status_code == 409:
        assert 'Necesitas activar tu cuenta revisa tu correo para confirmar' in response.json()['detail']['msg']
    
def test_register():
    payload = {
        "nombre": "David",
        "apellido": "Basantes",
        "email": "sebastian2405lucero@gmail.com",
        "telefono": "090095964",
        "password": "@asdaw@qweDb"
    }
    
    response = client.post('/api/v1/register', json=payload)
    if response.status_code == 201:
        assert "Revisa tu correo para activar tu cuenta" in response.json()["detail"]['msg']
    
    elif response.status_code == 409:
        assert 'Este email ya se encuentra en uso' in response.json()['detail']['msg']
    
def test_check_mail():
    token = 'RdGZA0TaHXdpSeOm051uZkkKXFoU1oHa5KRt'
    response = client.get(f'/api/v1/check-email/{token}')
    if response.status_code == 200:
        assert "Ya puedes iniciar sesión" in response.json()['detail']['msg']
    elif response.status_code == 400:
        assert "La cuenta ya ha sido confirmada" in response.json()[
            'detail']['msg']
        
# def test_recover_password():
#     payload = {
#         "email": "sebastian2405lucero@hotmail.com"
#     }
#     response = client.post('/api/v1/recover-password', json=payload)
    
#     if response.status_code == 202:
#         assert "Revisa tu correo para recuperar tu contraseña" in response.json()['detail']["msg"]
#     elif response.status_code == 422:
#         assert "Necesita activar su cuenta" in response.json()[
#             'detail']["msg"]
# def test_recover_password_token():
#     token = "VoghhVZHnO5Xv7pkzDGBB4UjCrMiASabK8ju"
    
#     response = client.get(f'/api/v1/recover-password/{token}')
    
#     assert response.status_code == 200
#     assert "Token confirmado ya puedes crear tu nueva contraseña" in response.json()[
#         'detail']["msg"]
    
# def test_new_password():
#     token = "VoghhVZHnO5Xv7pkzDGBB4UjCrMiASabK8ju"
#     payload = {
#         "new_password": "@asdaw@qweDb",
#         "check_password": "@asdaw@qweDb"
#     }
#     response = client.post(f'/api/v1/new-password/{token}',json=payload)
#     if response.status_code == 200:
#         assert "Tu contraseña a sido actualizada ya puedes iniciar sesión" in response.json()[
#             'detail']["msg"]
#     elif response.status_code ==400:
#         assert "La cuenta ya ha sido confirmada" in response.json()['detail']['msg']

def test_profile():
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/profile",headers=header)
    assert response.status_code == 202
    assert "nombre" in response.json()['detail']
    assert "apellido" in response.json()['detail']
    assert "telefono" in response.json()['detail']
    assert "email" in response.json()['detail']
    
def test_update_password():
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    payload = {
        "new_password": "@asdaw@qweDb",
        "check_password": "@asdaw@qweDb"
    }
    response = client.put("/api/v1/update-password",headers=header, json=payload)
    if response.status_code == 202:
        assert "Tu contraseña a sido actualizada" in response.json()['detail']['msg']
    elif response.status_code == 406:
        assert "La contraseña es igual a la anterior" in response.json()[
            'detail']['msg']
        
def test_user_detail_id():
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    id_user = 'user_saturnina:duarv161uh97q49gus2r'
    response = client.get(f'/api/v1/user/{id_user}',headers=header)
    
    assert response.status_code == 202
    assert "nombre" in response.json()['detail']
    assert "apellido" in response.json()['detail']
    assert "telefono" in response.json()['detail']
    assert "email" in response.json()['detail']
    assert "id" in response.json()['detail']

def test_user_update():
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    id_user = 'user_saturnina:duarv161uh97q49gus2r'
    payload = {
        "nombre": "Sebastian",
        "apellido": "Lucero",
        "telefono": "0990095963",
        "email": "sebastian2405lucero@hotmail.com"
    }
    response = client.put(f'/api/v1/user/{id_user}',headers=header,json=payload)
    assert response.status_code == 202
    assert "Datos actualizados correctamente" in response.json()["detail"]['msg']

def test_order():
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    id_user = 'user_saturnina:duarv161uh97q49gus2r'
    response = client.get(f'/api/v1/order/{id_user}',headers=header)
    if response.status_code == 202:
        assert "id_orden" in response.json()['detail'][0]['result'][0]
    elif response.status_code == 404:
        assert 'No tienes ningún pedido' in response.json()['detail']['msg']
def test_create_order():
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    transfer_image_file = open("C:/Users/sebas/Downloads/icon-foreground.png", "rb")

    payload = FormData(
        data='{"user_id": "user_saturnina:duarv161uh97q49gus2r", "price_order": 12.5, "products": [{"id_producto": "product:bm1s2kehfff6s2prcxih", "cantidad": 1}, {"id_producto": "product:bm1s2kehfff6s2prcxih", "cantidad": 3}], "nombre": "David", "apellido": "Basantes", "direccion": "La magdalena", "email": "sebastian2405lucero@hotmail.com", "telefono": "090095964", "descripcion": "Me gustaria que fuera de color rojo y el bordado con una letra D"}',        
        file={"transfer_image": ("icon-foreground.png", transfer_image_file, "image/png"), 'type':'image/png'}
        
    )
    
    response = client.post("/api/v1/order",headers=header,data=payload)
    print(response.json())
    assert response.status_code == 200