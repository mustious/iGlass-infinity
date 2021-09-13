import picamera
from PIL import Image
import time
import os
import re

project_root_path = os.path.abspath(os.path.dirname(__file__))

images_path = os.path.join(project_root_path, "photos/")
processed_images_path = os.path.join(project_root_path, "processed_images")


def capture_image():
    """
    captures an image using picamera library

    :return processed_image_path: returns processed image path
    :rtype: str
    """

    camera = picamera.PiCamera()
    image_name = get_next_image_name()
    image_path = os.path.join(images_path, image_name)
    try:
        with camera as my_camera:
            my_camera.resolution = (1280, 1280)
            time.sleep(1)  # one second delay for better capture
            my_camera.capture(image_path)
        processed_image_path = preprocess_image(image_path)
        camera.close()
        return processed_image_path

    except:
        camera.close()


def get_next_image_name():
    """
    consecutively names the images to be captured

    :return: next consecutive image name
    :rtype: str
    """

    if not os.path.exists(images_path):
        """
        creates image path if it does not exists and returns an
        index file name of 'image001.jpg' 
        """
        os.mkdir(images_path)  # creates a directory
        next_image_name = 'image001.jpg'

        return next_image_name

    elif len(os.listdir(images_path)) == 0:
        """
        'image_captured' directory exists but it is empty then it returns an
       index file name of 'image001.jpg'
        """
        next_image_name = 'image001.jpg'

        return next_image_name

    else:
        image_names = os.listdir(images_path)  # list of images in the directory
        last_image_name = sorted(image_names)[-1]  # last image name
        pattern = r'\d{3}'  # regex pattern to find the index
        match = re.search(pattern, last_image_name)

        if match is None:
            next_image_name = 'image001.jpg'
            return next_image_name

        current_index = int(match.group(0))  # current image index or number
        next_index = current_index + 1
        next_image_name = "image{:03d}.jpg".format(next_index)

        return next_image_name


def preprocess_image(full_image_path: str):
    """
    rotates image 90 degrees and compresses the size by reducing the image quality

    :param full_image_path: path of captured image
    :return:
    """

    im = Image.open(full_image_path)  # creates a PIL Image instance
    im_rotated_90 = im.rotate(90)  # rotates the image by 90 degress counter-clockwise
    if not os.path.exists(processed_images_path):
        os.mkdir(processed_images_path)

    _, image_file_name = os.path.split(full_image_path)  # gets the basename of the image e.g image003.jpg

    processed_image_name = "processed_" + image_file_name
    full_image_path = os.path.join(processed_images_path, processed_image_name)
    im_rotated_90.save(full_image_path, quality=90)  # compresses the image by saving at 90% quality

    return full_image_path
