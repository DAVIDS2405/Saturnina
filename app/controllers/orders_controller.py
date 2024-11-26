from datetime import datetime

from fastapi import HTTPException, status

from app.config.cloudinary_config import Upload_image


async def View_order(id_user):
    User_Db = await Connection()

    all_orders = await User_Db.query("select *, id_producto.*,id_orden.* from order_detail where id_orden.user_id = ($id_user) fetch product, order;", {"id_user": id_user})

    if not all_orders[0]['result']:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "No tienes ningún pedido"})

    await User_Db.close()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail=all_orders)


async def Create_order(data, transfer_image):

    User_Db = await Connection()
    found = False

    if not await is_image(transfer_image):
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                            "msg": "Unicamente las extensiones de tipo jpg, jpeg, png y webp están permitidos "})

    db_products = await User_Db.select("product")

    if not db_products:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                            "msg": "No existe este producto"})

    for value in data.products:
        found = False
        for check_product in db_products:
            if check_product.get("id") == value.id_producto:
                found = True

                if str(value.talla) != "None":
                    if not check_product.get("tallas"):
                        await User_Db.close()
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                            "msg": f"No existe ninguna talla para este producto {check_product.get('name')}"})
                    if str(value.talla.value) not in [t.get("name") for t in check_product.get("tallas", [])]:
                        await User_Db.close()
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                            "msg": f"No existe esta talla para el producto {check_product.get('name')}"})
                if str(value.color) != "None":
                    if not check_product.get("colores"):
                        await User_Db.close()
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": f"No hay ningún color asignado a este producto {check_product.get('name')}"})
                    if str(value.color) not in [c.get("name") for c in check_product.get("colores", [])]:
                        await User_Db.close()
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": f"En el  productos {check_product.get('name')} el color esta mal"})
        if not found:
            found = False
            break
        else:
            found = True

    if not found:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "El id de alguno de los productos esta mal intenta de nuevo"})

    db_user = await User_Db.select(data.user_id)
    if not db_user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "Este usuario no existe"})

    order_list = dict(data)
    data_order_keys = {"nombre", "apellido",
                       "telefono", "direccion", "user_id", "email", "price_order", "descripcion"}

    data_order_filtered = {key: order_list[key]
                           for key in data_order_keys if key in order_list}

    upload_cloudinary = await Upload_image(transfer_image.file)
    cloudinary_key = {"public_id", "secure_url"}
    data_cloudinary_filtered = {
        key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}

    cloudinary_image = {"image_transaccion": data_cloudinary_filtered}
    data_order_filtered.update(cloudinary_image)

    id_order = await User_Db.create("order", data_order_filtered)
    for id_order_db in id_order:
        if (id_order_db.get("id")):
            id_order_db = id_order_db

    for product in data.products:
        status_default = {"status": "Pendiente",
                          "descripcion": "se esta verificando tus datos"}
        fecha_actual = datetime.now()
        fecha_actual = str(fecha_actual)
        date_now = {"fecha": fecha_actual}
        id_order_key = {"id_orden": id_order_db.get("id")}
        product = dict(product)
        product.update(id_order_key)
        product.update(date_now)
        product.update(status_default)
        await User_Db.create("order_detail", product)

    fecha_actual = datetime.now()
    fecha_actual = str(fecha_actual)
    await User_Db.query('update ($id) merge {"order_date": ($now_date)};', {"id": id_order_db.get("id"), "now_date": fecha_actual})

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail={"msg": "Pedido realizado"})


async def Update_order(id_order, data, transfer_image):
    User_Db = await Connection()
    fecha_actual = datetime.now()
    fecha_actual = str(fecha_actual)

    async def is_image(file) -> bool:
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension in allowed_extensions:
            return True

        return False

    if transfer_image:
        if not await is_image(transfer_image):
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                                "msg": "Unicamente las extensiones de tipo jpg, jpeg, png y webp están permitidos "})

    check_order = await User_Db.query("select * from order where id = ($id_order_db)", {"id_order_db": id_order})

    if not check_order:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "el id de la orden es incorrecto"})

    print(check_order[0].get('result')[0])
    if transfer_image:

        await Delete_image(check_order[0].get('result')[0].get("image_transaccion").get("public_id"))
        upload_cloudinary = await Upload_image(transfer_image.file)
        cloudinary_key = {"public_id", "secure_url"}
        data_cloudinary_filtered = {
            key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
        await User_Db.query('update ($id) merge {"apellido":($new_apellido),"nombre":($new_name),"telefono":($new_phone),"direccion":($new_address),"image_transaccion":($new_image),"order_date":($new_date),"email":($new_email)};', {"id": check_order[0].get('result')[0].get('id'), "new_apellido": data.apellido, "new_name": data.nombre, "new_phone": data.telefono, "new_address": data.direccion, "new_email": data.email, "new_image": data_cloudinary_filtered, "new_date": fecha_actual})
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
            "msg": "Tu pedido fue actualizado"})

    await User_Db.query('update ($id) merge {"apellido":($new_apellido),"nombre":($new_name),"telefono":($new_phone),"direccion":($new_address),"order_date":($new_date),"email":($new_email)};', {"id": check_order[0].get('result')[0].get('id'), "new_apellido": data.apellido, "new_name": data.nombre, "new_phone": data.telefono, "new_address": data.direccion, "new_email": data.email, "new_date": fecha_actual})

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                        "msg": "Tu pedido fue actualizado"})
