from fastapi import HTTPException, status
from prisma import Prisma


async def get_all():
    db_connection = Prisma()
    category_list = await User_Db.select("category")

    if not category_list:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "No existe ninguna categoría"})

    await User_Db.close()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail=category_list)


async def create(data):
    db_connection = Prisma()

    check_category = await User_Db.select("category")

    for category in check_category:
        if (category.get("name") == category_name):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                "msg": "Esta categoría ya existe"})

    new_category = Category(**data.dict())
    await User_Db.create("category", new_category)
    await User_Db.close()

    raise HTTPException(status_code=status.HTTP_201_CREATED, detail={
                        "msg": "Categoría creada con éxito"})


async def update(id_category, data):
    db_connection = Prisma()
    category_name = data.name
    check_category = await User_Db.select(id_category)
    all_categorys = await User_Db.select("category")

    if not check_category:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No existe esta categoría"})

    if (check_category.get("name") == category_name):
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "No puede ser igual al nombre que ya posee"})

    for all_category in all_categorys:
        if (all_category.get("name") == category_name):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                "msg": "Este nombre de categoría ya existe en otra categoría"})

    await User_Db.query('update ($id) merge {"name":($new_name_category)};', {"id": id_category, "new_name_category": category_name})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "Categoría actualizada"})


async def delete(id_category):
    db_connection = Prisma()
    check_id_category = await User_Db.select(id_category)
    check_products = await User_Db.select("product")

    if not check_id_category:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No existe esta categoría"})

    for product in check_products:
        if (product.get("category") == id_category):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                                "msg": "Existen productos ligados a esta categoría"})

    await User_Db.delete(id_category)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "La categoría selecciona se ha eliminado con éxito"})
