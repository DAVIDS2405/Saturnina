@router.get("/products")
async def Obtener_Productos():
    response = await admin_controller.Get_products()
    return response


@router.get("/products/{id_products}")
async def Obtener_Productos(id_products: str):
    response = await admin_controller.Get_one_products(id_products)
    return response


@router.post("/products", dependencies=[Depends(JWTBearer)])
async def Crear_Producto(token: Request, imagen_producto: list[UploadFile], data: Products = Body(),):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await admin_controller.Create_products(data, imagen_producto)
    return response


@router.put("/products/{id_product}", dependencies=[Depends(JWTBearer)])
async def Actualizar_producto(id_product: str, token: Request, imagen_producto: list[UploadFile] = File(None), data: Products = Body(...)):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await admin_controller.Update_products(id_product, data, imagen_producto)
    return response


@router.delete("/products/{id_product}", dependencies=[Depends(JWTBearer)])
async def Eliminar_Producto(id_product: str, token: Request):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await admin_controller.Delete_products(id_product)
    return response
