from app.celery_app import celery

from PIL import Image

import os


@celery.task
def generate_image_thumbnail(
    image_path: str,
):
    """
    Creates a thumbnail for uploaded images.
    """

    image = Image.open(image_path)

    image.thumbnail((300, 300))

    filename = os.path.basename(image_path)

    thumbnail_dir = "uploads/thumbnails"

    os.makedirs(
        thumbnail_dir,
        exist_ok=True,
    )

    thumbnail_path = os.path.join(
        thumbnail_dir,
        filename,
    )

    image.save(thumbnail_path)

    return thumbnail_path


@celery.task
def compress_image(
    image_path: str,
):
    """
    Compress uploaded image.
    """

    image = Image.open(image_path)

    image.save(
        image_path,
        optimize=True,
        quality=80,
    )

    return image_path


@celery.task
def extract_video_metadata(
    video_path: str,
):
    """
    Placeholder for FFmpeg.
    Later we'll extract:

    duration

    width

    height

    fps

    bitrate
    """

    print("Processing:", video_path)

    return True