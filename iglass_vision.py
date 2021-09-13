import base64
import io
import json
import requests

import capture_image


vision_post_str = """
{
    "type": null,
    "image_b64": null
}
"""
vision_post_data = json.loads()
iglass_vision_cf_url = "https://us-central1-musty-1563232769915.cloudfunctions.net/iglass_vision"

def iglass_vision(vision_type):
    """
    returns a response of based on image
    :param vision_type: type of vision  analysis to be made e.g OCR, object-recognition
    :type vision_type: str

    :return text_response
    :rtype: str
    """
    
    captured_image_path = capture_image.capture_image()

    try:    
        with io.open(captured_image_path, 'rb') as image_file:
                content = image_file.read()

        image_b64 = base64.b64encode(content)
    except:
        raise ValueError

    vision_post_data["type"] = vision_type
    vision_post_data["image_b64"] = image_b64

    text_response = requests.post(url=iglass_vision_cf_url, data=vision_post_data)
    return text_response