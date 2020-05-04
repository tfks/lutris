import requests

try:
    from PIL import Image
except ImportError:
    Image = None

from lutris.util.log import logger


def load_image_from_url(url):
    logger.info("Load image from url")

    image = Image.open(requests.get(url, stream=True).raw)

    if image is None:
        return None

    return image


def load_image_from_file(path_to_image):
    image = Image.open(path_to_image)

    if image is None:
        return None

    return image


def resize_image_from_url(url, target_size, keep_aspect_ratio):
    logger.info("Image from url")
    image = load_image_from_url(url)

    if image is None:
        return None

    resized_image = resize_image(image, target_size, keep_aspect_ratio)

    return resized_image


def resize_image_from_path(path_to_image, target_size, keep_aspect_ratio):
    image = load_image_from_file(path_to_image)

    if image is None:
        return None

    resized_image = resize_image(image, target_size, keep_aspect_ratio)

    return resized_image


def resize_image(image, target_size, keep_aspect_ratio, not_smaller=True):
    logger.info("Resize image")
    if image is None:
        return None

    image = image.convert("RGBA")

    if keep_aspect_ratio:
        # ratio = 0

        wratio = 0.0
        hratio = 0.0

        image_width = 0
        image_height = 0

        if not_smaller:
            image_width = target_size[0]
            image_height = target_size[1]
        else:
            image_width = image.width
            image_height = image.height

        if image_width < image.width:
            wratio = image_width / image.width
        else:
            wratio = image.width / image_width

        if image_height < image.height:
            hratio = image_height / image.height
        else:
            hratio = image.height / image_height

        # ratio = min(wratio, hratio)

        logger.info("WRatio: %s" % wratio)
        logger.info("HRatio: %s" % hratio)

        if not_smaller:
            image = image.resize(
                (int(image_width),
                int(image_height)),
                Image.BICUBIC
            )
        else:
            image = image.resize(
                (int(image_width*wratio),
                int(image_height*hratio)),
                Image.BICUBIC
            )
    else:
        image = image.resize(target_size, Image.BICUBIC)

    return image


def get_max_dimensions_from_image(image, target_size):
    if image is None:
        return

    max_width = 0
    max_height = 0

    if image.width > target_size[0]:
        max_width = image.width
    else:
        max_width = target_size[0]

    if image.height > target_size[1]:
        max_height = image.height
    else:
        max_height = target_size[1]

    return (max_width, max_height)
