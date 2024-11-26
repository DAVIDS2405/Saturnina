@router.get("/comments")
async def Todos_comentarios():
    response = await user_controller.Get_comments()
    return response


@router.get("/comments/{user_id}", dependencies=[Depends(JWTBearerCookie)])
async def Todos_comentarios_usuario(user_id: str, token: Request):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Get_comments_user(user_id)
    return response


@router.post("/comments", dependencies=[Depends(JWTBearerCookie)])
async def Crear_comentario_producto(token: Request, data: user_model.Comment_product = Body(examples=[{
    "descripcion": "Me gusto mucho la decoracion les recomiendo",
    "user_id": "user_saturnina:duarv161uh97q49gus2r",
    "id_producto": "product:56btylsbf10jruqzh0da",
    "calificacion": 2
}])):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Create_comments(data)
    return response


@router.put("/comments/{id_comment}", dependencies=[Depends(JWTBearerCookie)])
async def Actualizar_comentario_producto(id_comment: str, token: Request, data: user_model.Comment_product = Body(examples=[{
    "descripcion": "Me gusto mucho la decoracion les recomiendo",
    "user_id": "user_saturnina:duarv161uh97q49gus2r",
    "id_producto": "product:56btylsbf10jruqzh0da",
    "calificacion": 2
}])):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Update_comments(data, id_comment)
    return response


@router.post("/comments-general", dependencies=[Depends(JWTBearerCookie)])
async def Crear_comentario_general(token: Request, data: user_model.Comment_general = Body(examples=[{
    "descripcion": "Me gusto mucho la decoración les recomiendo",
    "user_id": "user_saturnina:duarv161uh97q49gus2r",
    "calificacion": 2
}])):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Create_comments_general(data)
    return response


@router.put("/comments-general/{id_comment}", dependencies=[Depends(JWTBearer)])
async def Actualizar_comentario_general(id_comment: str, token: Request, data: user_model.Comment_general = Body(examples=[{
    "descripcion": "Me gusto mucho la decoración les recomiendo",
    "user_id": "user_saturnina:duarv161uh97q49gus2r",
    "calificacion": 2
}])):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Update_comments_general(data, id_comment)
    return response


@router.get("/comments-general/{user_id}", dependencies=[Depends(JWTBearer)])
async def Todos_comentarios_generales_usuario(user_id: str, token: Request):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Get_comments_general_user(user_id)
    return response


@router.get("/comments-general")
async def Todos_comentarios_generales():
    response = await user_controller.Get_comments_general()
    return response
