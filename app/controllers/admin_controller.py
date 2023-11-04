from config.cloudinary_config import Upload_image,Delete_image
from models.category_products import Category
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
    check_category = await User_Db.select("category")
    
    
    for category in check_category:
        if(category.get("name") == category_name):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta categoría ya existe"})
        if(category.get("id")!=id_category):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"Esta categoría no existe"})
        
    if not check_category:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"No existe ninguna categoría"})
        
        
    await User_Db.query('update ($id) merge {"name":($new_name_category)};' ,{"id":id_category, "new_name_category":category_name})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Categoría actualizada"})

async def Delete_category(id_category):
    User_Db = await Connection()
    check_id_category = await User_Db.select("category")
    
    for category in check_id_category:
        if category.get("id") == id_category:
            category = category
            break
    
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

async def Create_products(nombre_producto,id_categoria,descripcion,precio,imagen_producto):
    
    async def is_image(file) -> bool:
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension in allowed_extensions:
            return True

        return False

    User_Db = await Connection()
    products_list = await User_Db.select("product")
    category_list = await User_Db.select("category")
    
    if not await is_image(imagen_producto):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"Unicamente las extensiones de tipo jpg, jpeg, png y webp están permitidos "})

    for category in category_list:
        if(category.get("id") != id_categoria):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta categoría no existe"})

    for products in products_list:
        print(products.get("name") == nombre_producto)
        if products.get("name") == nombre_producto:
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg":"Este producto ya existe"})
        
    upload_cloudinary = await Upload_image(imagen_producto.file)
    cloudinary_key = {"public_id","secure_url"}
    data_cloudinary_filtered = {key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
    
    data_product = {"name": nombre_producto, "category":id_categoria, "descripcion":descripcion, "precio":precio, "imagen":data_cloudinary_filtered}

    await User_Db.create("product",data_product)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=data_product)

async def Update_products(id_product,nombre_producto,id_categoria,descripcion,precio,imagen_producto):
    User_Db = await Connection()
    category_list = await User_Db.select("category")
    check_product = await User_Db.select(id_product)
    
    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"Este producto no existe"}) 
    
    for category in category_list:
        if(category.get("id") != id_categoria):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta categoría no existe"})
    
    await Delete_image(check_product.get("imagen").get("public_id"))
    upload_cloudinary = await Upload_image(imagen_producto.file)
    cloudinary_key = {"public_id","secure_url"}
    data_cloudinary_filtered = {key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
    
    await User_Db.query('update ($id) merge {"name":($new_name_product),"precio":($new_price),"descripcion":($new_descripcion),"category":($new_category),"imagen":($new_image)};' ,{"id":id_product, "new_name_product":nombre_producto,"new_price":precio,"new_descripcion":descripcion,"new_category":id_categoria,"new_image":data_cloudinary_filtered})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Tu producto se ha actualizado"})

async def Delete_products(id_product):
    User_Db = await Connection()
    check_product = await User_Db.select(id_product)
    
    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"Este producto no existe"}) 


    await Delete_image(check_product.get("imagen").get("public_id"))
    await User_Db.delete(id_product)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Tu producto se ha eliminado"})

    


    
    
    
    

    
    