from config.cloudinary_config import Upload_image,Delete_image
from  models.admin_model import Category, Order_update_status
from database.database import Connection
from fastapi import HTTPException,status



async def List_category():
    User_Db = await Connection()
    category_list = await User_Db.select("category")



    if not category_list:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"No existe ninguna categoría"})
    

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=category_list)

async def Create_category(data):
    category_name = data.name
    User_Db = await Connection()
    
    check_category = await User_Db.select("category")
    
    for category in check_category:
        if(category.get("name") == category_name):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta categoría ya existe"})
            
    new_category = Category(**data.dict())
    await User_Db.create("category",new_category)
    await User_Db.close()
    
    raise HTTPException(status_code=status.HTTP_201_CREATED,detail={"msg":"Categoría creada con éxito"})

async def Update_category(id_category,data):
    category_name = data.name
    User_Db = await Connection()
    check_category = await User_Db.select(id_category)
    
    
    for category in check_category:
        if(category.get("name") == category_name):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Necesitas darle un nombre diferente"})

        
    if not check_category:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"No existe esta categoría"})
        
        
    await User_Db.query('update ($id) merge {"name":($new_name_category)};' ,{"id":id_category, "new_name_category":category_name})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Categoría actualizada"})

async def Delete_category(id_category):
    User_Db = await Connection()
    check_id_category = await User_Db.select("category")
    check_products = await User_Db.select("product")
    
    for category in check_id_category:
        if category.get("id") == id_category:
            category = category
            break
        
    for product in check_products:
        if(product.get("category") == id_category):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"msg":"Existen productos ligados a esta categoría"})
    
    if category is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"No hay ninguna categoría"})
    
    if category.get("id") != id_category:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"Esta categoría no existe"})        

    
    await User_Db.delete(id_category)
    await User_Db.close()
    raise HTTPException(status_code = status.HTTP_200_OK,detail={"msg":"La categoría selecciona se ha eliminado con éxito"})


async def Get_products():
    User_Db = await Connection()
    products_list = await User_Db.select("product")

    if not products_list:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"No existe ningún producto"})
    

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=products_list)


async def Get_one_products(id_product):
    User_Db = await Connection()
    products_list = await User_Db.select(id_product)

    if not products_list:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "No existe este producto"})

    await User_Db.close()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail=products_list)

async def Create_products(data,imagen_producto):
    id_categoria = data.id_categoria
    nombre_producto = data.nombre_producto
    async def is_image(file) -> bool:
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension in allowed_extensions:
            return True

        return False

    User_Db = await Connection()
    products_list = await User_Db.select("product")
    category = await User_Db.select(id_categoria)
    
    if not await is_image(imagen_producto):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"Unicamente las extensiones de tipo jpg, jpeg, png y webp están permitidos "})

    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Esta categoría no existe"})


    for products in products_list:
        if products.get("name") == nombre_producto:
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg":"Este producto ya existe"})
        
    upload_cloudinary = await Upload_image(imagen_producto.file)
    cloudinary_key = {"public_id","secure_url"}
    data_cloudinary_filtered = {key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
    
    data_product = {"name": nombre_producto, "category": id_categoria,
                    "descripcion": data.descripcion, "precio": data.precio, "imagen": data_cloudinary_filtered}

    await User_Db.create("product",data_product)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=data_product)

async def Update_products(id_product,data,imagen_producto):
    User_Db = await Connection()
    category = await User_Db.select(data.id_categoria)
    check_product = await User_Db.select(id_product)

    async def is_image(file) -> bool:
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension in allowed_extensions:
            return True

        return False

    if not await is_image(imagen_producto):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                            "msg": "Unicamente las extensiones de tipo jpg, jpeg, png y webp están permitidos "})
        
    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"Este producto no existe"}) 
    

    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Esta categoría no existe"})
        
    await Delete_image(check_product.get("imagen").get("public_id"))
    upload_cloudinary = await Upload_image(imagen_producto.file)
    cloudinary_key = {"public_id","secure_url"}
    data_cloudinary_filtered = {key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
    
    await User_Db.query('update ($id) merge {"name":($new_name_product),"precio":($new_price),"descripcion":($new_descripcion),"category":($new_category),"imagen":($new_image)};' ,{"id":id_product, "new_name_product":data.nombre_producto,"new_price":data.precio,"new_descripcion":data.descripcion,"new_category":data.id_categoria,"new_image":data_cloudinary_filtered})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Tu producto se ha actualizado"})

async def Delete_products(id_product):
    User_Db = await Connection()
    check_product = await User_Db.select(id_product)
    check_pedidos = await User_Db.select("order_detail")
    
    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"Este producto no existe"}) 
    check = True

    for product in check_pedidos:
        if product.get("status") != "Cancelado" and product.get("id_producto") == id_product:
            check = False
            break
        
    if check == False:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"msg":"necesitas primero poner en cancelada todas los pedidos que contengan este producto"})
    
    await Delete_image(check_product.get("imagen").get("public_id"))
    await User_Db.delete(id_product)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Tu producto se ha eliminado"})

async def Get_all_orders():
    User_Db = await Connection()

    all_orders = await User_Db.query("select *, id_producto.*,id_orden.* from order_detail fetch product, order;")

    if not all_orders[0]['result']:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "No tienes ningún pedido"})

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_302_FOUND, detail=all_orders)
    
async def Update_order_status(id_orden_detail,data):
    UserDb = await Connection()
    check_id_orden_detail = await UserDb.select(id_orden_detail)
    
    if not check_id_orden_detail:
        await UserDb.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"No existe este detalle de orden"})
    
    await UserDb.query('update ($id) merge {"status":($new_status)};', {"id": id_orden_detail, "new_status": data.status_order})
    await UserDb.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "EL estado se actualizo con exito"})
    
async def Get_comments():
    User_Db = await Connection()
    all_coments = await User_Db.select("comments")
    
    if not all_coments:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"No existe ninguna categoria"})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=all_coments)

async def Delete_comments(id_coment):
    User_Db = await Connection()
    


    
    

    
    