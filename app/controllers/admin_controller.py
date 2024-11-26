from config.cloudinary_config import Upload_image, Delete_image
from models.admin_model import Category, Order_update_status, Products, tallas_productos
from fastapi import HTTPException, status


async def getAllOrders():
    User_Db = await Connection()

    all_orders = await User_Db.query("select *, id_producto.*,id_orden.* from order_detail fetch product, order;")

    if not all_orders[0]['result']:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "No tienes ningún pedido"})

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail=all_orders)


async def updateOrderStatus(id_orden_detail, data):
    UserDb = await Connection()
    check_id_orden_detail = await UserDb.select(id_orden_detail)

    if not check_id_orden_detail:
        await UserDb.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "No existe este detalle de orden"})

    await UserDb.query('update ($id) merge {"status":($new_status),"descripcion":($new_description)};', {"id": id_orden_detail, "new_status": data.status_order, "new_description": data.descripcion})
    await UserDb.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "El estado se actualizo con éxito"})


async def DeleteComments(id_coment):
    User_Db = await Connection()

    check_comment = await User_Db.select(id_coment)

    if not check_comment:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "Este comentario no existe"})

    await User_Db.delete(check_comment.get("id"))
    await User_Db.close()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail={"msg": "Este comentario se ha eliminado"})


async def DeleteGeneralComments(id_coment):
    User_Db = await Connection()

    check_comment = await User_Db.select(id_coment)

    if not check_comment:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "Este comentario no existe"})

    await User_Db.delete(check_comment.get("id"))
    await User_Db.close()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail={"msg": "Este comentario se ha eliminado"})
