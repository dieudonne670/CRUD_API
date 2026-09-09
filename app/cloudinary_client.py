import os
from io import BytesIO

import cloudinary
from cloudinary.uploader import upload as cloudinary_upload

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME") or os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY") or os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET") or os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_bytes(content: bytes, public_id: str | None = None, folder: str | None = None, resource_type: str = "auto"):
    """Upload raw bytes to Cloudinary and return the upload result and public URL."""
    fileobj = BytesIO(content)
    opts = {"resource_type": resource_type}
    if folder:
        opts["folder"] = folder
    if public_id:
        opts["public_id"] = public_id
        opts["overwrite"] = True

    result = cloudinary_upload(fileobj, **opts)
    url = result.get("secure_url") or result.get("url")
    return result, url
