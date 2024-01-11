import os
from fastapi.datastructures import FormData
from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_main():
    response = client.get('/')
    assert response.status_code == 200
    
def test_admin_login():
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
       
def test_delete_comments():
    id_comment = 'comments:2tqxo62sgkj8nml69zmd'
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    
    response = client.delete(f'api/v1/comments/{id_comment}', headers=header)
    
    if response.status_code == 202:
        assert "Este comentario se ha eliminado" in response.json()['detail']['msg']
        
    elif response.status_code == 404:
        assert "Este comentario no existe" in response.json()[
            'detail']['msg']

def test_category ():
    response = client.get('/api/v1/category')
    
    if response.status_code == 404:
        assert "No existe ninguna categoría" in response.json()['detail']['msg']
        
    if response.status_code == 202:
        assert "name" in response.json()['detail'][0]

def test_create_category():
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Reparación de ropa"
    }
    response = client.post('/api/v1/category',headers=header,json=payload)
    
    if response.status_code == 400:
        assert "Esta categoría ya existe" in response.json()['detail']['msg']
        
    elif response.status_code == 201:
        assert "Categoría creada con éxito" in response.json()['detail']['msg']
        
def test_update_category():
    id_category = 'category:m090ohysn991cam0dgjy'
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Reparación de ropa"
    }
    
    response = client.put(f'/api/v1/category/{id_category}',headers=header,json=payload)
    
    if response.status_code == 400:
        assert "No puede ser igual al nombre que ya posee" in response.json()['detail']['msg']
        
    elif response.status_code == 400:
        assert "Este nombre de categoría ya existe en otra categoría" in response.json()[
            'detail']['msg']
        
    elif response.status_code == 422:
        assert "No existe esta categoría" in response.json()[
            'detail']['msg']
    
    elif response.status_code == 200:
        assert "Categoría actualizada" in response.json()[
            'detail']['msg']
        
def test_delete_category():
    id_category = 'category:m090ohysn991cam0dgjy'
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    response = client.delete(f'/api/v1/category/{id_category}', headers=header)
    
    if response.status_code == 200:
        assert "La categoría selecciona se ha eliminado con éxito" in response.json()[
            'detail']['msg']
    elif response.status_code == 422:
        assert "No existe esta categoría" in response.json()[
            'detail']['msg']
    elif response.status_code == 403:
        assert "Existen productos ligados a esta categoría" in response.json()[
            'detail']['msg']
        
def test_products():
    
    response = client.get('/api/v1/products')

    if response.status_code == 404:
        assert "No existe ningún producto" in response.json()[
            'detail']['msg']

    if response.status_code == 202:
        assert "id" in response.json()['detail'][0]
  

def test_create_products():
    
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}",
              " Content-Type": "multipart/form-data"}
    image_paths = [
        "C:/Users/sebas/Downloads/icon-foreground.png",
        "C:/Users/sebas/Downloads/Splash.png",
    ]
    files = [('imagen_producto', (os.path.basename(path), open(path, 'rb')))
             for path in image_paths]

    payload = FormData(
        data='{"nombre_producto": "test David","id_categoria": "category:zt97gfiw04qhkqugl3r2","descripcion": "Repara tu  gorra con lindos bordados","precio": 22.22,"tallas": [{"name": "Talla XL","status": true},{"name": "Talla L","status": true}],"colores": [{"name": "verde","status": true},{"name": "morado","status": true}]}'
    )

    response = client.post("/api/v1/products",headers=header,data=payload,files=files)
    if response.status_code == 202:
        assert "name" in response.json()['detail']
        
    elif response.status_code == 409:
        assert "Este producto ya existe" in response.json()['detail']['msg']

def  test_get_product():
    id_products = "product:kb60aa4uy6e7f88oo8ir"
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f'/api/v1/products/{id_products}',headers=header)
    
    if response.status_code == 202:
        assert "name" in response.json()['detail']
        
    elif response.status_code == 404:
        assert "No existe este producto" in response.json()['detail']['msg']
        
def test_put_product():
    id_product = 'product:yibkcmgrmzhvs0vyjvzk'
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}",
              " Content-Type": "multipart/form-data"}
    image_paths = [
        "C:/Users/sebas/Downloads/icon-foreground.png",
        "C:/Users/sebas/Downloads/Case_1.png",
    ]
    files = [('imagen_producto', (os.path.basename(path), open(path, 'rb')))
             for path in image_paths]

    payload = FormData(
        data='{"nombre_producto": "test David update","id_categoria": "category:zt97gfiw04qhkqugl3r2","descripcion": "Repara tu  gorra con lindos bordados","precio": 22.22,"tallas": [{"name": "Talla XL","status": true},{"name": "Talla L","status": true}],"colores": [{"name": "verde","status": true},{"name": "morado","status": true}]}'
    )
    response = client.put(f"/api/v1/products/{id_product}",headers=header,data=payload,files=files)
    
    if response.status_code == 404:
        assert "No existe este producto" in response.json()['detail']['msg']
        
    elif response.status_code == 202:
        assert "Tu producto se ha actualizado" in response.json()[
            'detail']['msg']
    

def test_delete_product():
    id_product = 'product:yibkcmgrmzhvs0vyjvzk'
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/v1/products/{id_product}",headers=header)
        
    if response.status_code == 404:
        assert "Este producto no existe" in response.json()['detail']['msg']
    elif response.status_code == 403:
        assert "necesitas primero poner en 'Cancelado' todas los pedidos que contengan este producto" in response.json()[
            'detail']['msg']
    elif response.status_code == 202:
        assert "Tu producto se ha eliminado" in response.json()[
            'detail']['msg']
def test_order():
    
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    
    response = client.get('/api/v1/orders',headers=header)
    
    if response.status_code == 404:
        assert "No tienes ningún pedido" in response.json()['detail']['msg']
        
    elif response.status_code == 200:
        assert "id" in response.json()['detail'][0]['result'][0]
        
def test_order_update():
    id_order_detail = "order_detail:au9sdaatcjfg2b4qqjx2"
    token = get_auth_token()
    header = {"Authorization": f"Bearer {token}"}
    payload ={
  "status_order": "Reenviar Transferencia"
}
    response = client.put(f'/api/v1/orders/{id_order_detail}', headers=header,json=payload)
    
    if response.status_code == 400:
        assert "No existe este detalle de orden" in response.json()['detail']['msg']
    elif response.status_code == 200:
        assert "El estado se actualizo con éxito" in response.json()[
            'detail']['msg']
