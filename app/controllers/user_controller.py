from datetime import datetime
from fastapi import HTTPException,status
from config.cloudinary_config import Delete_image, Upload_image
from config.smtp_config import smtp_config
from database.database import Connection
from helpers.jwt_helper import decodeJWT, signJWT
from models.user_model import Comment_product, Recover_Pass, User_DB, User_Recover_Password
    
async def Login(data):
    
    email = data.email
    password = data.password
    
        
    user = None
    User_Db = await Connection()
    Check_user = await User_Db.select("user_saturnina")
    
    
    for user in Check_user:
        if(user.get("email")==email):
            user = user
            break
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"Usuario no registrado"})
     
    if user.get("email") != email:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"El correo es incorrecto"})
    
    if user.get("confirmEmail") is not True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Necesitas activar tu cuenta revisa tu correo para confirmar"})
    
    data_user_keys = {"nombre", "apellido", "telefono", "dirrecion", "id", "email", "token","rol"}
    data_user_filtered = {key: user[key] for key in data_user_keys if key in user}
    data_user_filtered['token'] = signJWT(data_user_filtered['id'],user.get("rol")) 
    
    check_password = User_DB.verify_password(plain_password=password,password_bd=user.get("password"))
    
    if(check_password is not True):
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"La contraseña es incorrecta intenta de nuevo"})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=data_user_filtered)
    
    
async def Register(data): 
  
    email = data.email
    User_Db = await Connection()
    Check_email = await User_Db.select("user_saturnina")
    user = None
    for user in Check_email:
         if(user["email"] == email):
             user = user
             await User_Db.close()
             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg":"Este email ya se encuentra en uso"})
    
    
    new_User = User_DB(**data.dict())
    new_User.password =  new_User.encrypt_password()
    
    token = new_User.generate_token()

    new_User = new_User.dict()
    new_User['password'] = new_User['password'].decode("utf-8")

    id_user = await User_Db.create("user_saturnina",new_User)
    for id_user_database in id_user:
        if(id_user_database.get("id")):
            id_user_database = id_user_database
            break
    
    await User_Db.query('update ($id) merge {"rol":rol:vuqn7k4vw0m1a3wt7fkb};' ,{"id":id_user_database.get("id")})
    await User_Db.close()
        
    email_sender = smtp_config()
    email_sender.send_user(user_mail=email,token=token) 
        
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail={'msg':"Revisa tu correo para activar tu cuenta"})

async def Check_email(data):
    
    User_Db = await Connection()
    
    token_user = await User_Db.select("user_saturnina")
    user = None
    
    for user in token_user:
        if(user.get("token") == data):
            user = user
            break
     
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta cuenta no existe"})
        
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"La cuenta ya ha sido confirmada"})

    elif user.get("token") != data:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Lo sentimos, no se puede validar la cuenta"})


    
    await User_Db.query('update ($id) merge {"token":null,"confirmEmail":true};' ,{"id":user.get("id")})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Ya puedes iniciar sesión"})
  

async def Recover_Password (data):
    email = data.email
    User_Db = await Connection()
    
    email_user_register = await User_Db.select("user_saturnina")
    
    user = None
    
    for user in email_user_register:
        if(user.get("email") == email):
            user = user
            break
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"Usuario no registrado"})
    
    if user.get('confirmEmail') is not True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"Necesita activar su cuenta"})
    
    new_User = Recover_Pass(**user)
    token = new_User.generate_token()

    await User_Db.query('update ($id) merge {"token":($token_new),"confirmEmail":false};' ,{"id":user.get("id"),"token_new":token})
    await User_Db.close()

    email_sender = smtp_config()
    email_sender.Recover_password(user_mail=email,token=token)
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail={'msg':"Revisa tu correo para recuperar tu contraseña"})

async def Check_token(data):
    
    User_Db = await Connection()
    
    token_user = await User_Db.select("user_saturnina")
    user = None
    
    for user in token_user:
        if(user.get("token") == data):
            user = user
            break
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta cuenta no existe"})
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"La cuenta ya ha sido confirmada"})

    elif user.get("token") != data:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Lo sentimos, no se puede validar la cuenta"})
    
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Token confirmado ya puedes crear tu nueva contraseña"})

async def New_password(token,data):
    new_password = data.new_password
    check_new_password = data.check_password
    User_Db = await Connection()
    user = None
    
    check_token = await User_Db.select("user_saturnina")

    if new_password.get_secret_value() != check_new_password.get_secret_value():
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"Las password no coinciden"})
    
    for user in check_token:
        if(user.get('token') == token):
            user = user
            break
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta cuenta no existe"})
    
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"La cuenta ya ha sido confirmada"})
    
    if user.get("token") != token:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Lo sentimos, no se puede validar la cuenta"})
    

    new_User = User_Recover_Password(**data.dict())
    
    new_User.new_password = new_User.encrypt_password()
    new_User = new_User.dict()
    new_User['new_password'] = new_User['new_password'].decode("utf-8")
    password = new_User['new_password']
    
    await User_Db.query('update ($id) merge {"token":null,"confirmEmail":true,"password":($password_new)};' ,{"id":user.get("id"),"password_new":password})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Tu contraseña a sido actualizada ya puedes iniciar sesión"})


async def User_profile(data):
    UserDb = await Connection()
    decode_token = await decodeJWT(data)
    check_user_db = await UserDb.select(decode_token.get("user_id"))

    if not check_user_db:
        await UserDb.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            "msg": "El usuario no existe"})
    
    data_user_keys = {"nombre", "apellido", "telefono", "email"}
    data_user_filtered = {key: check_user_db[key] for key in data_user_keys if key in check_user_db}
    await UserDb.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=data_user_filtered)

async def User_profile_actualizar_contrasenia(password,data):
    decode_token = await decodeJWT(data)
    new_password = password.new_password
    check_new_password = password.check_password
    id_user = decode_token.get('user_id')
    User_Db = await Connection()
    user_update_password = await User_Db.select(id_user)
    
    if not user_update_password:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"no se encuentra el Usuario"})
    
    if (new_password.get_secret_value() != check_new_password.get_secret_value()):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"Las password no coinciden"})
    
    if user_update_password is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"No existe este usuario"})
    
    new_User = User_Recover_Password(**password.dict())

    new_User.new_password = new_User.encrypt_password()
    new_User = new_User.dict()
    new_User['new_password'] = new_User['new_password'].decode("utf-8")
    password = new_User['new_password']
    
    check_password = User_DB.verify_password(plain_password=check_new_password,password_bd=user_update_password['password'])
    
    if check_password is  True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"La contraseña es igual a la anterior"})
    

    
    await User_Db.query('update ($id) merge {"password":($password_new)};' ,{"id":id_user,"password_new":password})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Tu contraseña a sido actualizada"})

async def User_detail(id):
    User_Db = await Connection()
    
    user = await User_Db.select(id)
    
    if not user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"no se encuentra el Usuario"})
    
    data_user_keys = {"nombre", "apellido", "telefono", "dirrecion", "id", "email"}
    data_user_filtered = {key: user[key] for key in data_user_keys if key in user}
    
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=data_user_filtered)

async def User_detail_Update(id,data):
    User_Db = await Connection()
    user = await User_Db.select(id)
        
    if not user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"no se encuentra el Usuario"})
    

    new_email_user = data.email
    new_telefono = data.telefono
    new_apellido = data.apellido
    new_nombre = data.nombre
    
    await User_Db.query('update ($id) merge {"nombre":($new_name),"apellido":($new_lastname),"telefono":($new_phone),"email":($new_email)};' ,{"id":user.get("id"),"new_name":new_nombre,"new_lastname":new_apellido,"new_phone":new_telefono,"new_email":new_email_user})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Datos actualizados correctamente"})


async def View_order(id_user):
    User_Db= await Connection()
    
    all_orders = await User_Db.query("select *, id_producto.*,id_orden.* from order_detail where id_orden.user_id = ($id_user) fetch product, order;", {"id_user": id_user})
    
    if not all_orders[0]['result'] :
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"No tienes ningún pedido"})
    
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=all_orders)

async def Create_order(data, transfer_image):
    
    User_Db = await Connection()
    found = False
    
    async def is_image(file) -> bool:
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension in allowed_extensions:
            return True

        return False
    

    
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
                    if str(value.color)  not in [c.get("name") for c in check_product.get("colores", [])]:
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg":"El id de alguno de los productos esta mal intenta de nuevo"})
    
    db_user = await User_Db.select(data.user_id)
    if not db_user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg":"Este usuario no existe"})
    
    order_list = dict(data)
    data_order_keys = {"nombre", "apellido",
                       "telefono", "direccion", "user_id", "email", "price_order", "descripcion"}
    
    data_order_filtered = {key: order_list[key]
                           for key in data_order_keys if key in order_list}
    
    upload_cloudinary = await Upload_image(transfer_image.file)
    cloudinary_key = {"public_id","secure_url"}
    data_cloudinary_filtered = {key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
    
    cloudinary_image = {"image_transaccion": data_cloudinary_filtered}
    data_order_filtered.update(cloudinary_image)

    id_order = await User_Db.create("order", data_order_filtered)
    for id_order_db in id_order:
        if (id_order_db.get("id")):
            id_order_db = id_order_db
            
            
    for product in data.products:
        status_default = {"status": "Pendiente","descripcion":"se esta verificando tus datos"}
        fecha_actual = datetime.now()
        fecha_actual = str(fecha_actual)
        date_now = {"fecha":fecha_actual}
        id_order_key = {"id_orden": id_order_db.get("id")}
        product = dict(product)
        product.update(id_order_key)
        product.update(date_now)
        product.update(status_default)
        await User_Db.create("order_detail",product)
           
    fecha_actual = datetime.now()
    fecha_actual = str(fecha_actual)
    await User_Db.query('update ($id) merge {"order_date": ($now_date)};', {"id": id_order_db.get("id"), "now_date": fecha_actual})
    
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_201_CREATED,detail={"msg":"Pedido realizado"})


async def Update_order(id_order,data,transfer_image):
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



    
    check_order = await User_Db.select(id_order)
    
    if not check_order:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"msg":"el id de la orden es incorrecto"})
    
    if transfer_image:
        await Delete_image(check_order.get("image_transaccion").get("public_id"))
        upload_cloudinary = await Upload_image(transfer_image.file)
        cloudinary_key = {"public_id", "secure_url"}
        data_cloudinary_filtered = {
            key: upload_cloudinary[key] for key in cloudinary_key if key in upload_cloudinary}
        await User_Db.query('update ($id) merge {"apellido":($new_apellido),"nombre":($new_name),"telefono":($new_phone),"direccion":($new_address),"image_transaccion":($new_image),"order_date":($new_date),"email":($new_email)};', {"id": check_order.get("id"), "new_apellido": data.apellido, "new_name": data.nombre, "new_phone": data.telefono, "new_address": data.direccion, "new_email": data.email, "new_image": data_cloudinary_filtered, "new_date": fecha_actual})
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                        "msg": "Tu pedido fue actualizado"})
        
    await User_Db.query('update ($id) merge {"apellido":($new_apellido),"nombre":($new_name),"telefono":($new_phone),"direccion":($new_address),"order_date":($new_date),"email":($new_email)};', {"id": check_order.get("id"), "new_apellido": data.apellido, "new_name": data.nombre, "new_phone": data.telefono, "new_address": data.direccion, "new_email": data.email, "new_date": fecha_actual})


    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Tu pedido fue actualizado"})


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
                if(comment.get("id_producto") == data.id_producto):
                    await User_Db.close()
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No puedes realizar mas comentarios de este producto"})

            
    for orders in check_order_detail:
        for productos in orders.get("result"):
            
            if (productos['id_producto'] == data.id_producto and productos['status'] != "Finalizado") == True:
                new_comment = Comment_product(**data.dict())
                await User_Db.create("comments", new_comment)
                await User_Db.close()
                raise HTTPException(status_code=status.HTTP_201_CREATED, detail={
                        "msg": "Tu comentario se ha creado"})
                
            



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

async def Update_comments(data,id_comment):
    User_Db = await Connection()
    check_comment = await User_Db.select(id_comment)
    check_user = await User_Db.select(data.user_id)
    check_product = await User_Db.select(data.id_producto) 
    if not check_product:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg":"Este producto no existe"})

    if not check_user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg":"Este usuario no existe"})
    if not check_comment:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"No se encuentra este comentario"})
    
    if check_comment.get("user_id") != data.user_id:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg":"Este no es tu comentario"})    
    if check_comment.get('id_producto') != data.id_producto:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg":"Este producto no le corresponde a este comentario"})    
    
    await User_Db.update(id_comment,data)
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Tu comentario se ha actualizado"})

