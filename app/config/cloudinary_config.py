import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET"),
    secure=True,
)
async def Upload_image (image_product):

    upload = cloudinary.uploader.upload(image_product, folder="productos")
    return upload

async def Delete_image (public_id):
    delete =  cloudinary.uploader.destroy(public_id)
    return delete