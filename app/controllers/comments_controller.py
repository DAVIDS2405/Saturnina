async def Create_comments(data):
    User_Db = await Connection()
    comments_product = await User_Db.select("comments")
    check_user = await User_Db.select(data.user_id)
    check_product = await User_Db.select(data.id_producto)
    check_order_detail = await User_Db.query("select *, id_orden.* from order_detail where id_orden.user_id = ($id_user)", {"id_user": data.user_id})

    if not check_user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No se encuentra el Usuario"})
    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No se encuentra el producto"})

    if comments_product is not None:
        for comment in comments_product:
            if (comment.get("user_id") == data.user_id):
                if (comment.get("id_producto") == data.id_producto):
                    await User_Db.close()
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                        "msg": "No puedes realizar mas comentarios de este producto"})

    for orders in check_order_detail:
        if not orders.get('result'):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                                'msg': "No tienes ningún pedido realizado"})
        for productos in orders.get("result"):

            if (productos['id_producto'] == data.id_producto and productos['status'] == "Finalizado") == True:
                new_comment = Comment_product(**data.dict())
                await User_Db.create("comments", new_comment)
                await User_Db.close()
                raise HTTPException(status_code=status.HTTP_201_CREATED, detail={
                    "msg": "Tu comentario se ha creado"})

            elif ((productos['id_producto'] == data.id_producto and productos['status'] != "Finalizado") == True):
                await User_Db.close()
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                    "msg": "Necesitas esperar a que tu compra este en finalizada"})
            elif (productos['id_producto'] != data.id_producto):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                    'msg': "Revisa tus datos este producto no se encuentra en tu lista de pedidos"})


async def Get_comments():
    User_Db = await Connection()

    comments = await User_Db.query('select user_id.nombre, user_id.apellido,user_id.id,id,id_producto,calificacion,descripcion from comments fetch user_saturnina,product')

    if not comments:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No hay comentarios"})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=comments)


async def Get_comments_user(id_user):
    User_Db = await Connection()
    comments = await User_Db.query("select user_id.nombre, user_id.apellido,user_id.id,id,id_producto,calificacion,descripcion from comments where user_id = ($id_usuario) fetch user_saturnina,product", {"id_usuario": id_user})

    if not comments:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No hay comentarios"})

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=comments)


async def Update_comments(data, id_comment):
    User_Db = await Connection()
    check_comment = await User_Db.select(id_comment)
    check_user = await User_Db.select(data.user_id)
    check_product = await User_Db.select(data.id_producto)
    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "msg": "Este producto no existe"})

    if not check_user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "msg": "Este usuario no existe"})
    if not check_comment:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "No se encuentra este comentario"})

    if check_comment.get("user_id") != data.user_id:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "msg": "Este no es tu comentario"})
    if check_comment.get('id_producto') != data.id_producto:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "msg": "Este producto no le corresponde a este comentario"})

    await User_Db.update(id_comment, data)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                        "msg": "Tu comentario se ha actualizado"})


async def Create_comments_general(data):
    User_Db = await Connection()
    comments = await User_Db.select("comments_general")
    check_user = await User_Db.select(data.user_id)
    check_order_detail = await User_Db.query("select *, id_orden.* from order_detail where id_orden.user_id = ($id_user)", {"id_user": data.user_id})

    if not check_user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No se encuentra el Usuario"})

    if comments is not None:
        for comment in comments:
            if (comment.get("user_id") == data.user_id):
                await User_Db.close()
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                    "msg": "No puedes realizar mas comentarios"})

    created_comments = False
    for orders in check_order_detail:
        for comment in orders.get("result"):
            if (comment and comment['status'] == "Finalizado") == True:
                new_comment = Comment_general(**data.dict())
                await User_Db.create("comments_general", new_comment)
                await User_Db.close()
                created_comments = True
                raise HTTPException(status_code=status.HTTP_201_CREATED, detail={
                    "msg": "Tu comentario se ha creado"})

    if created_comments == False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
            "msg": "Necesitas esperar a que tu compra esté finalizada o comprar algo"})


async def Update_comments_general(data, id_comment):
    User_Db = await Connection()
    check_comment = await User_Db.select(id_comment)
    check_user = await User_Db.select(data.user_id)

    if not check_user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "msg": "Este usuario no existe"})
    if not check_comment:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "No se encuentra este comentario"})

    if check_comment.get("user_id") != data.user_id:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "msg": "Este no es tu comentario"})

    await User_Db.update(id_comment, data)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                        "msg": "Tu comentario se ha actualizado"})


async def Get_comments_general():
    User_Db = await Connection()

    comments = await User_Db.query('select user_id.nombre, user_id.apellido,user_id.id,id,calificacion,descripcion from comments_general fetch user_saturnina,product')

    if not comments:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No hay comentarios"})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=comments)


async def Get_comments_general_user(id_user):
    User_Db = await Connection()
    comments = await User_Db.query("select user_id.nombre, user_id.apellido,user_id.id,id,calificacion,descripcion from comments_general where user_id = ($id_usuario) fetch user_saturnina,product", {"id_usuario": id_user})

    if not comments:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No hay comentarios"})

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=comments)
