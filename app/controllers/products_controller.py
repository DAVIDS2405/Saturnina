async def Get_products():
    User_Db = await Connection()
    products_list = await User_Db.select("product")

    if not products_list:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "No existe ningún producto"})

    await User_Db.close()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail=products_list)


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


async def Create_products(data, imagen_producto):
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

    for imagen in imagen_producto:
        if not await is_image(imagen):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                                "msg": "Unicamente las extensiones de tipo jpg, jpeg, png y webp están permitidos, si tu error no es ese revisa tu formato puede que este dañado  "})

    if not category:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Esta categoría no existe"})

    for products in products_list:
        if products.get("name") == nombre_producto:
            await User_Db.close()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                                "msg": "Este producto ya existe"})
    cloudinary_data = []

    for imagen in imagen_producto:
        upload_cloudinary = await Upload_image(imagen.file)
        cloudinary_key = {"public_id", "secure_url"}
        data_cloudinary_filtered = {
            key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
        cloudinary_data.append(data_cloudinary_filtered)

    data_product = {"name": nombre_producto, "category": id_categoria,
                    "descripcion": data.descripcion, "precio": data.precio, "imagen": cloudinary_data, "tallas": data.tallas, "colores": data.colores}

    await User_Db.create("product", data_product)
    await User_Db.close()
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail=data_product)


async def Update_products(id_product, data, imagen_producto):
    User_Db = await Connection()
    category = await User_Db.select(data.id_categoria)
    check_product = await User_Db.select(id_product)

    async def is_image(file) -> bool:
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension in allowed_extensions:
            return True

        return False

    if imagen_producto:
        for imagen in imagen_producto:
            if not await is_image(imagen):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                                    "msg": "Unicamente las extensiones de tipo jpg, jpeg, png y webp están permitidos "})

    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "Este producto no existe"})

    if not category:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Esta categoría no existe"})

    if imagen_producto:
        cloudinary_data = []
        for imagen in imagen_producto:
            public_ids = [item['public_id']
                          for item in check_product.get("imagen")]
            for public_id in public_ids:
                await Delete_image(public_id)
            upload_cloudinary = await Upload_image(imagen.file)
            cloudinary_key = {"public_id", "secure_url"}
            data_cloudinary_filtered = {
                key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
            cloudinary_data.append(data_cloudinary_filtered)

        await User_Db.query('update ($id) merge {"name":($new_name_product),"precio":($new_price),"descripcion":($new_descripcion),"category":($new_category),"imagen":($new_image),"colores":($colores_new),"tallas":($new_tallas)};', {"id": id_product, "new_name_product": data.nombre_producto, "new_price": data.precio, "new_descripcion": data.descripcion, "new_category": data.id_categoria, "new_image": cloudinary_data, "new_tallas": data.tallas, "colores_new": data.colores})
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                            "msg": "Tu product.o se ha actualizado"})
    await User_Db.query('update ($id) merge {"name":($new_name_product),"precio":($new_price),"descripcion":($new_descripcion),"category":($new_category),"colores":($colores_new),"tallas":($new_tallas)};', {"id": id_product, "new_name_product": data.nombre_producto, "new_price": data.precio, "new_descripcion": data.descripcion, "new_category": data.id_categoria, "new_tallas": data.tallas, "colores_new": data.colores})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                        "msg": "Tu producto se ha actualizado"})


async def Delete_products(id_product):
    User_Db = await Connection()
    check_product = await User_Db.select(id_product)
    check_pedidos = await User_Db.select("order_detail")

    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "Este producto no existe"})
    check = True

    for product in check_pedidos:
        if product.get("status") != "Finalizado" and product.get("id_producto") == id_product:
            check = False
            break

    if check == False:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                            "msg": "necesitas primero poner en 'Finalizado' todas los pedidos que contengan este producto"})

    for imagen in check_product.get("imagen"):
        await Delete_image(imagen.get("public_id"))

    await User_Db.delete(id_product)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                        "msg": "Tu producto se ha eliminado"})
