try:
    from PIL import Image
except ImportError:
    Image = None

def load_image_from_file(path_to_image):
    image = Image.open(path_to_image)
    return image

def resize_image_from_path(path_to_image, target_size, keep_aspect_ratio):
    image = load_image_from_file(path_to_image)

    if image is None:
        return

    resized_image = resize_image(image, target_size, keep_aspect_ratio)

    return resized_image

def resize_image(image, target_size, keep_aspect_ratio):
    if image is None:
        return

    image = image.convert("RGBA")

    if keep_aspect_ratio:
        ratio = 0

        ratio = min(target_size[0]/image.width, target_size[1]/image.height)

        image = image.resize((int(target_size[0]*ratio), int(target_size[1]*ratio)), Image.BICUBIC)
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
