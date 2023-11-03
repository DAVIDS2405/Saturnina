import json
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


    
    