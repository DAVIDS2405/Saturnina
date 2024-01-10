import cloudinary
import cloudinary.uploader
from cloudinary import exceptions
import os

from fastapi import HTTPException,status

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET"),
    secure=True,
)
async def Upload_image (image_product):

    try:
        upload = cloudinary.uploader.upload(image_product, folder="productos")
        return upload
    except exceptions.Error as e:
       
        # Puedes realizar acciones adicionales o simplemente retornar None u otro valor que indique el fallo.
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"Hubo un problema con tu imagen intenta de nuevo"})


async def Delete_image (public_id):
    delete =  cloudinary.uploader.destroy(public_id)
    return delete